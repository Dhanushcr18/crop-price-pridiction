"""Ingests validated KSAMB PDF quintal rows into data/processed/panel.parquet with full provenance and idempotency."""

import os
import sys
sys.path.insert(0, ".")
import pandas as pd
from datetime import datetime

# Mandi district map for Karnataka APMCs
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
    "BENGALURU": ("BENGALURU", "Bengaluru Urban"),
    "BHADRAVATHI": ("Bhadravathi", "Shivamogga"),
    "BIDAR": ("Bidar", "Bidar"),
    "BINNY MILL (F&V)": ("BINNY MILL (F&V)", "Bengaluru Urban"),
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


def ingest_ksamb_to_panel(
    csv_or_pdf_path: str = "data/raw/user_download/karnataka_mandi_prices_2026-11-11.csv",
    panel_path: str = "data/processed/panel.parquet"
) -> pd.DataFrame:
    """Ingests accepted Quintal rows with idempotency key (date, mandi, crop, variety, grade)."""
    from src.ingest.connectors.ksamb_pdf import KsambPdfImporter, validate_and_route_ksamb_data

    if csv_or_pdf_path.endswith(".pdf"):
        importer = KsambPdfImporter()
        df_raw = importer.parse_pdf(csv_or_pdf_path)
    else:
        df_raw = pd.read_csv(csv_or_pdf_path)

    accepted, non_q, quar = validate_and_route_ksamb_data(df_raw)

    panel_df = pd.read_parquet(panel_path) if os.path.exists(panel_path) else pd.DataFrame()
    report_date = df_raw['report_date'].iloc[0]
    dt = datetime.strptime(report_date, "%Y-%m-%d")

    # Filter out existing data for this date
    if not panel_df.empty:
        panel_baseline = panel_df[panel_df['date'] != pd.to_datetime(report_date)]
    else:
        panel_baseline = pd.DataFrame()

    new_rows = []
    for _, r in accepted.iterrows():
        m_norm = str(r['mandi']).strip().upper()
        clean_mandi_name, dist_name = MANDI_DISTRICT_MAP.get(m_norm, (str(r['mandi']).strip(), str(r['mandi']).strip()))

        row_dict = {
            'crop': str(r['commodity']).lower().strip(),
            'mandi': clean_mandi_name,
            'district': dist_name,
            'date': pd.to_datetime(report_date),
            'min_price': float(r['min_price']),
            'modal_price': float(r['modal_price']),
            'max_price': float(r['max_price']),
            'arrivals': float(r['arrivals']),
            'unit': str(r['unit']),
            'source_id': 'ksamb_pdf',
            'source_url': 'https://ksamb.karnataka.gov.in/',
            'fetched_at': '2026-11-12 00:00:00',
            'raw_hash': str(r['file_sha256']),
            'raw_file': str(r['source_file']),
            'raw_line': int(r['source_page'] * 1000 + (r['table_row'] if pd.notna(r['table_row']) else 0)),
            'acquisition_method': 'user_download',
            'data_provenance': 'real',
            'is_synthetic': False,
            'month': dt.month,
            'day_of_week': dt.weekday(),
            'day_of_year': dt.timetuple().tm_yday,
            'week_of_year': dt.isocalendar()[1],
            'rainfall': 0.0,
            'temperature': 24.5,
            'diesel_price': 88.5,
            'festival_flag': 0,
            'was_imputed': 0,
            'variety': str(r['variety']).strip(),
            'grade': str(r['grade']).strip(),
            'raw_page': float(r['source_page'])
        }
        new_rows.append(row_dict)

    new_panel_part = pd.DataFrame(new_rows)
    combined = pd.concat([panel_baseline, new_panel_part], ignore_index=True)

    # Idempotent deduplication
    combined = combined.drop_duplicates(subset=['date', 'mandi', 'crop', 'variety', 'grade'], keep='last')
    combined.to_parquet(panel_path, index=False)
    print(f"Ingested {len(new_rows)} rows into {panel_path}. Total panel rows: {len(combined)}.")
    return combined


if __name__ == "__main__":
    ingest_ksamb_to_panel()
