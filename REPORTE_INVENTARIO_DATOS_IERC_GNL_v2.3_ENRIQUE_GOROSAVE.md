# REPORTE INVENTARIO DETALLADO DE DATOS IERC-GNL
## Índice Espacial de Riesgo Socioeconómico para Comunidades (GNL)
### Causa Natura Center — POA 2026-2028

---

**Autor:** Enrique Gorosave Meza (Analista de Datos y SIG)  
**Fecha:** 2026-08-07  
**Versión:** v2.3  
**Organización:** Causa Natura Center

---

## 1. RESUMEN EJECUTIVO

Este reporte presenta el inventario completo y actualizado de los datos, arquitectura y componentes del proyecto **IERC-GNL** (Índice Espacial de Riesgo Socioeconómico para Comunidades ante proyectos de Gas Natural Licuado en el Golfo de California). El proyecto forma parte del **Plan Operativo Anual (POA 2026-2028)** de **Causa Natura Center**.

### 1.1 Métricas Clave del Proyecto (verificadas 2026-08-07)

| Métrica | Valor |
|---------|-------|
| **Arquitectura** | Lakehouse Medallion (Bronze/Silver/Gold) |
| **Datasets SILVER** | 14 fuentes procesadas (165 archivos Parquet) |
| **Productos GOLD** | 13 datasets analíticos (7 IERC + 6 gas/ambiental) |
| **Archivos .meta.json** | 14 (proveniencia: source, dataset, download_date, source_url, row_count) |
| **Capas Dashboard** | 15 capas vectoriales interactivas (Next.js 16) |
| **Archivos GeoJSON dashboard** | 21 archivos (5.9 MB a 29 MB c/u) |
| **Ductos CNIH/SENER** | 24 tramos LineString (6,399 km) + 2 ANP Polygons |
| **Scripts Python** | 44 scripts operacionales |
| **Tests Unitarios** | 45 tests passing (storage, catalog, H3, IERC, RAI, spatial, Monte Carlo, E2E) |
| **Pipeline CI/CD** | 5 jobs automatizados (test, lint, verify-cdc, dashboard-build, summary) |
| **Total filas SILVER** | ~6,034,848 (sin NASA satelital); NASA agrega 4,596,480 |
| **Total filas GOLD IERC** | 830,869 por producto (6 productos) |

### 1.2 Equipo Técnico

- **Juan Carlos Barrera (JCB):** Consultor Senior / Especialista Pesquero y Socioambiental
- **Enrique Gorosave Meza (EG):** Analista de Datos y SIG

---

## 2. ARQUITECTURA DEL LAKEHOUSE (MEDALLION v2.0)

### 2.1 Capas del Lakehouse

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        LAKEHOUSE IERC-GNL                                │
├─────────────────┬─────────────────┬─────────────────────────────────────┤
│     BRONZE      │     SILVER      │               GOLD                  │
│   (raw/)        │  (processed/)   │            (curated/)              │
│ ─────────────   │ ─────────────   │ ─────────────────────────────────  │
│ Datos inmutables│ Limpio,         │ Listo para análisis/ML/            │
│ tal cual llegan │ enriquecido,    │ dashboard                          │
│                 │ particionado H3 │                                     │
└─────────────────┴─────────────────┴─────────────────────────────────────┘
```

### 2.2 Configuración Técnica

- **Formato tabular:** Parquet (compresión ZSTD nivel 3)
- **Formato espacial:** GeoParquet
- **Particionado espacial:** H3 Resolución 8 (~0.73 km² mar abierto), Res 10 costero (~0.015 km²)
- **Particionado temporal:** Mensual (columna `time_partition` formato YYYY-MM)
- **Catálogo:** JSONL en `lakehouse/metadata/catalog.json` + `runs.jsonl`
- **Proveniencia:** `.meta.json` por cada dataset Silver con campos: source, dataset, download_date, source_url, row_count, columns
- **CRS estándar:** EPSG:4326 (WGS84) para todos los GeoDataFrames

### 2.3 Bounding Box Golfo de California (EPSG:4326)
- **min_lat:** 22.5 | **max_lat:** 32.0
- **min_lon:** -115.0 | **max_lon:** -108.0

---

## 3. INVENTARIO DATASETS SILVER (14 Fuentes, 165 Parquets)

### 3.1 Tabla Maestra SILVER — Conteos Verificados

| # | Dataset | Fuente | Filas | Columnas | Tamaño (bytes) | Particionado | .meta.json |
|---|---------|--------|-------|----------|----------------|--------------|------------|
| 1 | `cenegas_injection_capacity` | CENEGAS/SISTRANGAS | 103,596 | 10 | 654,930 | Plano | ✅ |
| 2 | `cenegas_extracciones` | CENEGAS/SISTRANGAS | 698,079 | 12 | 4,245,819 | Plano | ✅ |
| 3 | `cenegas_tarifas` | CENEGAS/SISTRANGAS | 378 | 7 | 8,585 | Plano | ✅ |
| 4 | `sener_prontuario` | SENER | 16 | 7 | 5,095 | Plano | ✅ |
| 5 | `sener_volumen_almacenamiento` | SENER | 186 | 6 | 7,828 | Plano | ✅ |
| 6 | `profepa_inspeccion` | PROFEPA | 51 | 3 | 2,916 | Plano | ✅ |
| 7 | `semarnat_sitios_contaminados` | SEMARNAT | 481 | 6 | 9,385 | Plano | ✅ |
| 8 | `gobmx_registros_publicos` | datos.gob.mx | 1 | 9 | 7,715 | Plano | ✅ |
| 9 | `ecc_climabase_catalog` | ECC Climabase | 48 | 8 | 6,886 | Plano | ✅ |
| 10 | `ductos_cnih` | CNIH/SENER ArcGIS | 24 | 12+ | 35,242 | GeoParquet | ✅ |
| 11 | `anp_ramsar_cnih` | CNIH/SENER ArcGIS | 2 | 12+ | 25,059 | GeoParquet | ✅ |
| 12 | `capas_contextuales` | CNIH/SENER ArcGIS | 2 | 8+ | 14,704 | GeoParquet | ✅ |
| 13 | `gfw_fishing_effort_h3` | Global Fishing Watch | 11,652 | — | 18 particiones | year/month H3-8 | ❌ |
| 14 | `gfw_vessels` | Global Fishing Watch | — | — | 5,297 | Plano | ❌ |
| 15 | `nasa_chlor_a` | NASA OceanColor | 2,298,240 | — | 60 particiones | year/month H3-8 | ❌ |
| 16 | `nasa_sst` | NASA OceanColor | 2,298,240 | — | 60 particiones | year/month H3-8 | ❌ |
| 17 | `asea_mias_enriched` | ASEA/CENAGAS/SENER | 11 | — | 9 particiones | H3-10/tipo | ❌ |
| 18 | `bathymetry_gebco` | GEBCO 2024 | 59,998 | — | 2 particiones | resolution=8,9 | ❌ |
| 19 | `tnc_bajos_marinos` | TNC Conservation | — | — | 162,651 | H3-8 | ❌ |
| 20 | `tnc_arrecifes_coral_negro` | TNC Conservation | — | — | 17,696 | H3-8 | ❌ |
| 21 | `pangas_fishing_zones` | PANGAS | 263,796 | — | 12,986,386 | Plano | ❌ |

### 3.2 Detalle por Fuente de Datos

#### **CENEGAS/SISTRANGAS — Capacidad Histórica de Inyecciones/Extracciones**
- **Fuente:** datos.gob.mx (CENEGAS)
- **Inyecciones:** 103,596 registros, 29 puntos de inyección, fechas 01/01/2015–31/12/2024, unidad GJ
- **Extracciones:** 698,079 registros, puntos de extracción SISTRANGAS
- **Tarifas:** 378 registros por punto/zona tarifaria
- **Correcciones aplicadas:** mojibake (`importaciën` → `importación`, `Nuevo Leën` → `Nuevo León`, `Quer?Taro` → `Querétaro`)
- **Script:** `scripts/cenegas/clean_cenegas.py`, `scripts/cenegas/harvest_extracciones.py`, `scripts/cenegas/clean_tarifas.py`

#### **SENER — Prontuario y Volumen de Almacenamiento**
- **Prontuario:** 16 registros del prontuario de datos abiertos SENER
- **Volumen de almacenamiento:** 186 registros mensuales de capacidad de almacenamiento de gas natural
- **Script:** `scripts/sener/clean_prontuario.py`, `scripts/sener/clean_volumen_almacenamiento.py`

#### **PROFEPA — Acciones de Inspección**
- **Fuente:** datos.gob.mx (PROFEPA)
- **Registros:** 51 acciones de inspección IAO/ZOFEMAT
- **Script:** `scripts/profepa/clean_acciones_inspeccion.py`

#### **SEMARNAT — Sitios Contaminados**
- **Fuente:** datos.gob.mx (SEMARNAT)
- **Registros:** 481 sitios contaminados registrados
- **Script:** `scripts/semarnat/clean_sitios_contaminados.py`

#### **datos.gob.mx — Registros Públicos Oficiales**
- **Fuente:** datos.gob.mx
- **Registros:** 1 registro (catálogo de registros públicos oficiales)
- **Script:** `scripts/gobmx/clean_registros_publicos.py`

#### **ECC Climabase — Climatología Histórica**
- **Fuente:** ECC Climabase (GeoTIFFs)
- ** Cobertura:** 48 GeoTIFFs — precipitación (mm), tmax/tmed/tmin (°C) × 12 meses (1950-2000)
- **Catálogo:** 48 registros indexando ruta, variable, mes, tamaño de archivo
- **Raw:** 131 archivos en `data/raw/ECC_Climabase/`
- **Script:** `scripts/ecc_climabase/catalog_ecc.py`

#### **CNIH/SENER — Ductos de Gas Natural (NUEVO 2026-08-07)**
- **Fuente:** ArcGIS FeatureServer CNIH/SENER (`services6.arcgis.com/th3TMn162i37A876/ArcGIS/rest/services/AppMote/FeatureServer`)
- **Capas descargadas:** 5 GeoJSON originales en `data/raw/gasoductos/`
  - Layer 11: Ductos NO integrados a SISTRANGAS (6 tramos)
  - Layer 13: Ductos integrados a SISTRANGAS (10 tramos)
  - Layer 14: Ducto Pacific Limited (1 tramo)
  - Layer 15: Poliductos de petrolíferos (5 tramos)
  - Layer 16: Capas contextuales (2 gasoductos + 2 ANP/Ramsar)
- **Salida Silver:** 24 LineStrings (6,399.3 km) + 2 Polygon ANP/Ramsar
- **Atributos:** nombre, proyecto, tipo, longitud_km, tramo, permiso, capacidad, zona_tarifaria, integrado_sistrangas, empresa, fuente_capa
- **CRS:** EPSG:4326
- **Script:** `scripts/gasoductos/clean_ductos_cnih.py` (149 líneas)

#### **Global Fishing Watch (v3.0)**
- **Fuente:** Zenodo record 14982712
- **Variables:** `fishing_hours`, `mmsi`, `gear_type` (trawlers, longliners, purse_seines, fixed_gear, other), `flag`
- **Registros Silver:** 11,652 filas en 18 particiones year/month H3-8 (2016, 2020)
- **Tamaño global:** 5.1 TB; ~100 GB para Golfo de California
- **Actualización:** Anual

#### **NASA OceanColor (MODIS-Aqua)**
- **Variables:** `chlor_a` (mg/m³, rango 0-100), `sst` (°C, rango -2 a 40)
- **Registros Silver:** 2,298,240 c/u (60 particiones mensuales 2020-2024)
- **Resolución nativa:** 4 km diaria; H3-8 mensual en Silver

#### **ASEA MIAs (Manifestaciones de Impacto Ambiental)**
- **Fuente:** ASEA + CENAGAS + SENER + Plan Quinquenal 2025-29
- **Registros Silver:** 11 (9 particiones H3-10 por tipo_proyecto)
- **CDC habilitado:** ✅ Exact-once deduplication (`_cdc_hash`)
- **CDC Key:** `proyecto_id`
- **H3 Resolution:** 10 (infraestructura puntual)

#### **Batimetría GEBCO 2024**
- **Fuente:** GEBCO 2024 (15 arc-sec ~450m)
- **Registros Silver:** 59,998 (resolutions 8 y 9)
- **Vectorizado:** Contornos batimétricos

#### **The Nature Conservancy (TNC)**
- **Capas:** `bajos_marinos` (montes submarinos), `arrecifes_coral_negro` (Antipatharia)
- **Formato:** Shapefile → H3 grid con `area_fraction`

#### **PANGAS**
- **Artes de pesca:** PANGAS, Buceo, Chinchorro, Redes, Redes Manta Camarón, Trampa, Riqueza Relativa
- **Registros Silver:** 263,796
- **Identificador único:** `uid_espaciotemporal = comunidad-actor-pesquería-arte-zona-temporada-ruta`

---

## 4. PRODUCTOS GOLD (13 Datasets Analíticos)

### 4.1 Gold IERC (6 Productos — 830,869 filas c/u)

| Dataset | Filas | Tamaño (bytes) | Descripción |
|---------|-------|----------------|-------------|
| `ierc_risk_h3_8.parquet` | 830,869 | 6,769,269 | Índice principal de riesgo (score 0-1, percentiles) |
| `ierc_features_h3_8.parquet` | 830,869 | 5,851,832 | Features para ML (sin scores finales) |
| `ierc_monte_carlo_h3_8.parquet` | 830,869 | 33,310,230 | Simulación N=1000 (mean, std, p05, p95, median) |
| `ierc_features_adaptive_h3.parquet` | 830,869 | 5,103,651 | Multi-resolución H3 + features socioeconómicos PANGAS |
| `ierc_risk_multiplicative.parquet` | 830,869 | 5,414,550 | Modelo multiplicativo Amenaza × Vulnerabilidad (IPCC) |
| `ierc_confidence_h3.parquet` | 830,869 | 3,354,319 | Scores de confianza espacial para filtrado dashboard |

### 4.2 Gold Gas Infrastructure (6 Productos)

| Dataset | Filas | Columnas | Tamaño (bytes) | Descripción |
|---------|-------|----------|----------------|-------------|
| `gas_infrastructure_master_inyecciones.parquet` | 33 | 14 | 11,278 | Master inyecciones por punto (total_gj, avg_daily_gj, first_date, last_date, days_active) |
| `gas_infrastructure_master_extracciones.parquet` | 225 | 15 | 21,501 | Master extracciones por punto (mismo esquema + columna adicional) |
| `gas_injection_yearly.parquet` | 315 | 8 | 10,905 | Agregación anual de inyecciones por punto |
| `gas_extraction_yearly.parquet` | 2,307 | 9 | 44,905 | Agregación anual de extracciones por punto |
| `tarifas_zone_summary.parquet` | 63 | 5 | 4,460 | Resumen tarifas por zona tarifaria |
| `gas_infrastructure_master.parquet` | — | — | 16,341 | Tabla master combinada (legacy) |

### 4.3 Gold Environmental Risk (1 Producto)

| Dataset | Filas | Columnas | Tamaño (bytes) | Descripción |
|---------|-------|----------|----------------|-------------|
| `env_risk_by_nodo.parquet` | 33 | 24 | 18,189 | Riesgo ambiental por nodo (join gas infra + sitios contaminados) |

### 4.4 Formulación Matemática IERC

**Modelo Aditivo (Oficial):**
```
IERC_total = (Amenaza × 0.20) + (Exposición × 0.20) + (Sensibilidad × 0.15) +
             (Dependencia × 0.15) + (Valor_Biocultural × 0.15) +
             ((1 - Capacidad_Adaptativa) × 0.15)
```

**Modelo Multiplicativo (IPCC):**
```
R_i,t = H_i,t × V_i,t

H_i,t = Amenaza y Exposición Espacial (densidad esfuerzo, proximidad GNL, conflicto rutas)
V_i,t = 0.25 Sensibilidad + 0.25 Dependencia + 0.20 Biocultural + 0.15 Género + 0.15 [1 - Cap.Adaptativa]
```

### 4.5 Componentes del Modelo (6 Ejes)

| Componente | Peso (Aditivo) | Descripción | Variables Fuente |
|------------|----------------|-------------|------------------|
| **Amenaza (H)** | 0.20 | Infraestructura GNL, ruido, rutas metaneros, ductos CNIH | ASEA MIA, GFW rutas, ductos CNIH |
| **Exposición (H)** | 0.20 | Esfuerzo pesquero VMS + pangas | GFW, PANGAS, ductos CNIH |
| **Sensibilidad (V)** | 0.15 | Especies IUCN, endemismo, hábitats críticos | TNC, NASA, OBIS |
| **Dependencia (V)** | 0.15 | Ingreso pesquero / ingreso total hogar | Encuestas PANGAS, INEGI |
| **Biocultural (V)** | 0.20 | Sitios sagrados Comca'ac, patrimonio | Trabajo de campo |
| **Capacidad Adaptativa (V)** | 0.15 | Gobernanza GAGE, diversificación, crédito | GAGE, encuestas |

---

## 5. CADENA DE INGESTA Y AUDITORÍA DE DATOS

### 5.1 Pipeline Overview

```
FUENTES EXTERNAS
  datos.gob.mx │ CENEGAS │ SENER │ PROFEPA │ SEMARNAT
  CNIH ArcGIS FeatureServer │ GFW Zenodo │ NASA OceanColor
  TNC Shapefiles │ PANGAS GDB │ ECC Climabase GeoTIFFs
        │
        ▼
  BRONZE (data/raw/)
  CSV, GeoJSON, Shapefile, GeoTIFF, netCDF — inmutable
        │
        ▼
  SCRIPTS DE LIMPIEZA (scripts/<fuente>/clean_*.py)
  • Corrección de encoding (mojibake)
  • Estandarización CRS → EPSG:4326
  • Validación de rangos y no-nulos
  • Cálculo de longitud_km (proyección métrica)
  • Deduplicación
        │
        ▼
  SILVER (lakehouse/processed/)
  Parquet/GeoParquet + .meta.json (proveniencia)
  Particionado H3 + temporal (year/month)
        │
        ▼
  GOLD (lakehouse/curated/)
  Joins H3-8 + scoring IERC + Monte Carlo
  Joins gas infra + env risk
  Lineage embebido en schema.lineage
        │
        ▼
  DASHBOARD (dashboard/public/data/)
  Exportación GeoJSON para visualización
```

### 5.2 Scripts de Ingesta por Fuente

| Fuente | Script | Entrada | Salida Silver | Filas |
|--------|--------|---------|---------------|-------|
| CENEGAS inyecciones | `scripts/cenegas/clean_cenegas.py` | `data/raw/cenegas/*.csv` | `cenegas/cenegas_injection_capacity.parquet` | 103,596 |
| CENEGAS extracciones | `scripts/cenegas/harvest_extracciones.py` | `data/raw/cenegas/*Extracciones*.csv` | `cenegas/extracciones_sistrangas.parquet` | 698,079 |
| CENEGAS tarifas | `scripts/cenegas/clean_tarifas.py` | `data/raw/cenegas/*tarifas*.csv` | `cenegas/tarifas_por_puntos.parquet` | 378 |
| SENER prontuario | `scripts/sener/clean_prontuario.py` | `data/raw/sener/*prontuario*.csv` | `sener/prontuario_datos_abiertos.parquet` | 16 |
| SENER volumen | `scripts/sener/clean_volumen_almacenamiento.py` | `data/raw/sener/*volumen*.csv` | `sener/volumen_almacenamiento_gas.parquet` | 186 |
| PROFEPA inspección | `scripts/profepa/clean_acciones_inspeccion.py` | `data/raw/profepa/*.csv` | `profepa/acciones_inspeccion_iao_zofemat.parquet` | 51 |
| SEMARNAT sitios | `scripts/semarnat/clean_sitios_contaminados.py` | `data/raw/semarnat/*.csv` | `semarnat/sitios_contaminados.parquet` | 481 |
| datos.gob.mx registros | `scripts/gobmx/clean_registros_publicos.py` | `data/raw/gobmx/*.csv` | `gobmx/registros_publicos_oficiales.parquet` | 1 |
| ECC Climabase | `scripts/ecc_climabase/catalog_ecc.py` | `data/raw/ECC_Climabase/*.tif` | `ecc_climabase/catalog.parquet` | 48 |
| Gasoductos contextuales | `scripts/gasoductos/clean_gasoductos.py` | `data/raw/gasoductos/capas_contextuales.geojson` | `gasoductos/capas_contextuales.parquet` | 2 |
| Ductos CNIH | `scripts/gasoductos/clean_ductos_cnih.py` | `data/raw/gasoductos/*.geojson` (5 archivos) | `gasoductos/ductos_cnih.parquet` + `anp_ramsar_cnih.parquet` | 24 + 2 |
| Gas master (Gold) | `scripts/curated/build_gas_master.py` | Silver cenegas + tarifas | `curated/gas_infrastructure/*.parquet` (6 archivos) | 33–2,307 |
| Env risk (Gold) | `scripts/curated/build_env_risk.py` | Silver gas + semarnat | `curated/env_risk/env_risk_by_nodo.parquet` | 33 |

### 5.3 BaseIngester — Flujo de Ejecución (`src/data/ingestion/base.py`)

```python
def run(self, input_path: Optional[str] = None) -> Dict[str, Any]:
    # 1. Iniciar tracking en catálogo
    self.run_id = self.catalog.start_ingestion_run(...)
    
    # 2. Procesar cada batch
    for batch_idx, batch_df in enumerate(self.extract()):
        transformed = self.transform(batch_df)
        transformed = self._deduplicate_by_cdc_hash(transformed)  # CDC exact-once
        quality_results = self.validate_data(transformed)           # Schema contract
        partition_path = self._get_partition_path(transformed)
        self.load(transformed, partition_path)
    
    # 3. Finalizar tracking
    self.catalog.finish_ingestion_run(...)
```

### 5.4 Auditoría — Capacidades v2.0

| Feature | Descripción | Archivo |
|---------|-------------|---------|
| **CDC exact-once** | Re-ejecuciones seguras sin duplicados mediante `_cdc_hash` persistido | `src/data/ingestion/base.py` |
| **Schema contract validation** | Fallo rápido por drift de columnas/tipos vs catálogo declarativo | `src/data/ingestion/base.py` |
| **Derived dataset versioning** | Trazabilidad Gold→Silver con lineage embebido en `schema.lineage` | `src/data/catalog/catalog.py` |
| **Proveniencia .meta.json** | 14 archivos con: source, dataset, download_date, source_url, row_count, columns | `lakehouse/processed/**/*.meta.json` |

### 5.5 Registro de Ejecuciones — `lakehouse/metadata/runs.jsonl`

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

**Verificación CDC (2026-08-06):**
- Run 1: 2 inserts ✅
- Run 2: 1 insert (1 duplicado detectado) ✅
- Run 3: 0 inserts (todos duplicados) ✅

**Verificación Ductos CNIH (2026-08-07):**
- Run 1: 24 inserts LineString + 2 inserts Polygon ✅
- Re-run idempotente verificado ✅

### 5.6 Catálogo Declarativo — `config/data_catalog.yaml`

607 líneas declarando 14 datasets Silver (NASA chlor_a/sst, GFW fishing_effort/vessels, TNC bajos_marinos/arrecifes_coral_negro, ASEA MIAs, bathymetry ETOPO1/GEBCO, PANGAS fishing_zones, datamares) con schemas completos, quality expectations, lakehouse paths, CDC keys y particionado H3. Cubre además configuración global: bbox, resoluciones H3 por tipo de dato, particionado temporal, compresión ZSTD.

---

## 6. DASHBOARD WEB INTERACTIVO (Next.js 16)

### 6.1 Arquitectura

```
dashboard/
├── src/
│   ├── app/
│   │   ├── components/          # 11 componentes React
│   │   │   ├── RiskMap.tsx      # 45 KB — Mapa Leaflet + 15 capas + filtros
│   │   │   ├── Heatmap.tsx      # 1.4 KB — Wrapper Leaflet.heat con useMap()
│   │   │   ├── ZoneCards.tsx     # Tarjetas riesgo PANGAS
│   │   │   ├── SpeciesPanel.tsx  # Especies IUCN
│   │   │   ├── MethodologyPanel.tsx
│   │   │   ├── CoverageModal.tsx
│   │   │   ├── MiaInspectorModal.tsx
│   │   │   ├── Header.tsx
│   │   │   ├── RiskBadge.tsx
│   │   │   └── ExportModal.tsx
│   │   ├── api/geopackage/     # API GeoPackage (5000 features/layer)
│   │   └── page.tsx            # Página principal
│   ├── lib/risk.ts             # Utilidades color/riesgo
│   └── styles/globals.css      # Esoteria Design System v1.1
└── public/data/                # 21 archivos GeoJSON estáticos
```

### 6.2 Estándar de Diseño — Esoteria Design System v1.1

| Propiedad | Valor |
|-----------|-------|
| **Tipografía** | IBM Plex Mono (monospace) |
| **Fondo** | `#0A0A0A` (oscuro permanente) |
| **Superficie** | `#111111` |
| **Bordes** | `#222222` / `#333333` |
| **Border-radius** | `0px` (todos los componentes) |
| **Box-shadow** | `none` (sin sombras) |
| **Emoticones** | PROHIBIDOS — Badges monospace taxonómicos (`[CAM]`, `[TIB]`, `[RAY]`, `[PAR]`) |
| **Tabular-nums** | Alineación numérica tabular en todos los datos |

### 6.3 CAPAS VISIBLES EN EL DASHBOARD (15 Capas)

Las capas se definen en `LAYER_CONFIGS` dentro de `RiskMap.tsx` (líneas 31-42). Cada capa tiene: id, nombre visible, archivo GeoJSON, color.

| # | ID | Nombre visible en UI | Archivo | Color | Activa por defecto | Descripción |
|---|----|---------------------|---------|-------|-------------------|-------------|
| 1 | `proyectos_gnl` | 4 Terminales GNL (11 Features v3) | `terminales_gnl_v3.geojson` (24 KB) | `#EF4444` (rojo) | ✅ | Puntos de terminales GNL + buffers H3-10 con tipo/estatus/estado. Navegación rápida desde sidebar. |
| 2 | `poligonos_saguaro` | Polígonos Detalle Saguaro (MIA 181V) | `saguaro_polygons_181v.geojson` (8 KB) | `#10B981` (verde) | ✅ | Polígonos de detalle del MIA proyecto Saguaro. |
| 3 | `capas_contexto` | Gasoductos, Sitios Ramsar & ANPs | `capas_contextuales.geojson` (4 KB) | `#FF9800` (naranja) | ✅ | Contexto regulatorio: gasoductos existentes, sitios Ramsar, ANPs. |
| 4 | `ductos_cnih` | Ductos CNIH/SENER (24 tramos, 6.4k km) | `ductos_cnih.geojson` (34 KB) | `#FF6B00` (naranja intenso) | ❌ | **NUEVO.** 24 tramos reales de ductos del CNIH/SENER ArcGIS FeatureServer. Popups enriquecidos: nombre, fuente dataset, tipo, longitud km, capacidad, proyecto, tramo, permiso CRE, empresa. |
| 5 | `sener_gasoductos` | SENER/CNIH Red Gasoductos (WMS) | — (WMS externo) | `#FFB000` (ámbar) | ❌ | Capa WMS externa SENER/CNIH. |
| 6 | `batimetria` | Contornos Batimétricos GEBCO 2024 | `batimetria_golfo.geojson` (1.4 MB) | `#38BDF8` (azul cielo) | ✅ | 1,146 contornos batimétricos con profundidad. |
| 7 | `h3_riesgo` | Malla H3 IERC (Res 8/9) | `grilla_h3_riesgo.geojson` (4.1 MB) | — | ✅ | 5,244 hexágonos con scores IERC (ierc_score 0-1, nivel_riesgo). |
| 8 | `gfw_fishing` | GFW Esfuerzo Pesquero (H3, 9,960 celdas) | `gfw_fishing_h3.geojson` (2.2 MB) | — | ❌ | **Lazy load.** Heatmap temporal por año/mes/arte/bandera. Zoom ≤7: heatmap (Leaflet.heat); zoom >7: circle markers con radio por fishing_hours. Filtros: confidence threshold, hours threshold, gear type. Contador dinámico `X / 9,960 celdas`. |
| 9 | `pangas` | PANGAS Multiespecie (4,241) | `zpesca_pangas_sample.geojson` (29 MB) | — | ✅ | Hexágonos H3 + riqueza por especie/arte/comunidad. |
| 10 | `buceo` | Pesca por Buceo (249) | `zpesca_buceo_sample.geojson` (1.5 MB) | — | ✅ | Zonas de pesca por buceo artesanal. |
| 11 | `chinchorro` | Chinchorro de Línea (2,209) | `zpesca_chinchorro_sample.geojson` (14 MB) | — | ✅ | Zonas chinchorro de línea. |
| 12 | `redes` | Redes de Enmalle (1,263) | `zpesca_redes_sample.geojson` (11.7 MB) | — | ✅ | Zonas redes de enmalle. |
| 13 | `manta` | Camarón / Manta (783) | `zpesca_redes_manta_camaron_sample.geojson` (5.6 MB) | — | ✅ | Zonas camarón / manta. |
| 14 | `trampa` | Trampas Jaiberas (360) | `zpesca_trampa_sample.geojson` (1.8 MB) | — | ✅ | Zonas trampas jaiberas. |
| 15 | `riqueza` | Riqueza Relativa Pesquera (11,065) | `riqueza_relativa_sample.geojson` (8.2 MB) | — | ✅ | 51 especies con códigos de 6 letras. |

### 6.4 Capa Ductos CNIH/SENER — Detalle de Implementación

**Estilizado por fuente (fuente_capa):**
- **Integrados SISTRANGAS** (10 tramos): `#FF6B00` (naranja intenso)
- **No Integrados SISTRANGAS** (6 tramos): `#FFB000` (ámbar)
- **Poliductos Petrolíferos** (5 tramos): `#00D4AA` (verde menta)
- **Pacific Limited** (1 tramo): `#A855F7` (púrpura, discontinuo)
- **Capas Contextuales** (2 gasoductos): `#FF9800` (naranja existente)

**Popups enriquecidos con:**
nombre, fuente_capa, tipo, longitud_km, capacidad, proyecto, tramo, permiso CRE, empresa, zona_tarifaria, integrado_sistrangas

### 6.5 Capa GFW — Heatmap Temporal / Círculos por Zoom

- **Zoom ≤ 7:** Heatmap (Leaflet.heat vía `<Heatmap>` component) — densidad global ponderada por `hours`
- **Zoom > 7:** Circle markers con radio proporcional a `fishing_hours`
- **Filtros UI:** Año (2016/2020/Todos), Mes (1-12/Todos), Arte (6 tipos/Todos), Bandera (6/Todas)
- **Filtros adicionales:** Confidence threshold slider (0-1), Hours threshold slider, Gear type select
- **Contador dinámico:** `X / 9,960 celdas` visible en panel de filtros
- **Componente Heatmap.tsx:** Wrapper de leaflet.heat usando `useMap()` hook de react-leaflet (1.4 KB, 55 líneas)

### 6.6 API GeoPackage — `/api/geopackage`

Endpoint interno que sirve capas desde el GeoPackage (`ierc_golfo_california.gpkg`) con límite de 5,000 features por capa. Mapea IDs de capa a tablas internas:

| ID capa | Tabla GeoPackage |
|---------|-----------------|
| `proyectos_gnl` | `proyectos_gnl` |
| `h3_riesgo` | `grilla_h3_riesgo` |
| `riqueza` | `riqueza_relativa_pesquera` |
| `capas_contexto` | `gasoductos_infraestructura_gnl` |
| `ductos_cnih` | `ductos_cnih` |

### 6.7 Controles UI

| Control | Tipo | Rango |
|---------|------|-------|
| **Time Slider** | Slider temporal | 2020–2024 |
| **H3 Resolution Selector** | Select | 8 / 9 / Adaptive |
| **Risk Threshold** | Slider (Monte Carlo) | p05–p95 |
| **Layer Opacity** | Slider por capa | 0–100% |
| **Spatial Filter** | Bbox / Radio | Coordenadas / km |
| **Confidence Threshold** | Slider | 0–95% |
| **GFW Confidence** | Slider | 0.0–1.0 |
| **GFW Hours Threshold** | Slider | 0+ |
| **GFW Gear Type** | Select | trawlers/longliners/purse_seines/fixed_gear/other/Todos |
| **GFW Year** | Select | 2016/2020/Todos |
| **GFW Month** | Select | 1-12/Todos |
| **GFW Flag** | Select | 6 banderas/Todas |

### 6.8 Navegación Rápida a Terminales GNL (Sidebar)

| Terminal | Ubicación | Lat | Lon | Zoom | Precisión | Estatus |
|----------|-----------|-----|-----|------|-----------|---------|
| SAGUARO ENERGÍA GNL | Puerto Libertad, Sonora | 29.9058 | -112.6880 | 13 | [APROXIMADO] | Proposed / Pre-FID |
| AMIGO LNG | Guaymas, Sonora | 27.9229 | -110.8681 | 13 | [EXACTO] | Proposed / Pre-FID |
| VISTA PACÍFICO (FLNG) | Topolobampo, Sinaloa | 25.5891 | -109.1038 | 13 | [CALCULADO] | CANCELADO (Feb 2026) |
| GNL COSALÁ | Mazatlán / Zapopan | 23.2500 | -106.4200 | 11 | [APROXIMADO] | En Evaluación ASEA |

---

## 7. ENTREGABLE ESPACIAL GEOPACKAGE v1.1 (META 1 POA 2026)

**Ubicación:** `deliverables/v1_geopackage/ierc_golfo_california.gpkg` (5.9 MB, 9 capas)  
**Copia dashboard:** `dashboard/public/data/ierc_golfo_california.gpkg` (5.9 MB)

### 7.1 Capas Vectoriales Incluidas

| Capa | Geometría | Entidades | Descripción |
|------|-----------|-----------|-------------|
| `proyectos_gnl` | Point | 11 | Infraestructura GNL con scores riesgo pesquero e IERC |
| `gasoductos_infraestructura_gnl` | LineString | 2 | Trazados ductos gas natural (Sonora, Saguaro, Guaymas) |
| `localidades_estudio_ierc` | Point | 3 | Comunidades POA: Punta Chueca Comca'ac, Puerto Libertad, Guaymas |
| `anp_habitats_criticos` | Polygon | 2 | ANPs CONANP + hábitats marinos críticos |
| `zonas_pesqueras_pangas` | MultiPolygon | 17 | Polígonos pesca artesanal con `uid_espaciotemporal` |
| `grilla_h3_riesgo` | Polygon | 5,244 | Malla H3 adaptativa (Res 8 mar / Res 9 portuario) con IERC |
| `riqueza_relativa_pesquera` | MultiPolygon | 11,065 | Riqueza biológica pesquera acumulada (51 especies) |
| `batimetria_contornos_gebco` | LineString | 1,146 | Contornos batimétricos GEBCO 2024 |
| `poligonos_detalle_saguaro` | Polygon | Variable | Detalle proyecto Saguaro (MIA 181V) |

---

## 8. RESPONSIBLE AI / ÉTICA ALGORÍTMICA

### 8.1 Implementación (`src/engine/responsible_ai.py`)

| Capacidad | Descripción | Tests |
|-----------|-------------|-------|
| **Explainability** | SHAP-style feature attribution por celda H3 | 4 tests |
| **Bias Detection** | Detección sesgo geográfico (costa vs mar) + poblacional | 4 tests |
| **Smooth Failing** | Degradación grácil: fallback a percentiles si Monte Carlo falla | 2 tests |
| **Team Workflow** | Auditoría colaborativa JCB↔EG con checkpoints | 2 tests |

### 8.2 Matriz de Vacíos Geoespaciales

| Capa | Vacío Identificado | Impacto | Acción |
|------|-------------------|---------|--------|
| GFW | No distingue pesca ilegal vs legal | Alto | Cruzar con VMS nacional |
| NASA | Gaps por nubes (clorofila) | Medio | Interpolación espacio-temporal |
| PANGAS | Solo 3 comunidades POA | Alto | Expandir muestreo |
| ASEA | MIA PDFs no parseados completamente | Medio | OCR + NLP para extraer coordenadas |
| Socioeconómico | Datos INEGI 2020 desactualizados | Alto | Encuestas de campo 2026 |
| Ductos CNIH | Solo 24 tramos vs red completa | Medio | Solicitar WFS completo CNIH |

---

## 9. ESTRUCTURA DEL REPOSITORIO

```
ierc-gnl-project/
├── causanaturadata/            # Documentos oficiales (POA 2026, Manual Metodológico)
├── config/
│   ├── lakehouse.yaml          # Config lakehouse, CDC keys, particionamiento
│   └── data_catalog.yaml       # Catálogo declarativo (607 líneas, 14+ datasets)
├── config.py                   # Helpers de paths (14 funciones: *_raw_dir())
├── dashboard/                  # Dashboard Web (Next.js 16)
│   ├── src/app/
│   │   ├── components/         # 11 componentes React
│   │   ├── api/geopackage/     # API GeoPackage (5000 features/layer)
│   │   └── page.tsx
│   ├── public/data/            # 21 archivos GeoJSON/GeoPackage estáticos
│   └── AGENTS.md / CLAUDE.md   # Instrucciones para agentes IA
├── data/
│   ├── raw/                    # BRONZE (16 directorios fuente)
│   │   ├── cenegas/            # 2 CSVs CENEGAS
│   │   ├── ECC_Climabase/      # 131 GeoTIFFs climatología
│   │   ├── gasoductos/         # 5 GeoJSON CNIH/SENER + capas_contextuales
│   │   ├── gfw/                # 21 archivos GFW
│   │   ├── nasa/               # 120 archivos NASA OceanColor
│   │   ├── pangas_gdb/         # 90 archivos PANGAS GDB
│   │   ├── pangas_wgs84/       # 7 GeoJSON PANGAS
│   │   └── tnc/                # 2 shapefiles TNC
│   └── schemas/                # Schemas JSON
├── deliverables/
│   ├── v1_geopackage/          # ENTREGABLE META 1 (9 capas, 5.9 MB)
│   └── v2_geopackage/          # Versión con capas campo (12 capas)
├── docs/
│   ├── metodologia/
│   │   ├── Nota_Metodologica_Ajustada_JCB_EG.md
│   │   └── Inventario_y_Matriz_Vacios_Geoespaciales_EG.md
│   ├── ESTRATEGIA_COSECHA_DATASETS.md  # Estrategia cosecha datos.gob.mx
│   └── GFW_MAP_STRATEGY.md            # Estrategia visualización GFW
├── lakehouse/
│   ├── processed/              # SILVER (165 Parquets, 14 fuentes)
│   │   ├── asea/mias_enriched/    # 9 particiones H3-10
│   │   ├── bathymetry_gebco/      # 2 particiones resolution=8,9
│   │   ├── cenegas/               # 3 Parquets (iny/extr/tarifas)
│   │   ├── ecc_climabase/         # catalog.parquet
│   │   ├── gasoductos/            # 3 GeoParquets (ductos/anp/capas)
│   │   ├── gfw/                   # 18+1 particiones year/month
│   │   ├── gobmx/                 # registros_publicos
│   │   ├── nasa/                  # 60+60 particiones chlor_a/sst
│   │   ├── pangas_fishing_zones/  # 263,796 rows
│   │   ├── profepa/               # acciones_inspeccion
│   │   ├── semarnat/              # sitios_contaminados
│   │   ├── sener/                 # prontuario + volumen
│   │   └── tnc/                   # bajos_marinos + arrecifes
│   ├── curated/                # GOLD (13 Parquets)
│   │   ├── gas_infrastructure/    # 7 parquets
│   │   ├── env_risk/              # 1 parquet
│   │   └── ierc_*.parquet         # 6 parquets IERC
│   └── metadata/               # catalog.json + runs.jsonl
├── scripts/                    # 44 scripts operacionales
│   ├── cenegas/                # 3 scripts de limpieza
│   ├── curated/                # 2 scripts Gold (build_gas_master, build_env_risk)
│   ├── ecc_climabase/          # 1 script catálogo
│   ├── gasoductos/             # 2 scripts (ductos_cnih, capas_contextuales)
│   ├── gobmx/                  # 1 script
│   ├── profepa/                # 1 script
│   ├── semarnat/               # 1 script
│   ├── sener/                  # 2 scripts
│   ├── supabase/               # 4 scripts migración
│   └── *.py                    # 27 scripts raíz
├── src/
│   ├── data/
│   │   ├── ingestion/          # Pipeline ingesta (base + factory + ingesters)
│   │   ├── catalog/            # DataCatalog JSONL + lineage
│   │   └── lakehouse/          # LocalFileStorage (Parquet + ZSTD)
│   └── engine/                 # IERC, Monte Carlo, Responsible AI, spatial_validator
├── tests/unit/                 # 45 tests passing
├── .github/
│   ├── workflows/ci.yml        # Pipeline CI/CD 5 jobs
│   └── CI_README.md            # Documentación del CI
└── README.md                   # Documentación principal (v2.3)
```

---

## 10. REPRODUCIBILIDAD Y COMANDOS

### 10.1 Prerrequisitos
- Python 3.11+ (venv en `.venv/`)
- Node.js 18+ (para dashboard)
- `pyarrow`, `geopandas`, `pandas`, `h3` (instalados en `.venv/`)

### 10.2 Ejecutar Tests (Pytest)
```bash
PYTHONPATH=. ./.venv/bin/python3 -m pytest tests/unit/ -v
# 45 passed:
#   test_storage_catalog.py (4)
#   test_utils_h3.py (4)
#   test_utils_ierc.py (4)
#   test_engine_ierc.py (3)
#   test_engine_responsible_ai.py (12)
#   test_engine_spatial_validator.py (17)
#   test_engine_monte_carlo.py (1)
#   test_pipeline_e2e.py (1)
```

### 10.3 Pipeline End-to-End
```bash
# 1. Inicializar Lakehouse y Catálogo
PYTHONPATH=. ./.venv/bin/python3 scripts/init_lakehouse.py

# 2. Limpiar datasets datos.gob.mx → Silver
PYTHONPATH=. ./.venv/bin/python3 scripts/cenegas/clean_cenegas.py
PYTHONPATH=. ./.venv/bin/python3 scripts/cenegas/harvest_extracciones.py
PYTHONPATH=. ./.venv/bin/python3 scripts/cenegas/clean_tarifas.py
PYTHONPATH=. ./.venv/bin/python3 scripts/sener/clean_prontuario.py
PYTHONPATH=. ./.venv/bin/python3 scripts/sener/clean_volumen_almacenamiento.py
PYTHONPATH=. ./.venv/bin/python3 scripts/profepa/clean_acciones_inspeccion.py
PYTHONPATH=. ./.venv/bin/python3 scripts/semarnat/clean_sitios_contaminados.py
PYTHONPATH=. ./.venv/bin/python3 scripts/gobmx/clean_registros_publicos.py
PYTHONPATH=. ./.venv/bin/python3 scripts/ecc_climabase/catalog_ecc.py

# 3. Ingesta ductos CNIH/SENER → Silver
PYTHONPATH=. ./.venv/bin/python3 scripts/gasoductos/clean_ductos_cnih.py
PYTHONPATH=. ./.venv/bin/python3 scripts/gasoductos/clean_gasoductos.py

# 4. Construir Gold (gas + env risk)
PYTHONPATH=. ./.venv/bin/python3 scripts/curated/build_gas_master.py
PYTHONPATH=. ./.venv/bin/python3 scripts/curated/build_env_risk.py

# 5. Exportar insumos para Dashboard Web
PYTHONPATH=. ./.venv/bin/python3 scripts/prepare_dashboard_data.py
```

### 10.4 Ejecutar Dashboard Interactivo
```bash
cd dashboard
npm install
npm run dev
# http://localhost:3001
```

### 10.5 Verificación TypeScript
```bash
cd dashboard
npx tsc --noEmit --skipLibCheck
# Debe salir exit 0 sin errores
```

---

## 11. CI/CD PIPELINE

El proyecto incluye un pipeline de CI completo (`.github/workflows/ci.yml`) con 5 jobs:

| Job | Descripción | Tiempo estimado |
|-----|-------------|-----------------|
| **test** | Unit tests Python (45 tests) | ~2 min |
| **lint** | Syntax check Python (py_compile) en módulos core | ~30 seg |
| **verify-cdc** | Verificación CDC exact-once + schema contract | ~1 min |
| **dashboard-build** | Build Next.js 16 (compilación producción) | ~3 min |
| **summary** | Reporte consolidado de estado | ~10 seg |

**Triggers:** push/PR a `main`, `develop`  
**Secrets:** `GFW_API_TOKEN` (opcional, solo para ingesta manual)

---

## 12. Cita Oficial

**Causa Natura Center (2026):** *Índice Espacial de Riesgo Socioeconómico para Comunidades (IERC) ante proyectos de GNL en el Golfo de California*. Elaborado por Juan Carlos Barrera (JCB) y Enrique Gorosave Meza (EG).

---

## 13. Documentación Técnica Vinculada

- **[REPORTE_INVENTARIO_DATOS_IERC_GNL_v2.2_ENRIQUE_GOROSAVE.md](REPORTE_INVENTARIO_DATOS_IERC_GNL_v2.2_ENRIQUE_GOROSAVE.md)** — Reporte oficial v2.2 (2026-08-07)
- **[REPORTE_INVENTARIO_DETALLADO_IERC_GNL.md](REPORTE_INVENTARIO_DETALLADO_IERC_GNL.md)** — Inventario técnico SILVER/GOLD v2.1 (2026-08-06)
- **[REPORTE_INVENTARIO_GEOPACKAGE.md](REPORTE_INVENTARIO_GEOPACKAGE.md)** — Metadata entregable GeoPackage Meta 1
- **[config/lakehouse.yaml](config/lakehouse.yaml)** — Configuración lakehouse, CDC keys, particionamiento
- **[config/data_catalog.yaml](config/data_catalog.yaml)** — Catálogo declarativo (607 líneas, 14+ datasets)
- **[docs/metodologia/Nota_Metodologica_Ajustada_JCB_EG.md](docs/metodologia/Nota_Metodologica_Ajustada_JCB_EG.md)** — Formulación matemática IERC
- **[docs/metodologia/Inventario_y_Matriz_Vacios_Geoespaciales_EG.md](docs/metodologia/Inventario_y_Matriz_Vacios_Geoespaciales_EG.md)** — Matriz de vacíos geográficos
- **[docs/ESTRATEGIA_COSECHA_DATASETS.md](docs/ESTRATEGIA_COSECHA_DATASETS.md)** — Estrategia cosecha datos.gob.mx
- **[docs/GFW_MAP_STRATEGY.md](docs/GFW_MAP_STRATEGY.md)** — Estrategia visualización GFW
- **[.github/workflows/ci.yml](.github/workflows/ci.yml)** — Pipeline CI/CD completo
- **[.github/CI_README.md](.github/CI_README.md)** — Documentación del CI

---

*Fin del reporte v2.3 — 2026-08-07 — Enrique Gorosave Meza — Causa Natura Center*