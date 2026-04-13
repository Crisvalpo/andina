# Bitácora de Implementación: LukeAPP Andina

Este documento registra la arquitectura, flujos técnicos y decisiones de diseño implementadas en la aplicación AppSheet para el contrato 4600022667 (Espesador de Concentrado Colectivo PMFC).

## ⚙️ Mapeo de Módulos AppSheet a Work Packages (WP)

| Módulo App | Título | WP Asociado | Estado |
|:---|:---|:---|:---|
| Módulo 1 | Control Documental (P&IDs) | WP1 | ✅ |
| Módulo 2 | Line List (AWP) | WP1 | ✅ |
| Módulo 3 | Isométricos | WP4 | ✅ |
| Módulo 4 | Spools y Weld Log | WP4 / WP5 | [/] |
| Módulo 5 | Impacto de Revisiones | WP1 / WP5 | [/] |
| Módulo 6 | Logística (WMS) | WP3 / WP7 | ✅ |
| Módulo 7 | Registro de Soldadura | WP5 / WP8 | [/] |

---

## ⚙️ Módulo 0: Configuración Global y Variables de Entorno

**Objetivo:** Centralizar parámetros temporales o de negocio (como fechas de inicio o metas) en una única tabla inteligente para alimentar fórmulas de la aplicación de manera dinámica, eliminando la dependencia de código "quemado" (Hardcodeo).

### 1. Arquitectura de Configuración (`CONFIG_APP_MS`)
- **Ubicación Física:** Vive como una pestaña dentro del archivo maestro de UX (`LIST_uxApp_MS.xlsx`), separando la meta-data de la "Data Dura" de ingeniería.
- **Estructura:** Consiste en una única fila de datos (Singleton). 
  - Columnas clave actuales: `ID_CONFIG`, `FECHA_INICIO_OBRA`, `USA_PWHT`, `CLASSES_CON_PWHT`.
- **Seguridad (AppSheet):** La tabla posee permisos restrictivos y su vista en el menú lateral ("Configuracion") suele estar bloqueada solo para usuarios con `USERSETTINGS("Rol") = "ADMIN"`.

#### Módulo de Isométricos: Arquitectura documental Simplificada
Se ha optimizado el flujo para evitar errores de seguridad y redundancia:

1.  **Entidades**:
    - `LIST_Iso_MS`: Entidad maestra (solo metadatos de ingeniería).
    - `LOG_Iso_MS`: Repositorio único de archivos y revisiones (El Historial).

2.  **Nueva Lógica de Carga**:
    - Se elimina la carga de PDF desde la tabla `LIST`.
    - **Paso 1**: Crear Isométrico (Formulario limpio sin archivos).
    - **Paso 2**: El usuario carga la revisión inicial (y las futuras) desde la tabla `LOG`.
    - **Efecto**: Elimina errores de "Path Traversal" y asegura que todos los archivos vivan en una sola carpeta física (`/LOG/Archivos/PDF`).

3.  **Sincronización Inversa**:
    - Un Bot monitorea la tabla `LOG` y actualiza automáticamente el campo `ARCHIVO_PDF_ISO` en `LIST` con la última versión cargada.

---

## Próximos Pasos (Demo Jueves)
1.  [x] Configuración de botones de carga masiva para P&IDs y Relaciones.
2.  [x] Definición de lógica de avance WDI en Juntas.
3.  [ ] Verificación final de flujo de "Reportar Ejecución" en terreno.
4.  [ ] Configuración de Semáforos en Vista Maestro de Spools.

### 2. Caso de Uso: Semana de Proyecto Dinámica
Para automatizar el cálculo de la "Semana en curso" en la pantalla de bienvenida, se extrae el parámetro base desde la configuración.
- **Lógica Matemática Estándar:** La App resta la fecha actual (`TODAY()`) menos la `FECHA_INICIO_OBRA`. Esto lo pasa a horas, lo divide en los bloques de 168hrs de una semana, y usa `FLOOR()` para saber las semanas completas ejecutadas.
- **Extracción de Variables:** La función `ANY(CONFIG_APP_MS[FECHA_INICIO_OBRA])` busca en la única celda de configuración disponible. Si gerencia define postergar el inicio del proyecto 1 mes, el ADMIN simplemente modifica este único valor en la App, y toda la matemática de calendarios se recalibra mundialmente de forma instantánea.

---

## 🏗️ Módulo 1: Control Documental de P&IDs (Completado)

**Objetivo:** Gestionar el catálogo oficial de P&IDs y todas sus versiones/revisiones en terreno, asegurando que el personal siempre visualice el PDF vigente.

### 1. Estructura de Carpetas (SharePoint)

Toda la estructura física de este módulo vive dentro de la Célula corporativa de Luke App en MS365:
`2 - Espesador de Concentrado Colectivo PMFC / 1 - APP / 1_Tablas_MS`

Se divide en las siguientes subcarpetas clave:
- 📁 **`LIST`**: Contiene el archivo de Excel `LIST_Piping_MS.xlsx` (donde vive la hoja/tabla interna `LIST_PID_MS`, el catálogo oficial y visor principal).
- 📁 **`LOG`**: Contiene el archivo de Excel `LOG_Piping_MS.xlsx` (donde vive la hoja/tabla interna `LOG_PID_MS`, el historial inmutable de revisiones y PDFs adjuntos).
- 📁 **`Archivos/PDF/PID`**: Ruta de alojamiento configurada en la columna `Archivo_PDF` donde se guardan físicamente los anexos.

### 2. Arquitectura de Datos Optimizada (Patrón de 2 Capas)

Tras probar con éxito la arquitectura Bot-Driven en Isométricos, se refactorizó el modelo de P&IDs eliminando la redundancia de 3 capas, bajándolo a solo 2 capas jerárquicas:

#### Capa 1: La Bandeja Viva (`LIST_PID_MS`)
- **Naturaleza:** Tabla principal o "Master Card".
- **Rol:** Es la vista principal para Terreno. Muestra los metadatos fijos del P&ID y contiene las columnas "vivas" de `REVISION_VIGENTE`, `ESTADO_VIGENTE` y `ARCHIVO_PDF_VIGENTE` (actualizadas automáticamente por el Bot).

#### Capa 2: El Historial Inmutable (`LOG_PID_MS`)
- **Naturaleza:** Tabla de detalle (`IsPartOf` hacia `LIST_PID_MS`).
- **Rol:** Registrar de forma inmutable cada vez que se emite una nueva revisión (Almacenando: PDF Físico, Motivo de Cambio, Usuario, Revisión N°).
- **Seguridad Lógica:** Campos Automáticos e Invisibles de Auditoría (`FECHA_SUBIDA` y `SUBIDO_POR`) no son editables garantizando el control documental.

### 3. Lógica de Flujo en AppSheet (Motor Update-Bot)

El sistema está diseñado para que Oficina Técnica cargue el historial y el sistema haga el trabajo pesado de actualizar la vista de Terreno:

1. OT ingresa al detalle del plano en `LIST_PID_MS` y visualiza la lista vacía o histórica de `LOG_PID_MS` anidada abajo.
2. Oprime `[ + Nuevo ]` en la sección del Historial (LOG). Releyendo la nueva Revisión, Estado y subiendo el nuevo Archivo PDF.
3. **El Motor "Action / Bot":** Al presionar Guardar, una Automatización (Bot) configurada *On Data Change* dispara una *Data Action* hacia el registro padre (`LIST_PID_MS`), sobrescribiendo las columnas de la Revisión y Archivo PDF vigentes, escondiendo instantáneamente el plano obsoleto para todo el proyecto.

### 4. Evolución Futura (Extracción de Metadatos P&ID)
### 4. Evolución Futura (Extracción de Metadatos P&ID)
Según las especificaciones técnicas del proyecto (SGP-02CAN-ESPTC-00001), los P&IDs son la fuente de datos matriz. El sistema actual controla el PDF inmutable, pero en el futuro se pueden extraer los siguientes catálogos satélites vinculados a la instancia viva (`LIST_PID_MS`):

1. **Catálogo de Válvulas e Ítems Especiales:**
   - **Formato Tag:** `[Diámetro] - [Acrónimo] - [Correlativo]` (Ej: `6"-VBB-105` para Válvula de Bola).
   - **Metadatos a capturar:** Tag Válvula/Componente, Número de Línea asociada, Descripción (material/clase), Proveedor, y P&ID de Origen.
   - **Acrónimos:** VBB (Bola), VMP (Mariposa), VKN (Cuchillo), VRC (Retención/Check), MNG (Mangueras), JEX (Juntas Expansión).
2. **Registro de Tie-Ins (Empalmes):**
   - **Formato Tag:** `[Área Física] - [Correlativo]` (Ej: `03351-002`).
   - Relacionar el Tie-In con el P&ID exacto donde ocurre el quiebre de batería.

### 5. Gobernanza de Tablas Relacionales Críticas (`REL_PIDLineas_MS`)

Dado que la tabla `REL_PIDLineas_MS` actúa como el **"Amarre de Ingeniería"** (vinculando un P&ID con múltiples líneas), es vital proteger su integridad. 

Para evitar que el personal de terreno (o roles no autorizados) alteren las relaciones de diseño, se implementó un cerrojo en la propiedad **`Are updates allowed?`** de la tabla, garantizando que el resto del proyecto visualice las relaciones en modo estricto de solo lectura (`READ_ONLY`).

**Fórmula de Gobernanza Implementada:**
```excel
SWITCH(
  USERSETTINGS("Rol"),
  "ADMIN", "ALL_CHANGES",
  "OT", "ALL_CHANGES",
  "READ_ONLY"
)
```

## 🏗️ Módulo 2: Catálogo de Líneas (Line List AWP)

**Objetivo:** Desarrollar un repositorio matricial estandarizado de tuberías ("Gemelo Digital"), diseñado de manera agnóstica para soportar columnas de cualquier cliente minero (AWS, Tiempos, Presiones, Aislamiento y Códigos NDE), sirviendo como la "columna vertebral" para los cruces con Calidad, Isométricos y Spools.

### 1. Arquitectura de Datos (Catálogo y Puente Relacional)

Para soportar la complejidad de que una Línea pase por múltiples Planos, y un Plano contenga múltiples Líneas (Relación N:N), dividimos el peso en dos tablas de SharePoint:

- **La Tabla Maestra (`LIST_Lineas_MS`):** Aloja los datos duros de ingeniería y parámetros operacionales (Ej: Diámetro, Clase, Fluidos, Pintura).
- **La Tabla Relacional (`REL_Piping_MS`):** Ubicada junto a los catálogos en SharePoint, funciona como el "Puente". En AppSheet se utiliza la propiedad `Ref` activando la opción `IsPartOf` apuntando a `LIST_PID_MS`. Esto le avisa al sistema que su única razón biológica es vincular planos vivos con tuberías maestras.

### 2. Lógica de Flujo en AppSheet (La Interfaz Asistida)

Al configurar la tabla Relacional con `IsPartOf`, AppSheet generó automáticamente una vista de "Líneas Asociadas" anidada en el fondo del visor de cada Plano (P&ID).

- **La Magia de la UX:** Cuando un usuario entra al Plano y oprime "Agregar (Nuevo)", el campo del Plano (`ID_PID`) ya viene anclado (pre-llenado), y el campo de la Línea (`ID_LINEA`) se presenta como un Menú Desplegable. Todo el complejo cruce de llaves primarias ocurre a nivel de sistema sin que el usuario de terreno teclee texto manual, previniendo errores de tipeo.

### 3. Carga Masiva (CSV) y Enriquecimiento Progresivo

Dada la realidad de la obra donde Ingeniería (OT) rara vez recibe toda la información el día 1, el flujo operativo real implementado aprovecha dos capacidades complementarias:

1.  **Carga Masiva Nativa (Bulk Upload):** En la vista general del Catálogo de Líneas, habilitamos una Acción Nativa `Import a CSV file for this view`. Esto permite que el equipo de OT importe miles de tuberías de golpe subiendo plantillas .csv estandarizadas desde su PC, sin poner en riesgo la integridad de la carpeta de SharePoint.
2.  **Enriquecimiento Celular (Progressive Data Entry):** Solo establecimos el `ID_LINEA` como campo obligatorio. Todas las columnas ricas en datos (Temperaturas, Pruebas NDE, Tracing, Pintura) se dejaron opcionales. Cuando un plano es subido vacío o con columnas de ingeniería en blanco vía CSV, cualquier supervisor con rol de "OT" puede hacer un tap en el ícono del Lápiz (Editar) y agregar la presión faltante directamente desde AppSheet, rellenando el archivo maestro.

### Tareas Pendientes o Responsabilidades a cargo de (OT):
- **Gestión Continua:** Su objetivo primordial hoy (además de crear las Líneas e iniciar los registros vía CSV) cruzar las líneas con los sub-sistemas de calidad (futuros isométricos y soldaduras).
- **Llenado en Terreno:** La arquitectura está lista; el esfuerzo actual requerido recae 100% en que Oficina Técnica (OT) y Calidad alimenten y auditen proactivamente el Data Model (que fue diseñado para ser ultra profundo y resistente a proyectos grandes).

---

## 📏 Módulo 3: Isométricos y Control de Revisiones (`LIST_Iso_MS`)

**Objetivo:** Controlar la ingeniería de detalle (hojas isométricas) vinculándolas a la Línea Maestra y gestionando su vigencia mediante el reporte de `CANTIDAD_SPOOLS_EST` para pre-configurar la fabricación.

### 1. Arquitectura de 2 Capas (Motor de Vigencia)
Similar a P&IDs, se utiliza `LIST_Iso_MS` (Bandeja Viva) y `LOG_Iso_MS` (Historial). 
- **Bot de Actualización:** Al subir una nueva revisión en el LOG, el Bot actualiza la `REV_VIGENTE` y el PDF en la tabla maestra.
- **Dato Crítico:** OT debe ingresar la cantidad estimada de spools. Este dato viaja al Módulo 4 para validar que no se fabriquen piezas de más o de menos.

---

## 🔩 Módulo 4: Fabricación de Spools y Weld Log (`LIST_Spools_MS`)

**Objetivo:** Gestionar el ciclo de vida de cada pieza física (Spool) y sus componentes de unión (Soldaduras, Pernos, Victaulic), integrando la metodología AWP y la trazabilidad logística de bodega.

### 1. El Spool como Unidad de Negocio
- **Identidad Dual:** Se utiliza un `ID_SPOOL` técnico para AppSheet y un `TAG_SPOOL` (Correlativo Único) para la placa física de acero.
- **Trazabilidad de Revisiones:** Se captura la `REV_ORIGEN` (con la que nació) y la `REV_VIGENTE` (la que lo valida hoy).
- **Ciclo de Vida:** El estado cambia dinámicamente: `Fabricado` → `Pintado` → `Acopiado` → `Despachado` → `Montado`.

### 2. Weld Log Universal (`LIST_Juntas_MS`)
- **Fuente Única:** OT carga masivamente desde Spoolgen (Welds & Bolted Joints). Calidad solo registra el resultado sobre esos registros.
- **Lógica S/F (Shop/Field):** Las uniones 'S' suman progreso al Spool (Taller). Las uniones 'F' suman progreso al montaje del Isométrico (Terreno).
- **Forense de Impacto:** La columna `REV_EJECUCION` congela la revisión del plano al momento de soldar, permitiendo auditorías contra cambios de ingeniería futuros.

### 3. Logística y Levantamiento (`LOG_Levantamiento_MS`)
Cada movimiento físico del spool (traslados entre Bodega EIMISA, Rinconada o Taller) se registra con foto y ubicación, alimentando el `STATUS` y `UBICACION_ACTUAL` del Spool maestro mediante un Bot de sincronización.

---

## 🔄 Módulo 5: Plan de Impacto por Cambio de Revisión (`IMP_RevisionImpacto_MS`)

**Objetivo:** Mitigar el riesgo de re-trabajos por cambios de ingeniería de último minuto.

- **Disparador Automático:** Cuando el Bot detecta una nueva Revisión de Isométrico, genera un registro "Pendiente de Evaluación" por cada spool hijo.
- **Clasificación OT:** Oficina Técnica debe clasificar el impacto: `SIN IMPACTO` (Válido), `IMPACTO MENOR` (Ajustar) o `IMPACTO MAYOR` (Anular y Re-fabricar).
- **Bloqueo Operativo:** El sistema alerta a Terreno si un Spool está en "Evaluación de Impacto", previniendo el montaje de piezas obsoletas.

---

### Directrices Futuras
*(Próximos pasos: Implementación de Módulo de Torque, Pruebas Hidrostáticas y Firma Digital de Protocolos).*

---

## 📈 Trazabilidad y Numeración Global de Spools
- **TAG_SPOOL Inteligente:** Se implementó una lógica de `Initial Value` que garantiza que cada pieza física tenga un número correlativo único (0001, 0002...) para el proyecto.
- **Manejo de Revisiones:** Si un spool ya existía en una revisión anterior (mismo DWG y número de spool), el sistema "hereda" el número global original. Esto permite que la placa metálica fabricada en la Rev 0 siga siendo válida y rastreable en la Rev 1, eliminando la necesidad de cambiar TAGs físicos por cambios menores de ingeniería.
- **Automatización PWHT por Clase:** Se añadió una capa de inteligencia donde el ADMIN define qué clases de piping requieren PWHT en `CONFIG_APP_MS`. 
  - En `LIST_Lineas_MS`: La columna `REQ_PWHT` usa un `Initial Value` que detecta la clase, pero permite sobrescritura manual si la ingeniería indica lo contrario.
  - En `LIST_Spools_MS` y `Juntas`: Heredan este valor como "Triple Blindaje".
- **Control de Calidad Multi-Fase Inteligente:** Se evolucionó el control de NDE a un sistema de "Checklist" dinámico en `LIST_Juntas_MS`. La App ahora detecta automáticamente la materialidad (Acero vs HDPE) mediante la clase de piping, ocultando o mostrando los controles de ensayos destructivos (DT) según corresponda para optimizar la toma de datos en terreno.

---

## 🚀 Hoja de Ruta: Demo Jueves
Para asegurar una presentación exitosa el jueves, nos enfocaremos en:
1. **Reporte en un Click:** Registro simplificado de soldadura con cálculo automático.
2. **Ciclo de Vida Automático:** Cambio de estado de Spools gatillado por terminación de juntas.
3. **Semáforo de Gestión:** Indicadores visuales de spools listos para despacho.

---

## 📦 Módulo 6: Logística y Trazabilidad de Materiales (WMS)

**Objetivo:** Controlar el ciclo de vida de los materiales de ingeniería (MTO) mediante identidades únicas, seguimiento de bultos y auditoría documental de recepciones y traslados.

### 1. Estructura de Datos (AppSheet Config)

#### A. Tabla Maestra: `LIST_MTO_MS` (Consolidado)
Controla el estado general del requerimiento de ingeniería.

| Columna | Tipo AppSheet | Función / Lógica |
| :--- | :--- | :--- |
| **`REVISION_MAT`** | `Enum` | `SIN REVISAR`, `DISPONIBLE`, `FALTANTE`, `PARCIAL`. |
| **`PRIORIDAD_FAB`** | `Enum` | `ALTA`🔴, `MEDIA`🟡, `BAJA`🟢. |
| **`CANT_REAL`** | `Number` | Suma total de piezas/metros recibidos (auditado). |
| **`UBICACION_ACTUAL`**| `Enum` | Posición final del componente en el proyecto. |
| **`REF_COMMON_MAT`** | `Virtual` | `CONCATENATE([DESCRIPCION], " - ", [DIAM.])` |

#### B. Tabla de Auditoría: `LOG_Materiales_MS` (Identidad Física)
Cada fila aquí es un **Bulto, Pallet o Paquete** físico real. Puede nacer vinculado a una línea o como Stock General.

| Columna | Tipo AppSheet | Función / Lógica |
| :--- | :--- | :--- |
| **`ID_LOG_MAT`** | `Text` (Key) | `Initial Value: UNIQUEID()` |
| **`ID_ASIGNACION`** | `Text` | **ID para Plumón/Sticker**. Identifica el bulto físico. |
| **`ID_MTO`** | `Ref` | Relación a `LIST_MTO_MS`. **Opcional** (Permite recibir Stock General). |
| **`DESC_BODEGA`** | `Text` | Descripción manual si no hay línea asignada aún. |
| **`DIAM_BODEGA`** | `Text` | Diámetro manual si no hay línea asignada aún. |
| **`EVENTO`** | `Enum` | `RECEPCIÓN`, `TRASLADO`, `MONTAJE`, `ASIGNACIÓN`. |
| **`CANT_MOVIMIENTO`**| `Number` | Cuánto material viene en este bulto específico. |
| **`FOTO_RESPALDO`** | `Image` | Evidencia física. |
| **`QR_MATERIAL`** | `Virtual` | QR dinámico del `ID_ASIGNACION`. |

### 2. Lógica de Operación (Flujo Pre-Etiquetado)
1.  **Etiquetado Previo:** OT dispone de un set de stickers con códigos `M-XXXXX` y sus respectivos QRs.
2.  **Registro en App:** Al recibir material, se adhiere el sticker, se abre el LOG y se **escanea** el código.
3.  **Resultado:** Vínculo inmediato entre el ID del sistema y la identidad física de terreno.
4.  **Trazabilidad:** Cualquier escaneo posterior del sticker muestra la ficha técnica del material asignado.

### 3. Casos Especiales (Recepciones Parciales)
- Si una sola línea de ingeniería llega en dos bultos separados:
  1. Se registran dos LOGs independientes.
  2. Cada uno recibe un sticker correlativo distinto (`M-00001` y `M-00002`).
  3. Ambos quedan vinculados al mismo item de la `LIST_MTO_MS`, permitiendo auditoría por separado de cada paquete físico.

---
 
 ## 🛠️ Módulo 7: Registro de Ejecución de Uniones (`REG_unionSoldadaEjecutada_MS`)
 
 **Objetivo:** Capturar la ejecución física en terreno de cada unión soldada o fusionada, vinculándola con la ingeniería maestra y asegurando la auditabilidad total.
 
 ### 1. Estructura de Datos (Registro de Ejecución)
 | Columna | Lógica / Función |
 | :--- | :--- |
 | **`ID_unionSoldadaEjecutada`** | Llave primaria (Key). |
 | **`ID_JUNTA`** | Relación Ref a `LIST_Juntas_MS`. |
 | **`ID_SPOOL`** | Relación Ref a `LIST_Spools_MS`. |
 | **`ID_ISO`** | Relación Ref a `LIST_Iso_MS`. |
 | **`ID_LINEA`** | Relación Ref a `LIST_Lineas_MS`. |
 | **`REV_EJECUCION`** | **Inmutable.** Captura la revisión del Isométrico al momento del reporte. |
 | **`NUM_JUNTA`** | Tag físico de la junta (Ej: J01). |
 | **`TIPO_JUNTA`** | Método de unión (BW, BF, etc.). |
 | **`DIAMETRO_NPS`** | Arrastre automático desde la Línea. |
 | **`WDI`** | Cálculo automático de pulgadas diametrales (`DIAMETRO_NPS` * Factor). |
 | **`PROCESO_SOLDADURA`**| Enum según Catálogo 8. |
 | **`RESPONSABLE`** | Supervisor a cargo de la actividad. |
 | **`ESTAMPA_SOLDADOR`** | ID del soldador ejecutante. |
 | **`FECHA_EJECUCION`** | Timestamp de la actividad. |
 | **`ESTADO_WELDING`** | `SOLO_PUNTEADO`, `SOLDADO_FULL`, `RECHAZADO`. |
 | **`OBSERVACIONES`** | Notas técnicas de terreno. |
 | **`FOTO_JUNTA`** | Evidencia fotográfica. |
 | **`usuarioReporte`** | Auditoría: `USEREMAIL()` automático. |
 
 ### 2. Lógicas de Control
 - **Bloqueo de Avance:** El WDI solo suma progreso real cuando el `ESTADO_WELDING` es `SOLDADO_FULL`.
 - **Filtro Inteligente:** Si la línea es HDPE, el formulario oculta procesos de acero (SMAW/GTAW) y muestra Termofusión/Electrofusión.
 - **Trazabilidad Forense:** Al congelar la `REV_EJECUCION`, si el isométrico cambia a una revisión nueva en el futuro, el registro de soldeo histórico permanece vinculado a la versión con la que fue ejecutado.
```

---

## 🛠️ Correcciones y Mejoras Recientes

### 1. Error Grave: Columnas de Spooling Faltantes en Formulario de Revisión
**Fecha:** 2026-03-24
**Problema:** Al cargar una revisión inicial o nueva de un isométrico desde el `LOG_Iso_MS`, el formulario no solicitaba los campos `SPOOLED_BY`, `FECHA_SPOOLING` y `REV_SPOOLING`. Esto impedía que la tabla maestra `LIST_Iso_MS` se actualizara con los datos de quién y cuándo realizó el spooling del plano.
**Acción Realizada:** 
1. Se agregaron las columnas `;SPOOLED_BY;FECHA_SPOOLING;REV_SPOOLING` al encabezado del archivo físico `LOG_Piping_MS(LOG_Iso_MS).csv`.
2. **Requerimiento en AppSheet:** El administrador debe "Regenerar" la tabla `LOG_Iso_MS` en el editor de AppSheet y asegurar que la "Data Action" del Bot de actualización incluya el mapeo de estos tres campos desde el LOG hacia el LIST.

---

## 🤖 Módulo 8: Automatizaciones de Ciclo de Vida de Spools (Bots)

**Objetivo:** Automatizar la actualización del estado y ubicación de los spools en la tabla maestra (`LIST_Spools_MS`) a medida que se registran eventos en las tablas de control logístico y de calidad.

### 1. Matriz de Automatización (Events -> Actions)

| Evento de Origen | Tabla Gatillo | Condición | Acción en `LIST_Spools_MS` |
| :--- | :--- | :--- | :--- |
| **Liberación Dimensional** | `REG_DimensionalSpool_MS` | `[RESULTADO] = "APROBADO"` | `ESTADO_CICLO_VIDA`: "Liberado Dimensional"<br>`UBICACION_ACTUAL`: "Patio Taller"<br>`FECHA_FIN_FAB`: `[FECHA]`<br>`ESTADO_FABRICACION`: "🟢 EJECUTADO" |
| **Despacho a Pintura** | `REG_LogisticaSpool_MS` | `[EVENTO] = "DESPACHO_PINTURA"` | `ESTADO_CICLO_VIDA`: "En Pintura"<br>`UBICACION_ACTUAL`: "Planta Pintura"<br>`FECHA_ENVIO_PINTURA`: `[FECHA]` |
| **Liberación de Pintura**| `REG_PinturaSpool_MS` | `[RESULTADO] = "APROBADO"` | `ESTADO_CICLO_VIDA`: "Liberado Pintura"<br>`UBICACION_ACTUAL`: "Patio Pintura"<br>`FECHA_RECEPCION_PINTURA`: `[FECHA]` |
| **Despacho a Terreno** | `REG_LogisticaSpool_MS` | `[EVENTO] = "DESPACHO_TERRENO"` | `ESTADO_CICLO_VIDA`: "En Tránsito"<br>`UBICACION_ACTUAL`: "Transporte"<br>`FECHA_DESPACHO_REAL`: `[FECHA]` |
| **Recepción Terreno** | `REG_LogisticaSpool_MS` | `[EVENTO] = "RECEPCION_TERRENO"` | `ESTADO_CICLO_VIDA`: "En Terreno"<br>`UBICACION_ACTUAL`: "Bodega Terreno"<br>`FECHA_LLEGADA_TERRENO`: `[FECHA]` |

### 2. Lógica Técnica de Implementación (AppSheet Actions)

Para cada Bot, se requiere configurar una acción de tipo **"Data: execute an action on a set of rows"**:
- **Referenced Rows:** `LIST(LOOKUP([ID_SPOOL], "LIST_Spools_MS", "ID_SPOOL", "ID_SPOOL"))`
- **Action to run:** Una acción de actualización ("Data: set the values of some columns in this row") en la tabla `LIST_Spools_MS`.

### 3. Notificaciones Proactivas (Telegram via jAIme)
Cada uno de estos eventos debe disparar un mensaje al grupo de supervisión indicando:
- `📦 Spool [TAG_SPOOL] ha cambiado a estado: [ESTADO_CICLO_VIDA]`
- `📍 Ubicación: [UBICACION_ACTUAL]`
- `👤 Responsable: [USUARIO]`


