# 🚀 Plan de Integración de Catálogos en AppSheet
# Proyecto: Andina - Módulo de Control de Líneas (AWP)

Este documento define la arquitectura exacta de cómo conectaremos las **8 hojas de Catálogos Físicos Excel** con nuestra tabla operativa maestra `LIST_Lineas_MS` dentro de AppSheet, logrando una carga automatizada, libre de errores tipográficos y 100% blindada.

---

## 🏗️ Arquitectura de Relaciones (Ref vs Enum/Valid_If)

Para optimizar el rendimiento y la experiencia de usuario (UX) de AppSheet, usaremos dos estrategias distintas dependiendo de la complejidad del catálogo:

### 1. Inyección de Datos Complejos (Uso de `Ref`)
Cuando al seleccionar un dato (Ej: Clase de Piping `C3`), necesitamos que AppSheet "arrastre" o autocomplete mágicamente otros 3 o 4 campos subyacentes (Material, Presiones, Temperaturas).

**Implementación en AppSheet (`Data > Columns > LIST_Lineas_MS`):**
- **Columna `CLASE_PIPING`:** Tipo `Ref` -> Source Table: `CAT_ClasePiping_MS`
- **Resultados Mágicos (Initial_Value / App Formula):**
  - Columna `PRESION_DISENO_KG`: `[CLASE_PIPING].[PRESION_DISENO_KG]`
  - Columna `TEMP_DISENO_C`: `[CLASE_PIPING].[TEMP_DISENO_C]`
  - Columna `MATERIAL_BASE`: `[CLASE_PIPING].[MATERIAL]`

*(La belleza de esto: El Planificador de Oficina Técnica sólo selecciona "C3" en el menú desplegable, y automáticamente AppSheet rellena los campos de presión a **20.0 kg/cm²** y temperatura a **38°C**. ¡Cero posibilidad de error!)*

### 2. Validaciones Simples (Uso de `Valid_If` dinámico)
Cuando sólo necesitamos una lista desplegable simple estandarizada, sin arrastrar metadata extra (salvo fluidos).

**Implementación en AppSheet:**
- **Columna `FLUIDO_SERVICIO`:** Tipo `Ref` -> Source Table: `CAT_FluidoServicio_MS`. Esto permite arrastrar el color.
  - Columna `COLOR_PINTURA`: `[FLUIDO_SERVICIO].[COLOR_PINTURA]` (Initial_Value)
- **Columna `NPS_SIZE`:** Tipo `Enum` -> Valid_If: `CTG_DiametrosNPS_MS[NPS_SIZE]`
- **Columna `REVESTIMIENTO_INT`:** Tipo `Enum` -> Valid_If: `CTG_RevestimientoInt_MS[CODIGO_INT]`
- **Columna `AISLACION_EXT`:** Tipo `Enum` -> Valid_If: `CTG_AislacionExt_MS[CODIGO_EXT]`
- **Columna `SISTEMA_CWPA`:** Tipo `Enum` -> Valid_If: `CAT_SistemasCWPA_MS[NUMERO_SISTEMA]`

---

## 🛠️ Roadmap de Configuración (Lista de Tareas AppSheet)

Una vez que tengas los Excel cargados en tu nube y AppSheet lea las tablas, debes ejecutar exactamente este paso a paso:

### Paso 1: Configurar las tablas "Catálogos" (`CAT_*` y `CTG_*`)
1. Ve a `Data > Tables`. Asegúrate que **todas** las tablas de catálogos independientes estén cargadas (incluyendo los nuevos `CTG_RevestimientoInt_MS` y `CTG_AislacionExt_MS`).
2. Ingresa a las columnas de cada catálogo y asegúrate de aplicar el patrón de **Natural Keys**:
   - La columna `ID_...` (Ej: `ID_CLASE`, `ID_FLUIDO`) sea la **Key** (llave primaria).
   - *Nota de Arquitectura:* A diferencia de UUIDs incomprensibles, hemos diseñado estas tablas usando **Natural Keys** (ej. el ID de la clase "C1" es literalmente "C1"). Esto permite que, si un gerente exporta el Excel puro de la tabla `LIST_Lineas_MS`, la columna `CLASE_PIPING` mostrará "C1" de forma legible matemáticamente sin romper AppSheet.
   - La columna del código (Ej: `CLASE`, `CODIGO`, o `NPS_SIZE`) sea el **Label** (Lo que el usuario ve visualmente en el menú).
3. Todas estas tablas de catálogo deben quedar con privilegios de **Read-Only** (*Updates Allowed: None*). ¡Nadie puede alterar los estándares Codelco desde la app móvil!

### Paso 2: Conectar la Mente Maestra (`LIST_Lineas_MS`)
1. En tu Excel `LIST_Lineas_MS` de SharePoint, crea una nueva columna llamada `ESQUEMA_PINTURA` (si no la tenías).
2. Ve a AppSheet > Data > Tables > **LIST_Lineas_MS** y presiona **"Regenerate Structure"** para que AppSheet lea la nueva columna.
3. Busca la columna `CLASE_PIPING`. Cambia su tipo (*Type*) a **Ref**. Selecciona como *Source table* `CAT_ClasePiping_MS`. AppSheet creará automáticamente la relación.
4. Busca la columna `TEMP_DISENO_C`. En su casilla de *Auto Compute > Initial value* escribe la fórmula: `[CLASE_PIPING].[TEMP_DISENO_C]`.
5. Repite lo mismo para la columna `PRESION_DISENO_KG` usando la fórmula `[CLASE_PIPING].[PRESION_DISENO_KG]`.
6. Repite la mecánica para el Fluido: Asegúrate que `FLUIDO_SERVICIO` sea tipo **Ref** apuntando a su catálogo, y en `COLOR_PINTURA` pon la fórmula mágica de *Initial value*: `[FLUIDO_SERVICIO].[COLOR_PINTURA]`.
7. Busca las columnas de `DIAMETRO_NPS`, `SISTEMA`, `REVESTIMIENTO_INT`, `AISLACION_EXT` y `ESQUEMA_PINTURA`.
   - Cambia sus tipos a **Enum**.
   - En *Data Validity > Valid_If*, pon las fórmulas (Ej: `CTG_AislacionExt_MS[CODIGO_EXT]`, `CTG_RevestimientoInt_MS[CODIGO_INT]` o `CTG_EsquemaPintura_MS[CODIGO_ESQUEMA]`).
   - Activa el switch inferior que dice *"Input mode: Dropdown"*.

### Paso 3: Probando el Gemelo Digital
Abre el emulador visual de AppSheet a tu derecha. Ingresa a la vista de "Líneas" y presiona el botón **(+) Nuevo**.
Al rellenar el formulario, si seleccionas `C1`, maravillosamente verás como Temperatura y Presión se completan solos.

---
> **📌 Estado del Hito:** Todo el Data Model en Excel ya está finalizado matemáticamente. El balón está ahora en la cancha de configuración interna de la consola nube de AppSheet.
