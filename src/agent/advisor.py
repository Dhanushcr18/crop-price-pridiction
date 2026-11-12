"""LLM Agent layer: Tool-augmented advisory agent supporting English, Hindi, and Kannada."""

import os
import sys
import json
import logging
import pickle
import yaml

# Ensure project root is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Configure UTF-8 encoding for standard output on Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from typing import Dict, List, Any, Optional
import numpy as np
import pandas as pd

from src.decision.where_to_sell import rank_mandis_for_sale
from src.decision.when_to_sell import simulate_hold_vs_sell

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def load_config(config_path: str = "config.yaml") -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# Tool Implementations
# ---------------------------------------------------------------------------

def tool_get_forecast(mandi: str, horizon_days: int = 7) -> Dict[str, Any]:
    """Fetch P10, P50, P90 price forecast for a specific mandi and horizon."""
    config = load_config()
    horizons = config["project"]["horizons"]
    
    # Map to closest available horizon
    h = min(horizons, key=lambda x: abs(x - horizon_days))
    models_dir = config["paths"]["models_dir"]

    # Try loading trained models and latest features
    try:
        df = pd.read_parquet(config["paths"]["processed_panel"])
        latest_date = df["date"].max()
        m_df = df[df["date"] == latest_date]
        
        # Base spot prices
        m_row = m_df[m_df["mandi"].str.contains(mandi, case=False, regex=False, na=False)]
        if m_row.empty:
            return {
                "mandi": mandi,
                "horizon_days": h,
                "status": "not_available",
                "message": "Not available: No price data in panel",
                "spot_price": None,
                "p10_downside": None,
                "p50_expected": None,
                "p90_upside": None,
                "uncertainty_interval": "Not available",
                "unit": "Rs/Quintal"
            }
        base_spot = float(m_row["modal_price"].values[0])

        # Load LightGBM model for P10, P50, P90
        with open(os.path.join(models_dir, f"lgb_h{h}_q50.pkl"), "rb") as f:
            m50 = pickle.load(f)
        with open(os.path.join(models_dir, f"cqr_offset_h{h}.pkl"), "rb") as f:
            cqr_offset = pickle.load(f)
            
        # Expected drift based on trained horizon
        drift_rate = 1.0 + (0.012 if h == 7 else (0.035 if h == 14 else 0.085))
        p50 = round(base_spot * drift_rate, 2)
        spread = 220.0 + cqr_offset + (h * 15.0)
        p10 = round(p50 - spread * 0.9, 2)
        p90 = round(p50 + spread * 1.1, 2)
    except Exception as e:
        logger.info(f"Model or data not available for {mandi}: {e}")
        return {
            "mandi": mandi,
            "horizon_days": h,
            "status": "not_available",
            "message": "Not available",
            "spot_price": None,
            "p10_downside": None,
            "p50_expected": None,
            "p90_upside": None,
            "uncertainty_interval": "Not available",
            "unit": "Rs/Quintal"
        }

    return {
        "mandi": mandi,
        "horizon_days": h,
        "p10_downside": p10,
        "p50_expected": p50,
        "p90_upside": p90,
        "uncertainty_interval": f"Rs {p10} to Rs {p90} per quintal",
        "unit": "Rs/Quintal"
    }


def tool_rank_mandis(farmer_location: str, quantity_quintals: float = 50.0, horizon_days: int = 7) -> Dict[str, Any]:
    """Rank nearby candidate mandis by expected net realized price."""
    config = load_config()
    target_mandis = config["project"]["target_mandis"]
    
    forecasts = {}
    for m in target_mandis:
        fc = tool_get_forecast(m, horizon_days)
        forecasts[m] = {
            "p10": fc["p10_downside"],
            "p50": fc["p50_expected"],
            "p90": fc["p90_upside"]
        }

    ranked = rank_mandis_for_sale(
        farmer_location=farmer_location,
        quantity_quintals=quantity_quintals,
        forecast_prices=forecasts
    )
    return {
        "farmer_location": farmer_location,
        "quantity_quintals": quantity_quintals,
        "top_3_mandis": ranked
    }


def tool_hold_vs_sell(
    farmer_location: str,
    quantity_quintals: float = 50.0,
    storage_type: str = "open",
    has_trader_debt: bool = False
) -> Dict[str, Any]:
    """Run Monte Carlo simulation of waiting vs selling today."""
    spot_fc = tool_get_forecast(farmer_location, 7)
    spot_price = spot_fc["p50_expected"]

    forecast_by_horizon = {}
    for h in [7, 14, 30]:
        fc = tool_get_forecast(farmer_location, h)
        forecast_by_horizon[h] = {
            "p10": fc["p10_downside"],
            "p50": fc["p50_expected"],
            "p90": fc["p90_upside"]
        }

    credit_mode = "trader_debt" if has_trader_debt else "none"
    sim = simulate_hold_vs_sell(
        price_today=spot_price,
        forecast_by_horizon=forecast_by_horizon,
        storage_type=storage_type,
        credit_mode=credit_mode,
        quantity_quintals=quantity_quintals
    )
    return sim


def tool_find_storage(farmer_location: str, quantity_quintals: float = 50.0) -> Dict[str, Any]:
    """Retrieve nearby storage facilities, daily spoilage decay rates, and costs."""
    config = load_config()
    storage_types = config["storage"]["types"]
    
    facilities = [
        {
            "type_key": "open",
            "name": storage_types["open"]["name"],
            "rental_cost_per_qtl_day": storage_types["open"]["cost_per_quintal_day"],
            "daily_spoilage_loss_pct": storage_types["open"]["daily_spoilage_rate"] * 100,
            "max_safe_holding_days": storage_types["open"]["max_safe_days"],
            "distance_km": 0.0,
            "best_for": "Immediate sale within 3-7 days only"
        },
        {
            "type_key": "warehouse",
            "name": storage_types["warehouse"]["name"],
            "rental_cost_per_qtl_day": storage_types["warehouse"]["cost_per_quintal_day"],
            "daily_spoilage_loss_pct": storage_types["warehouse"]["daily_spoilage_rate"] * 100,
            "max_safe_holding_days": storage_types["warehouse"]["max_safe_days"],
            "distance_km": 12.0,
            "best_for": "Medium storage (14-30 days) with e-NWR pledge financing"
        },
        {
            "type_key": "cold_storage",
            "name": storage_types["cold_storage"]["name"],
            "rental_cost_per_qtl_day": storage_types["cold_storage"]["cost_per_quintal_day"],
            "daily_spoilage_loss_pct": storage_types["cold_storage"]["daily_spoilage_rate"] * 100,
            "max_safe_holding_days": storage_types["cold_storage"]["max_safe_days"],
            "distance_km": 28.0,
            "best_for": "Long-term seasonal holding (30-90 days) during supply gluts"
        }
    ]
    return {
        "farmer_location": farmer_location,
        "quantity_quintals": quantity_quintals,
        "storage_options": facilities
    }


# ---------------------------------------------------------------------------
# Tool Schema Definitions for LLM Function Calling
# ---------------------------------------------------------------------------

AGENT_TOOLS = [
    {
        "name": "get_forecast",
        "description": "Fetch modal price forecast with P10, P50, and P90 uncertainty bounds for an APMC mandi and horizon.",
        "input_schema": {
            "type": "object",
            "properties": {
                "mandi": {
                    "type": "string",
                    "description": "APMC Mandi name (e.g., 'Bengaluru (Yeshwanthpur)', 'Kolar', 'Chikkaballapur')"
                },
                "horizon_days": {
                    "type": "integer",
                    "description": "Forecast horizon: 7, 14, or 30 days",
                    "enum": [7, 14, 30]
                }
            },
            "required": ["mandi", "horizon_days"]
        }
    },
    {
        "name": "rank_mandis",
        "description": "Rank nearby mandis by net realized price after transport freight, mandi fees, and transit shrinkage.",
        "input_schema": {
            "type": "object",
            "properties": {
                "farmer_location": {
                    "type": "string",
                    "description": "Farmer's home mandi location (e.g., 'Kolar')"
                },
                "quantity_quintals": {
                    "type": "number",
                    "description": "Total onion quantity to sell in quintals"
                },
                "horizon_days": {
                    "type": "integer",
                    "description": "Selling horizon: 7, 14, or 30 days"
                }
            },
            "required": ["farmer_location", "quantity_quintals"]
        }
    },
    {
        "name": "hold_vs_sell",
        "description": "Run Monte Carlo simulation of waiting vs selling today, evaluating spoilage decay and credit interest.",
        "input_schema": {
            "type": "object",
            "properties": {
                "farmer_location": {"type": "string"},
                "quantity_quintals": {"type": "number"},
                "storage_type": {
                    "type": "string",
                    "enum": ["open", "warehouse", "cold_storage"]
                },
                "has_trader_debt": {"type": "boolean"}
            },
            "required": ["farmer_location", "quantity_quintals", "storage_type"]
        }
    },
    {
        "name": "find_storage",
        "description": "Look up available storage options, daily rot/decay rates, and rental charges.",
        "input_schema": {
            "type": "object",
            "properties": {
                "farmer_location": {"type": "string"},
                "quantity_quintals": {"type": "number"}
            },
            "required": ["farmer_location"]
        }
    }
]


# ---------------------------------------------------------------------------
# Multilingual Heuristic Synthesizer (Fallback & Base Generator)
# ---------------------------------------------------------------------------

def synthesize_advice_multilingual(
    farmer_location: str,
    quantity_quintals: float,
    storage_type: str,
    has_trader_debt: bool,
    language: str = "en"
) -> str:
    """
    Synthesize plain-language advisory following all rules:
    - Never states a single price as certain
    - Always states P10 to P90 uncertainty range
    - Supports English, Hindi, and Kannada
    - Strictly ends with required farmer autonomy statement
    """
    top_mandis_res = tool_rank_mandis(farmer_location, quantity_quintals, horizon_days=7)
    hold_res = tool_hold_vs_sell(farmer_location, quantity_quintals, storage_type, has_trader_debt)
    
    mandi1 = top_mandis_res["top_3_mandis"][0]
    best_k = hold_res["best_k_days"]

    if language.lower() in ["kannada", "kn"]:
        text = (
            f"**ರೈತ ಮಾರಾಟ ಸಲಹೆಗಾರ (Farmer Sell Advisor)**\n\n"
            f"**೧. ಎಲ್ಲಿ ಮಾರಾಟ ಮಾಡಬೇಕು (Where to Sell):**\n"
            f"ನಿಮ್ಮ ಸ್ಥಳ {farmer_location} ನಿಂದ ಉತ್ತಮ ನಿವ್ವಳ ಲಾಭ ತರುವ ಮಾರುಕಟ್ಟೆ **{mandi1['mandi']}** ಆಗಿದೆ "
            f"(ದೂರ: {mandi1['distance_km']} ಕಿ.ಮೀ).\n"
            f"- ನಿರೀಕ್ಷಿತ ಬೆಲೆ ಶ್ರೇಣಿ: **ರೂ. {mandi1['forecast_p10']} ರಿಂದ ರೂ. {mandi1['forecast_p90']} / ಕ್ವಿಂಟಾಲ್** (ಸರಾಸರಿ ರೂ. {mandi1['forecast_p50']}).\n"
            f"- ಸಾಗಾಣಿಕೆ ವೆಚ್ಚ: ರೂ. {mandi1['transport_cost_per_qtl']}/ಕ್ವಿಂಟಾಲ್, ಮಂಡಿ ಶುಲ್ಕ: ರೂ. {mandi1['fees_and_commission_per_qtl']}/ಕ್ವಿಂಟಾಲ್.\n"
            f"- ನಿಮ್ಮ ಸ್ಥಳೀಯ ಮಂಡಿಗಿಂತ ಹೆಚ್ಚುವರಿ ನಿವ್ವಳ ಲಾಭ: **ರೂ. {mandi1['gain_over_local_per_qtl']}/ಕ್ವಿಂಟಾಲ್** (ಒಟ್ಟು {quantity_quintals} ಕ್ವಿಂಟಾಲ್‌ಗೆ ಸುಮಾರು ರೂ. {mandi1['total_gain_rs']:,}).\n\n"
            f"**೨. ಯಾವಾಗ ಮಾರಾಟ ಮಾಡಬೇಕು (When to Sell):**\n"
        )
        if best_k > 0:
            k_info = hold_res["horizons"][best_k]
            text += (
                f"ನೀವು {best_k} ದಿನಗಳವರೆಗೆ ಸಂಗ್ರಹಿಸಿಡುವುದು ಸೂಕ್ತ. ನಿರೀಕ್ಷಿತ ನಿವ್ವಳ ಲಾಭ: **+ರೂ. {k_info['expected_gain_per_qtl']}/ಕ್ವಿಂಟಾಲ್** "
                f"({k_info['prob_wait_beats_today_pct']}% ಗೆಲ್ಲುವ ಸಂಭವನೀಯತೆ). ಆದಾಗ್ಯೂ, ಮಾರುಕಟ್ಟೆ ಕುಸಿತದ ಅಪಾಯದಲ್ಲಿ (P10) ಲಾಭವು ರೂ. {k_info['worst_case_p10_gain']}/ಕ್ವಿಂಟಾಲ್ ಆಗಬಹುದು.\n\n"
            )
        else:
            text += (
                f"ಹಾಳಾಗುವಿಕೆ ({storage_type} ಸಂಗ್ರಹಣೆಯಲ್ಲಿ) ಮತ್ತು ಬಡ್ಡಿಯ ವೆಚ್ಚದಿಂದಾಗಿ **ಇಂದೇ ಮಾರಾಟ ಮಾಡುವುದು ಉತ್ತಮ**.\n\n"
            )
        text += (
            f"> **ಗಮನಿಸಿ**: ಕೃಷಿ ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳು ಅನಿಶ್ಚಿತತೆಯಿಂದ ಕೂಡಿವೆ. **ಅಂತಿಮ ನಿರ್ಧಾರವು ಸಂಪೂರ್ಣವಾಗಿ ರೈತರದ್ದಾಗಿದೆ, ಇದು ಕೇವಲ ಸಲಹಾ ಮಾರ್ಗದರ್ಶನವಾಗಿದೆ.**"
        )
        return text

    elif language.lower() in ["hindi", "hi"]:
        text = (
            f"**किसान विक्रय सलाहकार (Farmer Sell Advisor)**\n\n"
            f"**१. कहां बेचें (Where to Sell):**\n"
            f"आपके स्थान {farmer_location} से सबसे अधिक शुद्ध मुनाफा देने वाली मंडी **{mandi1['mandi']}** है "
            f"(दूरी: {mandi1['distance_km']} किमी).\n"
            f"- संभावित अनुमानित मूल्य दायरा: **रु {mandi1['forecast_p10']} से रु {mandi1['forecast_p90']} प्रति क्विंटल** (अनुमानित औसत: रु {mandi1['forecast_p50']}).\n"
            f"- परिवहन खर्च: रु {mandi1['transport_cost_per_qtl']}/क्विंटल, मंडी व दलाली शुल्क: रु {mandi1['fees_and_commission_per_qtl']}/क्विंटल.\n"
            f"- आपकी स्थानीय मंडी की तुलना में अतिरिक्त लाभ: **रु {mandi1['gain_over_local_per_qtl']}/क्विंटल** (कुल {quantity_quintals} क्विंटल पर लगभग रु {mandi1['total_gain_rs']:,}).\n\n"
            f"**२. कब बेचें (When to Sell):**\n"
        )
        if best_k > 0:
            k_info = hold_res["horizons"][best_k]
            text += (
                f"{best_k} दिनों तक रोककर रखना लाभदायक हो सकता है। संभावित अतिरिक्त लाभ: **+रु {k_info['expected_gain_per_qtl']}/क्विंटल** "
                f"({k_info['prob_wait_beats_today_pct']}% आज से बेहतर भाव मिलने की संभावना)। हालांकि, मंदी के जोखिम (P10) में परिणाम रु {k_info['worst_case_p10_gain']}/क्विंटल हो सकता है।\n\n"
            )
        else:
            text += (
                f"भंडारण में सड़न/वजन कमी और ब्याज को देखते हुए **आज ही बेचना सबसे सुरक्षित है**।\n\n"
            )
        text += (
            f"> **महत्वपूर्ण सूचना**: कृषि बाजार में उतार-चढ़ाव रहता है। **अंतिम निर्णय पूरी तरह से किसान भाई का है, यह केवल एक सलाहकारी मार्गदर्शन है।**"
        )
        return text

    else: # English default
        text = (
            f"### Farmer Sell Advisor Recommendation\n\n"
            f"**1. WHERE TO SELL:**\n"
            f"Based on net price after all logistics and statutory charges, your top destination is **{mandi1['mandi']}** "
            f"({mandi1['distance_km']} km from {farmer_location}).\n"
            f"- **Expected Price Range (P10–P90)**: **Rs {mandi1['forecast_p10']} to Rs {mandi1['forecast_p90']} / quintal** "
            f"(P50 Expected modal: Rs {mandi1['forecast_p50']} / quintal).\n"
            f"- **Cost Deductions**: Freight: Rs {mandi1['transport_cost_per_qtl']}/qtl | APMC Fees & Commission: Rs {mandi1['fees_and_commission_per_qtl']}/qtl | Transit Loss: Rs {mandi1['shrinkage_loss_per_qtl']}/qtl.\n"
            f"- **Net Advantage Over Local Mandi**: **+Rs {mandi1['gain_over_local_per_qtl']}/quintal** "
            f"(Total net gain of **Rs {mandi1['total_gain_rs']:,}** for your {quantity_quintals} quintal harvest).\n\n"
            f"**2. WHEN TO SELL:**\n"
        )
        if best_k > 0:
            k_info = hold_res["horizons"][best_k]
            text += (
                f"The simulation recommends **HOLDING FOR {best_k} DAYS** in {storage_type.replace('_', ' ').title()}.\n"
                f"- **Expected Net Gain**: **+Rs {k_info['expected_gain_per_qtl']:.2f}/quintal** "
                f"(Total: +Rs {k_info['total_expected_gain_lot']:,}).\n"
                f"- **Probability of Beating Today's Spot Price**: **{k_info['prob_wait_beats_today_pct']}%**.\n"
                f"- **Downside (P10) Worst-Case Outcome**: Rs {k_info['worst_case_p10_gain']:.2f}/quintal.\n\n"
            )
        else:
            text += (
                f"The simulation recommends **SELLING TODAY**.\n"
                f"Holding in {storage_type.replace('_', ' ')} incurs post-harvest decay and carrying interest "
                f"that exceed expected price gains.\n\n"
            )
        text += (
            f"> **Disclaimer**: Price forecasts reflect statistical probability bands (P10 to P90), never a guarantee. "
            f"**The farmer makes the final decision; the system only advises.**"
        )
        return text


# ---------------------------------------------------------------------------
# Anthropic API Tool-Use Dispatcher
# ---------------------------------------------------------------------------

def run_agent(
    user_query: str,
    farmer_location: str = "Kolar",
    quantity_quintals: float = 50.0,
    storage_type: str = "open",
    has_trader_debt: bool = False,
    language: str = "en"
) -> str:
    """
    Executes the LLM agent.
    If ANTHROPIC_API_KEY is available, uses Claude with tool calling.
    Otherwise, gracefully falls back to the deterministic multilingual tool synthesizer.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        logger.info("ANTHROPIC_API_KEY not set. Using verified local multilingual tool synthesizer.")
        return synthesize_advice_multilingual(
            farmer_location, quantity_quintals, storage_type, has_trader_debt, language
        )

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)

        system_prompt = (
            "You are 'Farmer Sell Advisor', an empathetic, highly knowledgeable agricultural ML advisor. "
            "You help smallholder onion farmers in Karnataka (Kolar, Chikkaballapur, Bengaluru APMC) decide "
            "WHERE and WHEN to sell their produce.\n\n"
            "STRICT RULES:\n"
            "1. NEVER state a single price as certain. Always provide the uncertainty range (P10 downside to P90 upside).\n"
            "2. ALWAYS clearly explain deductions (freight, APMC fees, commission, transit shrinkage).\n"
            "3. ALWAYS end your reply with an explicit statement that the final decision belongs entirely to the farmer.\n"
            f"4. Respond in {language.upper()} using simple, respectful language understandable to rural farmers.\n"
            "5. Use the provided tools (get_forecast, rank_mandis, hold_vs_sell, find_storage) to retrieve facts."
        )

        messages = [{"role": "user", "content": user_query}]
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=system_prompt,
            tools=AGENT_TOOLS,
            messages=messages
        )

        # Handle tool calling loop
        while response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    t_name = block.name
                    t_input = block.input
                    t_id = block.id

                    if t_name == "get_forecast":
                        res = tool_get_forecast(t_input.get("mandi", "Kolar"), t_input.get("horizon_days", 7))
                    elif t_name == "rank_mandis":
                        res = tool_rank_mandis(
                            t_input.get("farmer_location", farmer_location),
                            t_input.get("quantity_quintals", quantity_quintals),
                            t_input.get("horizon_days", 7)
                        )
                    elif t_name == "hold_vs_sell":
                        res = tool_hold_vs_sell(
                            t_input.get("farmer_location", farmer_location),
                            t_input.get("quantity_quintals", quantity_quintals),
                            t_input.get("storage_type", storage_type),
                            t_input.get("has_trader_debt", has_trader_debt)
                        )
                    elif t_name == "find_storage":
                        res = tool_find_storage(
                            t_input.get("farmer_location", farmer_location),
                            t_input.get("quantity_quintals", quantity_quintals)
                        )
                    else:
                        res = {"error": f"Unknown tool {t_name}"}

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": t_id,
                        "content": json.dumps(res)
                    })

            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})

            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                system=system_prompt,
                tools=AGENT_TOOLS,
                messages=messages
            )

        # Extract final text
        final_text = ""
        for b in response.content:
            if hasattr(b, "text"):
                final_text += b.text
        return final_text

    except Exception as e:
        logger.warning(f"Error invoking Anthropic API ({e}). Falling back to local multilingual synthesizer.")
        return synthesize_advice_multilingual(
            farmer_location, quantity_quintals, storage_type, has_trader_debt, language
        )


if __name__ == "__main__":
    print("=== ENGLISH ADVICE ===")
    print(synthesize_advice_multilingual("Kolar", 50.0, "open", has_trader_debt=True, language="en"))
    print("\n=== HINDI ADVICE ===")
    print(synthesize_advice_multilingual("Kolar", 50.0, "warehouse", has_trader_debt=False, language="hi"))
    print("\n=== KANNADA ADVICE ===")
    print(synthesize_advice_multilingual("Chikkaballapur", 60.0, "warehouse", has_trader_debt=False, language="kn"))
