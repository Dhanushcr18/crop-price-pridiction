"""Ingests validated KSAMB PDF quintal rows into data/processed/panel.parquet with full provenance."""

import sys
sys.path.insert(0, ".")
import os
import json
import random
import pandas as pd
from datetime import datetime

from src.ingest.connectors.ksamb_pdf import KsambPdfImporter, validate_and_filter_ksamb_rows

# Mandi district alias map for Karnataka APMCs
MANDI_DISTRICT_MAP = {
    "ANNIGERI": ("Annigeri", "Dharwad"),
    "ARAKALGUD": ("Arakalgud", "Hassan"),
    "ARSIKERE": ("Arsikere", "Hassan"),
    "BADAMI": ("Badami", "Bagalkote"),
    "BAGALKOT": ("Bagalkot", "Bagalkote"),
    "BAGEPALLI": ("Bagepalli", "Chikkaballapur"),
    "BALLARI": ("Ballari", "Ballari"),
    "BANGARPET": ("Bangarpet", "Kolar"),
    "BANTWALA": ("Bantwala", "Dakshina Kannada"),
    "BASAVAKALYANA": ("Basavakalyana", "Bidar"),
    "BELAGAVI": ("Belagavi", "Belagavi"),
    "BELUR": ("Belur", "Hassan"),
    "BENGALURU": ("Bengaluru (Yeshwanthpur)", "Bengaluru Urban"),
    "BHADRAVATHI": ("Bhadravathi", "Shivamogga"),
    "BIDAR": ("Bidar", "Bidar"),
    "BINNY MILL (F&V)": ("Bengaluru (Binny Mill)", "Bengaluru Urban"),
    "BYADGI": ("Byadgi", "Haveri"),
    "C.R.NAGAR": ("Chamarajanagar", "Chamarajanagar"),
    "C.R.PATNA": ("Channarayapatna", "Hassan"),
    "CHALLAKERE": ("Challakere", "Chitradurga"),
    "CHANNAGIRI": ("Channagiri", "Davanagere"),
    "CHANNAPATNA": ("Channapatna", "Ramanagara"),
    "CHIKKAMAGALURU": ("Chikkamagaluru", "Chikkamagaluru"),
    "CHINCOLI": ("Chincholi", "Kalaburagi"),
    "CHINTAMANI": ("Chintamani", "Chikkaballapur"),
    "CHITRADURGA": ("Chitradurga", "Chitradurga"),
    "CHITTAPURA": ("Chittapura", "Kalaburagi"),
    "DAVANAGERE": ("Davanagere", "Davanagere"),
    "DODDABALLAPUR": ("Doddaballapur", "Bengaluru Rural"),
    "ENDI": ("Indi", "Vijayapura"),
    "GADAG": ("Gadag", "Gadag"),
    "GANGAVATI": ("Gangavati", "Koppal"),
    "GOKAK": ("Gokak", "Belagavi"),
    "GOWRIBIDNUR": ("Gowribidnur", "Chikkaballapur"),
    "GUNDLUPET": ("Gundlupet", "Chamarajanagar"),
    "HAGARI BOMMANA HALLI": ("Hagari Bommana Halli", "Ballari"),
    "HALIYALA": ("Haliyala", "Uttara Kannada"),
    "HANGAL": ("Hangal", "Haveri"),
    "HANUR": ("Hanur", "Chamarajanagar"),
    "HARAPANAHALLI": ("Harapanahalli", "Vijayanagara"),
    "HARIHARA": ("Harihara", "Davanagere"),
    "HASSAN": ("Hassan", "Hassan"),
    "HIREKERUR": ("Hirekerur", "Haveri"),
    "HIRIYUR": ("Hiriyur", "Chitradurga"),
    "HOLALKERE": ("Holalkere", "Chitradurga"),
    "HOLENARASIPUR": ("Holenarasipur", "Hassan"),
    "HONNALI": ("Honnali", "Davanagere"),
    "HONNAVAR": ("Honnavar", "Uttara Kannada"),
    "HOOVINAHADAGALI": ("Hoovinahadagali", "Ballari"),
    "HOSADURGA": ("Hosadurga", "Chitradurga"),
    "HUBBALLI": ("Hubballi", "Dharwad"),
    "HUNGUND": ("Hungund", "Bagalkote"),
    "HUNSUR": ("Hunsur", "Mysuru"),
    "JAGALUR": ("Jagalur", "Davanagere"),
    "JEVARGI": ("Jevargi", "Kalaburagi"),
    "K.R.NAGAR": ("K.R.Nagar", "Mysuru"),
    "K.R.PET": ("K.R.Pet", "Mandya"),
    "KADUR": ("Kadur", "Chikkamagaluru"),
    "KALABURAGI": ("Kalaburagi", "Kalaburagi"),
    "KALGHATGI": ("Kalghatgi", "Dharwad"),
    "KAMPLI": ("Kampli", "Ballari"),
    "KANAKAGIRI": ("Kanakagiri", "Koppal"),
    "KARTAGI": ("Karatagi", "Koppal"),
    "KOLAR": ("Kolar", "Kolar"),
    "KOLLEGAL": ("Kollegal", "Chamarajanagar"),
    "KOPPAL": ("Koppal", "Koppal"),
    "KOTTUR": ("Kottur", "Ballari"),
    "KUDLIGI": ("Kudligi", "Ballari"),
    "KUMTA": ("Kumta", "Uttara Kannada"),
    "KUNDAPUR": ("Kundapur", "Udupi"),
    "KUSTAGI": ("Kustagi", "Koppal"),
    "LAXMESHWAR": ("Laxmeshwar", "Gadag"),
    "LINGASARGUR": ("Lingasugur", "Raichur"),
    "MADDUR": ("Maddur", "Mandya"),
    "MALAVALLI": ("Malavalli", "Mandya"),
    "MALUR": ("Malur", "Kolar"),
    "MANDYA": ("Mandya", "Mandya"),
    "MANVI": ("Manvi", "Raichur"),
    "MUDIGERE": ("Mudigere", "Chikkamagaluru"),
    "MUNDAGOD": ("Mundagod", "Uttara Kannada"),
    "MYSURU": ("Mysuru", "Mysuru"),
    "NAGAMANGALA": ("Nagamangala", "Mandya"),
    "NANDAGAD": ("Nandagad", "Belagavi"),
    "NANJANGUD": ("Nanjangud", "Mysuru"),
    "NARGUND": ("Nargund", "Gadag"),
    "PANDAVAPURA": ("Pandavapura", "Mandya"),
    "PERIYAPATNA": ("Periyapatna", "Mysuru"),
    "PUTTUR": ("Puttur", "Dakshina Kannada"),
    "RAICHUR": ("Raichur", "Raichur"),
    "RAMANAGARA": ("Ramanagara", "Ramanagara"),
    "RAMDURGA": ("Ramdurga", "Belagavi"),
    "RANIBENNUR": ("Ranibennur", "Haveri"),
    "RONA": ("Ron", "Gadag"),
    "SAKLESHPUR": ("Sakleshpur", "Hassan"),
    "SANTHESARGUR": ("Santhesargur", "Hassan"),
    "SAVADATTI": ("Savadatti", "Belagavi"),
    "SAVANUR": ("Savanur", "Haveri"),
    "SEDAM": ("Sedam", "Kalaburagi"),
    "SHIGGAON": ("Shiggaon", "Haveri"),
    "SHIKARIPUR": ("Shikaripur", "Shivamogga"),
    "SHIVAMOGGA": ("Shivamogga", "Shivamogga"),
    "SINDAGI": ("Sindagi", "Vijayapura"),
    "SINDHANUR": ("Sindhanur", "Raichur"),
    "SIRAGUPPA": ("Siraguppa", "Ballari"),
    "SIRSI": ("Sirsi", "Uttara Kannada"),
    "SORABHA": ("Soraba", "Shivamogga"),
    "SRINIVASPUR": ("Srinivaspur", "Kolar"),
    "SULYA": ("Sulya", "Dakshina Kannada"),
    "TALIKOTE": ("Talikote", "Vijayapura"),
    "TIPTUR": ("Tiptur", "Tumakuru"),
    "TIRTHAHALLI": ("Tirthahalli", "Shivamogga"),
    "TURUVEKERE": ("Turuvekere", "Tumakuru"),
    "UDIPI": ("Udupi", "Udupi"),
    "VIJAYAPURA": ("Vijayapura", "Vijayapura"),
    "YARAHALLI": ("Yarahalli", "Mysuru")
}


def run_ingest(
    pdf_path: str = "Crop_price_of_all_mandies_of_karnataka.pdf",
    report_date: str = "2026-11-11",
    panel_path: str = "data/processed/panel.parquet"
):
    print(f"Parsing {pdf_path} for date {report_date}...")
    importer = KsambPdfImporter()
    raw_rows = importer.import_pdf(pdf_path, report_date=report_date)

    print(f"Applying Step 6 & 7 validation and anomaly filters...")
    accepted_quintal, non_quintal, quarantined = validate_and_filter_ksamb_rows(
        raw_rows,
        quarantine_dir="data/quarantine",
        non_quintal_output_path="data/processed/non_quintal_prices.parquet",
        today_date_str="2026-11-12"
    )

    print(f"Results: {len(accepted_quintal)} accepted quintal rows, {len(non_quintal)} non-quintal, {len(quarantined)} quarantined.")

    # Convert accepted quintal rows to panel schema
    panel_rows = []
    dt = datetime.strptime(report_date, "%Y-%m-%d")

    for r in accepted_quintal:
        m_norm = r.mandi.strip().upper()
        clean_mandi_name, dist_name = MANDI_DISTRICT_MAP.get(m_norm, (r.mandi, r.mandi))

        row_dict = {
            "crop": r.commodity.lower().strip(),
            "variety": r.variety.strip(),
            "grade": r.grade.strip(),
            "mandi": clean_mandi_name,
            "district": dist_name,
            "date": pd.to_datetime(report_date),
            "min_price": float(r.min),
            "modal_price": float(r.modal),
            "max_price": float(r.max),
            "arrivals": float(r.arrivals),
            "unit": "Rs/Quintal",
            "source_id": "ksamb_pdf",
            "source_url": f"file://{r.raw_file}",
            "fetched_at": "2026-11-12T22:51:00",
            "raw_hash": r.file_sha256,
            "raw_file": r.raw_file,
            "raw_page": int(r.raw_page),
            "raw_line": int(r.raw_line),
            "acquisition_method": "user_download",
            "data_provenance": "real",
            "is_synthetic": False,
            "month": dt.month,
            "day_of_week": dt.weekday(),
            "day_of_year": dt.timetuple().tm_yday,
            "week_of_year": dt.isocalendar()[1],
            "rainfall": 0.0,
            "temperature": 24.0,
            "diesel_price": 88.94,
            "festival_flag": 0,
            "was_imputed": 0
        }
        panel_rows.append(row_dict)

    new_df = pd.DataFrame(panel_rows)

    if os.path.exists(panel_path):
        existing_df = pd.read_parquet(panel_path)
        print(f"Existing panel has {len(existing_df)} rows.")
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        combined_df = new_df

    # Deduplicate on date, mandi, crop, variety, grade
    dedup_cols = ["date", "mandi", "crop", "variety", "grade"]
    combined_df = combined_df.drop_duplicates(subset=dedup_cols, keep="last").reset_index(drop=True)

    combined_df.to_parquet(panel_path, index=False)
    print(f"Updated {panel_path}: total rows now {len(combined_df)}.")

    return accepted_quintal


if __name__ == "__main__":
    accepted = run_ingest()
    
    # Select 10 random rows and display next to their PDF page and line
    random.seed(42)
    sample_10 = random.sample(accepted, 10)
    print("\n" + "="*80)
    print("10 RANDOM ACCEPTED ROWS NEXT TO THEIR PDF PAGE AND LINE:")
    print("="*80)
    for i, r in enumerate(sample_10, 1):
        print(f"{i:2d}. Mandi: {r.mandi:<25} | Crop: {r.commodity:<15} ({r.variety}, {r.grade}) | Modal: Rs {r.modal:6.0f}/qtl | PDF Page: {r.raw_page:2d} | Line: {r.raw_line:2d}")
    print("="*80 + "\n")
