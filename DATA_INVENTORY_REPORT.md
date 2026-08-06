# Inventario de Datos del Proyecto IERC-GNL
## Reporte de Auditoría de Capas y Cadena de Ingesta

**Autor:** Enrique Gorosave Meza  
**Rol:** Analista de Datos GIS  
**Organización:** Causa Natura Center  
**Fecha:** 2026-08-04  
**Versión:** 1.0

---

## 1. Resumen Ejecutivo

Este documento presenta el inventario completo de los datos disponibles en el Lakehouse del proyecto **IERC-GNL** (Índice de Riesgo Ecosistémico - Golfo de California / Gas Natural Licuado), desarrollado para **Causa Natura Center**. El sistema implementa una arquitectura de **Medallion Architecture** (Bronze → Silver → Gold) con particionamiento H3 multi-resolución para análisis espacial del Golfo de California.

### Métricas Globales
- **Total datasets Silver:** 12 particiones de datos fuente
- **Total datasets Gold:** 6 productos analíticos derivados
- **Cobertura espacial:** Golfo de California (bbox: 22.5°–32.0° N, -115.0°–-108.0° W)
- **Resolución H3 base:** Nivel 8 (~0.74 km² por celda)
- **Período temporal:** 2020–2024 (series mensuales NASA) + datos estáticos

---

## 2. Arquitectura del Lakehouse

```
lakehouse/
├── bronze/          # Raw data (no versionado en este reporte)
├── processed/       # SILVER - Datos limpios, particionados, estandarizados
│   ├── gfw/                    # Global Fishing Watch
│   │   ├── vessels/            # Buques mexicanos (API v3)
│   │   └── fishing_effort_h3/  # Esfuerzo pesquero H3 + año/mes
│   ├── nasa/                   # NASA OceanColor (NetCDF → H3)
│   │   ├── chlor_a/            # Clorofila-a mensual 2020-2024
│   │   └── sst/                # Temperatura superficial mensual 2020-2024
│   ├── pangas_fishing_zones/   # Zonas pesqueras artesanales PANGAS
│   ├── tnc/                    # The Nature Conservancy
│   │   ├── bajos_marinos_h3/   # Bajos marinos → H3 grid
│   │   └── arrecifes_coral_negro_h3/  # Arrecifes coral negro → H3 grid
│   ├── bathymetry_gebco/       # Batimetría GEBCO (res 8, 9)
│   └── asea/mias_enriched/     # Proyectos GNL ASEA/CENAGAS (H3-10)
└── curated/         # GOLD - Productos analíticos listos para dashboard
    ├── ierc_risk_h3_8.parquet           # Índice de riesgo principal
    ├── ierc_features_h3_8.parquet       # Features para modelado
    ├── ierc_monte_carlo_h3_8.parquet    # Simulación Monte Carlo
    ├── ierc_features_adaptive_h3.parquet # Features adaptativos multi-res
    ├── ierc_risk_multiplicative.parquet  # Riesgo multiplicativo
    └── ierc_confidence_h3.parquet        # Scores de confianza
```

---

## 3. Inventario Detallado por Capa SILVER

### 3.1 Global Fishing Watch (GFW)

| Dataset | Filas | Columnas | Particionamiento | Fuente |
|---------|-------|----------|------------------|--------|
| `gfw/vessels` | 22 | 8 | Ninguno (tabla plana) | API v3 `/vessels/search` |
| `gfw/fishing_effort_h3` | 1 (h3_cell=8848055949fffff) | 6 | `year/month/h3_cell` | API v3 `/events` |

**Columnas GFW Vessels:** `year, month, time_partition, mmsi, flag, vessel_name, imo, callsign`  
**Columnas GFW Fishing Effort:** `time_partition, fishing_hours, mmsi, flag, lat, lon` (+ h3_cell implícito en path)

**Nota:** El token GFW API permite consultas en tiempo real. Los datos de vessels usan endpoint `/vessels/search` con query "Mexico" y dataset `public-global-vessel-identity:latest`. El esfuerzo pesquero usa `/events` con `public-global-fishing-events:latest`.

### 3.2 NASA OceanColor (MODIS-Aqua L3SMI)

| Variable | Período | Meses | Filas/mes | Columnas | Tamaño total |
|----------|---------|-------|-----------|----------|--------------|
| Chlorofila-a (`chlor_a`) | 2020–2024 | 60 | 38,304 | 8 | ~51 MB |
| SST (`sst`) | 2020–2024 | 60 | 38,304 | 8 | ~51 MB |

**Columnas:** `time, time_partition, h3_cell, {variable}, {variable}_std, {variable}_count, lat_mean, lon_mean`  
**Particionamiento:** `year=YYYY/month=MM/`  
**Procesamiento:** NetCDF → recorte bbox Golfo → agregación H3-8 (mean, std, count)

### 3.3 PANGAS - Zonas Pesqueras Artesanales

| Métrica | Valor |
|---------|-------|
| Filas | 263,796 |
| Columnas | 26 |
| Tamaño | 12.99 MB |
| Particionamiento | Tabla plana (H3-8 embebido) |

**Columnas clave:** `h3_cell, spp_code, sitio_code, sitio_nomb, arte, uid_espaciotemporal, riqueza_relativa_mean, h3_geometry_wkt`  
**Estándar:** `uid_espaciotemporal` = `{comunidad}-ARTESANAL-{especie}-{arte}-{sitio}-ANUAL-RUTA_PRINCIPAL`  
**Fuente:** GeoJSON `ZPesca_PANGAS_wgs84.geojson` + `Riqueza_Relativa_wgs84.geojson`

### 3.4 TNC - Capas Vectoriales (The Nature Conservancy)

| Capa | Filas | Columnas | Tipo | Resolución H3 |
|------|-------|----------|------|---------------|
| Bajos Marinos | 2,440 | 14 | Polígonos | H3-8 |
| Arrecifes Coral Negro | 105 | 13 | Polígonos | H3-8 |

**Columnas comunes:** `h3_cell, tnc_layer, source_file, area_fraction, area_km2, nombre, tipo, h3_geometry_wkt`  
**Particionamiento:** `tnc_layer` + `h3_cell` (patrón `h3_8={h3_cell}/`)  
**Procesamiento:** Shapefile/ZIP → GeoPandas → `vector_to_h3_grid(area_weight=True)`

### 3.5 Batimetría GEBCO

| Resolución | Filas | Columnas | Tamaño |
|------------|-------|----------|--------|
| H3-8 | 7,431 | 10 | 0.06 MB |
| H3-9 | 52,567 | 10 | 0.33 MB |

**Columnas:** `h3_cell, bathymetry_mean, bathymetry_min, bathymetry_max, bathymetry_count, area_total, year, month, time_partition, source`  
**Fuente:** `GEBCO_Batimetria_Golfo.gpkg` (contornos vectoriales)  
**Procesamiento:** Vector → H3 grid con pesos de área

### 3.6 ASEA - Proyectos GNL / MIA

| Métrica | Valor |
|---------|-------|
| Proyectos únicos | 11 |
| Particiones H3-10 | 12 celdas |
| Tipos de proyecto | Terminal GNL, Gasoducto, Planta Licuefacción, Estación Compresión, Gasoducto Distribución |

**Columnas:** `proyecto_id, nombre, estado, tipo_proyecto, fuente, lat, lon, estatus, source_file, source_type, ingestion_timestamp, year, month, time_partition`  
**Particionamiento:** `h3_cell_10, year, month` + `tipo_proyecto`  
**Fuentes:** `gnl_proyectos_consolidados.csv` + `asea_mias_alto_golfo.csv`  
**Estandarización:** `estatus` normalizado (En_operación, En_construcción, En_evaluación, etc.)

---

## 4. Capa GOLD - Productos Analíticos

### 4.1 `ierc_risk_h3_8.parquet` — Índice Principal
- **Filas:** 830,869 celdas H3-8
- **Columnas:** 27
- **Tamaño:** 6.77 MB

**Variables de riesgo:**
- **Oceanográficas:** `chlor_a_mean, chlor_a_std, chlor_a_max, chlor_a_trend, sst_mean, sst_std, sst_max, sst_min`
- **Batimétricas:** `depth_mean, depth_min, depth_max, depth_range, depth_slope`
- **Ecosistémicas (TNC):** `tnc_bajos_count, tnc_bajos_area_frac, tnc_bajos_area_km2, tnc_coral_count, tnc_coral_area_frac, tnc_coral_area_km2`
- **Antropogénicas (ASEA):** `asea_count, asea_terminal_gnl, asea_gasoducto, asea_operando`
- **Score final:** `ierc_score, risk_level, ierc_percentile`

### 4.2 `ierc_features_h3_8.parquet` — Features para ML
- **Filas:** 830,869 | **Columnas:** 24 | **Tamaño:** 5.85 MB
- Mismas features que `ierc_risk` sin columnas de score final

### 4.3 `ierc_monte_carlo_h3_8.parquet` — Simulación Monte Carlo
- **Filas:** 830,869 | **Columnas:** 6 | **Tamaño:** 33.31 MB
- **Columnas:** `h3_cell_8, ierc_mean, ierc_std, ierc_p05, ierc_p95, ierc_median`
- **Uso:** Intervalos de confianza, análisis de incertidumbre

### 4.4 `ierc_features_adaptive_h3.parquet` — Multi-resolución Adaptativa
- **Filas:** 830,869 | **Columnas:** 22 | **Tamaño:** 4.94 MB
- **Resoluciones:** H3-8 base + features agregados de H3-9/10 donde aplica
- **Features socioeconómicos PANGAS:** `pangas_densidad_esfuerzo, pangas_riqueza_mean, dependencia_ingreso, patrimonio_biocultural, genero_postcaptura, capacidad_adaptativa`

### 4.5 `ierc_risk_multiplicative.parquet` — Modelo Multiplicativo
- **Filas:** 833,032 | **Columnas:** 26 | **Tamaño:** 4.96 MB
- **Componentes:** `amenaza_score, vulnerabilidad_score, ierc_score, nivel_riesgo`
- **Metodología:** Riesgo = Amenaza × Vulnerabilidad (framework IPCC)

### 4.6 `ierc_confidence_h3.parquet` — Confianza Espacial
- **Filas:** 833,032 | **Columnas:** 4 | **Tamaño:** 3.36 MB
- **Columnas:** `h3_cell, confidence_score, nivel_confianza, resolution`
- **Uso:** Filtrado de celdas con datos insuficientes en dashboard

---

## 5. Capas Visibles en el Dashboard

### 5.1 Capas Base (Toggleables)
| Capa | Fuente SILVER | Visualización | Filtros Disponibles |
|------|---------------|---------------|---------------------|
| **Esfuerzo Pesquero GFW** | `gfw/fishing_effort_h3` | Heatmap H3 temporal | Año, Mes, Tipo arte, Bandera |
| **Buques Mexicanos** | `gfw/vessels` | Puntos + metadata popup | Bandera, Tipo buque, IMO/MMSI |
| **Clorofila-a** | `nasa/chlor_a` | Raster temporal mensual | Año, Mes, Percentiles |
| **SST** | `nasa/sst` | Raster temporal mensual | Año, Mes, Anomalías |
| **Batimetría** | `bathymetry_gebco` | Contornos + hillshade | Resolución 8/9 |
| **Bajos Marinos** | `tnc/bajos_marinos_h3` | Polígonos H3 (area_fraction) | Tipo, Profundidad |
| **Arrecifes Coral Negro** | `tnc/arrecifes_coral_negro_h3` | Polígonos H3 | Área km² |
| **PANGAS Zonas** | `pangas_fishing_zones` | Hexágonos H3 + riqueza | Especie, Arte, Comunidad |
| **Proyectos GNL** | `asea/mias_enriched` | Puntos + buffers H3-10 | Tipo, Estatus, Estado |

### 5.2 Capas Derivadas (Análisis)
| Capa | Fuente GOLD | Descripción |
|------|-------------|-------------|
| **IERC Score** | `ierc_risk_h3_8.ierc_score` | Índice integrado 0–1 |
| **Nivel de Riesgo** | `ierc_risk_h3_8.risk_level` | Categorical: Muy Bajo / Bajo / Medio / Alto / Muy Alto |
| **Amenaza** | `ierc_risk_multiplicative.amenaza_score` | Componente antropogénico |
| **Vulnerabilidad** | `ierc_risk_multiplicative.vulnerabilidad_score` | Componente ecosistémico |
| **Confianza** | `ierc_confidence_h3.confidence_score` | 0–1, filtro calidad datos |

### 5.3 Controles de Dashboard Recomendados
- **Time Slider:** 2020–2024 (mensual para NASA, tiempo real para GFW)
- **H3 Resolution Selector:** 8 / 9 / Adaptive
- **Risk Threshold:** Slider percentil (p05–p95 desde Monte Carlo)
- **Layer Opacity:** Control individual por capa
- **Spatial Filter:** Bbox draw / Estado / Municipio / Área marina

---

## 6. Cadena de Ingesta y Auditoría

### 6.1 Pipeline de Ingesta (src/data/ingestion/)

```
┌─────────────────────────────────────────────────────────────────┐
│                        FACTORY LAYER                            │
│  create_gfw_ingester()  create_nasa_ingester()  create_tnc_*() │
│  create_asea_ingester()  create_bathymetry_ingester()           │
│  create_pangas_ingester()                                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BASE INGESTER                              │
│  BaseIngester.run() → extract() → transform() → load()         │
│  + Catalog tracking (start_ingestion_run / finish_ingestion_run)│
│  + Validación calidad (validate_data)                           │
│  + Particionamiento H3 + temporal                               │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
       ┌──────────┐    ┌──────────┐    ┌──────────┐
       │   GFW    │    │  NASA    │    │   TNC    │
       │Fishing   │    │OceanColor│    │ Vector   │
       └──────────┘    └──────────┘    └──────────┘
              │               │               │
              ▼               ▼               ▼
       ┌──────────┐    ┌──────────┐    ┌──────────┐
       │  ASEA    │    │Bathymetry│    │  PANGAS  │
       │  MIA     │    │  GEBCO   │    │ Vector   │
       └──────────┘    └──────────┘    └──────────┘
```

### 6.2 Detalle por Ingester

| Ingester | Clase | Config Dataset | Particionamiento | Validaciones |
|----------|-------|----------------|------------------|--------------|
| **GFW Fishing** | `GFWFishingEffortIngester` | `gfw_fishing_effort` | `h3_cell, year, month` | bbox Golfo, H3 válido, fishing_hours numérico |
| **GFW Vessels** | `GFWFishingEffortIngester` | `gfw_vessels` | Ninguno (tabla) | MMSI string, flag presente |
| **NASA Chlor_a** | `NASAOceanColorIngester` | `nasa_chlor_a` | `year, month` | Valores no fill_value, H3 en bbox |
| **NASA SST** | `NASAOceanColorIngester` | `nasa_sst` | `year, month` | Valores no fill_value, H3 en bbox |
| **TNC Bajos** | `TNCVectorIngester` | `tnc_bajos_marinos` | `tnc_layer` | Geometría válida, CRS EPSG:4326 |
| **TNC Coral** | `TNCVectorIngester` | `tnc_arrecifes_coral_negro` | `tnc_layer` | Geometría válida, CRS EPSG:4326 |
| **Bathymetry** | `BathymetryIngester` | `bathymetry_gebco` | `resolution` | Stats numéricas, H3 coverage |
| **ASEA MIA** | `ASEAMIASIngester` | `asea_mias` | `h3_cell_10, year, month` | Estatus normalizado, coords válidas |
| **PANGAS** | `PangasVectorIngester` | `pangas_fishing_zones` | Ninguno (H3 embebido) | `uid_espaciotemporal` formato |

### 6.3 Catálogo de Auditoría (DataCatalog)

Cada ejecución de ingesta genera registro en `lakehouse/metadata/ingestion_runs.jsonl`:

```json
{
  "run_id": "gfw_fishing_effort_20260805_023139_f74f5f5d",
  "dataset_name": "gfw_fishing_effort",
  "started_at": "2026-08-05T02:31:39.485",
  "finished_at": "2026-08-05T02:31:42.846",
  "status": "success",
  "input_path": null,
  "records_processed": 1,
  "records_inserted": 1,
  "records_updated": 0,
  "records_failed": 0,
  "quality_results": {"total_batches": 1, "warnings_count": 0},
  "error_message": null
}
```

**Campos de auditoría:**
- `run_id`: UUID único con timestamp
- `status`: success / failed / partial
- `records_*`: Métricas de volumen
- `quality_results`: Warnings de validación (H3 nulos, fuera de bbox, duplicados)
- `error_message`: Stack trace si falla

### 6.4 Validaciones de Calidad Automáticas

```python
# En BaseIngester.validate_data()
- total_rows: conteo
- null_counts: por columna
- duplicate_rows: duplicados exactos
- h3_cells_unique: cardinalidad espacial
- time_partitions: particiones temporales
- H3 nulos → FAIL
- Fuera de bbox Golfo → WARNING
- time_partition nulos → WARNING
```

### 6.5 Trazabilidad de Datos (Lineage)

| Capa Gold | Fuentes Silver | Transformación |
|-----------|----------------|----------------|
| `ierc_risk_h3_8` | NASA (chlor_a, sst), Bathymetry, TNC, ASEA | Join espacial H3-8 + feature engineering + scoring |
| `ierc_features_adaptive_h3` | Silver + PANGAS | Multi-resolución H3 + features socioeconómicos |
| `ierc_monte_carlo_h3_8` | `ierc_features_h3_8` | Simulación N=1000 iteraciones por celda |
| `ierc_risk_multiplicative` | Features adaptativas | Amenaza × Vulnerabilidad (IPCC) |
| `ierc_confidence_h3` | Todas Silver | Completitud + consistencia temporal + densidad muestral |

---

## 7. Comandos de Operación

### 7.1 Ejecutar Ingesta Individual
```bash
# Con token GFW API
export GFW_API_TOKEN="<token>"
python -c "
from scripts.init_lakehouse import run_gfw_ingestion, run_nasa_ingestion, run_tnc_ingestion, run_asea_ingestion
from src.data.catalog.catalog import DataCatalog, load_catalog_from_yaml
from src.data.lakehouse.storage import create_storage_from_config
from config import get_config_dir

storage = create_storage_from_config(str(get_config_dir() / 'lakehouse.yaml'))
catalog_dir = storage.root / 'metadata'
catalog = load_catalog_from_yaml(str(catalog_dir), str(get_config_dir() / 'data_catalog.yaml'))

run_gfw_ingestion(catalog, storage, 'fishing_effort')
run_gfw_ingestion(catalog, storage, 'vessels')
run_nasa_ingestion(catalog, storage, 'chlor_a')
run_tnc_ingestion(catalog, storage)
run_asea_ingestion(catalog, storage)
"
```

### 7.2 Verificar Estado del Catálogo
```bash
python -c "
from src.data.catalog.catalog import DataCatalog, load_catalog_from_yaml
from src.data.lakehouse.storage import create_storage_from_config
from config import get_config_dir

storage = create_storage_from_config(str(get_config_dir() / 'lakehouse.yaml'))
catalog = load_catalog_from_yaml(str(storage.root / 'metadata'), str(get_config_dir() / 'data_catalog.yaml'))

for ds in catalog.list_datasets():
    print(f'{ds.name} [{ds.priority}] - {ds.format} - {ds.source_type}')
"
```

### 7.3 Consultar Runs de Auditoría
```bash
python -c "
from src.data.catalog.catalog import DataCatalog, load_catalog_from_yaml
from src.data.lakehouse.storage import create_storage_from_config
from config import get_config_dir

storage = create_storage_from_config(str(get_config_dir() / 'lakehouse.yaml'))
catalog = load_catalog_from_yaml(str(storage.root / 'metadata'), str(get_config_dir() / 'data_catalog.yaml'))

runs = catalog.get_ingestion_runs('gfw_fishing_effort', limit=5)
for r in runs:
    print(f'{r.run_id} | {r.status} | {r.records_inserted} rows | {r.finished_at}')
"
```

---

## 8. Próximos Pasos y Mejoras

| Área | Acción | Prioridad |
|------|--------|-----------|
| **NASA** | Instalar `netCDF4` para habilitar ingesta chlor_a/SST | Alta |
| **GFW** | Programar ingesta diaria vía cron (últimos 30 días) | Media |
| **PANGAS** | Integrar capas de buceo/redes/chinchorro/trampa | Media |
| **ASEA** | Conectar fuente oficial CENAGAS/SENER API | Alta |
| **Gold** | Refrescar features adaptativas mensualmente | Media |
| **Dashboard** | Implementar filtro de confianza (confidence_score > 0.7) | Alta |

---

## 9. Referencias Técnicas

- **H3 Library:** Uber H3 v4.x (resolución 8–10)
- **Catálogo:** JSONL local (`lakehouse/metadata/datasets.json` + `ingestion_runs.jsonl`)
- **Storage:** Parquet + ZSTD, particionado Hive-style
- **Config:** `config/lakehouse.yaml`, `config/data_catalog.yaml`
- **Tests:** `pytest tests/unit/test_storage_catalog.py` (4 passed)

---

*Fin del reporte — Generado automáticamente desde inventario live del Lakehouse IERC-GNL*