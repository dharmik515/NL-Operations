import pandas as pd

files = [
    ('INBOUND STOCKTAKE 01 MAY.xlsm', 'INBOUND'),
    ('EVAL_Stocktake-2026-May-01.xlsm', 'EVAL')
]

for fname, ftype in files:
    df = pd.read_excel(fname, sheet_name='Sheet1')
    df = df[df['Room'].notna()]
    
    print(f'\n{ftype} File:')
    print(f'Total rows: {len(df)}')
    print(f'Rows with IMEI: {df["IMEI"].notna().sum()}')
    print(f'Rows with LOA: {df["LOA"].notna().sum()}')
    print(f'Rows with both empty: {((df["IMEI"].isna()) & (df["LOA"].isna())).sum()}')
    print(f'Rows with at least one: {((df["IMEI"].notna()) | (df["LOA"].notna())).sum()}')
