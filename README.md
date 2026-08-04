#  IERC-GNL: Índice Espacial de Riesgo Socioeconómico para Comunidades

[![GeoPackage](https://img.shields.io/badge/OGC-GeoPackage_v1.1-blue.svg)](https://www.ogc.org/standard/geopackage/)
[![CRS](https://img.shields.io/badge/CRS-EPSG%3A4326_(WGS84)-green.svg)](https://epsg.io/4326)
[![H3 Grid](https://img.shields.io/badge/Uber_H3-Adaptive_Res_8%2F9-orange.svg)](https://h3geo.org/)
[![Organization](https://img.shields.io/badge/Organization-Causa_Natura_Center-emerald.svg)](https://causanatura.org/)
[![Next.js](https://img.shields.io/badge/Dashboard-Next.js_16-black.svg)](https://nextjs.org/)
[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](LICENSE)

---

##  Resumen del Proyecto

El **Índice Espacial de Riesgo Socioeconómico para Comunidades (IERC-GNL)** es una plataforma espacial e instrumento metodológico desarrollado en el marco del **Plan Operativo Anual (POA 2026-2028)** de **Causa Natura Center**. Su objetivo es evaluar la vulnerabilidad socioecológica, pesquera y de gobernanza de las comunidades pesqueras artesanales ante la expansión de proyectos de **Gas Natural Licuado (GNL)** en el **Golfo de California, México**.

### Equipo Técnico del Proyecto
- **Juan Carlos Barrera (JCB):** Consultor Senior / Especialista Pesquero y Socioambiental
- **Enrique Gorosave (EG):** Analista de Datos y SIG

---

##  Entregable Espacial GeoPackage v1.1 (Meta 1 POA 2026)

El archivo principal de datos geográficos estandarizado OGC se ubica en:  
`deliverables/v1_geopackage/ierc_golfo_california.gpkg`

### Capas Vectoriales Incluidas (7 Capas)

| Nombre de Capa | Geometría | Entidades | Descripción |
|---|---|---|---|
|  **`proyectos_gnl`** | `Point` | 5 | Infraestructura y terminales GNL en el Golfo con scores de riesgo pesquero (Moreno-Báez et al.) e IERC. |
|  **`gasoductos_infraestructura_gnl`** | `LineString` | 2 | Trazados conocidos y proyectados de ductos de gas natural (Sonora, Saguaro, Guaymas). |
|  **`localidades_estudio_ierc`** | `Point` | 3 | Delimitación de las 3 comunidades del POA (**Punta Chueca Comca'ac**, **Puerto Libertad**, **Guaymas**). |
|  **`anp_habitats_criticos`** | `Polygon` | 2 | Áreas Naturales Protegidas (CONANP) y hábitats marinos críticos. |
|  **`zonas_pesqueras_pangas`** | `MultiPolygon` | 17 | Polígonos pesqueros artesanales PANGAS integrados con la clave única `uid_espaciotemporal`. |
| ⬡ **`grilla_h3_riesgo`** | `Polygon` | 5,244 | Malla hexagonal Uber H3 adaptativa (Res 8 en mar / Res 9 en zonas portuarias) con evaluación del IERC. |
|  **`riqueza_relativa_pesquera`** | `MultiPolygon` | 11,065 | Malla espacial de riqueza biológica pesquera acumulada. |

---

##  Metodología y Formulación Matemática

El riesgo integral por celda $i$ y periodo $t$ se calcula mediante:

$$R_{i,t} = H_{i,t} \times V_{i,t}$$

Donde $H_{i,t}$ representa la amenaza y exposición espacial (densidad de esfuerzo, proximidad GNL, conflicto de rutas) y $V_{i,t}$ la vulnerabilidad socioeconómica y de gobernanza ($V_{i,t} = 0.25 \text{Sensibilidad} + 0.25 \text{Dependencia} + 0.20 \text{Biocultural} + 0.15 \text{Género} + 0.15 [1 - \text{Cap.Adaptative}]$).

### Estándar de Identificador Único Espacio-Temporal (`uid_espaciotemporal`)
$$\text{uid\_espaciotemporal} = \text{comunidad} - \text{actor} - \text{pesquería} - \text{arte} - \text{zona} - \text{temporada} - \text{ruta}$$

---

##  Estructura del Repositorio

```bash
ierc-gnl-project/
├── causanaturadata/            #  Documentos oficiales del proyecto (POA 2026, Manual Metodológico)
├── dashboard/                  # Dashboard Web Interactivo (Next.js 15, React, Tailwind)
├── data/                       # Insumos geográficos de gabinete (PANGAS, CONANP, GFW, INEGI)
├── deliverables/
│   └── v1_geopackage/          #  ENTREGABLE ESPACIAL META 1
│       ├── ierc_golfo_california.gpkg  # GeoPackage OGC v1.1 (EPSG:4326)
│       ├── build_geopackage.py         # Script de generación y compilación en Python
│       └── GEOPACKAGE_METADATA.md      # Diccionario técnico de datos
├── docs/                       # Documentación metodológica e inventario de vacíos
│   └── metodologia/
│       ├── Nota_Metodologica_Ajustada_JCB_EG.md
│       └── Inventario_y_Matriz_Vacios_Geoespaciales_EG.md
└── src/                        # Motores de cálculo y validación en Python
├── engine/                 # Validadores espaciales (spatial_validator.py)
└── h3_indexer/             # Indexador espacial Uber H3
```

---

## 🛠️ Reproducibilidad e Instalación

### Ejecutar Suite Modular de Pruebas (Pytest)

```bash
PYTHONPATH=. ./.venv/bin/python3 -m pytest tests/ -v
```

### Ejecutar Pipeline End-to-End de Ingesta y Cálculo

```bash
# 1. Inicializar Lakehouse y Catálogo JSON
PYTHONPATH=. ./.venv/bin/python3 scripts/init_lakehouse.py

# 2. Computar Features Gold IERC H3
PYTHONPATH=. ./.venv/bin/python3 scripts/compute_ierc_features.py

# 3. Exportar insumos para el Dashboard Web
PYTHONPATH=. ./.venv/bin/python3 scripts/prepare_dashboard_data.py
```

### Ejecutar el Dashboard Interactivo

```bash
cd dashboard
npm run dev
```

---

##  Cita Oficial

**Causa Natura Center (2026):** *Índice Espacial de Riesgo Socioeconómico para Comunidades (IERC) ante proyectos de GNL en el Golfo de California*. Elaborado por Juan Carlos Barrera (JCB) y Enrique Gorosave (EG).
