import json

notebook_content = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Farmer Sell Advisor: Exploratory Analysis & Decision Demo\n",
                "Demonstrating spatial arbitrage and hold-vs-sell optimization for Onion farmers in Karnataka (Kolar, Chikkaballapur, Bengaluru)."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import pandas as pd\n",
                "import numpy as np\n",
                "from src.decision.where_to_sell import rank_mandis_for_sale\n",
                "from src.decision.when_to_sell import simulate_hold_vs_sell"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 1. Inspect Processed Daily Panel"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "panel_df = pd.read_parquet('data/processed/panel.parquet')\n",
                "panel_df.tail(10)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Evaluate Spatial Optimizer (Where to Sell)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "sample_forecasts = {\n",
                "    'Bengaluru (Yeshwanthpur)': {'p10': 3500.0, 'p50': 4100.0, 'p90': 4500.0},\n",
                "    'Kolar': {'p10': 3200.0, 'p50': 3750.0, 'p90': 4150.0},\n",
                "    'Chikkaballapur': {'p10': 3150.0, 'p50': 3700.0, 'p90': 4080.0}\n",
                "}\n",
                "ranked = rank_mandis_for_sale('Kolar', quantity_quintals=50.0, forecast_prices=sample_forecasts)\n",
                "pd.DataFrame(ranked)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. Evaluate Temporal Simulator (When to Sell)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "sim = simulate_hold_vs_sell(\n",
                "    price_today=3750.0,\n",
                "    forecast_by_horizon={7: sample_forecasts['Kolar'], 14: sample_forecasts['Kolar'], 30: sample_forecasts['Kolar']},\n",
                "    storage_type='warehouse',\n",
                "    credit_mode='warehouse_receipt'\n",
                ")\n",
                "print(sim['advice_summary'])"
            ]
        }
    ],
    "metadata": {
        "language_info": {"name": "python"}
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

with open("notebooks/farmer_advisor_demo.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook_content, f, indent=2)

print("Generated notebooks/farmer_advisor_demo.ipynb successfully")

