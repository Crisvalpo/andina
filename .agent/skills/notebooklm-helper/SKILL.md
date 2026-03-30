---
name: notebooklm-helper
description: Habilidad para gestionar la autenticación y consulta de NotebookLM en el entorno de LukeAPP.
---

# NotebookLM Helper Skill

Esta habilidad permite al asistente (y al usuario) interactuar con NotebookLM de forma fluida, manejando la autenticación y proporcionando acceso rápido a los cuadernos del proyecto.

## 🛠️ Autenticación

Si recibes un error de "Authentication expired", usa el siguiente comando en la terminal (PowerShell):

```pwsh
& "C:\Users\Luke\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts\notebooklm-mcp-auth.exe"
```

## 📚 Cuadernos Críticos

- **Control de Oficina Técnica de Obra**: `b4158db1-b469-4118-9c7c-82c7738b53b4`
  - Contiene procedimientos de OT (`EIM-PRO-OFT-001`), listados de documentos vigentes y flujos de control documental.

## 📋 Comandos y Flujos

1. **Refrescar Tokens**: Siempre ejecuta `mcp_notebooklm_refresh_auth` antes de iniciar una sesión de investigación.
2. **Listar Notebooks**: Usa `mcp_notebooklm_notebook_list` para verificar el acceso.
3. **Consultas Estratégicas**:
   - Para entender roles: Pregunta sobre "DCC vs OT" o "Responsabilidades de Jefatura".
   - Para WP1: Pregunta sobre "Criterios de cubicación" o "Control de Isométricos".
   - Para WP2: Pregunta sobre "Planificación trisemanal", "Last Planner" o "WBS".

## ⚠️ Notas Técnicas
- El binario de autenticación reside en el path de Python 3.13 de Windows Store. 
- No compartas los tokens del archivo `auth.json` fuera del entorno seguro.
