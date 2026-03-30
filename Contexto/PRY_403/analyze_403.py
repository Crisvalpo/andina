import pandas as pd
import json
from datetime import datetime

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, pd.Timestamp)):
            return obj.isoformat()
        if pd.isna(obj):
            return None
        return super().default(obj)

path = r'd:\Github\Andina\Contexto\PRY_403\1. Cubicacion_Piping_RT.xlsx'
xl = pd.ExcelFile(path)

full_report = {}

for sheet in xl.sheet_names:
    try:
        df = xl.parse(sheet, nrows=50)
        df_clean = df.dropna(how='all', axis=0).dropna(how='all', axis=1)
        
        if df_clean.empty:
            full_report[sheet] = {"status": "empty or all nan"}
            continue

        df_clean.columns = [str(c) for c in df_clean.columns]
        sample = df_clean.head(5).to_dict(orient='records')
        
        full_report[sheet] = {
            "rows_count": len(xl.parse(sheet, usecols=[0])),
            "columns": df_clean.columns.tolist(),
            "sample": sample
        }
    except Exception as e:
        full_report[sheet] = {"error": str(e)}

with open(r'd:\Github\Andina\Contexto\PRY_403\analysis_403.json', 'w', encoding='utf-8') as f:
    json.dump(full_report, f, indent=2, cls=CustomEncoder)
