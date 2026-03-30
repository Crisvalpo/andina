import pandas as pd
import json
import os

file_path = r"D:\Github\Andina\Contexto\PRY_389\Log Control Documentos GCC.xlsm"

def analyze_excel(path):
    try:
        xl = pd.ExcelFile(path)
        result = {"sheets": xl.sheet_names, "details": {}}
        for sheet in xl.sheet_names:
            # Read first 10 rows to find headers and sample data
            df = pd.read_excel(path, sheet_name=sheet, nrows=5)
            result["details"][sheet] = {
                "columns": list(df.columns),
                "sample": df.head(2).to_dict(orient='records')
            }
        return result
    except Exception as e:
        return {"error": str(e)}

analysis = analyze_excel(file_path)
print(json.dumps(analysis, indent=2, default=str))
