# 🌊 IERC-GNL: Índice Espacial de Riesgo Socioeconómico para Comunidades

[![GeoPackage](https://img.shields.io/badge/OGC-GeoPackage_v1.2-blue.svg)](https://www.ogc.org/standard/geopackage/)
[![CRS](https://img.shields.io/badge/CRS-EPSG%3A4326_(WGS84)-green.svg)](https://epsg.io/4326)
[![H3 Grid](https://img.shields.io/badge/Uber_H3-Resolution_8-orange.svg)](https://h3geo.org/)
[![Next.js](https://img.shields.io/badge/Dashboard-Next.js_15-black.svg)](https://nextjs.org/)
[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](LICENSE)

---

## 📌 Resumen del Proyecto

El **Índice Espacial de Riesgo Socioeconómico para Comunidades (IERC-GNL)** es una plataforma espacial e instrumento metodológico diseñado para evaluar y visibilizar la vulnerabilidad socioecológica y económica de las comunidades pesqueras artesanales ante la expansión de proyectos e infraestructura de **Gas Natural Licuado (GNL)** en la región del **Golfo de California, México**.

Este repositorio contiene la **base de datos espacial oficial en formato OGC GeoPackage (`ierc_golfo_california.gpkg`)**, los motores de cálculo espacial en Python, los datos geográficos de partida (PANGAS, GFW, IUCN) y el visor web interactivo en Next.js.

---

## 📦 Entregable Espacial GeoPackage v1

El archivo principal de datos geográficos se encuentra en:  
`deliverables/v1_geopackage/ierc_golfo_california.gpkg`

### Capas Vectoriales Incluidas

| Nombre de Capa | Geometría | N° Entidades | Descripción |
|---|---|---|---|
| 📍 **`proyectos_gnl`** | `Point` | 5 | Infraestructura y terminales GNL en el Golfo con scores de riesgo pesquero (Moreno-Báez et al.) e IERC. |
| 🐟 **`zonas_pesqueras_pangas`** | `MultiPolygon` | 17 | Polígonos de campos pesqueros artesanales (PANGAS) con riqueza de especies y presencia de especies amenazadas (IUCN). |
| ⬡ **`grilla_h3_riesgo`** | `Polygon` | 6,305 | Malla hexagonal Uber H3 Resolución 8 (~0.73 km²) con evaluación integrada del IERC y 6 sub-índices. |
| 📊 **`riqueza_relativa_pesquera`** | `MultiPolygon` | 11,065 | Malla de riqueza biológica pesquera relativa acumulada en el Golfo. |

---

## 📐 Metodología y Sub-índices IERC

El índice IERC evalúa el riesgo relativo combinando seis dimensiones ponderadas:

$$\text{IERC} = (0.20 \times \text{Amenaza}) + (0.20 \times \text{Exposición}) + (0.15 \times \text{Sensibilidad}) + (0.15 \times \text{Dependencia}) + (0.15 \times \text{Biocultural}) + (0.15 \times [1 - \text{Cap.Adaptativa}])$$

1. **Amenaza Industrial GNL (20%):** Proximidad espacial y densidad de operaciones de la infraestructura GNL.
2. **Exposición Pesquera (20%):** Intensidad y superposición del esfuerzo de pesca artesanal.
3. **Sensibilidad Biológica (15%):** Riqueza de especies y presencia de taxones en listas rojas IUCN.
4. **Dependencia Económica (15%):** Proporción del ingreso y empleo local dependiente de la pesca de panga.
5. **Patrimonio Biocultural (15%):** Presencia de sitios pesqueros tradicionales y conocimientos locales.
6. **Capacidad Adaptativa (15%):** Nivel de organización socio-comunitaria e infraestructura alternativa.

---

## 📁 Estructura del Repositorio

```bash
ierc-gnl-project/
├── dashboard/                  # Dashboard Web Interactivo (Next.js 15, React, Tailwind)
│   ├── src/app/api/geopackage/ # API Route para consultas al GeoPackage
│   └── src/app/components/     # Mapa de riesgo, gráficos y paneles metodológicos
├── data/                       # Insumos geográficos
│   ├── raw/                    # Capas PANGAS, GFW, IUCN en formato original y WGS84
│   └── processed/              # Evaluaciones procesadas en JSON/GeoJSON
├── deliverables/
│   └── v1_geopackage/          # 📦 1er ENTREGABLE ESPACIAL
│       ├── ierc_golfo_california.gpkg  # GeoPackage OGC (EPSG:4326)
│       ├── build_geopackage.py         # Script de generación y compilación
│       └── GEOPACKAGE_METADATA.md      # Diccionario técnico de datos
├── docs/                       # Documentación metodológica y protocolos de campo
├── scripts/                    # Scripts auxiliares de preparación de datos
└── src/                        # Motores de cálculo en Python
    ├── engine/                 # Motores IERC, Monte Carlo y validación espacial
    └── h3_indexer/             # Indexador espacial Uber H3
```

---

## ⚙️ Reproducibilidad e Instalación

### 1. Reconstruir el GeoPackage desde el Código Fuente

Para regenerar o actualizar `ierc_golfo_california.gpkg`:

```bash
# Requisitos: Python >= 3.10, geopandas, shapely, h3
uv run --with geopandas --with shapely --with h3 python3 deliverables/v1_geopackage/build_geopackage.py
```

### 2. Ejecutar el Dashboard Interactivo Localmente

```bash
cd dashboard
npm install
npm run dev
```
Accede a `http://localhost:3000` para explorar el mapa de riesgo y las capas del GeoPackage.

---

## 📄 Licencia y Cita

Proyecto desarrollado para la evaluación de impactos comunitarios socioecológicos en el Golfo de California.

Si utiliza estos datos o metodología, favor de citar:
- **IERC-GNL Project (2026):** *Índice Espacial de Riesgo Socioeconómico para Comunidades ante Proyectos de GNL en el Golfo de California*.
- **Moreno-Báez et al. (2011, 2012):** *Integrating spatial and temporal dimensions of artisanal fishing in the Gulf of California*.
