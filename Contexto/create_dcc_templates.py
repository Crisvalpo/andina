import pandas as pd
import os

base_path = r"d:\Github\Andina\REG\DCC"
os.makedirs(base_path, exist_ok=True)

templates = {
    "DCC_Log_Documentos_MS.xlsx": [
        "ID_PAQUETE", "ID_HOJA_ISO", "ITEM_CORRELATIVO", "NOMBRE_DOC", 
        "REVISION", "FECHA_RECEP", "TIPO_DOC", "ESPECIALIDAD", "AREA_CWP", "ESTATUS_DOC"
    ],
    "DCC_Log_SDI_RFI_MS.xlsx": [
        "ID_SDI", "ESTADO", "FECHA_EMISION", "DIAS_CLI", "IMPACTO", 
        "ESPECIALIDAD", "RESUMEN", "RESPUESTA_CLI"
    ],
    "DCC_Log_Transmittal_MS.xlsx": [
        "ID_TRANSMITTAL", "FECHA_ENVIO", "DESTINATARIO", "CONTENIDO", "ACUSE_RECIBO"
    ],
    "DCC_Log_Correspondencia_MS.xlsx": [
        "ID_CARTA", "SENTIDO", "ASUNTO", "REFERENCIA", "REQUIERE_RESP", "LINK_PDF"
    ],
    "DCC_Log_Instrucciones_MS.xlsx": [
        "ID_INSTRUCCION", "EVAL_ALCANCE", "AREAS_EVAL", "RESUMEN"
    ]
}

print(f"Creando plantillas en {base_path}...")

for filename, columns in templates.items():
    full_path = os.path.join(base_path, filename)
    df = pd.DataFrame(columns=columns)
    df.to_excel(full_path, index=False)
    print(f" - Creado: {filename}")

print("\n¡Proceso completado con éxito!")
