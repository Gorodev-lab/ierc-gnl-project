# Phase 2 Complete — Deep Dive Top 3 Proyectos Similares

**Fecha**: 2026-08-06  
**Proyectos analizados**: IFC 2015, UKRI CA-PipeFish, TNC Fisheries@Risk 2020

---

## 1. IFC 2015 — "Addressing Project Impacts on Fishing-based Livelihoods"

**Documento**: *Good Practice Handbook* (PDF, 2015)  
**Contacto**: `asksustainability@ifc.org` | www.commdev.org  
**Autor principal**: AM Esteves (IFC/World Bank)

### Metodología
- **Enfoque**: *Livelihoods-based assessment* — baseline + impact assessment + mitigation
- **Estructura**: Screening → Scoping → Baseline → Impact Assessment → Mitigation/Monitoring
- **Índice de riesgo**: **NO usa índice multiplicativo**. Usa matriz cualitativa (significancia × probabilidad)
- **Grid espacial**: NO usa H3. Usa GIS convencional (shapefiles, zonas de influencia)
- **Pesca**: Artesanal + industrial, enfoque en *livelihoods* (medios de vida)
- **Infraestructura**: LNG, puertos, dragado, ductos, planta procesamiento
- **Output**: Handbook (PDF) + hojas de cálculo Excel para baseline

### Datos / Código
- **Repositorio**: Ninguno público (PDF only)
- **Contacto IFC**: `asksustainability@ifc.org`
- **Autora clave**: AM Esteves (publica extensivamente sobre livelihoods + pesca)

### Gap vs IERC
| IERC | IFC |
|------|-----|
| H3 + multiplicativo (H×V) | Matriz cualitativa |
| Grid global H3 Res 8/9 | Zonas de influencia GIS |
| Dashboard/GeoPackage | PDF Handbook + Excel |
| Pesca PANGAS + H3 | Livelihoods genérico |

### Contacto sugerido
> **Email**: `asksustainability@ifc.org`  
> **Asunto**: "IFC Fishing Livelihoods Handbook 2015 — methodological details for spatial risk index adaptation"  
> **Preguntas clave**: ¿Consideraron grid H3? ¿Validaron índice multiplicativo? ¿Datos pesqueros geoespaciales disponibles?

---

## 2. UKRI NE/P016537/1 — CA-PipeFish / PipeFish (2016-2021)

**Proyecto**: *Optimising environment and fishing interests* — Pipeline decommissioning  
**PI**: Thomas Wilding (SAMS - Scottish Association for Marine Science)  
**URL**: https://gtr.ukri.org/projects?ref=NE%2FP016537%2F1  
**Contacto PI**: Thomas Wilding (ORCID en GtR)

### Metodología
- **Enfoque**: *Spatial risk-layers* para decommissioning de pipelines (oil & gas, NO LNG)
- **Estructura**: 3 pasos — (1) Collate data (ROV video, VMS fishing, snagging) → (2) Spatial risk-layers flexibles → (3) Embed en protocolo decommissioning
- **Índice de riesgo**: **Spatial risk-layers** — capas combinables (pesca intensity × snagging × conservation features). **NO multiplicativo H×V formal**, pero concepto similar de capas ponderadas.
- **Grid**: NO H3. Usa grid nacional UK (shapefiles, NMPi)
- **Pesca**: Comercial (demersal, pelágico) + VMS data 2007-2015 + snagging incidents
- **Infraestructura**: **Pipelines oil/gas** (UKCS) — 27,000 km instalados, 5,600 km a decommissionar
- **Output**: 
  - Spatial data layers en NMPi (National Marine Plan interactive)
  - Shapefiles descargables: `uk-fishing-intensity-associated-oil-and-gas-pipelines-2007-2015`
  - Publicaciones ICES JMS (4 papers)

### Datos / Código
- **Datos abiertos**: Shapefiles en Marine Scotland: https://data.marine.gov.scot/dataset/uk-fishing-intensity-associated-oil-and-gas-pipelines-2007-2015
- **Publicaciones**: 4 papers ICES JMS (2017-2019)
- **PI**: Thomas Wilding (SAMS) — thomas.wilding@sams.ac.uk
- **Colaboradores**: Marine Scotland Science, NatureScot, Oil & Gas UK, SFF, BP, Shell

### Gap vs IERC
| IERC | CA-PipeFish |
|------|-------------|
| LNG terminals + ductos | Pipelines oil/gas (decommissioning) |
| H3 Res 8/9 global | Grid UK national (shapefiles) |
| Multiplicativo H×V (fishing + social) | Risk-layers (fishing + conservation + snagging) |
| México Golfo California | UK Continental Shelf |
| Dashboard + GeoPackage | NMPi layers + shapefiles |

### Contacto sugerido
> **Email**: thomas.wilding@sams.ac.uk (cc: raeanne.miller@sams.ac.uk)  
> **Asunto**: "CA-PipeFish spatial risk-layers — methodological details for H3 adaptation in LNG context"  
> **Preguntas clave**: 
> - ¿Metodología ponderación capas (fishing intensity × snagging × conservation)?
> - ¿Validación con stakeholders (SFF, O&G UK)?
> - ¿Datos VMS + snagging disponibles para replicación?
> - ¿Consideraron grid H3 vs shapefiles?

---

## 3. TNC Fisheries@Risk 2020 — "Fisheries at Risk: Vulnerability of Fisheries to Climate Change"

**Documento**: *Technical Report* (PDF, 117 páginas) + Summary Report  
**Autores**: N. Heck, V. Agostini, B. Reguero, K. Pfliegner, P. Mucke, L. Kirch, M.W. Beck  
**URL**: https://www.nature.org/content/dam/tnc/nature/en/documents/Fisheries-at-Risk-Technical-Report.pdf  
**Contacto**: `europe@tnc.org` | Nadine Heck (ECU/UCSC) — nadine.heck@ecu.edu

### Metodología
- **Framework**: IPCC AR5 Risk Framework (Hazard × Exposure × Vulnerability)
- **Índice**: **Fisheries@Risk (F@R) = H × E × V**  
  - **Hazard (H)**: SST warming, ocean acidification, cyclones, SLR, wave action
  - **Exposure (E)**: 50% catch (landing × hazard), 50% fishers (SLR + cyclones + waves)
  - **Vulnerability (V) = Sensitivity (S) + Lack of Adaptive Capacity (1-AC)**
    - **S**: Pollution, fishing practices, habitat degradation, coastal pop density
    - **AC**: Gear diversity, fleet size, MPA coverage, GDP, governance
- **Grid**: **NO H3**. País-nivel (EEZ) + 0.25° grid para hazards
- **Pesca**: Nacional (EEZ-level) — captura + fishers per capita
- **Infraestructura**: **NO LNG/gas**. Climate-only (SST, acidificación, ciclones, SLR)
- **Output**: 
  - Índice por país (195 EEZs) — tabla completa en Appendix
  - Technical Report + Summary Report (PDF)
  - Datos: `nature.org/GlobalFisheryRiskReductionTechnicalReport`

### Fórmula (páginas 428-429 del PDF)
```
R = H × E × V
V = S + (1 - AC)
E = 50% Exposure_catch + 50% Exposure_fishers
```
- Indicadores normalizados 0-1 (min-max)
- Sub-indicadores log-transformados antes de normalizar
- Media aritmética para combinar sub-indicadores

### Datos / Código
- **Datos**: Nacional (EEZ), globales (195 países)
- **Fuentes**: FAO FishStat, OHI, FAOSTAT, World Bank, WDPA, OHI 2016
- **Repositorio**: Ninguno (PDF only). Contacto: `europe@tnc.org`
- **Contacto técnico**: Nadine Heck (ECU/UCSC Coastal Resilience Lab) — nadine.heck@ecu.edu

### Gap vs IERC
| IERC | TNC F@R |
|------|---------|
| LNG + gas infrastructure | Climate-only (SST, acidificación, ciclones) |
| H3 Res 8/9 local (Golfo) | EEZ nacional + 0.25° grid global |
| Multiplicativo H×V (fishing + social) | IPCC H×E×V (climate × exposure × vulnerability) |
| México Golfo California | Global (195 EEZs) |
| Pesca artesanal PANGAS + H3 | EEZ-level (catch + fishers per capita) |

### Contacto sugerido
> **Email**: `europe@tnc.org` (cc: nadine.heck@ecu.edu)  
> **Asunto**: "Fisheries@Risk Index 2020 — methodological details for H3 adaptation in LNG risk context"  
> **Preguntas clave**:
> - ¿Consideraron grid H3 vs EEZ para resolución local?
> - ¿Cómo validaron ponderación 50/50 catch/fishers en Exposure?
> - ¿Datos sub-nacionales (sub-EEZ) disponibles para México?
> - ¿Consideraron infraestructura energética (LNG) como hazard adicional?

---

## Matriz Comparativa Consolidada

| Criterio | IERC-GNL | IFC 2015 | CA-PipeFish | TNC F@R 2020 |
|----------|----------|----------|-------------|--------------|
| **Índice multiplicativo** | ✅ H×V | ❌ Cualitativo | ⚠️ Risk-layers | ✅ H×E×V (IPCC) |
| **Grid H3** | ✅ Res 8/9 | ❌ GIS zones | ❌ UK grid | ❌ EEZ + 0.25° |
| **LNG/Gas** | ✅ Terminal + ductos | ✅ LNG + ductos | ⚠️ Pipelines oil/gas | ❌ Climate-only |
| **Pesca artesanal** | ✅ PANGAS H3 | ✅ Livelihoods | ⚠️ Comercial VMS | ⚠️ EEZ-level catch |
| **Vulnerabilidad social** | ✅ 5 componentes | ✅ Livelihoods | ❌ Conservation | ✅ S + (1-AC) |
| **Dashboard/GeoPackage** | ✅ Web + GPKG | ❌ PDF + Excel | ✅ NMPi + shapefiles | ❌ PDF + tablas |
| **Código abierto** | ✅ Repo + datos | ❌ PDF only | ✅ Shapefiles abiertos | ❌ PDF only |
| **Contacto activo** | N/A | asksustainability@ifc.org | thomas.wilding@sams.ac.uk | europe@tnc.org / nadine.heck@ecu.edu |

---

## Conclusiones Fase 2

### Hallazgo Principal
**Ningún proyecto replica la arquitectura completa de IERC-GNL** (H3 + multiplicativo + LNG + pesca artesanal + dashboard + open source).

### Lo que SÍ es reutilizable/adaptable

| De IFC | Metodología *livelihoods baseline* para comunidades pesqueras; contacto IFC para validación |
|--------|-----------------------------------------------------------------------------------------------|
| De CA-PipeFish | **Spatial risk-layers** + ponderación fishing intensity × snagging × conservation; shapefiles abiertos; stakeholder engagement (SFF, O&G UK, BEIS) |
| De TNC F@R | **Fórmula IPCC H×E×V validada globalmente**; descomposición Exposure (catch/fishers 50/50); Vulnerability = S + (1-AC); fishery-specific AC indicators (gear diversity, MPA) |

### Lo que NO existe y IERC debe innovar
1. **Grid H3 Res 8/9** para LNG + pesca artesanal (novedad mundial)
2. **Índice multiplicativo H×V** adaptado a LNG (H = proximity + snagging + habitat loss; V = sensitivity + dependence + biocultural + gender + adaptive capacity)
3. **Dashboard interactivo + GeoPackage OGC** para stakeholders mexicanos (ASEA, CONAPESCA, comunidades)

---

## Acciones Inmediatas (Semana 3)

| Acción | Responsable | Plazo |
|--------|-------------|-------|
| Email IFC (`asksustainability@ifc.org`) | JCB/EG | Hoy |
| Email Thomas Wilding SAMS | EG | Hoy |
| Email TNC (`europe@tnc.org` + `nadine.heck@ecu.edu`) | JCB | Hoy |
| Descargar shapefiles CA-PipeFish (Marine Scotland) | EG | Mañana |
| Replicar fórmula F@R en H3 para subzona Golfo (piloto) | EG | Esta semana |

---

## Archivos Fase 2

- `docs/research/phase2/PHASE2_DEEP_DIVE.md` (este archivo)
- `docs/research/phase2/` — carpeta para respuestas de contacto y datos descargados