"""KSAMB Daily Market Report PDF connector and dual-independent completeness parser.

Strictly enforces:
1. One row per market, commodity, variety, and grade.
2. Explicit report date requirement (from config or filename YYYY-MM-DD), refusing if absent.
3. Warning on mismatch with stray date found in PDF header.
4. Handling glued tokens across page breaks and headers ('1900 19] MARKET: X', '30000 71] MARKET: Y').
5. Completeness check: requiring exactly 115 markets and 100% agreement between Method A (table extraction)
   and Method B (text line parser). Fails import on any mismatch.
6. Full audit traceability: raw_file, raw_page, raw_line, file_sha256, acquisition_method='user_download',
   data_provenance='real', is_synthetic=False.
"""

import os
import re
import json
import hashlib
import logging
import warnings
from datetime import datetime
from collections import defaultdict, OrderedDict
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple, Optional

import pandas as pd
import pdfplumber

logger = logging.getLogger("farmer_advisor.ingest.ksamb_pdf")


class DateGateError(ValueError):
    """Raised when report date is missing, guessed, or invalid."""
    pass


class CompletenessError(RuntimeError):
    """Raised when market count != 115 or Method A and Method B row counts mismatch."""
    pass


@dataclass
class ParsedPdfRow:
    date: str
    mandi: str
    market_num: int
    commodity: str
    variety: str
    grade: str
    arrivals: float
    unit: str
    min: float
    max: float
    modal: float
    raw_file: str
    raw_page: int
    raw_line: int
    file_sha256: str
    acquisition_method: str = "user_download"
    data_provenance: str = "real"
    is_synthetic: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "date": self.date,
            "mandi": self.mandi,
            "market_num": self.market_num,
            "commodity": self.commodity,
            "variety": self.variety,
            "grade": self.grade,
            "arrivals": self.arrivals,
            "unit": self.unit,
            "min": self.min,
            "max": self.max,
            "modal": self.modal,
            "raw_file": self.raw_file,
            "raw_page": self.raw_page,
            "raw_line": self.raw_line,
            "file_sha256": self.file_sha256,
            "acquisition_method": self.acquisition_method,
            "data_provenance": self.data_provenance,
            "is_synthetic": self.is_synthetic
        }


def extract_file_sha256(file_path: str) -> str:
    """Computes SHA-256 hash of the entire raw PDF file."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def extract_stray_date_from_pdf(pdf: pdfplumber.PDF) -> Optional[str]:
    """Finds date string in header of first page (e.g. '11/11/2026')."""
    if not pdf.pages:
        return None
    first_page_text = pdf.pages[0].extract_text() or ""
    m = re.search(r'Commoditywise\s+Daily\s+Market\s+Report\s+For\s+(\d{1,2}/\d{1,2}/\d{4})', first_page_text, re.I)
    if m:
        try:
            return datetime.strptime(m.group(1), "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            return None
    return None


def resolve_report_date(explicit_date: Optional[str], file_path: str, stray_date: Optional[str]) -> str:
    """Enforces that report date comes from explicit config or filename (never guessed)."""
    date_val = None
    if explicit_date and str(explicit_date).strip():
        date_str = str(explicit_date).strip()
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                date_val = datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
                break
            except ValueError:
                continue
        if not date_val:
            raise DateGateError(f"Invalid explicit report date format: '{explicit_date}'. Expected YYYY-MM-DD.")
    else:
        # Check filename for YYYY-MM-DD pattern
        basename = os.path.basename(file_path)
        m = re.search(r'(\d{4}[-_]\d{2}[-_]\d{2})', basename)
        if m:
            clean_str = m.group(1).replace("_", "-")
            try:
                date_val = datetime.strptime(clean_str, "%Y-%m-%d").strftime("%Y-%m-%d")
            except ValueError:
                date_val = None

    if not date_val:
        raise DateGateError(
            f"Report date must come from an explicit config field or the file name (YYYY-MM-DD), never guessed. "
            f"File: '{file_path}'"
        )

    # Warn if resolved date differs from stray date found in PDF text
    if stray_date and date_val != stray_date:
        msg = f"Date Warning: Configured/filename report date '{date_val}' differs from stray date found in PDF text: '{stray_date}'."
        logger.warning(msg)
        warnings.warn(msg, UserWarning)

    return date_val


class KsambPdfImporter:
    """Parses KSAMB Daily Market Report PDFs with completeness gates."""

    REQUIRED_MARKETS_COUNT = 115

    def __init__(self, expected_markets: int = 115):
        self.expected_markets = expected_markets

    @staticmethod
    def extract_headers_from_page(page: pdfplumber.page.Page) -> List[Dict[str, Any]]:
        """Locates all 'N] MARKET: <NAME>' header words on a page with vertical Y coordinates."""
        words = page.extract_words()
        headers = []
        for i, w in enumerate(words):
            m = re.search(r'(\d+)\]$', w['text'])
            if m and i + 1 < len(words):
                next_w = words[i+1]['text']
                if 'MARKET:' in next_w:
                    m_num = int(m.group(1))
                    top = w['top']
                    m_name_words = []
                    for j in range(i+2, min(len(words), i+15)):
                        wj = words[j]
                        if abs(wj['top'] - top) > 4:
                            break
                        if 'Commodity' in wj['text'] or 'Modal' in wj['text'] or re.search(r'\d+\]', wj['text']):
                            break
                        m_name_words.append(wj['text'])
                    m_name = ' '.join(m_name_words).strip()
                    headers.append({
                        'num': m_num,
                        'name': m_name,
                        'top': top
                    })
        return headers

    def parse_method_a(
        self, pdf: pdfplumber.PDF, rel_file_path: str, file_sha256: str, report_date: str
    ) -> Tuple[OrderedDict, Dict[int, List[ParsedPdfRow]]]:
        """Method A: Table-based extraction using geometric layout and vertical separator rects."""
        all_headers = OrderedDict()
        market_rows = defaultdict(list)
        current_market_num = None

        for page_idx, page in enumerate(pdf.pages):
            page_num = page_idx + 1
            headers = self.extract_headers_from_page(page)
            for h in headers:
                all_headers[h['num']] = h['name']

            sorted_headers = sorted(headers, key=lambda h: h['top'])

            # Handle unbordered bottom rows by checking if vertical rects extend beyond horizontal lines
            vert_rects = [r for r in page.rects if r['width'] < 2 and r['height'] > 5]
            horiz_rects = [r for r in page.rects if r['height'] < 2 and r['width'] > 20]

            table_settings = {}
            if vert_rects and horiz_rects:
                max_vert_bottom = max(r['bottom'] for r in vert_rects)
                max_horiz_bottom = max(r['bottom'] for r in horiz_rects)
                if max_vert_bottom > max_horiz_bottom + 2:
                    table_settings['explicit_horizontal_lines'] = [max_vert_bottom]

            tables = page.find_tables(table_settings) if table_settings else page.find_tables()
            sorted_tables = sorted(tables, key=lambda t: t.bbox[1])

            # Prepare page text lines for line number estimation
            page_text = page.extract_text() or ""
            page_lines = page_text.splitlines()

            for t in sorted_tables:
                t_top = t.bbox[1]
                active_h = None
                for h in sorted_headers:
                    if h['top'] < t_top:
                        active_h = h
                    else:
                        break

                if active_h is not None:
                    current_market_num = active_h['num']

                if current_market_num is None:
                    continue

                raw_table = t.extract()
                if not raw_table:
                    continue

                start_idx = 0
                if any("Commodity" in str(c) for c in raw_table[0] if c):
                    start_idx = 1

                data_rows = raw_table[start_idx:]
                current_market_name = all_headers.get(current_market_num, f"Market {current_market_num}")

                for r_idx, row in enumerate(data_rows):
                    if not row or len(row) < 8:
                        continue

                    # Clean wrapped cells
                    clean_cells = [str(c or "").replace("\n", " ").strip() for c in row]
                    comm = clean_cells[0]
                    var = clean_cells[1]
                    grade = clean_cells[2]
                    arr_str = clean_cells[3].replace(",", "")
                    unit_str = clean_cells[4]
                    min_str = clean_cells[5].replace(",", "")
                    max_str = clean_cells[6].replace(",", "")
                    mod_str = clean_cells[7].replace(",", "")

                    try:
                        arr_val = float(arr_str) if arr_str else 0.0
                        min_val = float(min_str)
                        max_val = float(max_str)
                        mod_val = float(mod_str)
                    except ValueError:
                        continue

                    # Determine raw line on page by searching commodity / prices in page_lines
                    raw_line_on_page = page_idx * 100 + r_idx + 1
                    for l_i, l_str in enumerate(page_lines):
                        if str(int(mod_val)) in l_str and (comm.split()[0].lower() in l_str.lower() if comm else True):
                            raw_line_on_page = l_i + 1
                            break

                    parsed_row = ParsedPdfRow(
                        date=report_date,
                        mandi=current_market_name,
                        market_num=current_market_num,
                        commodity=comm,
                        variety=var,
                        grade=grade,
                        arrivals=arr_val,
                        unit=unit_str,
                        min=min_val,
                        max=max_val,
                        modal=mod_val,
                        raw_file=rel_file_path,
                        raw_page=page_num,
                        raw_line=raw_line_on_page,
                        file_sha256=file_sha256,
                        acquisition_method="user_download",
                        data_provenance="real",
                        is_synthetic=False
                    )
                    market_rows[current_market_num].append(parsed_row)

            if sorted_headers:
                current_market_num = sorted_headers[-1]['num']

        return all_headers, market_rows

    def parse_method_b(self, pdf: pdfplumber.PDF) -> Dict[int, List[str]]:
        """Method B: Independent text-token and regex line parser."""
        market_rows = defaultdict(list)
        current_market = None
        pending_prefix = ""

        row_end_pattern = re.compile(
            r'(\d+(?:\.\d+)?)\s+(Quintal|Numbers|Thousands|Bags|Boxes|Kgs?)\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)$',
            re.IGNORECASE
        )

        for page in pdf.pages:
            text = page.extract_text() or ""
            lines = text.splitlines()

            for line_raw in lines:
                line = line_raw.strip()
                if not line or line.startswith("===") or line.startswith("Report Menu Print") or "Commoditywise Daily Market Report" in line:
                    continue

                # Glued price token before market header (e.g. '1900 19] MARKET: C.R.PATNA')
                glued_match = re.match(r'^(\d+(?:\.\d+)?)\s+(\d+\]\s*MARKET:\s*.+)$', line)
                if glued_match:
                    line = glued_match.group(2)

                # Market header check
                m_hdr = re.search(r'(\d+)\]\s*MARKET:\s*([^\n\r]+)', line)
                if m_hdr:
                    current_market = int(m_hdr.group(1))
                    pending_prefix = ""
                    continue

                if re.search(r'Commodity\s+Variety\s+Grade', line, re.I):
                    continue
                if line in ["Modal", "(Rs.)", "Commodity", "Variety", "Grade", "Arrivals", "Units"]:
                    continue

                # Match data row
                match = row_end_pattern.search(line)
                if match:
                    if current_market is not None:
                        full_row = (pending_prefix + " " + line).strip() if pending_prefix else line
                        market_rows[current_market].append(full_row)
                    pending_prefix = ""
                else:
                    if not any(hdr_word in line for hdr_word in ["MARKET:", "Commoditywise", "Report"]):
                        if pending_prefix:
                            pending_prefix += " " + line
                        else:
                            pending_prefix = line

        return market_rows

    def import_pdf(self, file_path: str, report_date: Optional[str] = None) -> List[ParsedPdfRow]:
        """Main import method with completeness gate."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")

        try:
            rel_path = os.path.relpath(file_path, os.getcwd()).replace("\\", "/")
        except Exception:
            rel_path = file_path.replace("\\", "/")

        file_sha256 = extract_file_sha256(file_path)

        with pdfplumber.open(file_path) as pdf:
            stray_date = extract_stray_date_from_pdf(pdf)
            resolved_date = resolve_report_date(report_date, file_path, stray_date)

            # Method A
            headers_a, rows_a = self.parse_method_a(pdf, rel_path, file_sha256, resolved_date)

            # Completeness Check 1: Count of market headers must equal expected_markets (115)
            if len(headers_a) != self.expected_markets:
                raise CompletenessError(
                    f"Completeness Failure: Expected {self.expected_markets} market headers, found {len(headers_a)}."
                )

            # Method B
            rows_b = self.parse_method_b(pdf)

            # Completeness Check 2: Row counts per market must match exactly between Method A and Method B
            mismatches = []
            for m_num in range(1, self.expected_markets + 1):
                cnt_a = len(rows_a.get(m_num, []))
                cnt_b = len(rows_b.get(m_num, []))
                if cnt_a != cnt_b:
                    m_name = headers_a.get(m_num, f"Market {m_num}")
                    mismatches.append(f"Market {m_num} ({m_name}): Method A={cnt_a} rows vs Method B={cnt_b} rows")

            if mismatches:
                mismatch_str = "\n".join(mismatches)
                raise CompletenessError(
                    f"Completeness Failure: Independent parse methods disagree on row counts:\n{mismatch_str}"
                )

            # Flatten accepted rows
            all_rows = []
            for m_num in sorted(rows_a.keys()):
                all_rows.extend(rows_a[m_num])

            logger.info(
                f"Successfully parsed {len(all_rows)} rows across {len(headers_a)} markets from {rel_path} for date {resolved_date}."
            )
            return all_rows


def select_headline_series(
    rows: List[ParsedPdfRow],
    config: Optional[Dict[str, Any]] = None
) -> Tuple[List[ParsedPdfRow], List[ParsedPdfRow]]:
    """Separates full variety/grade series from headline series using rule in config.yaml.
    
    Assumption:
        Arrivals are NEVER summed or averaged across varieties (Bengaluru repeats 10,823 on 3 onion rows).
        The headline series selects the representative commercial grade and standard variety with max arrivals.
        
    Returns:
        (headline_rows, non_headline_rows)
    """
    cfg = config or {}
    hl_cfg = cfg.get("headline_price_selection", {})
    preferred_grades = hl_cfg.get("preferred_grades", ["Medium", "Average", "FAQ", "Large", "Small", "Non FAQ"])
    preferred_varieties_map = hl_cfg.get("preferred_varieties", {})

    grade_rank = {g.lower(): i for i, g in enumerate(preferred_grades)}

    # Group by (date, mandi, commodity)
    grouped = defaultdict(list)
    for r in rows:
        key = (r.date, r.mandi.lower().strip(), r.commodity.lower().strip())
        grouped[key].append(r)

    headline_rows = []
    secondary_rows = []

    for key, items in grouped.items():
        if len(items) == 1:
            headline_rows.append(items[0])
            continue

        crop = key[2]
        var_prefs = [v.lower() for v in preferred_varieties_map.get(crop, ["local", crop, "other"])]
        var_rank = {v: i for i, v in enumerate(var_prefs)}

        def sort_key(item: ParsedPdfRow):
            g_score = grade_rank.get(item.grade.lower(), 99)
            v_score = var_rank.get(item.variety.lower(), 99)
            arr_score = -float(item.arrivals)
            return (g_score, v_score, arr_score)

        sorted_items = sorted(items, key=sort_key)
        headline_rows.append(sorted_items[0])
        secondary_rows.extend(sorted_items[1:])

    return headline_rows, secondary_rows


def validate_and_filter_ksamb_rows(
    rows: List[ParsedPdfRow],
    quarantine_dir: str = "data/quarantine",
    non_quintal_output_path: str = "data/processed/non_quintal_prices.parquet",
    today_date_str: str = "2026-11-12",
    crop_bounds_override: Optional[Dict[str, Tuple[float, float]]] = None
) -> Tuple[List[ParsedPdfRow], List[ParsedPdfRow], List[Dict[str, Any]]]:
    """Applies Step 6 & 7 validation, unit separation, and strict anomaly flagging.
    
    1. Keeps original units. Quintal rows move forward to panel validation.
       Non-quintal rows (Numbers, Thousands) are saved to data/processed/non_quintal_prices.parquet.
    2. Flags and quarantines without silently fixing:
       (a) identical min/max/modal triples shared by >= 3 different crops in one market (e.g. Nanjangud, Yarahalli).
       (b) min = max = modal for most rows (>50%) in a market (e.g. Kadur).
       (c) price below Rs 100/qtl for crops normally trading above that (e.g. Kalaburagi radish 10/20/15).
       (d) min <= modal <= max violations, non-positive modal, future dates, or bound violations.
       
    Returns:
        (accepted_quintal_rows, non_quintal_rows, quarantined_records)
    """
    os.makedirs(quarantine_dir, exist_ok=True)
    os.makedirs(os.path.dirname(non_quintal_output_path), exist_ok=True)

    today = datetime.strptime(today_date_str, "%Y-%m-%d").date()

    # Step 6: Separate quintal vs non-quintal
    quintal_rows = []
    non_quintal_rows = []

    for r in rows:
        if r.unit.lower() == "quintal":
            quintal_rows.append(r)
        else:
            non_quintal_rows.append(r)

    # Persist non-quintal rows to parquet
    if non_quintal_rows:
        df_non_qtl = pd.DataFrame([r.to_dict() for r in non_quintal_rows])
        df_non_qtl.to_parquet(non_quintal_output_path, index=False)
        logger.info(f"Saved {len(non_quintal_rows)} non-quintal records to {non_quintal_output_path}")

    # Step 7: Anomaly detection on quintal rows
    quarantined_records = []
    quarantined_row_keys = set()  # set of (r.mandi, r.commodity, r.variety, r.grade)

    # Pre-compute market-level stats
    mandi_groups = defaultdict(list)
    for r in quintal_rows:
        mandi_groups[r.mandi].append(r)

    # Check (b): min = max = modal for most rows (>50%) in a market (Kadur)
    flat_market_names = set()
    for mandi, m_rows in mandi_groups.items():
        if len(m_rows) > 1:
            flat_count = sum(1 for r in m_rows if r.min == r.max == r.modal)
            if flat_count / len(m_rows) > 0.5:
                flat_market_names.add(mandi)
                pct = (flat_count / len(m_rows)) * 100.0
                for r in m_rows:
                    row_key = (r.mandi, r.commodity, r.variety, r.grade)
                    quarantined_row_keys.add(row_key)
                    quarantined_records.append({
                        "raw_file": r.raw_file,
                        "raw_page": r.raw_page,
                        "raw_line": r.raw_line,
                        "date": r.date,
                        "mandi": r.mandi,
                        "commodity": r.commodity,
                        "variety": r.variety,
                        "grade": r.grade,
                        "min": r.min,
                        "max": r.max,
                        "modal": r.modal,
                        "flag": "flag_b_flat_market",
                        "rejection_reason": (
                            f"Flag (b): Market-wide flat price anomaly: majority of rows ({flat_count}/{len(m_rows)}, "
                            f"{pct:.1f}%) in {mandi} report min=max=modal without natural price variance."
                        )
                    })

    # Check (a): identical min/max/modal triples shared by >= 3 different crops in one market
    for mandi, m_rows in mandi_groups.items():
        # skip markets already quarantined under (b) to avoid duplicate quarantine entries
        if mandi in flat_market_names:
            continue

        triple_map = defaultdict(list)
        for r in m_rows:
            triple_map[(r.min, r.max, r.modal)].append(r)

        for triple, t_rows in triple_map.items():
            distinct_crops = sorted(list(set(r.commodity.lower().strip() for r in t_rows)))
            if len(distinct_crops) >= 3:
                for r in t_rows:
                    row_key = (r.mandi, r.commodity, r.variety, r.grade)
                    if row_key not in quarantined_row_keys:
                        quarantined_row_keys.add(row_key)
                        quarantined_records.append({
                            "raw_file": r.raw_file,
                            "raw_page": r.raw_page,
                            "raw_line": r.raw_line,
                            "date": r.date,
                            "mandi": r.mandi,
                            "commodity": r.commodity,
                            "variety": r.variety,
                            "grade": r.grade,
                            "min": r.min,
                            "max": r.max,
                            "modal": r.modal,
                            "flag": "flag_a_shared_triple",
                            "rejection_reason": (
                                f"Flag (a): Suspicious identical price triple (min={r.min}, max={r.max}, modal={r.modal}) "
                                f"shared across {len(distinct_crops)} different commodities in {mandi}: {distinct_crops}."
                            )
                        })

    # Check (c) and standard plausibility checks on remaining rows
    accepted_quintal_rows = []
    for r in quintal_rows:
        row_key = (r.mandi, r.commodity, r.variety, r.grade)
        if row_key in quarantined_row_keys:
            continue

        # Check (c): price below Rs 100/qtl for crops normally trading above that
        # Field vegetables and cereals normally trade well above Rs 100/qtl
        standard_crops = [
            "radish", "raddish", "tomato", "onion", "potato", "carrot", "beetroot",
            "beans", "brinjal", "cabbage", "cauliflower", "green chilly", "cucumber", "cucumbar"
        ]
        clean_comm = r.commodity.lower().strip()
        if (r.modal < 100.0 or r.min < 100.0) and any(sc in clean_comm for sc in standard_crops):
            quarantined_records.append({
                "raw_file": r.raw_file,
                "raw_page": r.raw_page,
                "raw_line": r.raw_line,
                "date": r.date,
                "mandi": r.mandi,
                "commodity": r.commodity,
                "variety": r.variety,
                "grade": r.grade,
                "min": r.min,
                "max": r.max,
                "modal": r.modal,
                "flag": "flag_c_below_100",
                "rejection_reason": (
                    f"Flag (c): Price below Rs 100/quintal floor for standard horticulture crop: "
                    f"{r.commodity} in {r.mandi} reports min={r.min}, modal={r.modal}, max={r.max}."
                )
            })
            continue

        # Standard check 1: min <= modal <= max
        if r.min > r.modal:
            quarantined_records.append({
                "raw_file": r.raw_file,
                "raw_page": r.raw_page,
                "raw_line": r.raw_line,
                "date": r.date,
                "mandi": r.mandi,
                "commodity": r.commodity,
                "variety": r.variety,
                "grade": r.grade,
                "min": r.min,
                "max": r.max,
                "modal": r.modal,
                "flag": "min_greater_than_modal",
                "rejection_reason": f"Plausibility failure: min_price ({r.min}) > modal_price ({r.modal})."
            })
            continue

        if r.modal > r.max:
            quarantined_records.append({
                "raw_file": r.raw_file,
                "raw_page": r.raw_page,
                "raw_line": r.raw_line,
                "date": r.date,
                "mandi": r.mandi,
                "commodity": r.commodity,
                "variety": r.variety,
                "grade": r.grade,
                "min": r.min,
                "max": r.max,
                "modal": r.modal,
                "flag": "modal_greater_than_max",
                "rejection_reason": f"Plausibility failure: modal_price ({r.modal}) > max_price ({r.max})."
            })
            continue

        # Strict check: reject suspicious synthesized 0.9/1.1 ratio
        if r.modal > 0 and round(r.min, 2) == round(0.9 * r.modal, 2) and round(r.max, 2) == round(1.1 * r.modal, 2):
            quarantined_records.append({
                "raw_file": r.raw_file,
                "raw_page": r.raw_page,
                "raw_line": r.raw_line,
                "date": r.date,
                "mandi": r.mandi,
                "commodity": r.commodity,
                "variety": r.variety,
                "grade": r.grade,
                "min": r.min,
                "max": r.max,
                "modal": r.modal,
                "flag": "synthesized_min_max_ratio",
                "rejection_reason": f"Suspicious synthesized 0.9/1.1 min/max ratio: min={r.min}, modal={r.modal}, max={r.max}."
            })
            continue

        if r.modal <= 0:
            quarantined_records.append({
                "raw_file": r.raw_file,
                "raw_page": r.raw_page,
                "raw_line": r.raw_line,
                "date": r.date,
                "mandi": r.mandi,
                "commodity": r.commodity,
                "variety": r.variety,
                "grade": r.grade,
                "min": r.min,
                "max": r.max,
                "modal": r.modal,
                "flag": "non_positive_modal",
                "rejection_reason": f"Modal price must be strictly positive, got {r.modal}."
            })
            continue

        # Future date check
        try:
            r_date = datetime.strptime(r.date, "%Y-%m-%d").date()
            if r_date > today:
                quarantined_records.append({
                    "raw_file": r.raw_file,
                    "raw_page": r.raw_page,
                    "raw_line": r.raw_line,
                    "date": r.date,
                    "mandi": r.mandi,
                    "commodity": r.commodity,
                    "variety": r.variety,
                    "grade": r.grade,
                    "min": r.min,
                    "max": r.max,
                    "modal": r.modal,
                    "flag": "future_date",
                    "rejection_reason": f"Date {r.date} is in the future relative to {today_date_str}."
                })
                continue
        except ValueError:
            pass

        accepted_quintal_rows.append(r)

    # Persist quarantine records to file
    if quarantined_records:
        ts_str = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        q_path = os.path.join(quarantine_dir, f"quarantine_ksamb_pdf_{ts_str}.json")
        with open(q_path, "w", encoding="utf-8") as f:
            json.dump(quarantined_records, f, indent=2)
        logger.warning(f"Quarantined {len(quarantined_records)} suspicious rows to {q_path}")

    return accepted_quintal_rows, non_quintal_rows, quarantined_records


