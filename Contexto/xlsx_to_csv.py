import pandas as pd
import os
import sys

def process_folder(xlsx_path, output_dir):
    filename = os.path.basename(xlsx_path).replace('.xlsx', '')
    try:
        xls = pd.ExcelFile(xlsx_path)
        print(f"Opening {xlsx_path}")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for sheet_name in xls.sheet_names:
            print(f"Processing sheet: {sheet_name}")
            df = pd.read_excel(xlsx_path, sheet_name=sheet_name)
            csv_name = f"{filename}({sheet_name}).csv"
            csv_path = os.path.join(output_dir, csv_name)
            df.to_csv(csv_path, index=False)
            print(f"Created {csv_path}")
    except Exception as e:
        print(f"Error processing {xlsx_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        process_folder(sys.argv[1], sys.argv[2])
    else:
        # Default for the previous task if no args
        process_folder(
            r'C:\Users\Luke\EISA\EIMI00413 - Andina - 25. LukeAPP\2 - Espesador de Concentrado Colectivo PMFC - CODELCO - 2025\1 - APP\1_Tablas_MS\REG\REG_Piping_MS.xlsx',
            r'D:\Github\Andina\Contexto\PRY_413\REG'
        )
