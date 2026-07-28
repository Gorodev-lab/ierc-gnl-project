# Especificación Técnica y Diccionario de Datos — Repositorio GeoPackage v1

**Nombre del Entregable:** `ierc_golfo_california.gpkg`  
**Ubicación:** `deliverables/v1_geopackage/ierc_golfo_california.gpkg`  
**Formato:** OGC GeoPackage Version 1.2/1.3 (SQLite Database)  
**Sistema de Referencia Espacial (CRS):** EPSG:4326 (WGS 84 - Coordenadas Geográficas)  
**Proyecto:** Índice Espacial de Riesgo Socioeconómico para Comunidades (IERC) ante proyectos de Gas Natural Licuado (GNL)  
**Región de Estudio:** Golfo de California, México  

---

## 1. Resumen Ejecutivo

Este archivo GeoPackage constituye el **1er Entregable Espacial del Proyecto IERC-GNL**. Consolida la información geográfica de infraestructura industrial de GNL, espacialización del esfuerzo pesquero artesanal (PANGAS / Moreno-Báez et al. 2011, 2012), y la grilla hexagonal de resolución 8 (H3) con la evaluación integrada del riesgo pesquero y los sub-índices socioeconómicos del IERC.

---

## 2. Estructura de Capas Espaciales

| Nombre de Capa | Tipo Geometría | N° Entidades | Descripción |
|---|---|---|---|
| `proyectos_gnl` | `Point` | 5 | Ubicación puntual y nivel de riesgo de terminales GNL en el Golfo. |
| `zonas_pesqueras_pangas` | `MultiPolygon` | 17 | Polígonos consolidados por sitio pesquero con riqueza y presencia de especies amenazadas (IUCN). |
| `grilla_h3_riesgo` | `Polygon` | 6,305 | Grilla hexagonal Uber H3 Res 8 (~0.73 km²) con scores IERC y sub-índices. |
| `riqueza_relativa_pesquera` | `MultiPolygon` | 11,065 | Malla espacial de riqueza biológica pesquera relativa del estudio PANGAS. |

---

## 3. Diccionario de Datos por Capa

### Capa 1: `proyectos_gnl`
Contiene la localización geográfica de los 5 proyectos de infraestructura GNL evaluados.

* **`proyecto_id`** (`String`): Identificador único del proyecto (ej. `Bazan_San_Felipe`, `NFE_Puerto_Libertad`, `Guaymas_Terminal`).
* **`nombre`** (`String`): Nombre completo comercial/oficial del proyecto.
* **`estado`** (`String`): Entidad federativa (`Sonora`, `Baja California`).
* **`estatus`** (`String`): Estado operativo (`Propuesto`, `En desarrollo`, `En operación`).
* **`latitud`** / **`longitud`** (`Real`): Coordenadas en grados decimales (WGS84).
* **`riesgo_pesquero_score`** (`Real`): Score de riesgo pesquero (0 a 100) según la metodología Moreno-Báez.
* **`nivel_riesgo`** (`String`): Categoría cualitativa (`Alto`, `Moderado`, `Bajo`, `Sin datos`).
* **`densidad_esfuerzo`** (`Real`): Proporción normalizada de esfuerzo pesquero en el radio de influencia (0.0 a 1.0).
* **`proximidad_normalizada`** (`Real`): Sub-índice de cercanía a zonas de pesca (0.0 a 1.0).
* **`especies_criticas_score`** (`Real`): Presencia de especies críticas en la zona (0.0 a 1.0).
* **`num_zonas_50km`** (`Integer`): Cantidad de zonas pesqueras dentro del radio de 50 km.
* **`distancia_zona_cercana_km`** (`Real`): Distancia en kilómetros a la zona pesquera más cercana.
* **`artes_pesca`** (`String`): Lista de artes de pesca afectadas en la zona (ej. `Chinchorro, PANGAS, Redes`).

---

### Capa 2: `zonas_pesqueras_pangas`
Zonas pesqueras artesanales consolidadas a partir de las entrevistas del proyecto PANGAS.

* **`sitio_code`** (`String`): Código identificador único del sitio de pesca artesanal.
* **`nombre_sitio`** (`String`): Nombre de la comunidad o localidad pesquera de referencia.
* **`habitat`** (`String`): Tipo de hábitat marino/costero registrado.
* **`total_registros_entrevista`** (`Integer`): Número total de entrevistas registradas en el sitio.
* **`riqueza_total_especies`** (`Integer`): Conteo total de especies biológicas identificadas.
* **`especies_criticas_iucn_count`** (`Integer`): Número de especies en la lista roja de la IUCN (CR, EN, VU, NT).
* **`tiene_especies_amenazadas`** (`Integer`): Indicador binario (`1` si cuenta con especies de prioridad de conservación, `0` en otro caso).

---

### Capa 3: `grilla_h3_riesgo`
Grilla espacial hexagonal H3 Nivel 8 (~0.73 km² por celda) que permite análisis espacial multinivel.

* **`h3_index`** (`String`): Índice hexadecimal único de celda Uber H3 (ej. `88485c65c5fffff`).
* **`resolucion`** (`Integer`): Nivel de resolución espacial H3 (`8`).
* **`latitud_centroide`** / **`longitud_centroide`** (`Real`): Coordenadas del centroide de la celda.
* **`ierc_score`** (`Real`): Score final del Índice Espacial de Riesgo Socioeconómico (0.00 a 100.00).
* **`nivel_riesgo`** (`String`): Clasificación del riesgo (`Alto` ≥ 75.0, `Moderado` 50.0-74.9, `Bajo` < 50.0).
* **`amenaza_score`** (`Real`): Sub-índice de exposición a amenaza industrial GNL (peso 20%).
* **`exposicion_score`** (`Real`): Sub-índice de exposición del esfuerzo pesquero (peso 20%).
* **`sensibilidad_score`** (`Real`): Sub-índice de sensibilidad ecológica y de especies (peso 15%).
* **`dependencia_score`** (`Real`): Sub-índice de dependencia económica pesquera (peso 15%).
* **`biocultural_score`** (`Real`): Sub-índice de valor patrimonio biocultural (peso 15%).
* **`capacidad_adaptativa_score`** (`Real`): Sub-índice de capacidad de adaptación de la comunidad (peso 15%).
* **`distancia_proyecto_mas_cercano_km`** (`Real`): Distancia lineal en km a la infraestructura GNL más próxima.

---

### Capa 4: `riqueza_relativa_pesquera`
Capa de polígonos de riqueza espacial relativa adaptada de la base geográfica PANGAS.

* **`CODE_COMP`** (`String`): Código del polígono de grilla.
* **`riqueza_absoluta`** (`Real`): Riqueza de especies acumulada en la celda pesquera.

---

## 4. Metodología de Cálculo y Fuentes

1. **Riesgo Pesquero (Moreno-Báez et al. 2011, 2012):**  
   $$R_{\text{pesquero}} = (0.50 \times \text{Densidad Esfuerzo}) + (0.30 \times \text{Proximidad}) + (0.20 \times \text{Especies Críticas})$$

2. **Índice IERC:**  
   $$\text{IERC} = (\text{Amenaza} \times 0.20) + (\text{Exposición} \times 0.20) + (\text{Sensibilidad} \times 0.15) + (\text{Dependencia} \times 0.15) + (\text{Biocultural} \times 0.15) + ((1 - \text{Cap.Adaptativa}) \times 0.15)$$

3. **Fuentes Primarias:**
   - **PANGAS GDB:** Base de datos geográfica de pesca artesanal del Golfo de California.
   - **dataMares / UCSD:** Indicadores de volumen y esfuerzo pesquero.
   - **Global Fishing Watch (GFW):** Trazas de tráfico marítimo industrial.
   - **IUCN Red List 2024:** Clasificación de estado de conservación de especies.

---

## 5. Instrucciones de Reproducibilidad

Para regenerar o actualizar este archivo GeoPackage ejecute desde la raíz del proyecto:

```bash
uv run --with geopandas --with shapely --with h3 python3 deliverables/v1_geopackage/build_geopackage.py
```

El script verificará los insumos en `data/raw/` y `data/processed/` y reconstruirá las 4 capas vectoriales con índices espaciales R-Tree activados.
