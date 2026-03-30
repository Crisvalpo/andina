# Catálogos de Referencia - Proyecto Andina 4600022667
# Espesador de Concentrado Colectivo PMFC - F039 SS01

> Este documento concentra las tablas de referencia reales del proyecto extraídas de las
> especificaciones técnicas SGP-02CAN-ESPTC-00001 y cubicaciones 4600022667.
> Úsalo para poblar los Enum y Valid_If de AppSheet en las tablas LIST_Lineas_MS, LIST_Iso_MS, etc.

---

## 🧪 Catálogo 1: Fluidos de Servicio (FLUIDO_SERVICIO)

| Código | Nombre | Color Pintura Exterior |
|:---|:---|:---|
| `CT` | Concentrado Cu - Mo | Marrón RAL 8002 |
| `PW` | Agua de Proceso | Verde RAL 6024 |
| `GW` | Agua de Sello | Verde RAL 6024 |
| `RW` | Agua Recuperada | Verde RAL 6024 |
| `PA` | Aire Planta | Celeste RAL 5012 |
| `IA` | Aire de Instrumentos | Celeste RAL 5012 |
| `FP` | Agua Contra Incendio | Rojo RAL 3020 |

---

## 🏗️ Catálogo 2: Clases de Piping (CLASE_PIPING)

Fuente: Especificación Técnica SGP-02CAN-ESPTC-00001 - Tabla de Clases de Material.

| Clase | Fluido | P. Diseño (PSI) | P. Diseño (KG/cm²) | T. Diseño (°C) | Material / Norma |
|:---|:---|:---|:---|:---|:---|
| `C1` | PW / GW | 285 psi | 20.0 kg/cm² | 38°C | Acero carbono ASTM A106 Gr B / ASTM A53 Gr B |
| `C2` | CT | 285 psi | 20.0 kg/cm² | 38°C | Acero carbono ASTM A53 Gr B (liso) |
| `C3` | CT | 285 psi | 20.0 kg/cm² | 38°C | Acero carbono ASTM A53 Gr B + Neopreno interior (R3) |
| `C5` | FP | 175 psi | 12.3 kg/cm² | 40°C | Acero carbono ASTM A53 Gr B (incendio) |
| `C11` | CT | 285 psi | 20.0 kg/cm² | 38°C | Acero carbono ASTM A53 Gr B + Goma natural interior |
| `G1` | PA | 285 psi | 20.0 kg/cm² | 38°C | Acero carbono galvanizado ASTM A53 Gr B |
| `H1` | RW | 90 psi (PN6) | 6.3 kg/cm² | 20°C | HDPE PE100 PN6 (ISO 4427) |
| `H2` | RW / CT | 145 psi (PN10) | 10.2 kg/cm² | 20°C | HDPE PE100 PN10 (ISO 4427) |

---

## 🛡️ Catálogo 3: Revestimientos Interiores (CODIGO_REVESTIMIENTO_INT)

> **Campo F del Tag de Línea.** Es el ÚLTIMO campo del identificador de tubería.
> `03351 - CT - 6" - C3 - 0005 - [R3]`
> Este campo NO es la revisión del isométrico.

Fuente: SGP-02EST-ESPTC-00001 y 4600022667...ESPME-00004. Utilizado exclusivamente para protección interna contra desgaste abrasivo o químico.

| Código | Función | Aplicación Típica / Especificación |
|:---|:---|:---|
| `N` | Sin Revestimiento Interior | Cañerías desnudas internamente (Acero, HDPE) |
| `R1` | Goma Natural Rubber Lined (6mm) | Cajas compensadoras, spooling crítico de agua turbia |
| `R2` | Goma Natural Rubber Lined (12mm) | Zonas de mayor desgaste |
| `R3` | Neopreno (3mm a 15mm) | **Exclusivo para Líneas de Concentrado (CT)** |

> ⚠️ Toda línea con código R1, R2 o R3 se debe rotular obligatoriamente en taller con la leyenda **"PRECAUCION CAÑERIA REVESTIDA INTERIORMENTE. NO SUBIR NI QUEMAR."**

---

## 🏔️ Catálogo 16: Aislación Externa (CODIGO_AISLACION_EXT)

Fuente: SGP-02CAN-ESPTC-00001. Aísla térmicamente el exterior de la cañería. **Su uso anula visualmente la pintura de la cañería**.

| Código | Función | Efecto en Sistema | Restricción de Pintura y Trazabilidad |
|:---|:---|:---|:---|
| `N` | Sin Aislación | Normal | La cañería luce el esquema de pintura asignado |
| `HC` | Hot Conservation | Conservación Calor | La línea va revestida en chaqueta metálica o térmica exterior. |
| `PP` | Personal Protection | Protección Física | Malla o recubrimiento externo de seguridad. |
| `ET` | Electrical Tracing | Cinta Calefactora | Requiere llenado del campo TEMP_TRACING en el Line List. |

---

## 📐 Catálogo 4: Diámetros Nominales Usados (NPS_SIZE)

> **Formato AppSheet:** Los valores se listan puramente numéricos (sin el símbolo `"` ni `mm`) para mantener integridad con la carga masiva y listas restrictivas Enum.

Los siguientes diámetros nominales están documentados en las cubicaciones del proyecto:

**Acero Carbono (en pulgadas - norma ASME B36.10):**
`3/4` | `1` | `2` | `3` | `4` | `6` | `8` | `10` | `12` | `16` | `24`

> Nota: Los diámetros 1¼, 2½, 3½, 7 y 20 **NO se usan** para transporte de pulpa. El diámetro `10` fue documentado activo en terreno.

**HDPE (en milímetros - norma ISO 4427):**
`50` | `110` | `160` | `200` | `250` | `315` | `400` | `450`

---

## 🔬 Catálogo 5: Requisitos NDE (PORCENTAJE_NDE)

Aplicable a tabla LIST_Lineas_MS y al historial de soldaduras.

| Material | Tipo Junta | Ensayo | Cobertura | Norma/Código |
|:---|:---|:---|:---|:---|
| Acero | Visual | Visual (VT) | 100% | Criterio propio |
| Acero | A tope (BW) | Radiografía (RT) | **100%** | API 1104 Cláusula 9 |
| Acero | No-BW (Slip-On, arranques) | Líquidos Penetrantes (PT/LP) | 100% | - |
| HDPE | Visual | Visual (VT) | 100% | - |
| HDPE | Termofusión | Ultrasonido (UT) | **100%** | ASME B31.3 Cap VII |
| HDPE | Termofusión | Destructivo (tensión/doblado) | **5% aleatorio** | ASTM F2620 |

---

## 💧 Catálogo 6: Tipo de Prueba de Presión (TIPO_PRUEBA)

| Código | Tipo | Presión | Duración | Medio |
|:---|:---|:---|:---|:---|
| `Hidrostática` | Prueba hidrostática (acero) | **1.5x** presión diseño | Mínimo **2 horas** | Agua potable |
| `Hidrostática HDPE` | Prueba hidrostática (HDPE/PVC) | **1.5x** presión máx. fabricante ≤ PN+500 kPa | 2 horas | Agua |
| `Neumática` | Prueba en sistemas de gas | **1.1x** presión diseño | Incremental | Aire comprimido |

> **Prueba Neumática:** Chequeo preliminar a 130 kPa (19 psig), luego incrementos de 34.5 kPa (5 psig). Detección por gas y burbujas (ASME Sección V).

---

## 🔩 Catálogo 7: Materiales ASTM de Referencia

| Componente | Norma / Material |
|:---|:---|
| Tubería acero sin costura | ASTM A106 Gr B |
| Tubería acero soldada (ERW) | ASTM A53 Gr B |
| Tubería acero (API) | API 5L Gr B |
| Tubería HDPE | PE100 (norma ISO 4427) |
| Bridas y fittings forjados | ASTM A105 |
| Fittings soldados a tope (BW) | ASTM A234 Gr WPB |
| Fittings roscados / galvanizados | ASTM A197 (hierro maleable) |
| Hierro fundido dúctil | ASTM A536 Gr 65-45-12 |
| Pernos espárrago | ASTM A193 Gr B7 |
| Tuercas hexagonales | ASTM A194 Gr 2H |

---

## ⚡ Catálogo 8: Procesos de Soldadura Permitidos

| Proceso | Código AWS | Acero | HDPE | Restricción |
|:---|:---|:---|:---|:---|
| Arco manual | SMAW | ✅ | ❌ | - |
| TIG | GTAW | ✅ | ❌ | - |
| MIG/MAG | GMAW | ✅ | ❌ | ❌ NO en cordones de raíz sin back gouging |
| Tubular | FCAW | ✅ | ❌ | - |
| Termofusión | - | ❌ | ✅ | Solo máquinas automatizadas, NO manual |
| Electrofusión | - | ❌ | ✅ | Solo máquinas automatizadas |

**Normas de Ejecución y Calificación:**
- Acero: ASME B31.3 • ASME B31.4 • API 1104 • AWS D1.1 • ASME BPVC Sección IX
- HDPE: ASME B31.3 Cap. VII • ASTM F2620 • Instrucciones del fabricante

**Documentos requeridos (WBS Calidad):**
- `WPS` = Welding Procedure Specification
- `PQR` = Procedure Qualification Record
- `WPQ` = Welder Performance Qualification

---

## 🏷️ Catálogo 9: Sistemas AWP / Áreas (SISTEMA_CWPA)

| Área | Descripción |
|:---|:---|
| `03351` | Espesador de Concentrado Colectivo PMFC |

> Para proyectos futuros este catálogo se irá extendiendo con nuevas áreas constructivas.

---

## 📋 Catálogo 10: Tags de Líneas Reales del Proyecto (Muestra)

### Concentrado Cu-Mo (CT)
```
03351-CT-6"-C3-0005-R3    → 6" Conc., Clase C3 (Neopreno 15mm)
03351-CT-6"-C3-0018-R3
03351-CT-6"-C3-0021-R3
03351-CT-6"-C3-0023-R3
03351-CT-3"-C2-0059-N     → 3" Conc., Clase C2 (sin revestimiento)
03351-CT-3"-C2-0060-N
03351-CT-3"-C2-0061-N
03351-CT-3"-C2-0062-N
03351-CT-3"-C2-0063-N
03351-CT-3"-C2-0064-N
03351-CT-3"-C2-0065-N
03351-CT-3"-C2-0066-N
03351-CT-3"-C2-0067-N
03351-CT-3"-C2-0068-N
03351-CT-3"-C2-0069-N
03351-CT-3"-C2-0070-N
03351-CT-3"-C2-0086-N
03351-CT-4"C2-0003-N
03351-CT-4"C2-0004-N
03351-CT-6"-C11-0001-N    → 6" Conc., Clase C11 (Goma natural)
03351-CT-200-H2-0002-N    → 200mm HDPE PN10
03351-CT-200-H2-0045-N
```

### Agua de Proceso (PW)
```
03351-PW-6"-C1-0013-N     → 6" Agua Proceso, Clase C1
03351-PW-4"-C1-0016-N
03351-PW-4"-C1-0094-N
03351-PW-2"-C1-0024-N
03351-PW-2"-C1-0025-N
03351-PW-2"-C1-0026-N
03351-PW-2"-C1-0039-N
03351-PW-2"-C1-0048-N
03351-PW-2"-C1-0049-N
03351-PW-2"-C1-0054-N
03351-PW-2"-C1-0056-N
03351-PW-2"-C1-0081-N
03351-PW-2"-C1-0082-N
03351-PW-2"-C1-0083-N
03351-PW-2"-C1-0084-N
03351-PW-2"-C1-0088-N
03351-PW-2"-C1-0089-N
03351-PW-2"-C1-0090-N
03351-PW-2"-C1-0091-N
03351-PW-2"-C1-0092-N
03351-PW-2"-C1-0093-N
```

### Agua de Sello (GW)
```
03351-GW-1"-C1-0031-N
03351-GW-1"-C1-0032-N
03351-GW-1"-C1-0033-N
03351-GW-1"-C1-0034-N
03351-GW-1"-C1-0035-N
03351-GW-1"-C1-0036-N
03351-GW-1"-C1-0043-N
03351-GW-1"-C1-0075-N
03351-GW-1"-C1-0076-N
03351-GW-2"-C1-0042-N
03351-GW-2"-C1-0095-N
```

### Agua Recuperada (RW) - HDPE
```
03351-RW-250-H1-0009-N    → 250mm HDPE PN6
03351-RW-250-H1-0010-N
03351-RW-250-H1-0011-N
03351-RW-450-H1-0008-N    → 450mm HDPE PN6
```

---

## 📊 Catálogo 11: Campos Paramétricos Obligatorios del Line List

Fuente: SGP-02CAN-ESPTC-00001 (Anexo 3 - Formato exigido para base de datos de tuberías). Estos son los campos duros que OT debe mapear por cada línea:

*   **Identificación (Tag):** `Área` - `Fluido` - `NPS` - `Clase` - `Correlativo` - `Cod.Revestimiento`
*   **Origen/Destino:** `Desde` y `Hasta`
*   **Flujo:** `Caudal Diseño (m3/h)` y `Velocidad Diseño (m/s)`
*   **Condiciones Físicas:** `Gravedad Específica`
*   **Temperatura:** `Operación (°C)`, `Mínima (°C)` y `Máxima (°C)`
*   **Presión:** `Operación (kPa)` y `Prueba (kPa)`
*   **Medio de Prueba:** Ej. Agua potable o Aire
*   **Documento Base:** `N° P&ID`
*   **Visual:** `Línea Color Codificación Base` y `Línea Color Codificación Secundaria`

---

## 🎨 Catálogo 12: Revestimiento Exterior y Señalética Colorimétrica

Revestimiento Tricapa exigido para Tuberías de Acero (SGP-02CAN-ESPTC-00001):

| Capa | Material | Espesor Película (Seca) |
|---|---|---|
| Capa 1 | FBE (Fusion Bonded Epoxy) | Mínimo `150 micras` |
| Capa 2 | Copolímero adhesivo | `175 micras` |
| Capa 3 | HDPE exterior | Mínimo `1.8 mm` |
| Borde | Reserva sin revestir (soldeo) | `100 mm` (Bisel 45°) |
| Prep. | Superficie (Metal Blanco) | `SSPC SP-5` |

**Señalización por Código de Colores:**
*   **Franja de anillo continuo:** Longitud mínima = `6 veces el Diámetro Nominal`.
*   **Distancia máxima entre anillos de color:** `10 metros` a lo largo de la tubería.
*   **Tuberías Enterradas:** Cinta amarilla de alerta instalada a `300 mm` desde la superficie (de `150 mm` de ancho).

---

## 🧪 Catálogo 13: Criterios Exactos de Pruebas y Tolerancias

**Tolerancia de Reparación Soldaduras:**
La norma restringe categóricamente a un máximo de **2 veces permitidas en el mismo lugar de la soldadura**.

**Factores de Diseño de Pruebas de Presión:**
*   **Prueba Hidrostática (Plásticos):** `1.5` x Presión máxima admisible (Límite: PN + 500 kPa).
*   **Prueba Hidrostática (Acero):** `1.5` x Presión de diseño.
*   **Prueba Neumática (Gases):** `1.1` x Presión de diseño (Incrementos de `34.5 kPa` / 5 psig).
*   **Temperatura obligatoria del agua (prueba):** Entre `16 °C` y `30 °C`.

---

## 🔗 Catálogo 14: Tipos de Uniones Restringidas (Joint Types)

Fuente: SGP-02CAN-ESPTC-00001. Listado oficial de métodos de unión y terminaciones permitidos.

| Acrónimo | Nombre en Inglés | Nombre en Español | Aplicación Obligatoria |
|:---|:---|:---|:---|
| `BW` / `BE` | Butt Weld / Beveled Edge | Soldadura a Tope | Cañerías de acero. Uniones deben tener igual diámetro y espesores similares (dif < 1.5mm) |
| `SW` | Socket Weld | Soldadura a Encaje | Bridas y válvulas de acero compuerta (Socketweld/screwed) |
| `FLG` | Flanged (FF/RF) | Unión con Bridas | Válvulas, equipos y metales disímiles (Flat Face para hierro fundido, Raised Face el resto) |
| `NPT` / `SE`| Threaded / Screwed | Conexiones Roscadas | Cañerías no subterráneas. Hilo NPT bajo norma ASME B1.20.1. (Sello teflón o soldadura sellante) |
| `GE` / `VG` | Grooved / Victaulic | Acoples Ranurados / Mecánicos | Solo mediante instrucción del fabricante original |
| `BF` | Butt Fusion | Electrofusión / Termofusión | **Solo HDPE**. Prohibida soldadura manual en plástico |
| `SO` | Slip On | Soldadura Deslizable (Filete) | Flanges Slip-On. Requiere doble soldadura de filete (interior y exterior) |
| `MJ` | Mechanical Joint | Uniones Mecánicas | Exclusivo para instalaciones de cañerías en PVC |

---

## 🖌️ Catálogo 15: Esquemas de Pintura y Revestimiento Exterior

Fuente: SGP-02EST-ESPTC-00001 y Criterio de Diseño 4600022667-001.

| Código Esquema | Aplicación (Medio) | Prep. Superficie (SSPC) | Capas | Espesor (μm) | Detalle del Sistema Corrosivo |
|:---|:---|:---|:---|:---|:---|
| `EPC-9` | Acero Superficial (Cordillerano) | SSPC-SP10 (Metal casi blanco) | 4 | 275 μm | Imprimante P14 (100) + Inter P14 (100) + Term P19 (50) + Sello P25 (25) |
| `TRICAPA` | Acero Enterrado | SSPC-SP5 (Metal blanco) | 3 | > 2125 μm | FBE (150) + Adhesivo (175) + HDPE exterior (1.8mm) |
| `C209` | Acero Enterrado | Manual o Mecánico Exhaustivo | 2 | Según fab. | Puente adherencia + Cinta anticorrosiva AWWA C209 |
| `C210` | Acero Enterrado | Limpieza Abrasiva (Taller) | Varía | Según fab. | Revestimiento epóxico líquido AWWA C210 |
| `N/A` | Sin Esquema Obligatorio | No Aplica | 0 | 0 | Tuberías HDPE, PVC o Acero Galvanizado |
