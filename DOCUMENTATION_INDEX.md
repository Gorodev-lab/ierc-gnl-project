# Documentación IERC-GNL — Índice Principal

> **Proyecto:** Índice Espacial de Riesgo Socioeconómico para Comunidades (GNL)
> **Organización:** Causa Natura Center
> **POA:** 2026-2028
> **Última actualización:** 2026-08-06

---

## 📚 Documentos Principales

| Documento | Descripción | Versión |
|-----------|-------------|---------|
| **[README.md](README.md)** | Resumen ejecutivo, arquitectura, instalación, cita oficial, CI/CD | v2.1 |
| **[REPORTE_INVENTARIO_DATOS_IERC_GNL_v2.1_ENRIQUE_GOROSAVE.md](REPORTE_INVENTARIO_DATOS_IERC_GNL_v2.1_ENRIQUE_GOROSAVE.md)** | **Reporte oficial detallado** — Inventario SILVER/GOLD + capas dashboard + cadena ingesta y auditoría + Responsible AI — *Autor: Enrique Gorosave Meza* | v2.1 (2026-08-06) |
| **[INVENTARIO_DATOS_IERC_GNL_v2.1.md](INVENTARIO_DATOS_IERC_GNL_v2.1.md)** | Inventario técnico SILVER/GOLD + cadena ingesta + auditoría + Responsible AI | v2.1 (2026-08-06) |
| **[REPORTE_INVENTARIO_GEOPACKAGE.md](REPORTE_INVENTARIO_GEOPACKAGE.md)** | Metadata entregable GeoPackage Meta 1 (OGC v1.1) | v1.1 |
| **[DATA_INVENTORY_REPORT.md](DATA_INVENTORY_REPORT.md)** | Inventario completo SILVER/GOLD + cadena ingesta + auditoría | v2.0 (versión anterior) |

---

## ⚙️ Configuración del Sistema

| Archivo | Propósito |
|---------|-----------|
| **[config/lakehouse.yaml](config/lakehouse.yaml)** | Config lakehouse: capas, particionamiento H3, CDC keys, compresión |
| **[config/data_catalog.yaml](config/data_catalog.yaml)** | Catálogo declarativo: 12 datasets Silver + 6 Gold con schemas completos |

---

## 📐 Metodología

| Documento | Contenido |
|-----------|-----------|
| **[docs/metodologia/Nota_Metodologica_Ajustada_JCB_EG.md](docs/metodologia/Nota_Metodologica_Ajustada_JCB_EG.md)** | Formulación matemática IERC: $R = H \times V$, componentes, pesos |
| **[docs/metodologia/Inventario_y_Matriz_Vacios_Geoespaciales_EG.md](docs/metodologia/Inventario_y_Matriz_Vacios_Geoespaciales_EG.md)** | Matriz de vacíos geográficos por capa y comunidad |

---

## 🔧 Código Fuente (src/)

```
src/
├── data/
│   ├── ingestion/
│   │   ├── base.py              # BaseIngester + CDC exact-once + Schema contract
│   │   ├── factory.py           # Factory pattern para 9 ingesters
│   │   ├── asea_mias.py         # ASEA MIA + CDC (proyecto_id, 10 hash cols)
│   │   ├── gfw_fishing.py       # GFW API v3 fishing effort + vessels
│   │   ├── nasa_oceancolor.py   # NASA MODIS NetCDF → H3 (chlor_a, SST)
│   │   ├── tnc_vector.py        # TNC Shapefile → H3 grid (area_weight)
│   │   ├── bathymetry.py        # GEBCO vector → H3 multi-res
│   │   └── pangas_vector.py     # PANGAS GeoJSON + uid_espaciotemporal
│   ├── catalog/
│   │   └── catalog.py           # DataCatalog JSONL + register_derived_dataset()
│   └── lakehouse/
│       └── storage.py           # LocalFileStorage (Parquet + ZSTD, Hive partitioning)
└── engine/
    ├── spatial_validator.py     # Validación bbox, no-deformación UTM12N, vacíos Moreno-Báez
    ├── ierc_calculator.py       # IERC aditivo (6 componentes) + multiplicativo
    ├── monte_carlo_engine.py    # Simulación N=1000 iteraciones
    └── responsible_ai.py        # Explainability, bias detection, smooth failing
```

### Pipeline de Ingesta (v2.0)

```
FACTORY → BASE INGESTER (CDC + Schema validation) → SILVER (H3-partitioned)
                              ↓
                      CATALOG TRACKING (runs.jsonl)
                              ↓
                      GOLD (joins H3-8 + scoring + Monte Carlo)
                              ↓
                      DERIVED VERSIONING (lineage en schema.lineage)
```

---

## 🧪 Tests

```bash
PYTHONPATH=. ./.venv/bin/python3 -m pytest tests/unit/ -v
# 45 tests passing:
#   test_storage_catalog.py (4)       - catalog + storage roundtrip + predicate pushdown
#   test_utils_h3.py (4)              - H3 cells, vectorized, grid, temporal partitions
#   test_utils_ierc.py (4)            - IERC bounds, weights, components, adaptive capacity
#   test_engine_ierc.py (3)           - IERC aditivo, multiplicativo, bounds
#   test_engine_responsible_ai.py (12) # Explainability, bias detection, smooth failing, team workflow
#   test_engine_spatial_validator.py (17) # Bbox, UTM12N, vacíos Moreno-Báez, H3 validation
#   test_engine_monte_carlo.py (1)    - Integration test N=1000
#   test_pipeline_e2e.py (1)          - Pipeline end-to-end
```

---

## 📊 Dashboard (Next.js 16)

| Ruta | Componente | Descripción |
|------|------------|-------------|
| `dashboard/src/app/components/RiskMap.tsx` | Mapa Leaflet H3 + GNL terminals |
| `dashboard/src/app/components/ZoneCards.tsx` | Tarjetas riesgo PANGAS (ASCII bars) |
| `dashboard/src/app/components/SpeciesPanel.tsx` | Especies IUCN (badges monospace) |
| `dashboard/src/app/components/MethodologyPanel.tsx` | Fórmulas + Monte Carlo |
| `dashboard/src/app/components/CoverageModal.tsx` | Matriz vacíos + ingestas |
| `dashboard/src/app/components/MiaInspectorModal.tsx` | Visor planos MIA (macro/micro/distribución) |
| `dashboard/src/app/components/Header.tsx` | System ticker, brand, metrics strip |
| `dashboard/src/app/components/RiskBadge.tsx` | Badge nivel de riesgo |
| `dashboard/src/app/components/ExportModal.tsx` | Export GeoJSON/CSV/GeoPackage |

**Estándar:** Esoteria Design System v1.1 — IBM Plex Mono, `#0A0A0A`, `border-radius: 0`, sin sombras.

---

## 🚀 Comandos Rápidos

```bash
# Tests
PYTHONPATH=. ./.venv/bin/python3 -m pytest tests/unit/ -v

# Lakehouse init
PYTHONPATH=. ./.venv/bin/python3 scripts/init_lakehouse.py

# Compute Gold features
PYTHONPATH=. ./.venv/bin/python3 scripts/compute_ierc_features.py

# Dashboard
cd dashboard && npm run dev  # localhost:3001

# Dashboard build
cd dashboard && npm run build
```

---

## 🔍 Verificaciones v2.1 (2026-08-06)

| Feature | Verificación |
|---------|--------------|
| **CDC exact-once** | Run1=2 inserts, Run2=1 insert, Run3=0 inserts ✅ |
| **Schema contract** | Missing columns / Extra columns / Type mismatch detected ✅ |
| **Derived versioning** | Lineage embebido en `schema.lineage` ✅ |
| **Responsible AI** | 12 tests: explainability, bias detection, smooth failing, team workflow ✅ |
| **Spatial validator** | 17 tests: bbox, UTM12N, vacíos Moreno-Báez, H3 validation ✅ |

---

## 👥 Autores

- **Juan Carlos Barrera (JCB)** — Consultor Senior, Especialista Pesquero/Socioambiental
- **Enrique Gorosave Meza (EG)** — Analista de Datos GIS, Causa Natura Center

---

## 📄 Licencia

MIT — Ver [LICENSE](LICENSE)

---

*Documentación generada y mantenida por el equipo técnico IERC-GNL para Causa Natura Center.*