import pandas as pd
import json

files = {
    "CONTROL_UNIONES": r'd:\Github\Andina\Contexto\CONTROL GENERAL DE UNIONES EIMISA RV7.xlsx',
    "MASTER_PIPING": r'd:\Github\Andina\Contexto\MASTER PIPING 20-02-2026 REAL.xlsx'
}

important_sheets = {
    "CONTROL_UNIONES": ["TABLA GENERAL ", "DETALLE"],
    "MASTER_PIPING": ["List. Iso. Recibidos", "LineListWorkREV 1A", "Resumen Spool", "Control Uniones"]
}

report = {}

for name, path in files.items():
    report[name] = {}
    try:
        xl = pd.ExcelFile(path)
        sheets = important_sheets[name]
        for s in sheets:
            if s in xl.sheet_names:
                df = xl.parse(s, nrows=20)
                # Try to find headers if the first row is nan
                df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)
                report[name][s] = {
                    "columns": df.columns.tolist(),
                    "sample": df.head(3).to_dict(orient='records')
                }
    except Exception as e:
        report[name]["error"] = str(e)

with open(r'd:\Github\Andina\Contexto\headers_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2, default=str)
