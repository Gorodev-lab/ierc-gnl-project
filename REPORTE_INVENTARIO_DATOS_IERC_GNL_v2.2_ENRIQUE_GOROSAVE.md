# REPORTE INVENTARIO DETALLADO DE DATOS IERC-GNL
## Índice Espacial de Riesgo Socioeconómico para Comunidades (GNL)
### Causa Natura Center — POA 2026-2028

---

**Autor:** Enrique Gorosave Meza (Analista de Datos y SIG)  
**Fecha:** 2026-08-07  
**Versión:** v2.2  
**Organización:** Causa Natura Center

---

## 1. RESUMEN EJECUTIVO

Este reporte presenta el inventario completo y actualizado de los datos, arquitectura y componentes del proyecto **IERC-GNL** (Índice Espacial de Riesgo Socioeconómico para Comunidades ante proyectos de Gas Natural Licuado en el Golfo de California). El proyecto forma parte del **Plan Operativo Anual (POA 2026-2028)** de **Causa Natura Center**.

### 1.1 Métricas Clave del Proyecto

| Métrica | Valor |
|---------|-------|
| **Arquitectura** | Lakehouse Medallion (Bronze/Silver/Gold) |
| **Datasets SILVER** | 12 fuentes procesadas y particionadas H3 |
| **Productos GOLD** | 6 datasets analíticos listos para ML/dashboard |
| **Capas Dashboard** | 15+ capas vectoriales interactivas (Next.js 16) |
| **Entregable GeoPackage** | v1.1 (9 capas) + v2 (12 capas con campo) |
| **Ductos CNIH/SENER** | 24 tramos LineString (6,399 km) + 2 ANP Polygons |
| **Tests Unitarios** | 45 tests passing (storage, catalog, H3, IERC, RAI, spatial, Monte Carlo, E2E) |
| **Pipeline CI/CD** | 5 jobs automatizados (test, lint, verify-cdc, dashboard-build, summary) |

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

**Configuración técnica (`config/lakehouse.yaml`):**
- **Formato tabular:** Parquet (compresión ZSTD nivel 3)
- **Formato espacial:** GeoParquet
- **Particionado espacial por defecto:** H3 Resolución 8 (~0.73 km² mar abierto), Res 10 costero (~0.015 km²)
- **Particionado temporal:** Mensual (columna `time_partition` formato YYYY-MM)
- **Catálogo:** JSONL en `lakehouse/metadata/catalog.json` + `runs.jsonl`

### 2.2 Bounding Box Golfo de California (EPSG:4326)
- **min_lat:** 22.5 | **max_lat:** 32.0
- **min_lon:** -115.0 | **max_lon:** -108.0

---

## 3. INVENTARIO DATASETS SILVER (12 Fuentes Procesadas)

### 3.1 Tabla Maestra SILVER

| # | Dataset | Dominio | Resolución H3 | Frecuencia | Tamaño Est. | Prioridad | Estado |
|---|---------|---------|---------------|------------|-------------|-----------|--------|
| 1 | `nasa_chlor_a` | NASA OceanColor | 8 | Mensual (2020-2024) | ~100 MB | Crítico | ✅ Activo |
| 2 | `nasa_sst` | NASA OceanColor | 8 | Mensual (2020-2024) | ~100 MB | Crítico | ✅ Activo |
| 3 | `gfw_fishing_effort` | Global Fishing Watch | 8 | Diario (2012-2023) | ~100 GB (Golfo) | Crítico | ✅ Activo |
| 4 | `gfw_vessels` | Global Fishing Watch | — | Estático | ~50 MB | Alto | ✅ Activo |
| 5 | `tnc_bajos_marinos` | TNC Conservation | 8 | Estático | ~10 MB | Alto | ✅ Activo |
| 6 | `tnc_arrecifes_coral_negro` | TNC Conservation | 8 | Estático | ~5 MB | Alto | ✅ Activo |
| 7 | `asea_mias_consolidated` | ASEA/CENAGAS/SENER | 10 | Incremental semanal | ~1 MB | Crítico | ✅ Activo (CDC) |
| 8 | `bathymetry_etopo1` | ETOPO1 | 8, 9, 10 | Estático | ~50 MB | Alto | ✅ Activo |
| 9 | `bathymetry_gebco` | GEBCO 2024 | 8, 9, 10 | Estático | ~20 MB | Medio | ✅ Activo |
| 10 | `pangas_fishing_zones` | PANGAS | 8 (embebido) | Estático | ~30 MB | Crítico | ✅ Activo |
| 11 | `pangas_riqueza_relativa` | PANGAS | 8 | Estático | ~200 MB | Alto | ✅ Activo |
| 12 | `gfw_vessels_mexican` | GFW subset | — | Estático | ~5 MB | Alto | ✅ Activo |
| 13 | **`ductos_cnih`** | **CNIH/SENER ArcGIS** | **8** | **Estático** | **~2 MB** | **Crítico** | **✅ Nuevo (2026-08-07)** |
| 14 | **`anp_ramsar_cnih`** | **CNIH/SENER ArcGIS** | **10** | **Estático** | **~1 MB** | **Alto** | **✅ Nuevo (2026-08-07)** |

### 3.2 Detalle por Fuente de Datos

#### **NASA OceanColor (MODIS-Aqua)**
- **Variables:** `chlor_a` (mg/m³, rango 0-100), `sst` (°C, rango -2 a 40)
- **Resolución nativa:** 4 km diaria
- **Particionado Silver:** `processed/nasa/{chlor_a,sst}/year={year}/month={month:02d}/h3_8={h3_cell_8}/`
- **Gold path:** `curated/nasa/{chlor_a,sst}_monthly_h3_8/`
- **Calidad:** Validación de rango, no nulos, frescura máx 7 días

#### **Global Fishing Watch (v3.0)**
- **Fuente:** Zenodo record 14982712
- **Variables:** `fishing_hours`, `mmsi`, `gear_type` (trawlers, longliners, purse_seines, fixed_gear, other), `flag`
- **Resolución nativa:** 0.01° × 0.01°
- **Particionado Silver:** `processed/gfw/fishing_effort_h3/year={year}/month={month:02d}/h3_8={h3_cell_8}/`
- **Tamaño total:** 5.1 TB global, ~100 GB para Golfo de California
- **Actualización:** Anual

#### **The Nature Conservancy (TNC)**
- **Capas:** `bajos_marinos` (montes submarinos, bancos), `arrecifes_coral_negro` (Antipatharia)
- **Formato:** Shapefile ZIP → H3 grid con `area_fraction` (fracción de celda cubierta)
- **Particionado Silver:** `processed/tnc/{bajos_marinos,arrecifes_coral_negro}_h3/h3_8={h3_cell_8}/`

#### **ASEA MIAs (Manifestaciones de Impacto Ambiental)**
- **Fuentes:** ASEA + CENAGAS + SENER + Plan Quinquenal 2025-29
- **Archivos:** `gnl_proyectos_consolidados.csv`, `asea_mias_alto_golfo.csv`
- **CDC habilitado:** ✅ Exact-once deduplication
- **CDC Key:** `proyecto_id`
- **CDC Hash columns:** 10 columnas (nombre, estado, tipo_proyecto, lat, lon, estatus, capacidad_mtpa, longitud_km, folio_asea, pdf_url)
- **H3 Resolution:** 10 (infraestructura puntual)
- **Frecuencia:** Incremental semanal

#### **Batimetría**
- **ETOPO1:** 1 arc-min (~1.8 km), stats: mean/min/max/std/count por H3 multi-res (8,9,10)
- **GEBCO 2024:** 15 arc-sec (~450 m), vectorizado en contornos
- **Particionado Silver:** `processed/bathymetry/{etopo1,gebco}_h3/h3_{resolution}={h3_cell}/`

#### **PANGAS (Programa de Acción para la Naturaleza, Golfo y Sociedad)**
- **Artes de pesca:** PANGAS, Buceo, Chinchorro, Redes, Redes Manta Camarón, Trampa, Riqueza Relativa
- **Identificador único:** `uid_espaciotemporal = comunidad-actor-pesquería-arte-zona-temporada-ruta`
- **Particionado Silver:** `processed/pangas/fishing_zones_h3/` + `pangas/riqueza_relativa_h3/`

#### **CNIH/SENER — Ductos de Gas Natural (NUEVO 2026-08-07)**
- **Fuente:** ArcGIS FeatureServer CNIH/SENER (`services6.arcgis.com/th3TMn162i37A876/ArcGIS/rest/services/AppMote/FeatureServer`)
- **Capas descargadas:**
  - Layer 11: `Ductos_NO_integrados_a_SISTRANGAS` (6 tramos)
  - Layer 12: `Ductos_integrados_a_SISTRANGAS` (10 tramos)
  - Layer 13: `Ducto_Pacific_Limited` (1 tramo)
  - Layer 14: `Poliductos_de_petrolíferos` (5 tramos)
  - Layer 1: `capas_contextuales` (2 gasoductos contextuales + 2 ANP/Ramsar)
- **Total:** 24 tramos LineString (6,399.3 km) + 2 ANP/Ramsar Polygons
- **Atributos clave:** nombre, proyecto, tipo, longitud_km, tramo, permiso, capacidad, zona_tarifaria, integrado_sistrangas, empresa, fuente_capa
- **H3 Resolution:** 8 (corredores lineales)
- **Formato:** GeoJSON + GeoParquet (Silver)

---

## 4. PRODUCTOS GOLD (6 Datasets Analíticos)

| Dataset | Filas | Descripción |
|---------|-------|-------------|
| `ierc_risk_h3_8.parquet` | 830,869 | Índice principal de riesgo (score 0-1, percentiles) |
| `ierc_features_h3_8.parquet` | 830,869 | Features para ML (sin scores finales) |
| `ierc_monte_carlo_h3_8.parquet` | 830,869 | Simulación N=1000 (mean, std, p05, p95, median) |
| `ierc_features_adaptive_h3.parquet` | 830,869 | Multi-resolución H3 + features socioeconómicos PANGAS |
| `ierc_risk_multiplicative.parquet` | 833,032 | Modelo multiplicativo Amenaza × Vulnerabilidad (IPCC) |
| `ierc_confidence_h3.parquet` | 833,032 | Scores de confianza espacial para filtrado dashboard |

### 4.1 Formulación Matemática IERC

**Modelo Aditivo (Oficial):**
```
IERC_total = (Amenaza × 0.20) + (Exposición × 0.20) + (Sensibilidad × 0.15) +
             (Dependencia × 0.15) + (Valor_Biocultural × 0.15) +
             ((1 - Capacidad_Adaptativa) × 0.15)
```

**Modelo Multiplicativo (IPCC):**
```
R_i,t = H_i,t × V_i,t

Donde:
H_i,t = Amenaza y Exposición Espacial (densidad esfuerzo, proximidad GNL, conflicto rutas)
V_i,t = 0.25 Sensibilidad + 0.25 Dependencia + 0.20 Biocultural + 0.15 Género + 0.15 [1 - Cap.Adaptativa]
```

### 4.2 Componentes del Modelo (6 Ejes)

| Componente | Peso (Aditivo) | Descripción | Variables Fuente |
|------------|----------------|-------------|------------------|
| **Amenaza (H)** | 0.20 | Infraestructura GNL, ruido, rutas metaneros | ASEA MIA, GFW rutas, ductos CNIH |
| **Exposición (H)** | 0.20 | Esfuerzo pesquero VMS + pangas | GFW, PANGAS, ductos CNIH |
| **Sensibilidad (V)** | 0.15 | Especies IUCN, endemismo, hábitats críticos | TNC, NASA, OBIS |
| **Dependencia (V)** | 0.15 | Ingreso pesquero / ingreso total hogar | Encuestas PANGAS, INEGI |
| **Biocultural (V)** | 0.20 | Sitios sagrados Comca'ac, patrimonio | Trabajo de campo |
| **Capacidad Adaptativa (V)** | 0.15 | Gobernanza GAGE, diversificación, crédito | GAGE, encuestas |

---

## 5. CADENA DE INGESTA Y AUDITORÍA (v2.0)

### 5.1 Pipeline Overview

```
FACTORY LAYER
  create_gfw_ingester()  create_nasa_ingester()  create_tnc_*()
  create_asea_ingester()  create_bathymetry_ingester()  create_pangas_ingester()
  create_ductos_cnih_ingester()          # NUEVO 2026-08-07
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
  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │   GFW    │  │  NASA    │  │   TNC    │  │  ASEA    │  │  PANGAS  │  │  DUCTOS  │
  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘
        │
        ▼
  SILVER (H3-partitioned Parquet ZSTD)
        │
        ▼
  CATALOG TRACKING (runs.jsonl)
        │
        ▼
  GOLD (joins H3-8 + scoring + Monte Carlo)
        │
        ▼
  DERIVED VERSIONING (lineage en schema.lineage)
```

### 5.2 Nuevas Capacidades v2.0 (2026-08-06/07)

| Feature | Descripción | Archivo |
|---------|-------------|---------|
| **CDC exact-once** | Re-ejecuciones seguras sin duplicados mediante `_cdc_hash` persistido | `src/data/ingestion/base.py:309` |
| **Schema contract validation** | Fallo rápido por drift de columnas/tipos vs catálogo declarativo | `src/data/ingestion/base.py:158` |
| **Derived dataset versioning** | Trazabilidad Gold→Silver con lineage embebido en `schema.lineage` | `src/data/catalog/catalog.py:275` |
| **Ductos CNIH Ingester** | Descarga ArcGIS FeatureServer, estandariza columnas, separa LineString/Polygon | `scripts/gasoductos/clean_ductos_cnih.py` |

### 5.3 BaseIngester — Flujo de Ejecución (`src/data/ingestion/base.py`)

```python
def run(self, input_path: Optional[str] = None) -> Dict[str, Any]:
    # 1. Iniciar tracking en catálogo
    self.run_id = self.catalog.start_ingestion_run(...)
    
    # 2. Procesar cada batch
    for batch_idx, batch_df in enumerate(self.extract()):
        # Transform
        transformed = self.transform(batch_df)
        
        # CDC Deduplication (exact-once)
        transformed = self._deduplicate_by_cdc_hash(transformed)
        
        # Validar (schema contract + calidad)
        quality_results = self.validate_data(transformed)
        
        # Cargar particionado
        partition_path = self._get_partition_path(transformed)
        self.load(transformed, partition_path)
    
    # 3. Finalizar tracking
    self.catalog.finish_ingestion_run(...)
```

### 5.5 Auditoría de Ejecuciones — `lakehouse/metadata/runs.jsonl`

Cada ingesta genera registro estructurado:

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
- Run 1: 24 inserts (LineString) + 2 inserts (Polygon) ✅
- Re-run idempotente verificado ✅

---

## 6. DASHBOARD WEB INTERACTIVO (Next.js 16)

### 6.1 Arquitectura del Dashboard

```
dashboard/
├── src/
│   ├── app/
│   │   ├── components/          # 11 componentes React
│   │   ├── api/geopackage/      # API GeoPackage (5000 features/layer)
│   │   └── page.tsx             # Página principal
│   ├── lib/
│   │   └── risk.ts              # Utilidades color/riesgo
│   └── styles/
│       └── globals.css          # Esoteria Design System v1.1
└── public/data/                 # 18 archivos GeoJSON estáticos
```

### 6.2 Estándar de Diseño — Esoteria Design System v1.1

| Propiedad | Valor |
|-----------|-------|
| **Tipografía** | IBM Plex Mono (monospace) |
| **Fondo** | `#0A0A0A` (oscuro permanente) |
| **Superficie** | `#111111` |
| **Bordes** | `#222222` |
| **Border-radius** | `0px` (todos los componentes) |
| **Box-shadow** | `none` (sin sombras) |
| **Emoticones** | **PROHIBIDOS** — Badges monospace taxonómicos (`[CAM]`, `[TIB]`, `[RAY]`, `[PAR]`) |

### 6.3 Capas Visibles en el Dashboard (15 Capas Vectoriales)

| ID | Nombre | Archivo GeoJSON | Tamaño | Descripción |
|----|--------|-----------------|--------|-------------|
| `proyectos_gnl` | 4 Terminales GNL (11 Features v3) | `terminales_gnl_v3.geojson` | 24 KB | Puntos + buffers H3-10 (tipo/estatus/estado) |
| `poligonos_saguaro` | Polígonos Detalle Saguaro (MIA 181V) | `saguaro_polygons_181v.geojson` | 8 KB | Polígonos detalle MIA proyecto Saguaro |
| `capas_contexto` | Gasoductos, Sitios Ramsar & ANPs | `capas_contextuales.geojson` | 4 KB | Contexto regulatorio y conservación |
| **`ductos_cnih`** | **Ductos CNIH/SENER (24 tramos, 6.4k km)** | **`ductos_cnih.geojson`** | **34 KB** | **Tramos reales CNIH/SENER ArcGIS con popups ricos** |
| `sener_gasoductos` | SENER/CNIH Red Gasoductos (WMS) | — (WMS) | — | Capa WMS externa |
| `batimetria` | Contornos Batimétricos GEBCO 2024 | `batimetria_golfo.geojson` | 1.4 MB | 1,146 contornos con profundidad |
| `h3_riesgo` | Malla H3 IERC (Res 8/9) | `grilla_h3_riesgo.geojson` | 4.1 MB | 5,244 hexágonos con scores IERC |
| `gfw_fishing` | GFW Esfuerzo Pesquero (H3, 9960 celdas) | `gfw_fishing_h3.geojson` | 2.2 MB | Heatmap temporal año/mes/arte/bandera |
| `pangas` | PANGAS Multiespecie (4,241) | `zpesca_pangas_sample.geojson` | 29 MB | Hexágonos H3 + riqueza por especie/arte |
| `buceo` | Pesca por Buceo (249) | `zpesca_buceo_sample.geojson` | 1.5 MB | Zonas buceo artesanal |
| `chinchorro` | Chinchorro de Línea (2,209) | `zpesca_chinchorro_sample.geojson` | 14 MB | Zonas chinchorro |
| `redes` | Redes de Enmalle (1,263) | `zpesca_redes_sample.geojson` | 11.7 MB | Zonas redes |
| `manta` | Camarón / Manta (783) | `zpesca_redes_manta_camaron_sample.geojson` | 5.6 MB | Zonas camarón |
| `trampa` | Trampas Jaiberas (360) | `zpesca_trampa_sample.geojson` | 1.8 MB | Zonas trampa |
| `riqueza` | Riqueza Relativa Pesquera (11,065) | `riqueza_relativa_sample.geojson` | 8.2 MB | 51 especies (códigos 6 letras) |

### 6.4 Capas Derivadas (Análisis IERC)

| Capa | Descripción | Fuente |
|------|-------------|--------|
| **IERC Score** | Índice integrado 0–1 | `grilla_h3_riesgo.geojson` → `ierc_score` |
| **Nivel de Riesgo** | Muy Bajo / Bajo / Medio / Alto / Muy Alto | Percentiles IERC |
| **Amenaza / Vulnerabilidad** | Componentes modelo multiplicativo | `ierc_risk_multiplicative.parquet` |
| **Confianza Espacial** | Filtro calidad datos (threshold configurable) | `ierc_confidence_h3.parquet` |

### 6.5 Capa Ductos CNIH/SENER — Detalle de Implementación

**Archivo:** `dashboard/public/data/ductos_cnih.geojson` (34 KB, 24 features)

**Estilizado por fuente:**
- **Integrados SISTRANGAS** (10 tramos): `#FF6B00` (naranja intenso)
- **No Integrados SISTRANGAS** (6 tramos): `#FFB000` (ámbar)
- **Poliductos Petrolíferos** (5 tramos): `#00D4AA` (verde menta)
- **Pacific Limited** (1 tramo): `#A855F7` (púrpura, discontinuo)
- **Capas Contextuales** (2 gasoductos): `#FF9800` (naranja existente)

**Popups enriquecidos con:**
- Nombre del ducto/proyecto
- Fuente dataset (integrados_sistrangas, no_integrados_sistrangas, poliductos_petroliferos, pacific_limited, capas_contextuales)
- Tipo de ducto
- Longitud (km, calculada en proyección métrica)
- Capacidad (m³/d)
- Proyecto asociado
- Tramo
- Permiso CRE
- Empresa promotora

**Controles UI para la capa:**
- Checkbox en panel lateral (desactivado por defecto)
- Color codificado en leyenda del panel
- Zoom automático a feature al click en popup

### 6.6 Controles UI

| Control | Tipo | Rango |
|---------|------|-------|
| **Time Slider** | Slider temporal | 2020–2024 |
| **H3 Resolution Selector** | Select | 8 / 9 / Adaptive |
| **Risk Threshold** | Slider (Monte Carlo) | p05–p95 |
| **Layer Opacity** | Slider por capa | 0–100% |
| **Spatial Filter** | Bbox / Radio | Coordenadas / km |
| **Confidence Threshold** | Slider | 0–95% |

### 6.7 Capa GFW — Heatmap Temporal / Círculos por Zoom

- **Zoom ≤ 7:** Heatmap (Leaflet.heat) — densidad global ponderada por `hours`
- **Zoom > 7:** Circle markers con radio por `fishing_hours`
- **Filtros UI:** Año (2016/2020/Todos), Mes (1-12/Todos), Arte (6 tipos/Todos), Bandera (6/Todas)
- **Contador dinámico:** `X / 9,960 celdas` visible en panel de filtros

### 6.8 Componentes Principales

| Componente | Archivo | Función |
|------------|---------|---------|
| `RiskMap.tsx` | 45 KB | Mapa Leaflet H3 + navegación rápida 4 terminales GNL + 15 capas |
| `ZoneCards.tsx` | 9 KB | Tarjetas riesgo PANGAS con barras ASCII `[██████░░░░]` |
| `SpeciesPanel.tsx` | 8 KB | Especies IUCN (badges monospace `[CAM]`, `[TIB]`, `[RAY]`, `[PAR]`) |
| `MethodologyPanel.tsx` | 5 KB | Fórmulas IERC + Monte Carlo |
| `CoverageModal.tsx` | 7 KB | Matriz vacíos + ingestas institucionales |
| `MiaInspectorModal.tsx` | 14 KB | Visor planos MIA (macro/micro/distribución) |
| `Header.tsx` | 7 KB | System ticker, brand, metrics strip |
| `RiskBadge.tsx` | 1 KB | Badge nivel de riesgo |
| `ExportModal.tsx` | 12 KB | Exportación GeoJSON/CSV/GeoPackage |
| `Heatmap.tsx` | 1.4 KB | Wrapper Leaflet.heat con `useMap` hook |

### 6.9 Navegación Rápida a Terminales GNL (Sidebar)

| Terminal | Ubicación | Lat | Lon | Zoom | Precisión | Estatus |
|----------|-----------|-----|-----|------|-----------|---------|
| SAGUARO ENERGÍA GNL | Puerto Libertad, Sonora | 29.9058 | -112.6880 | 13 | [APROXIMADO] | Proposed / Pre-FID |
| AMIGO LNG | Guaymas, Sonora | 27.9229 | -110.8681 | 13 | [EXACTO] | Proposed / Pre-FID |
| VISTA PACÍFICO (FLNG) | Topolobampo, Sinaloa | 25.5891 | -109.1038 | 13 | [CALCULADO] | CANCELADO (Feb 2026) |
| GNL COSALÁ | Mazatlán / Zapopan | 23.2500 | -106.4200 | 11 | [APROXIMADO] | En Evaluación ASEA |

---

## 7. ENTREGABLE ESPACIAL GEOPACKAGE v1.1 (META 1 POA 2026)

**Ubicación:** `deliverables/v1_geopackage/ierc_golfo_california.gpkg` (5.9 MB, 9 capas)

### 7.1 Capas Vectoriales Incluidas

| Capa | Geometría | Entidades | Descripción |
|------|-----------|-----------|-------------|
| `proyectos_gnl` | Point | 11 | Infraestructura GNL con scores riesgo pesquero e IERC |
| `gasoductos_infraestructura_gnl` | LineString | 2 | Trazados ductos gas natural (Sonora, Saguaro, Guaymas) |
| `localidades_estudio_ierc` | Point | 3 | Comunidades POA: Punta Chueca Comca'ac, Puerto Libertad, Guaymas |
| `anp_habitats_criticos` | Polygon | 2 | ANPs CONANP + hábitats marinos críticos |
| `zonas_pesqueras_pangas` | MultiPolygon | 17 | Polígonos pesca artesanal con `uid_espaciotemporal` |
| `grilla_h3_riesgo` | Polygon | 5,244 | Malla H3 adaptativa (Res 8 mar / Res 9 portuario) con IERC |
| `riqueza_relativa_pesquera` | MultiPolygon | 11,065 | Malla espacial riqueza biológica pesquera acumulada |
| `batimetria_contornos_gebco` | LineString | 1,146 | Contornos batimétricos GEBCO 2024 |
| `poligonos_detalle_saguaro` | Polygon | Variable | Detalle proyecto Saguaro (MIA 181V) |

### 7.2 Esquema `grilla_h3_riesgo` (Capa Principal IERC)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `h3_index` | String | Identificador H3 |
| `resolucion` | Integer | 8 o 9 |
| `latitud_centroide` | Real | Centroide lat |
| `longitud_centroide` | Real | Centroide lon |
| `ierc_score` | Real | Score IERC 0-1 |
| `nivel_riesgo` | String | Muy Bajo/Bajo/Medio/Alto/Muy Alto |
| `amenaza_score` | Real | Componente H |
| `exposicion_score` | Real | Componente H |
| `sensibilidad_score` | Real | Componente V |
| `dependencia_score` | Real | Componente V |
| `biocultural_score` | Real | Componente V |
| `capacidad_adaptativa_score` | Real | Componente V |
| `distancia_proyecto_mas_cercano_km` | Real | Proximidad GNL |

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

Documentada en: `docs/metodologia/Inventario_y_Matriz_Vacios_Geoespaciales_EG.md`

| Capa | Vacío Identificado | Impacto | Acción |
|------|-------------------|---------|--------|
| GFW | No distingue pesca ilegal vs legal | Alto | Cruzar con VMS nacional |
| NASA | Gaps por nubes (clorofila) | Medio | Interpolación espacio-temporal |
| PANGAS | Solo 3 comunidades POA | Alto | Expandir muestreo |
| ASEA | MIA PDFs no parseados completamente | Medio | OCR + NLP para extraer coordenadas |
| Socioeconómico | Datos INEGI 2020 desactualizados | Alto | Encuestas de campo 2026 |
| **Ductos CNIH** | **Solo 24 tramos vs red completa** | **Medio** | **Solicitar WFS completo CNIH** |

---

## 9. ESTRUCTURA DEL REPOSITORIO

```
ierc-gnl-project/
├── causanaturadata/            # Documentos oficiales (POA 2026, Manual Metodológico)
├── dashboard/                  # Dashboard Web (Next.js 16, React, Tailwind)
│   ├── src/app/components/     # 11 componentes React
│   ├── public/data/            # 18 archivos GeoJSON estáticos (incl. ductos_cnih.geojson)
│   └── AGENTS.md / CLAUDE.md   # Instrucciones para agentes IA
├── data/                       # Insumos geográficos de gabinete
│   ├── raw/                    # BRONZE (14 fuentes)
│   │   └── gasoductos/         # NUEVO: 5 GeoJSON CNIH/SENER ArcGIS
│   ├── lakehouse/              # SILVER + GOLD (particionado H3)
│   │   ├── processed/          # SILVER (14 datasets)
│   │   │   └── gasoductos/     # NUEVO: ductos_cnih.parquet + anp_ramsar_cnih.parquet
│   │   └── curated/            # GOLD (6 productos)
│   └── schemas/                # Schemas JSON
├── deliverables/
│   ├── v1_geopackage/          # ENTREGABLE META 1 (9 capas)
│   │   ├── ierc_golfo_california.gpkg
│   │   ├── build_geopackage.py
│   │   └── GEOPACKAGE_METADATA.md
│   └── v2_geopackage/          # Versión con capas campo (12 capas)
├── docs/
│   └── metodologia/
│       ├── Nota_Metodologica_Ajustada_JCB_EG.md
│       └── Inventario_y_Matriz_Vacios_Geoespaciales_EG.md
├── src/
│   ├── data/
│   │   ├── ingestion/          # Pipeline ingesta (9 ingesters + base + factory + ductos_cnih.py)
│   │   ├── catalog/            # DataCatalog JSONL + lineage
│   │   └── lakehouse/          # LocalFileStorage (Parquet + ZSTD)
│   └── engine/                 # Validadores, IERC, Monte Carlo, Responsible AI
├── config/
│   ├── lakehouse.yaml          # Config lakehouse, CDC keys, particionamiento
│   └── data_catalog.yaml       # Catálogo declarativo 14 Silver + 6 Gold
├── scripts/                    # 26+ scripts operacionales (incl. clean_ductos_cnih.py)
├── tests/unit/                 # 45 tests (storage, catalog, h3, ierc, RAI, spatial, MC, E2E)
├── .github/workflows/ci.yml    # Pipeline CI/CD 5 jobs
└── README.md                   # Este archivo (actualizado v2.2)
```

---

## 10. REPRODUCIBILIDAD Y COMANDOS

### 10.1 Prerrequisitos
- Python 3.11+ (venv en `.venv/`)
- Node.js 18+ (para dashboard)
- `netCDF4` para ingesta NASA (opcional, pendiente instalar)

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

### 10.3 Pipeline End-to-End (incluyendo ductos CNIH)
```bash
# 1. Inicializar Lakehouse y Catálogo JSON
PYTHONPATH=. ./.venv/bin/python3 scripts/init_lakehouse.py

# 2. Computar Features Gold IERC H3
PYTHONPATH=. ./.venv/bin/python3 scripts/compute_ierc_features.py

# 3. Ingesta ductos CNIH/SENER (NUEVO)
PYTHONPATH=. ./.venv/bin/python3 scripts/gasoductos/clean_ductos_cnih.py

# 4. Exportar insumos para Dashboard Web
PYTHONPATH=. ./.venv/bin/python3 scripts/prepare_dashboard_data.py
```

### 10.4 Ejecutar Dashboard Interactivo
```bash
cd dashboard
npm install
npm run dev
# http://localhost:3001
```

---

## 11. CI/CD Pipeline

El proyecto incluye un pipeline de CI completo (`.github/workflows/ci.yml`) con 5 jobs:

| Job | Descripción |
|-----|-------------|
| **test** | Unit tests Python (45 tests) |
| **lint** | Syntax check en módulos core |
| **verify-cdc** | Verificación CDC exact-once + Schema contract |
| **dashboard-build** | Build Next.js 16 |
| **summary** | Resumen consolidado |

---

## 12. Cita Oficial

**Causa Natura Center (2026):** *Índice Espacial de Riesgo Socioeconómico para Comunidades (IERC) ante proyectos de GNL en el Golfo de California*. Elaborado por Juan Carlos Barrera (JCB) y Enrique Gorosave Meza (EG).

---

## 13. Documentación Técnica Vinculada

- **[REPORTE_INVENTARIO_DATOS_IERC_GNL_v2.2_ENRIQUE_GOROSAVE.md](REPORTE_INVENTARIO_DATOS_IERC_GNL_v2.2_ENRIQUE_GOROSAVE.md)** — Este reporte oficial v2.2
- **[REPORTE_INVENTARIO_DETALLADO_IERC_GNL.md](REPORTE_INVENTARIO_DETALLADO_IERC_GNL.md)** — Inventario técnico SILVER/GOLD
- **[REPORTE_INVENTARIO_GEOPACKAGE.md](REPORTE_INVENTARIO_GEOPACKAGE.md)** — Metadata entregable GeoPackage Meta 1
- **[config/lakehouse.yaml](config/lakehouse.yaml)** — Configuración lakehouse, CDC keys, particionamiento
- **[config/data_catalog.yaml](config/data_catalog.yaml)** — Catálogo declarativo 14 Silver + 6 Gold
- **[docs/metodologia/Nota_Metodologica_Ajustada_JCB_EG.md](docs/metodologia/Nota_Metodologica_Ajustada_JCB_EG.md)** — Formulación matemática IERC
- **[docs/metodologia/Inventario_y_Matriz_Vacios_Geoespaciales_EG.md](docs/metodologia/Inventario_y_Matriz_Vacios_Geoespaciales_EG.md)** — Matriz de vacíos geográficos
- **[.github/workflows/ci.yml](.github/workflows/ci.yml)** — Pipeline CI/CD completo

---

*Fin del reporte v2.2 — 2026-08-07 — Enrique Gorosave Meza — Causa Natura Center*