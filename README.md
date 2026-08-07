# IERC-GNL: Índice Espacial de Riesgo Socioeconómico para Comunidades

[![GeoPackage](https://img.shields.io/badge/OGC-GeoPackage_v1.1-blue.svg)](https://www.ogc.org/standard/geopackage/)
[![CRS](https://img.shields.io/badge/CRS-EPSG%3A4326_(WGS84)-green.svg)](https://epsg.io/4326)
[![H3 Grid](https://img.shields.io/badge/Uber_H3-Adaptive_Res_8%2F9-orange.svg)](https://h3geo.org/)
[![Organization](https://img.shields.io/badge/Organization-Causa_Natura_Center-emerald.svg)](https://causanatura.org/)
[![Next.js](https://img.shields.io/badge/Dashboard-Next.js_16-black.svg)](https://nextjs.org/)
[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![CI](https://github.com/causanatura/ierc-gnl-project/actions/workflows/ci.yml/badge.svg)](https://github.com/causanatura/ierc-gnl-project/actions/workflows/ci.yml)

---

## Resumen del Proyecto

El **Índice Espacial de Riesgo Socioeconómico para Comunidades (IERC-GNL)** es una plataforma espacial e instrumento metodológico desarrollado en el marco del **Plan Operativo Anual (POA 2026-2028)** de **Causa Natura Center**. Su objetivo es evaluar la vulnerabilidad socioecológica, pesquera y de gobernanza de las comunidades pesqueras artesanales ante la expansión de proyectos de **Gas Natural Licuado (GNL)** en el **Golfo de California, México**.

### Equipo Técnico del Proyecto
- **Juan Carlos Barrera (JCB):** Consultor Senior / Especialista Pesquero y Socioambiental
- **Enrique Gorosave Meza (EG):** Analista de Datos y SIG

---

## Reportes Oficiales

| Reporte | Descripción | Autor | Versión |
|---------|-------------|-------|---------|
| **[REPORTE_INVENTARIO_DATOS_IERC_GNL_v2.3_ENRIQUE_GOROSAVE.md](REPORTE_INVENTARIO_DATOS_IERC_GNL_v2.3_ENRIQUE_GOROSAVE.md)** | **Reporte oficial detallado v2.3** — Inventario SILVER (14 fuentes, 165 parquets, conteos verificados) + capas dashboard (15) + ductos CNIH/SENER + cadena ingesta y auditoría + Responsible AI | Enrique Gorosave Meza | v2.3 (2026-08-07) |
| **[REPORTE_INVENTARIO_DATOS_IERC_GNL_v2.2_ENRIQUE_GOROSAVE.md](REPORTE_INVENTARIO_DATOS_IERC_GNL_v2.2_ENRIQUE_GOROSAVE.md)** | Reporte v2.2 — Inventario + capas dashboard + ingesta + auditoría | Enrique Gorosave Meza | v2.2 (2026-08-07) |
| **[REPORTE_INVENTARIO_DETALLADO_IERC_GNL.md](REPORTE_INVENTARIO_DETALLADO_IERC_GNL.md)** | Inventario técnico SILVER/GOLD + cadena ingesta + auditoría + Responsible AI | Enrique Gorosave Meza | v2.1 (2026-08-06) |
| **[REPORTE_INVENTARIO_GEOPACKAGE.md](REPORTE_INVENTARIO_GEOPACKAGE.md)** | Metadata entregable GeoPackage Meta 1 | Enrique Gorosave Meza | v1.1 |

---

## Entregable Espacial GeoPackage v1.1 (Meta 1 POA 2026)

El archivo principal de datos geográficos estandarizado OGC se ubica en:
`deliverables/v1_geopackage/ierc_golfo_california.gpkg`

### Capas Vectoriales Incluidas (7 Capas)

| Nombre de Capa | Geometría | Entidades | Descripción |
|---|---|---|---|
| **`proyectos_gnl`** | `Point` | 5 | Infraestructura y terminales GNL en el Golfo con scores de riesgo pesquero (Moreno-Báez et al.) e IERC. |
| **`gasoductos_infraestructura_gnl`** | `LineString` | 2 | Trazados conocidos y proyectados de ductos de gas natural (Sonora, Saguaro, Guaymas). |
| **`localidades_estudio_ierc`** | `Point` | 3 | Delimitación de las 3 comunidades del POA (**Punta Chueca Comca'ac**, **Puerto Libertad**, **Guaymas**). |
| **`anp_habitats_criticos`** | `Polygon` | 2 | Áreas Naturales Protegidas (CONANP) y hábitats marinos críticos. |
| **`zonas_pesqueras_pangas`** | `MultiPolygon` | 17 | Polígonos pesqueros artesanales PANGAS integrados con la clave única `uid_espaciotemporal`. |
| **`grilla_h3_riesgo`** | `Polygon` | 5,244 | Malla hexagonal Uber H3 adaptativa (Res 8 en mar / Res 9 en zonas portuarias) con evaluación del IERC. |
| **`riqueza_relativa_pesquera`** | `MultiPolygon` | 11,065 | Malla espacial de riqueza biológica pesquera acumulada. |

---

## Lakehouse Medallion Architecture (v2.0)

### Capa SILVER — 14 Fuentes Procesadas (165 Parquets)

| Dominio | Datasets | Filas | Particionado |
|---------|----------|-------|--------------|
| **CENEGAS** | injection_capacity, extracciones, tarifas | 103,596 + 698,079 + 378 | Plano |
| **SENER** | prontuario, volumen_almacenamiento | 16 + 186 | Plano |
| **PROFEPA** | acciones_inspeccion | 51 | Plano |
| **SEMARNAT** | sitios_contaminados | 481 | Plano |
| **datos.gob.mx** | registros_publicos | 1 | Plano |
| **ECC Climabase** | catalog (48 GeoTIFFs) | 48 | Plano |
| **CNIH/SENER** | ductos_cnih (24 LineStrings, 6,399 km) + anp_ramsar (2 Polygons) + capas_contextuales (2) | 24 + 2 + 2 | GeoParquet |
| **GFW** | fishing_effort_h3, vessels | 11,652 | year/month H3-8 |
| **NASA** | chlor_a, sst | 2,298,240 c/u | year/month H3-8 |
| **ASEA** | mias_enriched (CDC) | 11 | H3-10/tipo |
| **GEBCO** | bathymetry (res 8, 9) | 59,998 | resolution |
| **TNC** | bajos_marinos, arrecifes_coral_negro | — | H3-8 |
| **PANGAS** | fishing_zones | 263,796 | Plano |

### Capa GOLD — 13 Productos Analíticos

| Dataset | Filas | Descripción |
|---------|-------|-------------|
| `ierc_risk_h3_8.parquet` | 830,869 | Índice principal de riesgo (score 0-1) |
| `ierc_features_h3_8.parquet` | 830,869 | Features para ML |
| `ierc_monte_carlo_h3_8.parquet` | 830,869 | Simulación N=1000 (p05, p95, median) |
| `ierc_features_adaptive_h3.parquet` | 830,869 | Multi-resolución H3 + PANGAS |
| `ierc_risk_multiplicative.parquet` | 830,869 | Modelo IPCC H×V |
| `ierc_confidence_h3.parquet` | 830,869 | Scores de confianza espacial |
| `gas_infrastructure_master_inyecciones.parquet` | 33 | Master inyecciones por punto |
| `gas_infrastructure_master_extracciones.parquet` | 225 | Master extracciones por punto |
| `gas_injection_yearly.parquet` | 315 | Agregación anual inyecciones |
| `gas_extraction_yearly.parquet` | 2,307 | Agregación anual extracciones |
| `tarifas_zone_summary.parquet` | 63 | Resumen tarifas por zona |
| `env_risk_by_nodo.parquet` | 33 | Riesgo ambiental por nodo |

---

## Metodología y Formulación Matemática

El riesgo integral por celda $i$ y periodo $t$ se calcula mediante:

$$R_{i,t} = H_{i,t} \times V_{i,t}$$

Donde $H_{i,t}$ representa la **amenaza y exposición espacial** (densidad de esfuerzo, proximidad GNL, conflicto de rutas) y $V_{i,t}$ la **vulnerabilidad socioeconómica y de gobernanza**:

$$V_{i,t} = 0.25 \text{Sensibilidad} + 0.25 \text{Dependencia} + 0.20 \text{Biocultural} + 0.15 \text{Género} + 0.15 [1 - \text{Cap.Adaptative}]$$

### Modelo Aditivo (Oficial POA 2026)
$$IERC_{total} = (Amenaza \times 0.20) + (Exposición \times 0.20) + (Sensibilidad \times 0.15) + (Dependencia \times 0.15) + (Valor\_Biocultural \times 0.15) + ((1 - Capacidad\_Adaptativa) \times 0.15)$$

### Estándar de Identificador Único Espacio-Temporal (`uid_espaciotemporal`)

$$\text{uid\_espaciotemporal} = \text{comunidad} - \text{actor} - \text{pesquería} - \text{arte} - \text{zona} - \text{temporada} - \text{ruta}$$

---

## Pipeline de Ingesta y Auditoría (v2.0)

### Nuevas Capacidades Implementadas (2026-08-06)

| Feature | Descripción | Archivo |
|---------|-------------|---------|
| **CDC exact-once** | Re-ejecuciones seguras sin duplicados mediante `_cdc_hash` persistido en lakehouse | `src/data/ingestion/base.py` |
| **Schema contract validation** | Fallo rápido por drift de columnas/tipos vs catálogo declarativo | `src/data/ingestion/base.py` |
| **Derived dataset versioning** | Trazabilidad Gold→Silver con lineage embebido en `schema.lineage` | `src/data/catalog/catalog.py` |

### Pipeline Overview

```
FACTORY LAYER
  create_gfw_ingester()  create_nasa_ingester()  create_tnc_*()
  create_asea_ingester()  create_bathymetry_ingester()  create_pangas_ingester()
        │
        ▼
BASE INGESTER
  run() → extract() → transform() → validate() → load()
  + Catalog tracking (runs.jsonl)
  + CDC exact-once dedup (_cdc_hash)
  + Schema contract validation
  + H3 + temporal partitioning
        │
        ▼
  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │   GFW    │  │  NASA    │  │   TNC    │  │  ASEA    │  │  PANGAS  │
  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘
```

### Auditoría de Ejecuciones

Cada ingesta genera registro en `lakehouse/metadata/ingestion_runs.jsonl`:

```json
{
  "run_id": "asea_mias_20260806_143022_a1b2c3d4",
  "dataset_name": "asea_mias",
  "started_at": "2026-08-06T14:30:22.123",
  "finished_at": "2026-08-06T14:30:25.456",
  "status": "success",
  "records_processed": 11,
  "records_inserted": 2,
  "records_updated": 0,
  "records_failed": 0,
  "quality_results": {"total_batches": 1, "warnings_count": 0},
  "error_message": null
}
```

---

## Dashboard Web Interactivo (Next.js 16)

### Capas Base Disponibles (15 Capas)
- **4 Terminales GNL (11 Features)** — Puntos + buffers H3-10 (tipo/estatus/estado)
- **Polígonos Saguaro (MIA 181V)** — Detalle del proyecto Saguaro
- **Gasoductos, Sitios Ramsar & ANPs** — Contexto regulatorio (capas_contextuales)
- **Ductos CNIH/SENER (24 tramos, 6,399 km)** — NUEVO: tramos reales de ArcGIS con popups enriquecidos
- **SENER/CNIH Red Gasoductos (WMS)** — Capa WMS externa
- **Contornos Batimétricos GEBCO 2024** — 1,146 contornos con profundidad
- **Malla H3 IERC (Res 8/9)** — 5,244 hexágonos con scores IERC
- **GFW Esfuerzo Pesquero (H3, 9,960)** — Heatmap zoom≤7 / círculos zoom>7, filtros: año/mes/arte/bandera/confianza
- **PANGAS Multiespecie (4,241)** — Hexágonos H3 + riqueza por especie/arte
- **Pesca Buceo (249)**, **Chinchorro (2,209)**, **Redes (1,263)**, **Camarón/Manta (783)**, **Trampas (360)**
- **Riqueza Relativa Pesquera (11,065)** — 51 especies

### Capas Derivadas (Análisis)
- **IERC Score** — Índice integrado 0–1
- **Nivel de Riesgo** — Muy Bajo / Bajo / Medio / Alto / Muy Alto
- **Amenaza / Vulnerabilidad** — Componentes modelo multiplicativo
- **Confianza Espacial** — Filtro calidad datos (threshold configurable)

### Controles UI
- Time Slider 2020–2024 | H3 Resolution Selector (8/9/Adaptive)
- Risk Threshold (p05–p95 Monte Carlo) | Layer Opacity | Spatial Filter

---

## Estructura del Repositorio

```bash
ierc-gnl-project/
├── causanaturadata/            # Documentos oficiales (POA 2026, Manual Metodológico)
├── dashboard/                  # Dashboard Web (Next.js 16, React, Tailwind)
├── data/                       # Insumos geográficos de gabinete (PANGAS, CONANP, GFW, INEGI)
├── deliverables/
│   └── v1_geopackage/          # ENTREGABLE ESPACIAL META 1
│       ├── ierc_golfo_california.gpkg
│       ├── build_geopackage.py
│       └── GEOPACKAGE_METADATA.md
├── docs/                       # Documentación metodológica e inventario de vacíos
│   └── metodologia/
│       ├── Nota_Metodologica_Ajustada_JCB_EG.md
│       └── Inventario_y_Matriz_Vacios_Geoespaciales_EG.md
├── src/
│   ├── data/
│   │   ├── ingestion/          # Pipeline ingesta (base.py, factory.py, asea_mias.py, etc.)
│   │   ├── catalog/            # DataCatalog JSONL + register_derived_dataset()
│   │   └── lakehouse/          # LocalFileStorage (Parquet + ZSTD)
│   └── engine/                 # Validadores espaciales (spatial_validator.py)
├── config/
│   ├── lakehouse.yaml          # Configuración lakehouse + CDC keys por dataset
│   └── data_catalog.yaml       # Catálogo declarativo con schemas por dataset
├── scripts/                    # Scripts operacionales (init, compute, dashboard prep)
├── tests/unit/                 # 45 tests pasando (storage, catalog, h3, ierc, responsible_ai, spatial_validator, monte_carlo, pipeline_e2e)
├── REPORTE_INVENTARIO_DATOS_IERC_GNL_v2.1_ENRIQUE_GOROSAVE.md
├── INVENTARIO_DATOS_IERC_GNL_v2.1.md
├── REPORTE_INVENTARIO_GEOPACKAGE.md
└── README.md
```

---

## Reproducibilidad e Instalación

### Prerrequisitos
- Python 3.11+ (venv en `.venv/`)
- Node.js 18+ (para dashboard)
- `netCDF4` para ingesta NASA (opcional, pendiente instalar)

### Ejecutar Suite de Pruebas (Pytest)
```bash
PYTHONPATH=. ./.venv/bin/python3 -m pytest tests/unit/ -v
# 45 passed: test_storage_catalog (4) + test_utils_h3 (4) + test_utils_ierc (4) + test_engine_ierc (3) + test_engine_responsible_ai (12) + test_engine_spatial_validator (17) + test_engine_monte_carlo (1) + test_pipeline_e2e (1)
```

### Pipeline End-to-End
```bash
# 1. Inicializar Lakehouse y Catálogo JSON
PYTHONPATH=. ./.venv/bin/python3 scripts/init_lakehouse.py

# 2. Computar Features Gold IERC H3
PYTHONPATH=. ./.venv/bin/python3 scripts/compute_ierc_features.py

# 3. Exportar insumos para Dashboard Web
PYTHONPATH=. ./.venv/bin/python3 scripts/prepare_dashboard_data.py
```

### Ejecutar Dashboard Interactivo
```bash
cd dashboard
npm install
npm run dev
# http://localhost:3001
```

---

## CI/CD Pipeline

El proyecto incluye un pipeline de CI completo (`.github/workflows/ci.yml`) con 5 jobs:

| Job | Descripción |
|-----|-------------|
| **test** | Unit tests Python (45 tests) |
| **lint** | Syntax check en módulos core |
| **verify-cdc** | Verificación CDC exact-once + Schema contract |
| **dashboard-build** | Build Next.js 16 |
| **summary** | Resumen consolidado |

---

## Cita Oficial

**Causa Natura Center (2026):** *Índice Espacial de Riesgo Socioeconómico para Comunidades (IERC) ante proyectos de GNL en el Golfo de California*. Elaborado por Juan Carlos Barrera (JCB) y Enrique Gorosave Meza (EG).

---

## Documentación Técnica Vinculada

- **[REPORTE_INVENTARIO_DATOS_IERC_GNL_v2.3_ENRIQUE_GOROSAVE.md](REPORTE_INVENTARIO_DATOS_IERC_GNL_v2.3_ENRIQUE_GOROSAVE.md)** — Reporte oficial v2.3 con conteos verificados de todos los datasets Silver/Gold, capas dashboard, cadena de ingesta y auditoría — *Autor: Enrique Gorosave Meza, Causa Natura Center*
- **[REPORTE_INVENTARIO_DATOS_IERC_GNL_v2.2_ENRIQUE_GOROSAVE.md](REPORTE_INVENTARIO_DATOS_IERC_GNL_v2.2_ENRIQUE_GOROSAVE.md)** — Reporte oficial v2.2
- **[REPORTE_INVENTARIO_GEOPACKAGE.md](REPORTE_INVENTARIO_GEOPACKAGE.md)** — Metadata entregable GeoPackage Meta 1
- **[config/lakehouse.yaml](config/lakehouse.yaml)** — Configuración lakehouse, CDC keys, particionamiento
- **[config/data_catalog.yaml](config/data_catalog.yaml)** — Catálogo declarativo con schemas por dataset
- **[docs/metodologia/Nota_Metodologica_Ajustada_JCB_EG.md](docs/metodologia/Nota_Metodologica_Ajustada_JCB_EG.md)** — Formulación matemática IERC
- **[docs/metodologia/Inventario_y_Matriz_Vacios_Geoespaciales_EG.md](docs/metodologia/Inventario_y_Matriz_Vacios_Geoespaciales_EG.md)** — Matriz de vacíos geográficos
- **[.github/workflows/ci.yml](.github/workflows/ci.yml)** — Pipeline CI/CD completo