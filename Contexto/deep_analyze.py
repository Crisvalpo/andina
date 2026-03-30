import pandas as pd
import json

path = r'd:\Github\Andina\Contexto\MASTER PIPING 20-02-2026 REAL.xlsx'
xl = pd.ExcelFile(path)

full_report = {}

for sheet in xl.sheet_names:
    try:
        # Load a larger sample to see patterns
        df = xl.parse(sheet, nrows=50)
        
        # Basic stats
        row_count = len(df)
        col_names = df.columns.tolist()
        
        # Identify if it has headers or if they are in the first few rows
        # Drop completely empty rows and columns
        df_clean = df.dropna(how='all', axis=0).dropna(how='all', axis=1)
        
        if df_clean.empty:
            full_report[sheet] = {"status": "empty or all nan"}
            continue

        sample = df_clean.head(5).to_dict(orient='records')
        
        # Check for typical keywords to guess sheet purpose
        keywords = {
            "Input": ["Line", "ISO", "Isometric", "Spool", "Joint", "Soldadura", "Material", "Unión"],
            "Report": ["Resumen", "Total", "KPI", "Avance", "%", "Suma", "HH", "EDP", "Pivote"],
            "Config": ["Catalogo", "Config", "Parametro", "WPS"]
        }
        
        purpose = []
        df_str = str(df_clean.to_string()).lower()
        for p, ks in keywords.items():
            if any(k.lower() in df_str or k.lower() in sheet.lower() for k in ks):
                purpose.append(p)

        full_report[sheet] = {
            "rows_sample": row_count,
            "columns": col_names,
            "sample": sample,
            "probable_purpose": purpose
        }
    except Exception as e:
        full_report[sheet] = {"error": str(e)}

with open(r'd:\Github\Andina\Contexto\deep_excel_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(full_report, f, indent=2, default=str)
