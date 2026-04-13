# 📘 Guía de Desarrollo Oficial: PipEI (Piping Echeverría Izquierdo)

Esta guía documenta la lógica, requisitos y visión técnica de **PipEI**, la solución corporativa para el control de piping de **Echeverría Izquierdo (EIMISA)**.

---

## 1. CONTEXTO
**Echeverría Izquierdo Montajes Industriales S.A. (EIMISA)** es una empresa chilena con más de 25 años de trayectoria en la ejecución de proyectos de construcción y montaje industrial de gran escala en sectores como minería, energía y oil & gas. Con presencia en Chile y Perú, la compañía se especializa en soluciones integrales que abarcan desde la ingeniería hasta la puesta en marcha de complejos industriales.

### Área de Aplicación y Motivación
La solución **PipEI** se aplicará específicamente en el control de fabricación y montaje de tuberías (piping). Actualmente, esta actividad se realiza de forma manual mediante planillas Excel aisladas y registros en papel, lo que genera una brecha crítica de información entre la oficina técnica, el taller y el montaje en terreno.

La motivación principal para este proyecto es mitigar la fragmentación de datos y eliminar ineficiencias sistémicas que impactan la rentabilidad, tales como:
*   **Falta de Trazabilidad**: Dificultad para rastrear el historial de piezas o soldaduras ya instaladas.
*   **Riesgo Operativo**: Montaje de componentes basado en planos obsoletos por fallas en la comunicación de revisiones.
*   **Impacto Financiero**: Pérdida de tiempo en la consolidación manual de datos para estados de pago y dossieres de calidad.

### Restricciones y Condiciones Operativas
El despliegue de la solución debe considerar las siguientes condiciones críticas:
*   **Ambiente Hostil**: La operación se realiza en terrenos con condiciones climáticas extremas y gran altitud geográfica.
*   **Conectividad**: Se requiere soporte para trabajo offline con sincronización posterior debido a la conectividad intermitente en las zonas de obra.
*   **Cumplimiento Normativo**: La herramienta debe alinearse con los estrictos estándares de calidad de EIMISA y los requerimientos específicos de clientes mineros de clase mundial.

---

## 2. OBJETIVO

### Objetivo General
Implementar una solución digital corporativa denominada **PipEI**, orientada al control integral del ciclo de vida de los materiales y de la ejecución de piping, asegurando una trazabilidad total desde la etapa de diseño hasta la puesta en marcha.

### Funciones Clave de la Herramienta
El proyecto contempla el desarrollo de una aplicación digital que permita:
*   La captura sistemática y automática de los hitos de fabricación y montaje.
*   La validación inteligente de las revisiones de ingeniería en tiempo real.
*   La generación proactiva de alertas ante desviaciones críticas del proceso operativo.

### Beneficios Esperados
Con esta herramienta, EIMISA busca optimizar su operación de la siguiente manera:
*   **Reducción de Costos**: Disminuir drásticamente los reprocesos derivados del uso de ingeniería obsoleta, garantizando un control del 100% sobre la vigencia documental.
*   **Mitigación de Riesgos**: Eliminar las no conformidades de calidad asociadas a documentación no vigente.
*   **Eficiencia Administrativa**: Estandarizar los controles operativos, automatizar la reportabilidad técnica del proyecto y mejorar significativamente la precisión de los estados de avance físicos.

---

## 3. ALCANCE DEL PROBLEMA
El proyecto abarca el diseño e implementación de la plataforma **PipEI** para la gestión integral de los procesos de ingeniería, prefabricado, calidad y logística vinculados al montaje de tuberías. La solución aborda el problema puntual de la fragmentación de datos y la falta de una identidad digital única para los componentes de piping.

### Alcance Operativo y Módulos
La solución abordará los siguientes aspectos críticos del ciclo de vida del proyecto:
*   **Ingeniería**: Gestión centralizada de catálogos técnicos, incluyendo P&IDs, Line Lists e Isométricos, junto con matrices de impacto para el control de revisiones.
*   **Prefabricado (Shop)**: Control unitario y seguimiento de hitos para cada Spool, abarcando las etapas de corte, armado, soldadura y limpieza.
*   **Calidad (QA/QC)**: Digitalización del registro de juntas (Weld Log), gestión de ensayos no destructivos (NDE) e inspecciones visuales y dimensionales.
*   **Logística**: Trazabilidad de suministros, gestión de bultos y control de despachos a terreno mediante el uso de tecnología de códigos QR.

### Usuarios y Beneficiarios
La aplicación estará disponible y adaptada para todos los niveles de la organización vinculados al contrato, asegurando que la información sea capturada y consultada por:
*   Niveles gerenciales y jefaturas de proyecto para la toma de decisiones basada en datos.
*   Personal de Oficina Técnica (OT) y Calidad para la validación de hitos críticos y gobernanza de datos.
*   Supervisores y capataces de terreno para el reporte de avances en tiempo real.

### Efectos Esperados y Exclusiones
El alcance del proyecto busca generar un quiebre definitivo con las prácticas manuales anteriores, logrando:
*   La eliminación total del uso de planillas Excel para el seguimiento operativo.
*   La consolidación automática del **WDI** y estados de avance.
*   La transición de marcas temporales en las piezas a una identidad digital permanente vinculada al historial de calidad.

---

## 4. DESCRIPCIÓN DE LA SITUACIÓN ACTUAL (LÍNEA BASE)
Tradicionalmente, el control de piping en los proyectos de EIMISA se ha realizado de forma manual mediante planillas Excel aisladas, registros en papel y reportes verbales. Esta metodología genera una desconexión entre la oficina técnica, el taller y el montaje en terreno, operando bajo silos de información que retrasan la detección de errores.

### El Proceso Actual y sus Deficiencias
La línea base actual se caracteriza por una dependencia crítica de procesos manuales para la consolidación de avances físicos (WDI) y la transcripción de datos desde el papel por parte de digitadores. Las principales problemáticas detectadas son:
*   **Falta de Validación en Tiempo Real**: No existe un mecanismo inmediato que permita al personal autorizado (OT/Calidad) validar los hitos críticos del proceso en el momento en que ocurren.
*   **Riesgo de Ingeniería Obsoleta**: Actualmente no existe un "cerrojo" sistémico que impida soldar o montar una pieza vinculada a un plano que ha sido actualizado, lo que genera un riesgo constante de retrabajos por falta de notificación inmediata al equipo de montaje.
*   **Deficiencias en Trazabilidad**: Existe una dificultad inherente para rastrear el historial completo de una pieza o soldadura una vez instalada, debido a que la información no está centralizada ni estandarizada.

### Hipótesis de Impacto
Sobre esta línea base, la implementación de la solución busca impactar positivamente en los siguientes ejes estratégicos:
*   **Hipótesis 1: Productividad y Eficiencia en el Flujo de Datos**: Busca eliminar los tiempos muertos asociados a la búsqueda manual de información y la transcripción de reportes, permitiendo que el personal de supervisión y oficina técnica se enfoque en tareas de análisis y control de mayor valor.
*   **Hipótesis 2: Control de Calidad y Reducción de Retrabajos**: Apunta a mitigar el riesgo de errores en la información mediante la validación automática de revisiones de ingeniería, asegurando que el montaje se realice siempre con documentación vigente y eliminando los costos derivados de fabricaciones duplicadas o erróneas.
*   **Hipótesis 3: Trazabilidad y Gestión Documental**: Busca garantizar la integridad de la información para la entrega final al cliente, automatizando la generación de dossieres de calidad y eliminando la latencia en la consolidación de los reportes necesarios para la liberación de estados de pago.

---

## 5. DESCRIPCIÓN DE LA SITUACIÓN DESEADA
La situación deseada se define por la implementación de **PipEI**, un ecosistema digital que estandariza el control de fabricación y montaje de tuberías, eliminando la fragmentación de datos y asegurando la integridad de la ingeniería en tiempo real.

### Requerimientos Funcionales (Core de PipEI)
La solución debe operar bajo una lógica de captura de datos en el origen y validación inteligente, con los siguientes módulos centrales:
*   **Gestión Inteligente de Revisiones**: Bloqueo proactivo de componentes (spools) al detectar cambios en la revisión del isométrico padre, impidiendo el avance de procesos con documentación obsoleta.
*   **Cálculo Automático de WDI**: Motor de cálculo integrado que determina el avance físico según diámetros y materialidad, eliminando la digitación manual de pulgadas.
*   **Trazabilidad Logística QR**: Uso de etiquetas físicas vinculadas a la nube para el rastreo de piezas en tránsito entre taller, pintura y terreno.
*   **Alertas Predictivas**: Notificaciones automáticas ante desviaciones en los tiempos de ciclo o fallas en ensayos NDE.
*   **Gestión de Guardado**: El sistema debe contar con mecanismos de autoguardado o guardado manual según la criticidad de la pantalla, para asegurar que no se pierda información en terreno.

### Requerimientos No Funcionales y de Seguridad
Para garantizar la robustez corporativa, la plataforma debe cumplir con los siguientes estándares:
*   **Seguridad y Gobernanza**: Control de acceso basado en roles corporativos y autenticación mediante cuentas empresariales, manteniendo una arquitectura de datos inmutable para auditorías.
*   **Roles de Usuario Definidos**: Acceso diferenciado por perfiles, incluyendo Administrador, Oficina Técnica (OT), QA/QC, Logística, Supervisor y personal de Terreno.
*   **Integración de Ecosistema**: Capacidad de conexión vía API con herramientas estratégicas de la compañía:
    *   **Dynamics**: Sincronización de proyectos y materiales.
    *   **BUK**: Gestión de personas, roles y proyectos asociados.
    *   **Aplicaciones de Cubicaciones**: Integración de datos técnicos base.
*   **Disponibilidad y UX**: Interfaz intuitiva y responsiva disponible 24/7, diseñada para minimizar la curva de aprendizaje y optimizada para dispositivos móviles.
*   **Propiedad y Mantenimiento**: Toda la información generada será propiedad exclusiva de EIMISA. El administrador de la compañía debe tener la autonomía para mantener parámetros y listas sin intervención del proveedor.
