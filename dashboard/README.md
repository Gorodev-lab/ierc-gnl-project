# IERC-GNL Interactive Dashboard (Next.js 16)

Dashboard de Inteligencia Geoespacial y Evaluación del Índice Espacial de Riesgo Socioeconómico (IERC) para **Causa Natura Center**.

---

## 🎨 Estándar de Diseño & Skill Hallmark Anti-AI-Slop

Este proyecto sigue estrictamente el **Esoteria Design System v1.1** (`STYLE_GUIDE.md`) y el protocolo anti-AI-slop de **Nutlope/Hallmark**:

- **Skill de Agente**: Todos los agentes de IA (Claude Code, Cursor, Codex, Gemini) deben acatar las reglas descritas en `.gemini/skills/hallmark/SKILL.md` y `dashboard/AGENTS.md`.
- **Política Cero-Emoticones**: Se prohíbe el uso de emojis decorativos en la interfaz (ej. 🦐, 🦈, 🐟). En su lugar se utilizan **Badges Monospace Taxonómicos** (`[CAM]`, `[TIB]`, `[RAY]`, `[PAR]`).
- **Restricciones Visuales**:
  - `IBM Plex Mono` como tipografía principal.
  - `border-radius: 0px` en todos los componentes.
  - `box-shadow: none` (sin sombras flotantes ni efectos glow).
  - Fondo oscuro permanente (`#0A0A0A`, superficie `#111111`, bordes `#222222`).

---

## 🚀 Inicio Rápido

```bash
# Instalar dependencias
npm install

# Iniciar servidor de desarrollo (puerto 3001)
npm run dev

# Compilar paquete de producción
npm run build
```

Navegar a [http://localhost:3001](http://localhost:3001) para ver el dashboard.

---

## 📁 Estructura de Componentes

| Componente | Archivo | Descripción |
|------------|---------|-------------|
| **Header** | `src/app/components/Header.tsx` | Consola superior con ticker de estado del sistema e indicadores OGC GeoPackage. |
| **RiskMap** | `src/app/components/RiskMap.tsx` | Visor mapa Leaflet con navegación rápida de terminales GNL, mallas Uber H3 y contornos GEBCO. |
| **ZoneCards** | `src/app/components/ZoneCards.tsx` | Tarjetas de riesgo pesquero PANGAS con barras ASCII `[██████░░░░]`. |
| **SpeciesPanel** | `src/app/components/SpeciesPanel.tsx` | Panel de especies en riesgo IUCN con badges taxonómicos monospace. |
| **MethodologyPanel** | `src/app/components/MethodologyPanel.tsx` | Desglose de fórmulas y motor de cálculo Monte Carlo. |
| **CoverageModal** | `src/app/components/CoverageModal.tsx` | Matriz de vacíos de información e ingestas institucionales. |
| **MiaInspectorModal** | `src/app/components/MiaInspectorModal.tsx` | Visor planos MIA (macro/micro/distribución). |
| **RiskBadge** | `src/app/components/RiskBadge.tsx` | Badge nivel de riesgo. |
| **ExportModal** | `src/app/components/ExportModal.tsx` | Exportación GeoJSON/CSV/GeoPackage. |

---

## 📊 Capas de Datos Disponibles

### Capas Base (14 capas vectoriales GeoJSON)

| ID | Nombre | Archivo | Tamaño | Descripción |
|----|--------|---------|--------|-------------|
| `proyectos_gnl` | 4 Terminales GNL (11 Features v3) | `terminales_gnl_v3.geojson` | 24 KB | Puntos + buffers H3-10 (tipo/estatus/estado) |
| `poligonos_saguaro` | Polígonos Detalle Saguaro (MIA 181V) | `saguaro_polygons_181v.geojson` | 8 KB | Polígonos detalle MIA proyecto Saguaro |
| `capas_contexto` | Gasoductos, Sitios Ramsar & ANPs | `capas_contextuales.geojson` | 4 KB | Contexto regulatorio y conservación |
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

### Capas Derivadas (Análisis IERC)

| Capa | Descripción | Fuente |
|------|-------------|--------|
| **IERC Score** | Índice integrado 0–1 | `grilla_h3_riesgo.geojson` → `ierc_score` |
| **Nivel de Riesgo** | Muy Bajo / Bajo / Medio / Alto / Muy Alto | Percentiles IERC |
| **Amenaza / Vulnerabilidad** | Componentes modelo multiplicativo | `ierc_risk_multiplicative.parquet` |
| **Confianza Espacial** | Filtro calidad datos (threshold configurable) | `ierc_confidence_h3.parquet` |

---

## 🎮 Controles de Interfaz

| Control | Tipo | Rango |
|---------|------|-------|
| **Time Slider** | Slider temporal | 2020–2024 |
| **H3 Resolution Selector** | Select | 8 / 9 / Adaptive |
| **Risk Threshold** | Slider (Monte Carlo) | p05–p95 |
| **Layer Opacity** | Slider por capa | 0–100% |
| **Spatial Filter** | Bbox / Radio | Coordenadas / km |
| **Confidence Threshold** | Slider | 0–95% |

---

## 🗺️ Navegación Rápida a Terminales GNL

El sidebar incluye botones de acceso directo a las 4 terminales principales:

| Terminal | Ubicación | Lat | Lon | Zoom | Precisión | Estatus |
|----------|-----------|-----|-----|------|-----------|---------|
| **SAGUARO ENERGÍA GNL** | Puerto Libertad, Sonora | 29.9058 | -112.6880 | 13 | `[APROXIMADO]` | Proposed / Pre-FID |
| **AMIGO LNG** | Guaymas, Sonora | 27.9229 | -110.8681 | 13 | `[EXACTO]` | Proposed / Pre-FID |
| **VISTA PACÍFICO (FLNG)** | Topolobampo, Sinaloa | 25.5891 | -109.1038 | 13 | `[CALCULADO]` | CANCELADO (Feb 2026) |
| **GNL COSALÁ** | Mazatlán / Zapopan | 23.2500 | -106.4200 | 11 | `[APROXIMADO]` | En Evaluación ASEA |

---

## 🔧 API Backend

### `/api/geopackage?layer=<name>&limit=5000`
Endpoint para servir capas del GeoPackage directamente desde el archivo `.gpkg` (hasta 5000 features por request).

**Capas disponibles:** `proyectos_gnl`, `grilla_h3_riesgo`, `zonas_pesqueras_pangas`, `gasoductos_infraestructura_gnl`, `anp_habitats_criticos`, `localidades_estudio_ierc`, `riqueza_relativa_pesquera`, `batimetria_contornos_gebco`, `poligonos_detalle_saguaro`.

---

## 📦 Datos Estáticos (`public/data/`)

Los 17 archivos GeoJSON se generan automáticamente via:
```bash
PYTHONPATH=. ./.venv/bin/python3 scripts/prepare_dashboard_data.py
```

Esto sincroniza desde `deliverables/v1_geopackage/ierc_golfo_california.gpkg` y `causanaturadata/output/`.

---

## 📚 Documentación Vinculada

- **Reporte principal:** `../REPORTE_INVENTARIO_DATOS_IERC_GNL_v2.1_ENRIQUE_GOROSAVE.md`
- **Inventario técnico:** `../INVENTARIO_DATOS_IERC_GNL_v2.1.md`
- **Metadata GeoPackage:** `../REPORTE_INVENTARIO_GEOPACKAGE.md`
- **Estilo de diseño:** `../STYLE_GUIDE.md`
- **Configuración Lakehouse:** `../config/lakehouse.yaml`

---

## 👥 Autores

- **Juan Carlos Barrera (JCB)** — Consultor Senior, Especialista Pesquero/Socioambiental
- **Enrique Gorosave Meza (EG)** — Analista de Datos GIS, Causa Natura Center

---

## 📄 Licencia

MIT — Ver [LICENSE](../LICENSE)