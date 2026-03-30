import pandas as pd
import json
import os

file_path = r"D:\Github\Andina\Contexto\PRY_413\Docs. Ingeniería Faltantes 27OCT.xlsx"

def analyze_excel(path):
    try:
        xl = pd.ExcelFile(path)
        result = {"sheets": xl.sheet_names, "details": {}}
        for sheet in xl.sheet_names:
            df = pd.read_excel(path, sheet_name=sheet, nrows=10)
            
            # Convert ALL keys and values to strings to avoid JSON serialization errors
            raw_sample = df.head(5).to_dict(orient='records')
            safe_sample = []
            for row in raw_sample:
                safe_row = {str(k): str(v) for k, v in row.items()}
                safe_sample.append(safe_row)
                
            result["details"][sheet] = {
                "columns": [str(c) for c in df.columns],
                "sample": safe_sample
            }
        return result
    except Exception as e:
        return {"error": str(e)}

analysis = analyze_excel(file_path)
print(json.dumps(analysis, indent=2))
