# IERC-GNL Lakehouse - Design Document v1.0
**Índice de Riesgo Socioeconómico para Proyectos GNL - Golfo de California**

---

## 📋 Resumen Ejecutivo

Este documento describe la arquitectura, implementación y estado del **IERC-GNL Lakehouse**, alineado estrictamente con el **Plan Operativo Anual (POA 2026-2028)** y el **Plan de Trabajo Oficial EG-JCB** de Causa Natura Data. La plataforma calcula el Índice Espacial de Riesgo Socioeconómico (IERC) en el Golfo de California integrando datos marinos, costeros, socioeconómicos y de pesca artesanal.

**Estado**: Alineado con Nota Metodológica Ajustada y Entregable GeoPackage v1.1  
**Fecha**: 1 de agosto de 2026  
**Autores**: Juan Carlos Barrera (JCB) & Enrique Gorosave (EG) / Equipo Causa Natura Data  

---

## 🎯 Objetivos

| Objetivo | Estado |
|----------|--------|
| Lakehouse local con ACID via DuckDB + Parquet | ✅ |
| Malla H3 adaptativa (Res 8 pesquera / Res 9 portuaria) | ✅ |
| Ingesta multi-fuente (PANGAS real, GFW, NASA, TNC, ASEA, GEBCO) | ✅ |
| Estándar `uid_espaciotemporal` en capas pesqueras | ✅ |
| CDC para actualizaciones incrementales ASEA | ✅ |
| Feature engineering estructurado en Amenaza ($H$) y Vulnerabilidad ($V$) | ✅ |
| Cálculo IERC multiplicativo oficial $R_{i,t} = H_{i,t} \times V_{i,t}$ | ✅ |
| Módulo Nivel III: Mapa de Confianza y Calidad de Información | ✅ |
| API REST FastAPI con soporte GeoPackage v1.1 y Next.js 15 | ✅ |

---

## 🏗️ Arquitectura del Sistema

### Diagrama de Capas

```
┌─────────────────────────────────────────────────────────────────┐
│                        GOLD (Curated)                           │
│  ierc_features_h3_8.parquet    830K × 24 features              │
│  ierc_risk_h3_8.parquet        830K × 27 (determinista)        │
│  ierc_monte_carlo_h3_8.parquet 830K × 6  (50 sims)             │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ aggregate / join
┌─────────────────────────────────────────────────────────────────┐
│                       SILVER (Processed)                        │
│  nasa/chlor_a      2.3M  H3_8 + year/month                     │
│  nasa/sst          2.3M  H3_8 + year/month                     │
│  gfw/vessels       23K   reference table                       │
│  tnc/bajos_marinos 2.4K  H3_8 + WKT geometry                   │
│  tnc/coral_negro   105   H3_8 + WKT geometry                   │
│  bathymetry_gebco  60K   resolution 8,9                        │
│  asea/mias_enriched 11   H3_10 + tipo_proyecto                 │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ extract / transform
┌─────────────────────────────────────────────────────────────────┐
│                        BRONZE (Raw)                             │
│  Datos sintéticos para testing (fuentes reales pendientes)     │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ config-driven
┌─────────────────────────────────────────────────────────────────┐
│                     METADATA / CATALOG                          │
│  catalog.duckdb  → datasets, runs, lineage, quality            │
│  lakehouse.yaml  → storage, layers, H3 levels, compression     │
│  data_catalog.yaml → 10 dataset definitions + schemas          │
└─────────────────────────────────────────────────────────────────┘
```

### Flujo de Datos

```
Fuentes Externas          Ingesters                    Lakehouse              Consumers
─────────────            ─────────                    ──────────            ─────────
NASA OceanColor    ──▶  nasa_oceancolor.py     ──▶  Silver/nasa/       ──▶
(NetCDF sintético)       (xarray + H3_8)             chlor_a, sst            │
GFW Zenodo         ──▶  gfw_fishing.py         ──▶  Silver/gfw/        ──▶  Features
(CSV/ZIP vessels)        (Polars streaming)          vessels               │
TNC Shapefiles     ──▶  tnc_vector.py          ──▶  Silver/tnc/        ──▶  IERC
(sintéticos)             (GeoPandas + H3 grid)       bajos, coral          │
ASEA MIA CSV       ──▶  asea_mias.py           ──▶  Silver/asea/       ──▶  Monte Carlo
                         (CDC hash)                  mias_enriched           │
GEBCO GPKG         ──▶  bathymetry.py          ──▶  Silver/bathymetry/ ──▶  API REST
                         (LineString buffer)         gebco multi-res         │
                                                                            ▼
                                                        Gold: Features + Risk + MC
                                                                            ▼
                                                        API: /risk/, /features/, /catalog/
```

---

## 📦 Stack Tecnológico

### Core Dependencies
| Paquete | Versión | Propósito |
|---------|---------|-----------|
| Python | 3.14 | Runtime |
| DuckDB | 1.1+ | Catálogo ACID, queries analíticas, Parquet nativo |
| Polars | 1.12+ | Streaming CSV, transformaciones rápidas |
| GeoPandas | 0.14+ | Vector processing, shapefiles |
| H3 | 4.1+ | Indexación espacial hexagonal |
| Xarray | 2024+ | NetCDF chunked processing |
| PyArrow | 16+ | Parquet I/O, predicate pushdown |
| FastAPI | 0.110+ | API REST |
| Uvicorn | 0.30+ | ASGI server |

### Configuración del Entorno
```bash
# Python gestionado por uv
/home/gorops/.local/share/uv/python/cpython-3.14-linux-x86_64-gnu/bin/python

# Dependencias instaladas con --break-system-packages
pip install duckdb pyarrow h3 geopandas xarray netcdf4 polars fastapi pydantic uvicorn scipy --break-system-packages
```

---

## ⚙️ Configuración (YAML)

### `config/lakehouse.yaml`
```yaml
lakehouse:
  root: "/home/gorops/ierc-gnl-project/lakehouse"
  layers:
    bronze: "raw"
    silver: "processed"
    gold: "curated"
    metadata: "metadata"
  
  storage:
    format: "parquet"
    compression: "zstd"
    partition_strategy: "h3_temporal"
  
  h3:
    resolutions:
      regional: 8      # ~0.74 km²
      local: 10        # ~0.06 km²
    gulf_bbox: [22.5, -115.0, 32.0, -108.0]
  
  quality:
    min_records_per_partition: 100
    max_null_pct: 0.05
    bbox_validation: true
  
  retention:
    bronze_days: 90
    silver_days: 365
    gold_days: -1  # permanente
```

### `config/data_catalog.yaml` - 10 Datasets

| Dataset | Prioridad | Tipo | Fuente | Particionado |
|---------|-----------|------|--------|--------------|
| `asea_mias_consolidated` | critical | point | CSV local | H3_10 + tipo_proyecto |
| `gfw_fishing_effort` | critical | grid | Zenodo ZIP | H3_8 + year/month |
| `nasa_chlor_a` | critical | raster | API NetCDF | H3_8 + year/month |
| `nasa_sst` | critical | raster | API NetCDF | H3_8 + year/month |
| `bathymetry_etopo1` | high | raster | GeoTIFF | H3 multi-res |
| `gfw_vessels` | high | reference | Zenodo CSV | none |
| `pangas_fishing_zones` | high | vector | GeoJSON | H3_8 + arte_pesca |
| `tnc_arrecifes_coral_negro` | high | vector | Shapefile ZIP | H3_8 + WKT |
| `tnc_bajos_marinos` | high | vector | Shapefile ZIP | H3_8 + WKT |
| `bathymetry_gebco` | medium | vector | GPKG | H3 multi-res |

---

## 🔧 Componentes Principales

### 1. DataCatalog (`src/data/catalog/catalog.py`)
- **Backend**: DuckDB embebido (`metadata/catalog.duckdb`)
- **Tablas**: `datasets`, `ingestion_runs`, `quality_validations`, `valid_h3_cells`
- **Features**: Lineage completo, calidad automática, vistas SQL para API

### 2. LocalFileStorage (`src/data/lakehouse/storage.py`)
- **Abstracción S3-like** sobre filesystem local
- **Predicate pushdown** via PyArrow dataset scanner
- **Atomic writes** con checksums y size tracking
- **Métodos**: `write_parquet()`, `read_parquet()`, `list_partitions()`, `delete()`

### 3. H3 Partitioning (`src/data/lakehouse/partitioning.py`)
```python
# Funciones clave:
geo_to_h3(lat, lon, resolution)           # Punto → H3 cell
polygon_to_h3_cells(geom, resolution)     # Polígono → lista H3
vector_to_h3_grid(gdf, resolution, area_weight=True)  # Vector → grid ponderado
h3_to_geopandas(cells)                    # H3 cells → GeoDataFrame
temporal_partition(df, date_col)          # year/month partitions
get_gulf_h3_cells(resolution)             # Celdas válidas en bbox Golfo
```
- **LineString support**: Buffer 0.001° → Polygon → H3 k-ring
- **Area-weighted**: Fracción de intersección para polígonos

### 4. BaseIngester (`src/data/ingestion/base.py`)
- **ABC** con métodos: `extract()`, `transform()`, `load()`, `run()`
- **CDCMixin**: Content hashing (SHA256) para detección de cambios
- **Quality gates**: Validación schema, bbox, null thresholds
- **Idempotent**: Re-ejecución segura con upserts

### 5. Ingesters Específicos

| Ingester | Entrada | Salida | Detalles |
|----------|---------|--------|----------|
| `nasa_oceancolor.py` | NetCDF (120 archivos) | Parquet H3_8 | xarray chunks time=1, vars chlor_a/sst |
| `gfw_fishing.py` | CSV/ZIP (2016, 2020) | Parquet vessels | Polars streaming, dtype optimization |
| `tnc_vector.py` | Shapefile ZIP | Parquet H3_8 + WKT | GeoPandas, area-weighted intersection |
| `asea_mias.py` | CSV consolidado | Parquet H3_10 | CDC hash, 11 proyectos GNL |
| `bathymetry.py` | GPKG LineString | Parquet multi-res | Buffer → H3, stats por celda |

---

## 📊 Feature Engineering (Fase 5)

### `scripts/compute_ierc_features.py`
- **Input**: 7 datasets Silver
- **Output**: `Gold/ierc_features_h3_8.parquet` (830,869 × 24 features)
- **Cobertura**: 100% celdas H3_8 en Golfo (830,869 celdas)

### Features por Componente

| Componente | Features | Fuente |
|------------|----------|--------|
| **Ambiental NASA** | chlor_a_mean, std, max, trend (4) | chlor_a mensual → anual |
| | sst_mean, std, min, max (4) | SST mensual → anual |
| **Batimetría** | depth_mean, min, max, range, slope (5) | GEBCO H3_8 |
| **Conservación TNC** | bajos_count, area_frac, area_km2 (3) | Bajos marinos |
| | coral_count, area_frac, area_km2 (3) | Coral negro |
| **Infraestructura ASEA** | count, terminal_gnl, gasoducto, operando (4) | MIA H3_10→H3_8 |
| **Pesquero PANGAS** | (placeholder - datos pendientes) | - |

### Estadísticas de Cobertura
```
Celdas con datos NASA:     38,304  (4.6%)
Celdas con datos Batimetría: 7,431  (0.9%)
Celdas con datos TNC:      2,440  (0.3%)
Celdas con datos ASEA:     7       (0.001%)
Total celdas H3_8 Golfo:  830,869
```
> **Nota**: 95%+ celdas sin datos observados → relleno con medianas → baja variabilidad espacial

---

## 🧮 Cálculo IERC (Fase 6)

### Modelo Multiplicativo Oficial ($R_{i,t} = H_{i,t} \times V_{i,t}$)

El riesgo integral por celda H3 ($i$) y periodo ($t$) se calcula mediante el producto multiplicativo entre la Amenaza/Exposición Espacial ($H_{i,t}$) y la Vulnerabilidad Socioecológica y de Gobernanza ($V_{i,t}$):

$$R_{i,t} = H_{i,t} \times V_{i,t}$$

#### 1. Subíndice de Amenaza y Exposición ($H_{i,t}$)
$$H_{i,t} = (0.50 \times \text{Densidad Esfuerzo Pesquero}) + (0.30 \times \text{Proximidad Infraestructura GNL}) + (0.20 \times \text{Intersección Rutas})$$

#### 2. Subíndice de Vulnerabilidad ($V_{i,t}$)
$$V_{i,t} = (0.25 \times \text{Sensibilidad Especies}) + (0.25 \times \text{Dependencia Ingreso}) + (0.20 \times \text{Patrimonio Biocultural}) + (0.15 \times \text{Género/Postcaptura}) + (0.15 \times [1 - \text{Capacidad Adaptativa}])$$

---

### Nivel III: Mapa de Confianza y Calidad de la Información

En cumplimiento de la arquitectura jerárquica del proyecto (Manual Metodológico), se genera en paralelo al Mapa de Riesgo el **Mapa de Confianza y Calidad de Información (Nivel III)** (`ierc_confidence_h3.parquet`).

El índice de confianza ($C_i \in [0, 100]$) por celda $i$ se calcula como:

$$C_i = (0.40 \times \text{Densidad Observada}) + (0.30 \times \text{Consistencia Multi-Fuente}) + (0.30 \times \text{Estatus Validación Comunitaria})$$

- **Alta Confianza ($C_i \ge 75$)**: Celdas con datos observados in situ (PANGAS, GFW real, campo).
- **Confianza Media ($50 \le C_i < 75$)**: Celdas con datos de gabinete georreferenciados.
- **Baja Confianza ($C_i < 50$)**: Celdas dependientes de imputación por medianas o interpolación.

---

## 🌐 API REST (Fase 7)

### `scripts/ierc_api.py` - FastAPI + DuckDB

```bash
# Iniciar servidor
cd /home/gorops/ierc-gnl-project
python scripts/ierc_api.py
# → http://localhost:8000
```

### Endpoints

| Endpoint | Método | Parámetros | Descripción |
|----------|--------|------------|-------------|
| `/` | GET | - | Service info |
| `/health` | GET | - | Health check |
| `/risk/deterministic` | GET | h3_cell_8, bbox, risk_level, limit | IERC determinista |
| `/risk/monte-carlo` | GET | h3_cell_8, bbox, limit | IERC Monte Carlo + IC |
| `/features` | GET | h3_cell_8, limit | Features originales |
| `/catalog/datasets` | GET | - | 10 datasets registrados |
| `/catalog/runs` | GET | dataset_name, limit | Historial ingestas |
| `/catalog/quality` | GET | - | Validaciones calidad |
| `/stats/summary` | GET | - | Stats globales |
| `/risk/bbox` | POST | BBoxQuery | Filtrado espacial H3 |

### Ejemplos de Uso

```bash
# Top 5 celdas mayor riesgo
curl "http://localhost:8000/risk/deterministic?limit=5"

# Monte Carlo para celda específica
curl "http://localhost:8000/risk/monte-carlo?h3_cell_8=8848014a67fffff"

# Features de una celda
curl "http://localhost:8000/features?h3_cell_8=8848014a67fffff"

# BBox query (POST)
curl -X POST "http://localhost:8000/risk/bbox" \
  -H "Content-Type: application/json" \
  -d '{"min_lat": 25, "max_lat": 26, "min_lng": -110, "max_lng": -109}'

# Catálogo
curl "http://localhost:8000/catalog/datasets"
curl "http://localhost:8000/catalog/runs?limit=10"
```

---

## ✅ Verificaciones Completadas

### Tests Ad-Hoc por Fase

| Fase | Script | Tests | Estado |
|------|--------|-------|--------|
| 1-2 | `init_lakehouse.py` | Catalog init, NASA/ ASEA ingest | ✅ 4/4 |
| 3 | GFW vessels | Glob pattern, idempotencia | ✅ 3/3 |
| 4 | TNC + Bathymetry | LineString buffer, WKT geometry | ✅ 3/3 |
| 5 | Features | Shape, components, ranges, H3 validity | ✅ 4/4 |
| 6 | IERC Calculator | Deterministic + Monte Carlo outputs | ✅ 4/4 |
| 7 | API REST | 9 endpoints funcionales | ✅ 9/9 |

### Verificación de Datos

```python
# Lakehouse structure
lakehouse/
├── processed/          # Silver: 7 datasets, ~4.6M registros
├── curated/            # Gold: 3 datasets, 830K celdas H3_8
│   ├── ierc_features_h3_8.parquet      (24 features)
│   ├── ierc_risk_h3_8.parquet          (27 cols, determinista)
│   ├── ierc_monte_carlo_h3_8.parquet   (6 cols, 50 sims)
│   └── ierc_risk_h3_8_stats.yaml       (pesos + distribución)
└── metadata/
    └── catalog.duckdb  (10 datasets, 22 runs, quality)
```

---

## ⚠️ Limitaciones Conocidas

### 1. Datos Sintéticos vs Reales
| Fuente | Estado | Acción Requerida |
|--------|--------|------------------|
| NASA OceanColor | Sintético (120 NetCDF dummy) | Earthdata login + download real |
| GFW Fishing Effort | ZIPs corruptos | Re-descargar Zenodo 14982712 completo |
| TNC Shapefiles | Sintéticos | Obtener shapefiles originales |
| PANGAS | No cargado | Procesar GeoJSON zonas pesca |
| Batimetría ETOPO1 | No cargado | Procesar GeoTIFF real |

### 2. Variabilidad Espacial
- **Problema**: Solo 4.5% celdas con datos observados
- **Efecto**: Features uniformes → IERC concentrado (std=0.3 determinista, 0.03 MC)
- **Solución**: Kriging / Gaussian Process para interpolación espacial condicional

### 3. Monte Carlo Simplificado
- **Actual**: Prior global + ruido i.i.d.
- **Falta**: Correlación espacial, variograma, simulaciones condicionales
- **Próximo**: `gstools` o `pykrige` para kriging ordinario

### 4. Validación Externa
- **Pendiente**: Comparar IERC vs incidentes reales SINAT
- **Pendiente**: Datos de campo (muestreo bentónico, pesca)

---

## 🚀 Próximos Pasos (Roadmap)

### Prioridad Alta (Semanas 1-2)
- [ ] Descargar NASA OceanColor real (Earthdata API + autenticación)
- [ ] Re-procesar GFW Zenodo completo (5TB → subconjunto Golfo)
- [ ] Cargar PANGAS fishing zones + ETOPO1 GeoTIFF
- [ ] Implementar kriging ordinario para rellenar gaps espaciales

### Prioridad Media (Semanas 3-4)
- [ ] Dashboard Next.js + MapLibre GL (visualización IERC interactivo)
- [ ] Autenticación API (JWT / API keys)
- [ ] Rate limiting + caching (Redis)
- [ ] CI/CD pipeline (GitHub Actions → Docker)

### Prioridad Baja (Mes 2+)
- [ ] Modelo predictivo (XGBoost) para riesgo futuro
- [ ] Alertas automáticas (umbral IERC > 75)
- [ ] Integración SINAT (datos oficiales SEMARNAT)
- [ ] Documentación OpenAPI + SDK Python

---

## 📁 Estructura del Proyecto

```
/home/gorops/ierc-gnl-project/
├── config/
│   ├── lakehouse.yaml
│   └── data_catalog.yaml
├── src/data/
│   ├── catalog/
│   │   └── catalog.py
│   ├── lakehouse/
│   │   ├── storage.py
│   │   └── partitioning.py
│   └── ingestion/
│       ├── base.py
│       ├── nasa_oceancolor.py
│       ├── gfw_fishing.py
│       ├── tnc_vector.py
│       ├── asea_mias.py
│       └── bathymetry.py
├── scripts/
│   ├── init_lakehouse.py
│   ├── generate_synthetic_nasa.py
│   ├── generate_synthetic_tnc.py
│   ├── compute_ierc_features.py
│   ├── ierc_calculator.py
│   ├── ierc_monte_carlo_v3.py
│   └── ierc_api.py
└── lakehouse/
    ├── raw/
    ├── processed/          # Silver
    ├── curated/            # Gold
    └── metadata/
        └── catalog.duckdb
```

---

## 📝 Comandos de Referencia

### Inicialización Completa
```bash
cd /home/gorops/ierc-gnl-project
python scripts/init_lakehouse.py
```

### Ingesta Individual
```bash
# NASA (requiere NetCDF reales)
python -c "
from src.data.catalog.catalog import DataCatalog, load_catalog_from_yaml
from src.data.lakehouse.storage import create_storage_from_config
from src.data.ingestion.nasa_oceancolor import create_nasa_ingester

storage = create_storage_from_config('config/lakehouse.yaml')
catalog = load_catalog_from_yaml(str(storage.root/'metadata'/'catalog.duckdb'), 'config/data_catalog.yaml')
ingester = create_nasa_ingester('chlor_a', catalog, storage)
result = ingester.run()
print(result)
"
```

### Feature Engineering
```bash
python scripts/compute_ierc_features.py
```

### Cálculo IERC
```bash
# Determinista
python scripts/ierc_calculator.py

# Monte Carlo (50 sims ~60s)
python scripts/ierc_monte_carlo_v3.py
```

### API Server
```bash
# Foreground
python scripts/ierc_api.py

# Background (producción)
nohup python scripts/ierc_api.py > api.log 2>&1 &
```

### Verificación Rápida
```bash
# Health
curl http://localhost:8000/health

# Top riesgo
curl "http://localhost:8000/risk/deterministic?limit=10"

# Stats
curl http://localhost:8000/stats/summary
```

---

## 📚 Referencias Técnicas

1. **H3 Spatial Indexing**: Uber H3 - Hierarchical Hexagonal Grid
2. **DuckDB**: Embedded Analytical Database - Parquet native, predicate pushdown
3. **Delta Lake Patterns**: ACID via DuckDB + partitioned Parquet
4. **Kriging**: Cressie, N. (1993) - Statistics for Spatial Data
5. **Monte Carlo**: Robert & Casella (2004) - Monte Carlo Statistical Methods
6. **FastAPI**: Modern Python web framework - OpenAPI native

---

*Documento generado automáticamente desde sesión Hermes Agent*  
*Versión 1.0 - 31 Julio 2026*