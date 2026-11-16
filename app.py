"""Streamlit UI for Farmer Sell Advisor - All Crops & All Mandis in Karnataka."""

import os
import sys
import yaml
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.models_loader import AdvisorService

# Page configuration
st.set_page_config(
    page_title="Karnataka Farmer Sell Advisor",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-left: 5px solid #27ae60;
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 10px;
    }
    .disclaimer-card {
        background-color: #fef9e7;
        border-left: 5px solid #f39c12;
        padding: 12px;
        border-radius: 6px;
        font-size: 0.9em;
        margin-top: 15px;
    }
    .stale-banner {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeeba;
        padding: 12px;
        border-radius: 8px;
        font-weight: 600;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_service():
    return AdvisorService.get_instance()


service = get_service()
crops_list = service.get_crops()
districts_list = service.get_districts()
mandis_list = service.get_mandis()

crops_df = pd.DataFrame(crops_list)
districts_df = pd.DataFrame(districts_list)
mandis_df = pd.DataFrame(mandis_list)

# Sidebar
st.sidebar.title("👨‍🌾 Farmer Profile & Inputs")

language_map = {
    "English": "en",
    "ಕನ್ನಡ (Kannada)": "kn",
    "हिन्दी (Hindi)": "hi"
}
selected_lang_label = st.sidebar.radio("Language / ಭಾಷೆ / भाषा", list(language_map.keys()), index=0)
selected_lang = language_map[selected_lang_label]

st.sidebar.markdown("---")

# Crop Selection: Category Filter + Crop Dropdown (All 102 crops)
st.sidebar.subheader("🌱 Select Crop / ಬೆಳೆ")
categories = ["All Categories"] + sorted(crops_df["category"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Filter Category", categories, index=0)

if selected_category != "All Categories":
    filtered_crops_df = crops_df[crops_df["category"] == selected_category]
else:
    filtered_crops_df = crops_df

crop_options = {}
for _, row in filtered_crops_df.iterrows():
    c_en = row["name_en"]
    c_kn = row.get("name_kn") or c_en
    c_hi = row.get("name_hi") or c_en
    unit = row.get("unit", "Quintal")
    cat = row.get("category", "")
    if selected_lang == "kn":
        display_name = f"{c_kn} ({c_en}) — {cat} ({unit})"
    elif selected_lang == "hi":
        display_name = f"{c_hi} ({c_en}) — {cat} ({unit})"
    else:
        display_name = f"{c_en} — {cat} ({unit})"
    crop_options[c_en] = display_name

selected_crop_en = st.sidebar.selectbox(
    f"Crop ({len(crop_options)} available)",
    options=list(crop_options.keys()),
    format_func=lambda x: crop_options[x],
    index=0
)
selected_crop_row = crops_df[crops_df["name_en"] == selected_crop_en].iloc[0]
crop_unit = selected_crop_row.get("unit", "Quintal")

st.sidebar.markdown("---")

# Mandi Selection: District Filter + Mandi Dropdown (All 115 mandis)
st.sidebar.subheader("📍 Select Mandi / ಮಾರುಕಟ್ಟೆ")
district_options = ["All Districts"] + sorted(districts_df["name_en"].dropna().unique().tolist())
selected_district = st.sidebar.selectbox("Filter District", district_options, index=0)

if selected_district != "All Districts":
    filtered_mandis_df = mandis_df[mandis_df["district_en"] == selected_district]
else:
    filtered_mandis_df = mandis_df

mandi_options = {}
for _, row in filtered_mandis_df.iterrows():
    m_en = row["name_en"]
    m_kn = row.get("name_kn") or m_en
    dist_en = row.get("district_en", "")
    tier_tag = row.get("tier", "APMC")
    if selected_lang == "kn":
        display_name = f"{m_kn} ({m_en}) — {dist_en} [{tier_tag}]"
    else:
        display_name = f"{m_en} — {dist_en} [{tier_tag}]"
    mandi_options[m_en] = display_name

selected_mandi_en = st.sidebar.selectbox(
    f"Mandi ({len(mandi_options)} available)",
    options=list(mandi_options.keys()),
    format_func=lambda x: mandi_options[x],
    index=0
)
selected_mandi_row = mandis_df[mandis_df["name_en"] == selected_mandi_en].iloc[0]
mandi_raw = selected_mandi_row["raw_market_name"]
mandi_lat = float(selected_mandi_row["lat"])
mandi_lon = float(selected_mandi_row["lon"])

# Harvest Quantity
quantity = st.sidebar.number_input(
    f"Harvest Quantity ({crop_unit})",
    min_value=1.0,
    max_value=5000.0,
    value=30.0,
    step=5.0
)

# Search Radius for where-to-sell
radius_km = st.sidebar.slider(
    "Search Radius for Nearby Mandis (km)",
    min_value=25,
    max_value=300,
    value=100,
    step=25
)

# Storage & Loan Inputs
storage_display_map = {
    "Open Farm Storage (Kaccha Shed - High Spoilage)": "open",
    "Standard Ventilated Warehouse (APMC / Govt)": "warehouse",
    "Cold Storage / Controlled Atmosphere": "cold_storage"
}
storage_selected_label = st.sidebar.selectbox("Storage Available", list(storage_display_map.keys()), index=0)
storage_type = storage_display_map[storage_selected_label]

has_trader_debt = st.sidebar.checkbox(
    "Farmer owes informal trader loan (24% p.a. interest)",
    value=False,
    help="Check if farmer has taken pre-harvest crop advances requiring immediate sale."
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Advisor Rule**: The farmer always makes the final sale decision. "
    "All reported prices are verified against KSAMB daily bulletins."
)

# Main Dashboard
st.title("🌾 Karnataka Farmer Sell Advisor (All Crops & Mandis)")
st.caption("Serving all 102 crops and 115 APMC mandis across Karnataka based on verified KSAMB daily reporting.")

# Mandatory Freshness Banner
health = service.get_health_status()
if health.get("is_stale"):
    st.markdown(
        f"""<div class="stale-banner">
        ⚠️ <strong>Latest reported: {health.get('last_data_date')}</strong> — 
        Showing latest verified KSAMB APMC daily bulletin ({health.get('days_since_data')} days ago). 
        Never presented as today's live spot rate.
        </div>""",
        unsafe_allow_html=True
    )

# 1. Fetch Today's Reported Price
price_data = service.get_today_price(selected_crop_en, mandi_raw)

st.subheader(f"📊 Market Report: {selected_crop_en} at {selected_mandi_en}")

if price_data.get("status") == "Data under review":
    st.error(
        f"⚠️ **Data Under Review**: All market records for **{selected_mandi_en}** were quarantined "
        f"during data ingestion due to anomalous flat pricing or identical triples across commodities. "
        f"No unverified prices are displayed to farmers."
    )
elif not price_data.get("available"):
    st.info(
        f"ℹ️ **Not Available**: No transaction recorded for **{selected_crop_en}** at **{selected_mandi_en}** "
        f"in the latest KSAMB report ({price_data.get('date', '2026-11-11')}). Never guessing or imputing prices."
    )
else:
    headline = price_data.get("headline_price", {})
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="Modal Price",
            value=f"Rs {headline.get('modal_price', 0):,.0f} / {crop_unit}",
            delta=f"Grade: {headline.get('grade', 'FAQ')}"
        )
    with col2:
        st.metric(
            label="Price Range (Min — Max)",
            value=f"Rs {headline.get('min_price', 0):,.0f} — {headline.get('max_price', 0):,.0f}",
            delta=f"Variety: {headline.get('variety', 'Standard')}"
        )
    with col3:
        st.metric(
            label="Arrival Volume",
            value=f"{headline.get('arrivals', 0):,.0f} {crop_unit}",
            delta="Daily reported volume"
        )
    with col4:
        st.metric(
            label="Report Freshness & Tier",
            value=f"Tier B (Reported Only)",
            delta=f"Reported: {price_data.get('date')}"
        )

    # Show all reported grades if multiple exist
    all_grades = price_data.get("all_grades", [])
    if len(all_grades) > 1:
        st.markdown("**All Reported Grades for this Mandi:**")
        grade_rows = []
        for g in all_grades:
            grade_rows.append({
                "Grade": g.get("grade"),
                "Variety": g.get("variety"),
                "Modal Price (Rs)": g.get("modal_price"),
                "Min Price (Rs)": g.get("min_price"),
                "Max Price (Rs)": g.get("max_price"),
                "Arrivals": g.get("arrivals"),
                "Status": "Headline (Highest Volume)" if g.get("is_headline") else "Additional Grade"
            })
        st.dataframe(pd.DataFrame(grade_rows), use_container_width=True)

st.markdown("---")

# 2. WHERE TO SELL: Spatial Comparison across All Mandis in Range
st.subheader(f"📍 WHERE TO SELL: Mandi Comparison within {radius_km} km")

if crop_unit != "Quintal":
    st.info(
        f"ℹ️ Transport net-price deduction math applies to Quintal commodities. "
        f"Non-quintal commodities ({crop_unit}) display reported prices only."
    )
else:
    with st.spinner("Analyzing all reporting APMC mandis within radius..."):
        where_res = service.evaluate_where_to_sell_all_mandis(
            crop_name=selected_crop_en,
            farmer_lat=mandi_lat,
            farmer_lon=mandi_lon,
            quantity_quintals=quantity,
            radius_km=float(radius_km)
        )

    candidates = where_res.get("results", [])
    if not candidates:
        st.warning(
            f"No APMC mandis within {radius_km} km reported transactions for **{selected_crop_en}** on this date. "
            f"({where_res.get('excluded_mandis_no_report', 0)} nearby mandis had zero reports)."
        )
    else:
        st.markdown(
            f"Found **{len(candidates)}** reporting markets within {radius_km} km. "
            f"Ranked by **net realized modal return** after transport freight (`1.25 # Assumption` road factor), "
            f"statutory APMC fees (1.5%) + commission (2.0%), and transit shrinkage (0.25%/100km)."
        )

        table_data = []
        for rank, c in enumerate(candidates, 1):
            table_data.append({
                "Rank": f"#{rank}",
                "Mandi": c["mandi"],
                "District": c["district"],
                "Road Dist (km)": f"{c['distance_km']} km",
                "Gross Modal": f"Rs {c['reported_modal_price']:,.0f}",
                "Transport Cost": f"- Rs {c['transport_cost_per_qtl']:,.1f}",
                "Fees & Comm.": f"- Rs {c['fees_and_commission_per_qtl']:,.1f}",
                "Shrinkage Loss": f"- Rs {c['transit_shrinkage_per_qtl']:,.1f}",
                "Net Modal Return": f"Rs {c['net_price_modal']:,.1f}",
                "Net Range (Min–Max)": c["net_price_range"],
                "Gain vs Local": f"{'+' if c['gain_over_local_per_qtl'] >= 0 else ''}Rs {c['gain_over_local_per_qtl']:.1f}/qtl",
                "Total Lot Gain": f"{'+' if c['total_gain_rs'] >= 0 else ''}Rs {c['total_gain_rs']:,.0f}"
            })
        st.dataframe(pd.DataFrame(table_data), use_container_width=True)

        if where_res.get("excluded_mandis_no_report", 0) > 0:
            st.caption(f"ℹ️ {where_res['excluded_mandis_no_report']} other mandis in radius had no reported transactions for {selected_crop_en}.")

st.markdown("---")

# 3. Advisory Summary
st.subheader("🗣️ Advisory Guidance & Decision Support")

if selected_lang == "kn":
    st.markdown(f"""
    - **ಆಯ್ಕೆ ಮಾಡಿದ ಬೆಳೆ**: {selected_crop_row.get('name_kn', selected_crop_en)} ({selected_crop_en})
    - **ಆಯ್ಕೆ ಮಾಡಿದ ಮಾರುಕಟ್ಟೆ**: {selected_mandi_row.get('name_kn', selected_mandi_en)} ({selected_mandi_en})
    - **ವರದಿ ಸ್ಥಿತಿ**: 2026-11-11 ರ KSAMB ಅಧಿಕೃತ ಬುಲೆಟಿನ್ ಪ್ರಕಾರ. ಹಳೆಯ ದರವನ್ನು ಇಂದಿನ ನೇರ ಬೆಲೆ ಎಂದು ಬಿಂಬಿಸಲಾಗುವುದಿಲ್ಲ.
    - **ಮುನ್ಸೂಚನೆ ಸ್ಥಿತಿ (Tier B)**: ಪ್ರಸ್ತುತ ಕೇವಲ 1 ದಿನದ ಅಧಿಕೃತ ವರದಿ ಇರುವುದರಿಂದ, ಮುಂದಿನ ದಿನಗಳ ಮುನ್ಸೂಚನೆ (Forecast) ಅನ್ನು ತಡೆಹಿಡಿಯಲಾಗಿದೆ. ಕನಿಷ್ಠ 2 ವರ್ಷಗಳ ಇತಿಹಾಸ ಲಭ್ಯವಾದಾಗ ಮಾತ್ರ ಮುನ್ಸೂಚನೆ ನೀಡಲಾಗುತ್ತದೆ.
    """)
elif selected_lang == "hi":
    st.markdown(f"""
    - **चयनित फसल**: {selected_crop_row.get('name_hi', selected_crop_en)} ({selected_crop_en})
    - **चयनित मंडी**: {selected_mandi_en} ({selected_mandi_row.get('district_en', '')})
    - **रिपोर्ट स्थिति**: KSAMB आधिकारिक दैनिक बुलेटिन (11 Nov 2026).
    - **पूर्वानुमान स्थिति (Tier B)**: चूंकि केवल 1 दिन का वास्तविक डेटा उपलब्ध है, अतः भविष्य का पूर्वानुमान अक्षम रखा गया है।
    """)
else:
    st.markdown(f"""
    - **Selected Crop**: {selected_crop_en} ({selected_crop_row.get('category', '')}, {crop_unit})
    - **Selected Mandi**: {selected_mandi_en} ({selected_mandi_row.get('district_en', '')})
    - **Report Status**: Latest KSAMB daily report dated 11 Nov 2026.
    - **Tier Status (Tier B)**: Real price reporting only. Forward ML price forecasts are disabled until 2 years of daily records exist.
    """)

st.markdown("""
<div class="disclaimer-card">
    ⚠️ <strong>Statutory Disclaimer for Farmers & FPOs</strong>: 
    Prices reflect KSAMB APMC daily reports. No prices are imputed or guessed. 
    <strong>The farmer makes the final sale decision; this advisor acts solely as decision intelligence.</strong>
</div>
""", unsafe_allow_html=True)
