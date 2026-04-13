# 📚 Manual Técnico y Funcional: PipEI

Este manual proporciona una descripción detallada del funcionamiento, arquitectura y operación de la plataforma **PipEI**, el sistema oficial de control de piping de **Echeverría Izquierdo (EIMISA)**.

---

## 1. ARQUITECTURA DEL SISTEMA

### Ecosistema Tecnológico
PipEI opera como un ecosistema integrado de tres capas:
1.  **Captura de Datos (AppSheet)**: Aplicación móvil y de escritorio para el registro en tiempo real en terreno y oficina técnica.
2.  **Análisis y Reportabilidad (PipEI Dashboard)**: Interfaz web construida en Node.js para la visualización de KPIs, curvas S y gestión gerencial.
3.  **Comunicación y Alertas (Bot jAIme)**: Asistente automatizado en Telegram para notificaciones proactivas y consultas rápidas.
4.  **Almacenamiento (SharePoint/Excel)**: Repositorio centralizado de datos y documentos (PDFs) en la nube corporativa de Microsoft 365.

### El Patrón LIST/LOG (Integridad de Datos)
Para garantizar una trazabilidad inmutable y evitar la pérdida de información, PipEI utiliza una arquitectura de dos capas para sus entidades críticas:

*   **Tablas LIST (Bandeja Viva)**: Contienen la "Foto Actual" del componente (ej. la última revisión de un plano). Es lo que el usuario consulta para operar.
*   **Tablas LOG (Historial Inmutable)**: Registran cada evento o cambio. Cuando se sube una nueva revisión de un plano, se crea una fila en el LOG; luego, un proceso automático (Bot) actualiza la tabla LIST.
    *   *Beneficio*: Permite auditar quién, cuándo y por qué cambió una información en cualquier momento.

---

## 2. MÓDULO DE INGENIERÍA

Este módulo es la base del sistema, donde se definen los parámetros técnicos que regirán la fabricación y el montaje.

### 2.1. Gestión de P&IDs
Controla el catálogo de diagramas de instrumentación y tuberías.
*   **Pantalla Principal**: Visor de planos vigentes con acceso directo al PDF.
*   **Lógica de Revisión**: El sistema bloquea visualmente las versiones anteriores, asegurando que Terreno siempre trabaje con la ingeniería aprobada.
*   **Gobernanza**: Solo el rol de **Oficina Técnica (OT)** puede cargar nuevas revisiones en el historial (LOG).

### 2.2. Line List (Catálogo de Líneas)
Es el "Gemelo Digital" del proyecto. Contiene todos los parámetros de diseño de cada línea de tubería.
*   **Datos Clave**: Diámetro (NPS), Clase de tubería, Fluido, Aislamiento, y requerimientos de Ensayos No Destructivos (NDE).
*   **Automatización NDE**: Según la clase de la línea, el sistema pre-configura los tipos de inspección necesarios (ej. Visual para todas, Líquidos Penetrantes o Radiografía para líneas críticas).
*   **Carga Masiva**: Permite la importación de miles de líneas mediante archivos CSV para agilizar el inicio del proyecto.

### 2.3. Isométricos y Control de Detalle
Gestiona las hojas isométricas vinculadas a las líneas maestras.
*   **Vigencia Documental**: Utiliza el motor de actualización automática (Bot) para sincronizar el PDF vigente desde el historial de revisiones.
*   **Configuración de Fabricación**: En este nivel, OT ingresa la cantidad estimada de **Spools** por cada isométrico, lo cual sirve de control para el módulo de Taller.
*   **Bloqueo Proactivo**: Si un isométrico cambia de revisión, el sistema marca automáticamente todos sus spools hijos como "En Evaluación", impidiendo su montaje hasta que OT valide el impacto del cambio.

### 2.4. Gestión de SDI (Solicitudes de Información)
Controla las consultas técnicas enviadas al cliente (DAND) que impactan el diseño o la construcción.
*   **Trazabilidad de Respuestas**: Rastrea el estado de cada SDI (PENDIENTE, RESPONDIDA) y la descripción de la respuesta oficial.
*   **Vínculo con Ingeniería**: Mediante una tabla relacional, cada SDI se vincula a los Isométricos afectados.
*   **Impacto en Dashboard**: Permite visualizar cuántas consultas están deteniendo el avance de fabricación o montaje.

---

## 3. MÓDULO DE TALLER (FABRICACIÓN DE SPOOLS)

Este módulo gestiona la transformación de la ingeniería en piezas físicas (Spools) y su seguimiento a través del taller.

### 3.1. El Spool como Unidad de Control
Cada pieza de tubería prefabricada tiene una identidad única en el sistema.
*   **Identificación (TAG)**: Cada spool tiene un correlativo único por proyecto (ej. 0001, 0002) que se marca físicamente en el acero.
*   **Ciclo de Vida del Spool**: El sistema rastrea automáticamente el estado del spool:
    1.  **En Fabricación**: El spool existe en el sistema y se están reportando sus juntas.
    2.  **Liberado Dimensional**: El spool ha pasado el control de geometría.
    3.  **En Pintura**: Se registra el envío y recepción en la planta de pintura.
    4.  **Listo para Despacho**: Cuenta con todas las aprobaciones de calidad.
    5.  **En Terreno / Montado**: Seguimiento final hasta su instalación definitiva.

### 3.2. Control de Hitos en Taller
Los supervisores de taller reportan los avances de cada pieza mediante:
*   **Corte y Armado**: Inicio de la vida física del spool.
*   **Reporte de Soldadura**: Actualiza automáticamente el avance físico del spool.
*   **Limpieza y Terminación**: Preparación para la etapa de calidad.

---

## 4. MÓDULO DE CALIDAD (QA/QC)

Es el motor de validación que asegura que cada unión cumpla con los estándares del proyecto.

### 4.1. El Weld Log (Registro de Juntas)
Centraliza toda la información de las uniones soldadas y fusionadas (HDPE).
*   **Origen de Datos**: Oficina Técnica carga los pulls de juntas desde Spoolgen.
*   **Registro Forense**: Al reportar una soldadura, el sistema congela la revisión actual del plano. Esto permite detectar si una junta fue ejecutada con una revisión que ya no es vigente.
*   **Cálculo de WDI (Work Density Index)**: El sistema calcula automáticamente las pulgadas diametrales según el NPS y material de la junta, alimentando los estados de avance sin errores manuales.

### 4.2. Control de Ensayos (NDE)
Gestión de resultados de Laboratorios y Ensayos No Destructivos.
*   **Integración de Resultados**: Permite vincular los reportes de Radiografía, Ultrasonido o Líquidos Penetrantes directamente a la ficha de la junta.
*   **Bloqueo de Avance**: Una junta con un ensayo rechazado bloquea automáticamente el estado de "Aprobado" del spool padre, impidiendo su despacho a terreno.

### 4.3. Inspecciones Visuales y Dimensionales
Checklists digitales para liberar hitos críticos.
*   **VT (Inspección Visual)**: Registro fotográfico y aprobación del soldador.
*   **DCC (Control Dimensional)**: Validación de que el spool respeta las medidas del isométrico antes de ir a pintura o despacho.

---

## 5. MÓDULO DE LOGÍSTICA Y TRAZABILIDAD QR

Este módulo asegura el control del flujo físico de materiales y piezas mediante identidades digitales vinculadas a códigos QR.

### 5.1. Trazabilidad de Materiales (MTO)
Gestión de suministros y bultos antes de la fabricación.
*   **Identidad de Bulto**: Cada pallet, paquete o caja recibe un sticker con una identidad única (`M-XXXXX`) y su respectivo código QR.
*   **Escaneo en Origen**: Al recibir material en bodega, se escanea el sticker para vincularlo a la línea de ingeniería o al stock general.
*   **Auditoría Fotográfica**: El sistema exige una foto del respaldo físico (guía de despacho o estado del material) para garantizar la integridad de la recepción.

### 5.2. Despacho y Recepción de Spools
Control de movimientos entre taller, pintura y terreno.
*   **Escaneo de Salida**: Al despachar un spool hacia pintura o terreno, el encargado escanea el código para cambiar el estado de ubicación en tiempo real.
*   **Escaneo de Recepción**: Valida la llegada de la pieza al punto de destino, cerrando el ciclo logístico y alertando a los supervisores de montaje sobre la disponibilidad de la pieza.

---

## 6. PIPEI DASHBOARD (ANÁLISIS Y REPORTABILIDAD)

Interfaz de gestión web diseñada para la toma de decisiones basada en datos reales de terreno.

### 6.1. Pantalla de KPIs (Cuadro de Mando)
*   **Avance Físico (WDI)**: Visualización en tiempo real de las pulgadas diametrales soldadas vs. las programadas.
*   **Productividad por Soldador**: Estadísticas de rendimiento y tasas de rechazo (NDE) segmentadas por estampa.
*   **Curvas S**: Gráficos de avance acumulado con proyección de cumplimiento según fecha de término.

### 6.2. Mapas de Calor y Estado Operativo
*   **Filtros de Gestión**: Capacidad de filtrar datos por Área, Isométrico o Línea para detectar cuellos de botella específicos.
*   **Status de SDI**: Monitor de consultas técnicas pendientes que están impactando la ingeniería viva.

---

## 7. EL BOT jAIme (NOTIFICACIONES PROACTIVAS)

Asistente inteligente integrado en Telegram para facilitar la comunicación del proyecto.

### 7.1. Canales de Alerta
*   **Alertas de Calidad**: Notificación inmediata si una junta es rechazada por NDE.
*   **Alertas de Ingeniería**: Aviso al grupo de OT cuando se sube una nueva revisión de plano.
*   **Alertas Logísticas**: Reporte diario de piezas despachadas y recibidas en terreno.

### 7.2. Consultas Rápidas
El bot permite a los usuarios autorizados consultar el estado de una pieza (`Status Spool`) o el avance de una línea mediante comandos directos, sin necesidad de abrir la aplicación completa.

---

## 8. SEGURIDAD Y GOBERNANZA

*   **Propiedad de la Data**: Toda la información generada es propiedad exclusiva de **Echeverría Izquierdo**.
*   **Acceso Empresarial**: Inicio de sesión obligatorio mediante cuentas de correo corporativas.
*   **Auditoría de Cambios**: Gracias al patrón LIST/LOG, cada cambio en el sistema queda registrado con el correo del usuario y la marca de tiempo exacta.

---
*Este manual es un documento vivo que se actualiza con cada mejora implementada en el ecosistema PipEI.*
