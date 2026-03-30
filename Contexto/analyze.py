import pandas as pd
import json
import traceback

def analyze_sheet(df):
    df = df.dropna(how='all')
    if len(df) == 0: return 'Empty'
    for idx, row in df.head(10).iterrows():
        non_nulls = row.notna().sum()
        if non_nulls > 5:
            df.columns = row.tolist()
            return df.iloc[list(df.index).index(idx)+1:].head(2).to_dict(orient='records')
    return 'Could not find header'

out = ''
fp1=r'd:\Github\Andina\contexto\CONTROL GENERAL DE UNIONES EIMISA RV7.xlsx'
try:
    xl = pd.ExcelFile(fp1)
    out += f'File 1 Sheets: {xl.sheet_names}\n'
    for s in xl.sheet_names:
        df = xl.parse(s)
        out += f'Sheet {s}:\n{str(analyze_sheet(df))[:1000]}\n\n'
except Exception as e: out += str(e) + '\n' + traceback.format_exc()

fp2=r'd:\Github\Andina\contexto\MASTER PIPING 20-02-2026 REAL.xlsx'
try:
    xl = pd.ExcelFile(fp2)
    out += f'\nFile 2 Sheets: {xl.sheet_names}\n'
    for s in xl.sheet_names:
        df = xl.parse(s)
        out += f'Sheet {s}:\n{str(analyze_sheet(df))[:1000]}\n\n'
except Exception as e: out += str(e) + '\n' + traceback.format_exc()

with open(r'd:\Github\Andina\contexto\analysis.txt', 'w', encoding='utf-8') as f:
    f.write(out)

