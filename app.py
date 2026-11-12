"""Streamlit Demo UI for Farmer Sell Advisor."""

import os
import sys
import yaml
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.agent.advisor import (
    tool_get_forecast,
    tool_rank_mandis,
    tool_hold_vs_sell,
    tool_find_storage,
    synthesize_advice_multilingual
)

# Page configuration
st.set_page_config(
    page_title="Farmer Sell Advisor (Onion)",
    page_icon="🧅",
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
</style>
""", unsafe_allow_html=True)


def load_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


config = load_config()

# Sidebar: Farmer Profile & Inputs
st.sidebar.title("👨‍🌾 Farmer Profile & Harvest")

crop_name = st.sidebar.selectbox("Crop", ["Onion (Nashik / Bellary Red)"], index=0)
farmer_location = st.sidebar.selectbox(
    "Farmer Mandi / Location",
    ["Kolar", "Chikkaballapur", "Bengaluru (Yeshwanthpur)"],
    index=0
)
quantity_quintals = st.sidebar.number_input(
    "Harvest Quantity to Sell (Quintals)",
    min_value=5.0,
    max_value=1000.0,
    value=50.0,
    step=5.0
)

storage_display_map = {
    "Open Farm Storage (Kaccha Shed - High Spoilage)": "open",
    "Standard Ventilated Warehouse (Govt / APMC)": "warehouse",
    "Cold Storage / Controlled Atmosphere": "cold_storage"
}
storage_selected_label = st.sidebar.selectbox("Storage Available", list(storage_display_map.keys()), index=0)
storage_type = storage_display_map[storage_selected_label]

has_trader_debt = st.sidebar.checkbox(
    "Farmer owes informal trader loan (24% p.a. interest)",
    value=False,
    help="Check if farmer has taken pre-harvest crop advances from a commission agent or trader."
)

language_map = {
    "English": "en",
    "हिन्दी (Hindi)": "hi",
    "ಕನ್ನಡ (Kannada)": "kn"
}
selected_lang_label = st.sidebar.radio("Advisory Language / ಭಾಷೆ / भाषा", list(language_map.keys()), index=0)
selected_lang = language_map[selected_lang_label]

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Advisor Rule**: The farmer always makes the final decision. "
    "All price projections show uncertainty ranges (P10 downside to P90 upside)."
)

# Main Dashboard
st.title("🧅 Farmer Sell Advisor: Onion Decision Support")

# DATA_PROVENANCE Check & Mandatory Banner
has_synthetic = True
try:
    panel_path = config["paths"]["processed_panel"]
    if os.path.exists(panel_path):
        pdf = pd.read_parquet(panel_path)
        if "is_synthetic" in pdf.columns:
            has_synthetic = bool(pdf["is_synthetic"].any())
        elif "data_provenance" in pdf.columns:
            has_synthetic = bool((pdf["data_provenance"] == "synthetic").any())
except Exception:
    pass

if has_synthetic:
    st.error(
        "⚠️ **SYNTHETIC DATA - NOT FOR REAL DECISIONS** ⚠️\n\n"
        "The underlying dataset and models contain generated/synthetic rows. "
        "This application is running in **DEMONSTRATION MODE ONLY**. "
        "**DO NOT USE THIS SYSTEM FOR REAL HARVESTING, COMMERCE, OR FINANCIAL COMMITMENTS.**\n\n"
        "*To transition to verified operational decisions: place real Agmarknet CSV files into `data/raw/real/`, "
        "rebuild the panel (`python run.py data`), and retrain the models (`python run.py train`).*"
    )
    st.sidebar.error("⚠️ **SYNTHETIC DATA - NOT FOR REAL DECISIONS**")

st.markdown(
    "**Objective**: Helping smallholder farmers decide **WHERE** to sell, **WHEN** to sell, "
    "and at what **expected price**, maximizing net income after freight, commissions, and storage spoilage."
)

# Fetch Decision Data
with st.spinner("Analyzing APMC market arrivals, spatial price spreads, and post-harvest decay..."):
    # 1. Where to sell optimization
    ranking_data = tool_rank_mandis(farmer_location, quantity_quintals, horizon_days=7)
    top_mandis = ranking_data["top_3_mandis"]
    best_mandi = top_mandis[0]

    # 2. When to sell simulation
    hold_data = tool_hold_vs_sell(farmer_location, quantity_quintals, storage_type, has_trader_debt)
    best_k = hold_data["best_k_days"]

    # 3. Plain language multilingual text
    advice_text = synthesize_advice_multilingual(
        farmer_location, quantity_quintals, storage_type, has_trader_debt, selected_lang
    )

# Top Metrics Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Top Mandi Destination",
        value=best_mandi["mandi"],
        delta=f"{best_mandi['distance_km']} km away"
    )

with col2:
    st.metric(
        label="Expected Net Price (P50)",
        value=f"Rs {best_mandi['net_price_p50']:.1f}/qtl",
        delta=f"P10: Rs {best_mandi['net_price_p10']:.1f}/qtl"
    )

with col3:
    gain_val = best_mandi["gain_over_local_per_qtl"]
    lot_val = best_mandi["total_gain_rs"]
    st.metric(
        label="Advantage vs Local Sale",
        value=f"+Rs {gain_val:.1f}/qtl",
        delta=f"+Rs {lot_val:,.0f} Total Lot"
    )

with col4:
    timing_label = "SELL TODAY" if best_k == 0 else f"HOLD {best_k} DAYS"
    timing_delta = "0d wait" if best_k == 0 else f"+Rs {hold_data['max_expected_gain_per_qtl']:.1f}/qtl gain"
    st.metric(
        label="Optimal Timing Recommendation",
        value=timing_label,
        delta=timing_delta
    )

st.markdown("---")

# Section: Plain Language Multilingual Advice Box
st.subheader("🗣️ Plain-Language Farmer Advisory")
st.markdown(advice_text)

st.markdown("---")

# Section: Where to Sell Breakdown Table
st.subheader("📍 WHERE TO SELL: Mandi Net Realized Return Comparison")
st.markdown(
    "Net price accounts for **gross market price**, **freight transport cost**, **APMC market fees (1.5%)**, "
    "**commission agent charges (2.0%)**, **handling hamali**, and **in-transit shrinkage**."
)

table_rows = []
for idx, m in enumerate(top_mandis, 1):
    table_rows.append({
        "Rank": f"#{idx}",
        "Mandi": m["mandi"],
        "Distance (km)": f"{m['distance_km']} km",
        "Forecast Range (P10–P90)": f"Rs {m['forecast_p10']:.0f} – {m['forecast_p90']:.0f}",
        "Expected Gross (P50)": f"Rs {m['forecast_p50']:.1f}",
        "Transport Freight": f"- Rs {m['transport_cost_per_qtl']:.1f}",
        "Fees & Comm.": f"- Rs {m['fees_and_commission_per_qtl']:.1f}",
        "Transit Loss": f"- Rs {m['shrinkage_loss_per_qtl']:.1f}",
        "Net Realized P50": f"Rs {m['net_price_p50']:.1f}",
        "Downside P10": f"Rs {m['net_price_p10']:.1f}",
        "Gain vs Local": f"+Rs {m['gain_over_local_per_qtl']:.1f}/qtl",
        "Total Lot Gain": f"+Rs {m['total_gain_rs']:,.0f}"
    })

st.dataframe(pd.DataFrame(table_rows), use_container_width=True)

# Section: Interactive Forecast Fan Chart & Hold-vs-Sell Simulation
st.markdown("---")
tab1, tab2 = st.tabs(["📈 Price Forecast Fan Chart (P10–P90)", "⏳ Hold vs. Sell Monte Carlo Simulation"])

with tab1:
    st.subheader(f"30-Day Forward Price Fan Chart: {farmer_location}")
    st.markdown(
        "LightGBM Quantile Regression forecasts across **7, 14, and 30-day horizons**. "
        "The shaded band represents the calibrated 80% confidence interval ($P10$ to $P90$)."
    )

    fc_7 = tool_get_forecast(farmer_location, 7)
    fc_14 = tool_get_forecast(farmer_location, 14)
    fc_30 = tool_get_forecast(farmer_location, 30)

    horizons_x = [0, 7, 14, 30]
    spot_val = fc_7["p50_expected"] / 1.012  # approximate spot today
    p10_y = [spot_val - 120, fc_7["p10_downside"], fc_14["p10_downside"], fc_30["p10_downside"]]
    p50_y = [spot_val, fc_7["p50_expected"], fc_14["p50_expected"], fc_30["p50_expected"]]
    p90_y = [spot_val + 140, fc_7["p90_upside"], fc_14["p90_upside"], fc_30["p90_upside"]]

    fig_fan = go.Figure()
    # P90
    fig_fan.add_trace(go.Scatter(
        x=horizons_x, y=p90_y,
        mode="lines",
        line=dict(width=0),
        showlegend=False,
        name="P90 Upside"
    ))
    # P10 with fill to P90
    fig_fan.add_trace(go.Scatter(
        x=horizons_x, y=p10_y,
        mode="lines",
        fill="tonexty",
        fillcolor="rgba(39, 174, 96, 0.25)",
        line=dict(width=0),
        name="80% Uncertainty Band (P10–P90)"
    ))
    # P50 Median Expected
    fig_fan.add_trace(go.Scatter(
        x=horizons_x, y=p50_y,
        mode="lines+markers",
        line=dict(color="#27ae60", width=3, dash="solid"),
        marker=dict(size=8),
        name="P50 Expected Price"
    ))

    fig_fan.update_layout(
        xaxis_title="Forecast Horizon (Days Ahead)",
        yaxis_title="Price (Rs / Quintal)",
        xaxis=dict(tickvals=[0, 7, 14, 30], ticktext=["Today (Spot)", "7 Days", "14 Days", "30 Days"]),
        template="plotly_white",
        height=420
    )
    st.plotly_chart(fig_fan, use_container_width=True)

with tab2:
    st.subheader(f"Monte Carlo Simulation: Spoilage Decay vs Market Gain")
    st.markdown(
        f"Simulating **10,000 draws** from the forward price distribution factoring in "
        f"**{storage_selected_label}** and **{'Trader Debt (24% p.a.)' if has_trader_debt else 'Zero Debt / e-NWR (9% p.a.)'}**."
    )

    sim_horizons = [7, 14, 30]
    expected_gains = [hold_data["horizons"][k]["expected_gain_per_qtl"] for k in sim_horizons]
    win_probs = [hold_data["horizons"][k]["prob_wait_beats_today_pct"] for k in sim_horizons]
    p10_worst = [hold_data["horizons"][k]["worst_case_p10_gain"] for k in sim_horizons]

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=[f"{k} Days" for k in sim_horizons],
        y=expected_gains,
        name="Expected Net Gain (Rs/qtl)",
        marker_color=["#27ae60" if g > 0 else "#e74c3c" for g in expected_gains],
        text=[f"Rs {g:+.1f}" for g in expected_gains],
        textposition="auto"
    ))
    fig_bar.add_trace(go.Scatter(
        x=[f"{k} Days" for k in sim_horizons],
        y=p10_worst,
        name="Worst Case (P10 Net Gain)",
        mode="lines+markers",
        line=dict(color="#e67e22", width=2.5, dash="dash"),
        marker=dict(size=6)
    ))
    fig_bar.update_layout(
        yaxis_title="Net Gain / Loss over Selling Today (Rs/qtl)",
        template="plotly_white",
        height=380,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Spoilage & cost detail table
    detail_rows = []
    for k in [0, 7, 14, 30]:
        h_info = hold_data["horizons"][k]
        detail_rows.append({
            "Wait (Days)": f"{k} Days" if k > 0 else "Sell Today",
            "Cumulative Spoilage Loss": f"{h_info['spoilage_loss_pct']:.1f}%",
            "Storage Rent / Qtl": f"Rs {h_info['storage_cost_per_qtl']:.2f}",
            "Interest Cost / Qtl": f"Rs {h_info['interest_cost_per_qtl']:.2f}",
            "Win Probability": f"{h_info['prob_wait_beats_today_pct']:.1f}%",
            "Expected Net Gain": f"Rs {h_info['expected_gain_per_qtl']:+.2f} / qtl",
            "Worst-Case (P10)": f"Rs {h_info['worst_case_p10_gain']:+.2f} / qtl"
        })
    st.table(pd.DataFrame(detail_rows))

st.markdown("""
<div class="disclaimer-card">
    ⚠️ <strong>Statutory Disclaimer for Farmers & FPOs</strong>: 
    All models produce probabilistic forecasts (P10 to P90) based on historical APMC arrivals and seasonal price volatility. 
    Weather shocks, border trade bans, or export duty changes can impact market prices. 
    <strong>The farmer makes the final sale decision; this advisor acts solely as decision intelligence.</strong>
</div>
""", unsafe_allow_html=True)

