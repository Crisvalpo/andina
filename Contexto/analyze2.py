import pandas as pd
import traceback

def extract(fp, sheet_name):
    try:
        df = pd.read_excel(fp, sheet_name=sheet_name)
        df = df.dropna(how='all')
        for idx, row in df.head(15).iterrows():
            if row.notna().sum() > 4:
                df.columns = row.tolist()
                parsed = df.iloc[list(df.index).index(idx)+1:].head(2).to_dict(orient='records')
                return f'Sheet {sheet_name}:\nHeaders: {list(df.columns)}\nRows: {parsed}\n'
        return f'Sheet {sheet_name} No headers found\n'
    except Exception as e:
        return f'Error in {sheet_name}: {e}\n'

fp = r'd:\Github\Andina\contexto\MASTER PIPING 20-02-2026 REAL.xlsx'
out = extract(fp, 'Control Uniones')
out += extract(fp, 'Resumen Spool')
out += extract(fp, 'Piping LB')
out += extract(fp, 'Cubicación LARGO SPOOLS')

with open(r'd:\Github\Andina\contexto\analysis2.txt', 'w', encoding='utf-8') as f:
    f.write(out)

