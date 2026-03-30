# LukeAPP – Andina 
**Proyecto:** 413 / 4600022667  
**Obra:** Espesador de Concentrado Colectivo PMFC – CODELCO – 2025  
**Disciplina:** Piping  

---

## 1. Propósito del Sistema 
El sistema gestiona de manera digital la trazabilidad integral del piping, desde la recepción de ingeniería hasta el montaje.
La solución digitaliza el flujo: `Spool` → `Fabricación` → `QA/QC` → `Despacho` → `Montaje`, buscando centralización, reducción de reprocesos y control en tiempo real.

---

## 2. Alcance Funcional (Work Packages) y Matriz RACI
El proyecto se divide en 5 áreas de madurez clave para la gestión de piping:

| WP | Nombre | Enfoque |
|:---|:---|:---|
| **WP1** | **Estandarización de bases de datos** | Normalización de cubicaciones Multi-Proyecto. |
| **WP2** | **Workfronts y Prioridades** | Definición de frentes de ataque y secuenciamiento. |
| **WP3** | **Recepción de Materiales** | Control de Stock Vivo y QR Único en bodega. |
| **WP4** | **Descomposición en Spools** | Trazabilidad Isométrico -> Pieza física. |
| **WP5** | **Weld Log y Soldadura** | Registro de juntas, NDE (RT/UT/PT) y PWHT. |
| **WP6** | **Liberación de Calidad** | Inspección dimensional y protocolos QA. |
| **WP7** | **Logística Taller-Obra** | Control de despacho y arribo de piezas. |
| **WP8** | **Montaje y Campo** | Registro de avance físico en terreno. |
| **WP9** | **KPI y Dashboards** | Reportabilidad consolidada en PowerBI. |

### Matriz RACI
| Etapa / Actividad | ADMIN | OT | QAQC | LOGISTICA | SUPERVISOR |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **WP1: Estandarización de Datos** | A | R | I | I | I |
| **WP2: Lookahead (3-semanas)** | I | R | I | I | C |
| **WP3: Recepción y Stock QR** | I | I | I | R | I |
| **WP3: Impresión/Etiquetado** | A | I | I | R | I |
| **WP5: Weld Log (Fabricación)** | I | I | R | I | I |
| **WP5: Liberación Dimensional** | I | I | R | I | I |
| **Montaje y Cierre (Campo)** | A | I | R | I | R |

---

## 3. Base Tecnológica e Infraestructura 
- **Capa Aplicación**: AppSheet (Google) - Interfaz móvil y formularios.
- **Capa Datos**: SharePoint (Microsoft 365) - Repositorio oficial `_MS`.
- **Arquitectura Híbrida**: Uso de Excels estructurados en la "Célula Luke App" para asegurar redundancia y seguridad institucional.

### Estructura de Carpetas (Célula SharePoint)
- 📁 **`CAT`**: Catálogos técnicos de referencia (Clases, Fluidos, NPS).
- 📁 **`DOC`**: Documentos PDF oficiales (Isométricos, P&IDs).
- 📁 **`LIST`**: Listas maestras (Líneas, Spools, MTO).
- 📁 **`LOG`**: Historial de movimientos, cambios de revisión y fotos.
- 📁 **`REG`**: Registros operativos (Soldaduras ejecutadas, Recepciones).

---

## 4. Roles y Responsabilidades
- **ADMIN**: Configuración, gestión de usuarios y seguridad.
- **OT (Oficina Técnica)**: Estandarización, carga de ingeniería y lookahead.
- **QAQC (Calidad)**: Registro de soldadura, liberación y control dimensional.
- **LOGISTICA**: Recepción de materiales, impresión de QRs y despacho.
- **SUPERVISOR**: Reporte de avance en terreno y montaje.

---

## 5. Gestión de Cuentas
- **AppSheet (Google)**: `eimisa.lukeapp@gmail.com`
- **SharePoint (M365)**: `cluke@eimontajes.cl`
- **Gobernanza**: Sitio alojado en "Célula Luke App" bajo control institucional de EIMISA.

---

## 6. Objetivos Estratégicos 
- Digitalizar integralmente el contrato 413.
- Obtener métricas confiables de avance físico (Ganado vs Real).
- Reducir pérdidas de trazabilidad documental.
- Establecer base replicable para futuros contratos EIMISA.
