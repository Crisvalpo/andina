# GUÍA DE DESARROLLO: SOLUCIÓN CONTROL DE PIPING (LUKEAPP / ANDINA)

---

## 1. CONTEXTO

### 1.1 Breve descripción de la empresa
**Echeverría Izquierdo Montajes Industriales (EIMISA)** es una empresa líder en ingeniería y construcción, especializada en el montaje de grandes estructuras y sistemas industriales para el sector minero y energético. 

### 1.2 Actividad principal y área de aplicación
La solución se aplica en el **Contrato 4600022667: Espesador de Concentrado Colectivo PMFC (Proyecto Andina)**. El área específica es la de **Piping (Cañerías)**, encargada de la fabricación, logística, montaje y control de calidad de líneas de tuberías, isométricos y spools.

### 1.3 Situación general que motiva la solución
La complejidad de los proyectos mineros modernos exige una gestión de datos milimétrica. La rotación de revisiones de ingeniería, la dispersión de materiales entre talleres y terreno, y la necesidad de reportar avances precisos a la gerencia motivan la creación de una herramienta digital que centralice la información y elimine el uso de planillas aisladas.

### 1.4 Restricciones o condiciones relevantes
*   **Normativas:** Cumplimiento estricto de estándares NDE (Ensayos No Destructivos), trazabilidad de soldadores y procedimientos de calidad (QA/QC).
*   **Ambiente Operativo:** Uso en faena minera (Andina) con conectividad intermitente (requiere soporte Offline en AppSheet).
*   **Recursos Disponibles:** Integración con el ecosistema Microsoft 365 (SharePoint como base de datos), AppSheet como interfaz móvil, y Telegram (via jAIme Bot) como canal de notificaciones y consultas rápidas.

---

## 2. OBJETIVO

### 2.1 ¿Qué se busca lograr con la solución?
Lograr la **trazabilidad total del ciclo de vida del piping**, desde el control documental (P&IDs e Isométricos) hasta el montaje final en terreno, asegurando que cada junta soldada y cada spool fabricado cumpla con la revisión vigente de ingeniería, optimizando la logística y automatizando el reporte de avance para la toma de decisiones.

---

## 3. ALCANCE DEL PROBLEMA

### 3.1 ¿Qué parte del problema se abordará?
La solución aborda la cadena completa de valor del piping:
1.  **Ingeniería:** Gestión documental y control de versiones.
2.  **Fabricación:** Control de juntas y spools en taller.
3.  **Logística:** Recepción de materiales y despacho de spools.
4.  **Calidad:** Registro de inspecciones, dimensionales y liberaciones (QAQC).

### 3.2 ¿Qué problema PUNTUAL resolverá la solución?
*   **Obsolescencia:** Evitar el montaje de piezas basadas en planos obsoletos mediante un sistema de bloqueo por impacto de revisión.
*   **Incertidumbre Logística:** Eliminar la pérdida de trazabilidad de los spools en tránsito entre el taller y el montaje.
*   **Fragmentación de Datos:** Centralizar el "Weld Log" y el "S-Curve" en un gemelo digital accesible desde dispositivos móviles.

---

## 4. DESCRIPCIÓN DE LA SITUACIÓN ACTUAL (LÍNEA BASE)

### 4.1 Proceso actual y problemas detectados
Actualmente, los procesos dependen de:
*   **Registros manuales y hojas de cálculo (Excel):** Generan duplicidad de datos y riesgo de error humano.
*   **Desfase de información:** Los reportes de avance suelen tener un retraso de 24 a 48 horas.
*   **Dificultad en gestión de cambios:** Notificar a todo el equipo de terreno sobre un cambio en un isométrico es lento, lo que resulta en re-trabajos costosos.

### 4.2 Hipótesis e impacto buscado
La línea base establece que el 15-20% de las ineficiencias provienen de falta de información oportuna en terreno. La hipótesis es que la digitalización reducirá los re-trabajos por ingeniería obsoleta a **cero** y optimizará el tiempo de reporte de supervisión en un **40%**.

---

## 5. DESCRIPCIÓN DE LA SITUACIÓN DESEADA

### 5.1 Requerimientos Funcionales (Lo que debe hacer)
*   **Gestión de 2 Capas:** Mantener una tabla "LIST" (viva/vigente) y una tabla "LOG" (historial inmutable) para cada entidad crítica.
*   **Trazabilidad mediante QR:** Identificación física de materiales y spools vinculada a la App.
*   **Automatización de Ciclo de Vida:** Bots que actualicen el estado del spool (ej. "Soldado" -> "Liberado dimensional") de forma automática al detectar registros de calidad.
*   **Interfaz de Consulta Jerárquica:** Navegación fluida: Proyecto > Línea > Isométrico > Spool > Junta.

### 5.2 Requerimientos No Funcionales (Condiciones adicionales)
*   **Seguridad:** Gobernanza de datos basada en roles (Admin, OT, Calidad, Terreno).
*   **Robustez:** Estructura de archivos en SharePoint organizada jerárquicamente para evitar saturación de carpetas.
*   **Portabilidad:** Notificaciones en tiempo real vía Telegram para hitos críticos de fabricación y despacho.
*   **Gobernanza de Ingeniería:** Bloqueo estricto de edición para tablas relacionales de diseño (sólo lectura para terreno).
