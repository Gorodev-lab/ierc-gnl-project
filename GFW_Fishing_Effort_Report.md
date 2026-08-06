# GFW (Global Fishing Watch) — Estado de Datos y Visualización

**Fecha**: 2026-08-06  
**Proyecto**: IERC-GNL — Golfo de California  
**Fuente**: Zenodo Record 14982712 + GFW Public API v3

---

## 1. Resumen de Disponibilidad

| Fuente | Estado | Registros Procesados | Cobertura Temporal |
|--------|--------|---------------------|-------------------|
| **Zenodo CSV (v3)** | ✅ Local (109 MB) | 0 en lakehouse (pendiente ingesta completa) | 2012-2023 |
| **Zenodo ZIP 2020** | ✅ Local (779 MB) | 22 vessels (fallback) | 2020 |
| **Zenodo ZIP 2016** | ✅ Local (40 MB) | 0 | 2016 |
| **GFW API v3 (token)** | ⚠️ Token existe, **endpoints 422/404** | 0 | — |

> **Conclusión**: La API v3 falla consistentemente (422 Unprocessable Entity en `/events`, `/vessels/search`). Única fuente usable hoy: **archivos Zenodo locales**.

---

## 2. Datos en Lakehouse (Procesados)

```
lakehouse/processed/gfw/
├── vessels/
│   └── part-0.parquet          # 22 embarcaciones (solo metadata, SIN H3)
└── fishing_effort_h3/
    └── year=2026/month=08/
        ├── part-0.parquet      # 22 rows (DUPLICADO de vessels, SIN fishing_hours ni H3)
        └── h3_cell=8848055949fffff/...  # Vacío
```

**Problema**: El ingester cayó en fallback a vessels pero escribió en `fishing_effort_h3` con schema incorrecto (falta `lat`, `lon`, `fishing_hours`, `h3_cell`, `gear_type`).

---

## 3. Capas GeoJSON Disponibles para Dashboard

| Archivo | Origen | Registros | Uso en Mapa |
|---------|--------|-----------|-------------|
| `zpesca_pangas_sample.geojson` | PANGAS (Moreno-Báez) | 4,241 | ✅ Capa "PANGAS Multiespecie" |
| `zpesca_buceo_sample.geojson` | PANGAS Buceo | 249 | ✅ Capa "Pesca por Buceo" |
| `zpesca_chinchorro_sample.geojson` | PANGAS Chinchorro | 2,209 | ✅ Capa "Chinchorro de Línea" |
| `zpesca_redes_sample.geojson` | PANGAS Redes | 1,263 | ✅ Capa "Redes de Enmalle" |
| `zpesca_redes_manta_camaron_sample.geojson` | PANGAS Camarón/Manta | 783 | ✅ Capa "Camarón / Manta" |
| `zpesca_trampa_sample.geojson` | PANGAS Trampa | 360 | ✅ Capa "Trampas Jaiberas" |
| `riqueza_relativa_sample.geojson` | Riqueza Pesquera | 11,065 | ✅ Capa "Riqueza Relativa" |

> **GFW nativo NO está exportado a `/dashboard/public/data/`**. Solo PANGAS (Moreno-Báez 2011/2012).

---

## 4. Recomendación de Visualización (Mapa)

### Opción A — Usar PANGAS como proxy (RECOMENDADA, ya implementada)
```tsx
// Ya existe en RiskMap.tsx líneas 500-580
{activeLayers.pangas && layersData.pangas && (
  <GeoJSON ... style={getFishingColor} ... />
)}
```
- 6 capas por arte de pesca + riqueza relativa
- Densidad de esfuerzo normalizada 0-1
- Listo para activar en Layer Control

### Opción B — Generar capa GFW H3 desde Zenodo (requiere procesamiento)
```bash
# 1. Ingesta completa 2020-2023 (tarda ~30 min)
PYTHONPATH=. ./.venv/bin/python -c "
from src.data.ingestion.gfw_fishing import create_gfw_ingester
from src.data.catalog.catalog import Catalog
from src.data.lakehouse.storage import Storage
catalog = Catalog()
storage = Storage()
ingester = create_gfw_ingester('fishing_effort', catalog, storage, target_years=[2020,2021,2022,2023])
for df in ingester.extract(): pass  # full pipeline
"

# 2. Exportar a GeoJSON para dashboard
PYTHONPATH=. ./.venv/bin/python scripts/prepare_dashboard_data.py  # añadir lógica GFW
```

### Opción C — Capa de calor simple (heatmap) desde Parquet existente
```tsx
// Si se genera H3 grid con fishing_hours sumados por celda
const gfwHeatmap = await fetch('/data/gfw_fishing_h3.geojson').then(r => r.json())
<GeoJSON data={gfwHeatmap} style={feat => ({
  fillColor: interpolateHeat(feat.properties.total_fishing_hours),
  fillOpacity: 0.6,
  weight: 0
})} />
```

---

## 5. Reporte Descargable (.md)

Ver archivo adjunto: `GFW_Fishing_Effort_Report.md` (generado abajo)

---

## 6. Próximos Pasos (Prioridad)

| Prioridad | Acción | Esfuerzo |
|-----------|--------|----------|
| **ALTA** | Corregir ingester GFW: separar vessels vs fishing_effort, validar schema H3 | 1-2h |
| **ALTA** | Procesar ZIP 2020 completo → Parquet particionado H3 (year/month) | 30 min CPU |
| **MEDIA** | Exportar `gfw_fishing_h3.geojson` a `/dashboard/public/data/` | 5 min |
| **MEDIA** | Añadir layer `gfw_fishing` a `RiskMap.tsx` (toggle + heatmap) | 15 min |
| **BAJA** | Investigar GFW API v3 scopes correctos (contactar GFW) | Variable |

---

## 7. Contacto / Referencias

- **GFW API Docs**: https://globalfishingwatch.org/our-data/api/
- **Zenodo Record**: https://zenodo.org/records/14982712 (Global Fishing Watch v3)
- **PANGAS Original**: Moreno-Báez et al. 2011, 2012 (datos 2006-2010)
- **IERC Metodología**: `docs/metodologia/Nota_Metodologica_Ajustada_JCB_EG.md`