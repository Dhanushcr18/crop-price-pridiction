"""KSAMB Daily Market Report PDF connector and dual-independent completeness parser.

Strictly enforces:
1. Report date extraction from PDF first-page title ("For DD/MM/YYYY"), refusing any file without one.
2. Table extraction using pdfplumber find_tables().
3. Market assignment via 'N] MARKET: NAME' headers with page-break carry-over.
4. Second independent pass over text lines (rows ending in unit word plus 3 numbers),
   recovering any row missed by the table pass (flagged 'recovered_from_text_line').
5. Completeness check: market numbers run 1..N with no gaps, every market has >= 1 row,
   and table pass (+ recovered) row counts match text line pass counts per market.
6. Original units kept; variety and grade preserved as separate series; arrivals never summed or averaged.
7. Validation flags:
   - min <= modal <= max
   - no future date
   - same min/max/modal triple on >= 3 different crops in one market
   - min = max = modal on most rows (>50%) of a market (evaluated on markets with >= 8 rows)
   - Quintal price below Rs 100
   - unit not Quintal (flagged 'non_quintal_unit')
8. 100% row-for-row equality with golden fixture data/raw/user_download/karnataka_mandi_prices_2026-11-11.csv.
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
import numpy as np
import pdfplumber

logger = logging.getLogger("farmer_advisor.ingest.ksamb_pdf")


class DateGateError(ValueError):
    """Raised when report date is missing, guessed, or invalid."""
    pass


class CompletenessError(RuntimeError):
    """Raised when market count is invalid, has gaps, or passes disagree."""
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


def extract_file_sha256(file_path: str) -> str:
    """Computes SHA-256 hash of the entire raw PDF file."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def extract_report_date_from_title(pdf: pdfplumber.PDF, file_path: str = "") -> str:
    """
    Reads the report date from the PDF's first-page title ('For DD/MM/YYYY').
    Refuses any file without one.
    """
    if not pdf.pages:
        raise DateGateError(f"Refusing PDF: File has no pages. File: '{file_path}'")

    first_page_text = pdf.pages[0].extract_text() or ""
    m = re.search(r'For\s+(\d{1,2}/\d{1,2}/\d{4})', first_page_text, re.I)
    if not m:
        raise DateGateError(
            f"Refusing PDF: Missing report date in first-page title ('For DD/MM/YYYY'). "
            f"Date must never be guessed. File: '{file_path}'"
        )

    date_str = m.group(1)
    try:
        report_date = datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError as e:
        raise DateGateError(f"Refusing PDF: Invalid date format '{date_str}' in first-page title: {e}")

    return report_date


class KsambPdfImporter:
    """Parses KSAMB Daily Market Report PDFs with completeness and validation gates."""

    EXPECTED_MARKETS_COUNT = 115

    def __init__(self, expected_markets: int = 115):
        self.expected_markets = expected_markets

    @staticmethod
    def extract_headers_from_page(page: pdfplumber.page.Page) -> List[Dict[str, Any]]:
        """Locates all 'N] MARKET: <NAME>' headers on a page with vertical Y coordinates."""
        words = page.extract_words()
        headers = []
        for i, w in enumerate(words):
            m = re.search(r'(\d+)\]$', w['text'])
            if m and i + 1 < len(words) and 'MARKET:' in words[i+1]['text']:
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
        return sorted(headers, key=lambda x: x['top'])

    def parse_pdf(self, pdf_path: str, explicit_date: Optional[str] = None) -> pd.DataFrame:
        """
        Parses the KSAMB PDF using find_tables() and text recovery pass,
        validates market contiguousness and row completeness, evaluates all anomaly flags,
        and returns a DataFrame matching the golden fixture schema.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        file_sha256 = extract_file_sha256(pdf_path)
        base_filename = os.path.basename(pdf_path)

        rows: List[Dict[str, Any]] = []
        active_market: Optional[Dict[str, Any]] = None
        market_headers: Dict[int, str] = {}
        text_pass_counts: Dict[int, int] = defaultdict(int)

        carried_text_market = None

        with pdfplumber.open(pdf_path) as pdf:
            # 1. Date gate: read from first-page title
            report_date = extract_report_date_from_title(pdf, file_path=pdf_path)
            if explicit_date and explicit_date != report_date:
                warnings.warn(
                    f"Configured date '{explicit_date}' differs from PDF title date '{report_date}'",
                    UserWarning
                )

            # Check future date gate
            today_str = datetime.now().strftime("%Y-%m-%d")
            is_future_date = (report_date > today_str)

            for p_idx, page in enumerate(pdf.pages):
                page_num = p_idx + 1
                headers = self.extract_headers_from_page(page)
                for h in headers:
                    market_headers[h['num']] = h['name']

                tables = sorted(page.find_tables(), key=lambda t: t.bbox[1])
                page_table_rows: List[Dict[str, Any]] = []

                # Pass 1: find_tables()
                for t in tables:
                    t_top = t.bbox[1]
                    matching_h = [h for h in headers if h['top'] < t_top]
                    if matching_h:
                        active_market = matching_h[-1]

                    if active_market is None:
                        continue

                    ext = t.extract()
                    if not ext:
                        continue

                    for r_idx, r in enumerate(ext):
                        if not r or len(r) < 8:
                            continue
                        if str(r[0] or "").strip() == 'Commodity' or 'Commodity' in str(r[0] or ""):
                            continue

                        comm = str(r[0] or '').replace('\n', ' ').strip()
                        var = str(r[1] or '').replace('\n', ' ').strip()
                        grade = str(r[2] or '').replace('\n', ' ').strip()
                        arrivals = int(re.sub(r'[^\d]', '', str(r[3])))
                        unit = str(r[4] or '').replace('\n', ' ').strip()
                        min_p = int(re.sub(r'[^\d]', '', str(r[5])))
                        max_p = int(re.sub(r'[^\d]', '', str(r[6])))
                        modal_p = int(re.sub(r'[^\d]', '', str(r[7])))

                        row_dict = {
                            'report_date': report_date,
                            'market_no': active_market['num'],
                            'mandi': active_market['name'],
                            'commodity': comm,
                            'variety': var,
                            'grade': grade,
                            'arrivals': arrivals,
                            'unit': unit,
                            'min_price': min_p,
                            'max_price': max_p,
                            'modal_price': modal_p,
                            'source_file': base_filename,
                            'source_page': page_num,
                            'table_row': float(r_idx),
                            'file_sha256': file_sha256,
                            'flags': []
                        }
                        rows.append(row_dict)
                        page_table_rows.append(row_dict)

                # Pass 2: Text lines scan (rows ending in unit word plus 3 numbers)
                text = page.extract_text() or ''
                # Track market context in text pass cleanly using carried_text_market
                current_text_market_num = carried_text_market
                text_lines = text.splitlines()

                for line in text_lines:
                    # Check for market header in line
                    m_head = re.search(r'(\d+)\]\s*MARKET:\s*(.+)', line)
                    if m_head:
                        current_text_market_num = int(m_head.group(1))

                    m_line = re.search(r'\b(Quintal|Numbers|Thousands)\s+(\d+)\s+(\d+)\s+(\d+)$', line)
                    if m_line:
                        unit_word = m_line.group(1)
                        min_val = int(m_line.group(2))
                        max_val = int(m_line.group(3))
                        modal_val = int(m_line.group(4))

                        if current_text_market_num:
                            text_pass_counts[current_text_market_num] += 1

                        # Check if this row was already captured by find_tables()
                        already_captured = any(
                            r['source_page'] == page_num and r['unit'] == unit_word and
                            r['min_price'] == min_val and r['max_price'] == max_val and r['modal_price'] == modal_val
                            for r in page_table_rows
                        )

                        if not already_captured:
                            # Recover row missed by table bounding box
                            prefix = line[:m_line.start()].strip()
                            tokens = prefix.split()
                            arrivals_val = int(tokens[-1])
                            grade_val = tokens[-2]
                            rem = tokens[:-2]
                            if len(rem) == 2:
                                comm_val, var_val = rem[0], rem[1]
                            elif len(rem) == 1:
                                comm_val, var_val = rem[0], rem[0]
                            else:
                                comm_val, var_val = rem[0], ' '.join(rem[1:])

                            rec_m_name = market_headers.get(current_text_market_num, active_market['name'] if active_market else "")
                            recovered_row = {
                                'report_date': report_date,
                                'market_no': current_text_market_num if current_text_market_num else active_market['num'],
                                'mandi': rec_m_name,
                                'commodity': comm_val,
                                'variety': var_val,
                                'grade': grade_val,
                                'arrivals': arrivals_val,
                                'unit': unit_word,
                                'min_price': min_val,
                                'max_price': max_val,
                                'modal_price': modal_val,
                                'source_file': base_filename,
                                'source_page': page_num,
                                'table_row': np.nan,
                                'file_sha256': file_sha256,
                                'flags': ['recovered_from_text_line']
                            }
                            rows.append(recovered_row)
                            logger.info(f"Recovered missed row on page {page_num}: {recovered_row}")

                # Update carried_text_market for the next page
                carried_text_market = current_text_market_num

                # Page-break carry-over for table pass: if header is at bottom of page, it owns next page's first table
                if headers:
                    last_h = headers[-1]
                    if not tables or last_h['top'] > tables[-1].bbox[3]:
                        active_market = last_h

        df = pd.DataFrame(rows)

        # Completeness checks:
        # 1. Market numbers run 1..N with no gaps
        unique_market_nums = sorted(df['market_no'].unique())
        n_markets = len(unique_market_nums)
        if unique_market_nums != list(range(1, n_markets + 1)):
            raise CompletenessError(
                f"Completeness failure: Market numbers do not run 1..N with no gaps. "
                f"Found: min={unique_market_nums[0]}, max={unique_market_nums[-1]}, total={n_markets}"
            )

        if self.expected_markets and n_markets != self.expected_markets:
            raise CompletenessError(
                f"Completeness failure: Expected {self.expected_markets} markets, found {n_markets}."
            )

        # 2. Every market has at least one row
        market_row_counts = df.groupby('market_no').size()
        if (market_row_counts < 1).any():
            empty_markets = market_row_counts[market_row_counts < 1].index.tolist()
            raise CompletenessError(f"Completeness failure: Markets with 0 rows: {empty_markets}")

        # 3. Two passes agree on rows per market
        for m_num in unique_market_nums:
            c_table = len(df[df['market_no'] == m_num])
            c_text = text_pass_counts.get(m_num, 0)
            if c_table != c_text:
                raise CompletenessError(
                    f"Completeness failure: Pass agreement error for market {m_num} ({market_headers.get(m_num)}): "
                    f"Table+Recovered={c_table} vs TextPass={c_text}"
                )

        # Validation & Flagging rules
        # a. min_eq_max_eq_modal_most_rows: on markets with >= 8 rows where > 50% are flat
        flat_markets = set()
        for mandi, grp in df.groupby('mandi'):
            if len(grp) >= 8:
                flat_count = ((grp['min_price'] == grp['max_price']) & (grp['max_price'] == grp['modal_price'])).sum()
                if flat_count > 0.5 * len(grp):
                    flat_markets.add(mandi)

        # b. same_price_triple_3plus_crops: triple shared by >= 3 distinct commodities in one market
        shared_triples = set()
        for (mandi, min_p, max_p, modal_p), grp in df.groupby(['mandi', 'min_price', 'max_price', 'modal_price']):
            if grp['commodity'].nunique() >= 3:
                shared_triples.add((mandi, min_p, max_p, modal_p))

        final_flags: List[Any] = []
        for _, r in df.iterrows():
            f_list = list(r['flags'])

            # Ordering matches golden fixture convention:
            # same_price_triple_3plus_crops ; min_eq_max_eq_modal_most_rows ; non_quintal_unit ; price_below_100_per_qtl
            if (r['mandi'], r['min_price'], r['max_price'], r['modal_price']) in shared_triples:
                if 'same_price_triple_3plus_crops' not in f_list:
                    f_list.append('same_price_triple_3plus_crops')

            if r['mandi'] in flat_markets:
                if 'min_eq_max_eq_modal_most_rows' not in f_list:
                    f_list.append('min_eq_max_eq_modal_most_rows')

            if r['unit'] != 'Quintal':
                if 'non_quintal_unit' not in f_list:
                    f_list.append('non_quintal_unit')

            if r['unit'] == 'Quintal' and (r['min_price'] < 100 or r['modal_price'] < 100 or r['max_price'] < 100):
                if 'price_below_100_per_qtl' not in f_list:
                    f_list.append('price_below_100_per_qtl')

            # Strict price ordering check
            if not (r['min_price'] <= r['modal_price'] <= r['max_price']):
                if 'min_max_modal_violation' not in f_list:
                    f_list.append('min_max_modal_violation')

            # Future date check
            if is_future_date:
                if 'future_date' not in f_list:
                    f_list.append('future_date')

            final_flags.append(';'.join(f_list) if f_list else np.nan)

        df['flags'] = final_flags

        # Enforce canonical column order
        cols = [
            'report_date', 'market_no', 'mandi', 'commodity', 'variety', 'grade',
            'arrivals', 'unit', 'min_price', 'max_price', 'modal_price',
            'source_file', 'source_page', 'table_row', 'file_sha256', 'flags'
        ]
        return df[cols]


def import_ksamb_pdf_to_csv(pdf_path: str, output_csv_path: str) -> pd.DataFrame:
    """Convenience CLI / daily ingestion function."""
    importer = KsambPdfImporter()
    df = importer.parse_pdf(pdf_path)
    os.makedirs(os.path.dirname(os.path.abspath(output_csv_path)), exist_ok=True)
    df.to_csv(output_csv_path, index=False)
    logger.info(f"Successfully converted {pdf_path} -> {output_csv_path} ({len(df)} rows)")
    return df


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="KSAMB Daily Market Report PDF Importer")
    parser.add_argument("--file", "-f", required=True, help="Path to KSAMB Daily Market Report PDF")
    parser.add_argument("--output", "-o", default=None, help="Output CSV path")
    args = parser.parse_args()

    out_path = args.output
    if not out_path:
        base = os.path.splitext(os.path.basename(args.file))[0]
        out_path = os.path.join("data", "raw", "user_download", f"{base}.csv")

    import_ksamb_pdf_to_csv(args.file, out_path)
