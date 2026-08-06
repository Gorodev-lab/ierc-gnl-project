# Phase 1 Complete — Deep Research: Proyectos Similares a IERC-GNL

**Fecha**: 2026-08-05  
**Fuentes**: Google Scholar, GitHub, FAO, World Bank, ICES, UKRI, IFC, TNC, NOAA  
**Queries ejecutadas**: 13  
**Resultados totales**: 12  
**Archivos**: `docs/research/phase1/phase1_results_20260805_231301.{csv,json}`

---

## Resumen de Hallazgos

| Score | Conteo | Descripción |
|-------|--------|-------------|
| 4 | 1 | Match casi completo (falta H3 + multiplicativo + output interactivo) |
| 3 | 7 | Match parcial fuerte (3-4 criterios) |
| 2 | 3 | Match débil (2 criterios) |
| 1 | 1 | Mínimo (solo pesca artesanal) |
| 0 | 0 | — |

**Ningún proyecto alcanza score ≥ 5** (requerido para "casi idéntico").

---

## Top Result — Score 4: IFC "Addressing Project Impacts on Fishing-based Livelihoods" (2015)

| Criterio | Match |
|----------|-------|
| Pesca artesanal + LNG | ✅ |
| Vulnerabilidad social | ✅ |
| Evaluación espacial | ✅ |
| Índice multiplicativo (H×V) | ❌ |
| Grid H3 / hexagonal | ❌ |
| Dashboard / GeoPackage | ❌ |
| Código abierto | ❌ (PDF only) |

**Gap crítico**: Metodología IFC usa evaluación cualitativa/cuantitativa simple, no índice espacial H3 multiplicativo.

---

## Proyectos Score 3 — Brechas Comunes

| Proyecto | Fortaleza | Gap vs IERC |
|----------|-----------|-------------|
| **Mediterranean QSR 2017** | Spatial risk index + small-scale fisheries | No LNG, no H3, no multiplicativo |
| **Mozambique Gas Pipeline (Norad)** | Artisanal + gas pipeline + vulnerability | No H3, no multiplicativo, no dashboard |
| **Angola Gas-to-Energy EIA 2022** | Artisanal + gas + vulnerability | No H3, no multiplicativo |
| **UKRI "optimising environment and fishing interests"** | Spatial risk-layers + fishing gear + gas infra | No H3, no multiplicativo, no LNG |
| **TNC Fisheries@Risk 2020** | Risk index + small-scale + social vulnerability | Climate-focused, no LNG/gas, no H3 |
| **EXIM Mozambique LNG EIA 2019** | Artisanal + LNG terminals | No spatial index, no H3, no multiplicativo |
| **Argentina artisanal + LNG (London 2017)** | Social-ecological + LNG conflict | No H3, no multiplicativo, no risk index formal |

---

## Criterios NO Cubiertos por NINGÚN Proyecto

| Criterio | Cobertura Global |
|----------|------------------|
| **Índice multiplicativo (H × V)** | 0/12 |
| **Grid H3 (Uber) / hexagonal** | 0/12 |
| **Dashboard interactivo / GeoPackage output** | 0/12 |
| **LNG + pesca artesanal + H3 + multiplicativo** | 0/12 |

---

## Conclusión Fase 1

**No existe proyecto "prácticamente idéntico" a IERC-GNL** (score ≥ 5).

- El proyecto IFC (score 4) es el más cercano conceptualmente pero usa metodología distinta (cualitativa, no H3).
- UKRI tiene "spatial risk-layers" + gas + pesca pero es oil/gas genérico, no LNG específico, y sin H3.
- TNC Fisheries@Risk es el mejor índice de riesgo pesquero pero es climate-only, sin infraestructura energética.

---

## Recomendación: **Avanzar a Fase 2 con Top 3 para Deep Dive**

1. **IFC (2015)** — Metodología livelihoods + LNG, contactar autores
2. **UKRI NE/P016537/1** — Spatial risk-layers + gas + pesca, revisar repo/datos
3. **TNC Fisheries@Risk** — Índice riesgo pesquero validado, adaptar fórmula

**Próximo paso**: Ejecutar Fase 2 (Semana 2) — Deep dive top 3 + contacto autores.

---

## Archivos Generados

- `docs/research/phase1/phase1_results_20260805_231301.csv` — Tabla completa
- `docs/research/phase1/phase1_results_20260805_231301.json` — Datos estructurados
- `scripts/save_phase1_results.py` — Script de guardado