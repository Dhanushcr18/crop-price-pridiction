import pandas as pd
df = pd.read_csv('data/raw/user_download/karnataka_mandi_prices_2026-11-11.csv')
for i, m in enumerate(sorted(df['mandi'].unique())):
    print(f'{i+1}: "{m}"')
