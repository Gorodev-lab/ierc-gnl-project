# Especificación Técnica y Diccionario de Datos — Repositorio GeoPackage v1.1

**Nombre del Entregable:** `ierc_golfo_california.gpkg`  
**Ubicación:** `deliverables/v1_geopackage/ierc_golfo_california.gpkg`  
**Formato:** OGC GeoPackage Version 1.2/1.3 (SQLite Database)  
**Sistema de Referencia Espacial (CRS):** EPSG:4326 (WGS 84 - Coordenadas Geográficas)  
**Proyecto:** Índice Espacial de Riesgo Socioeconómico para Comunidades (IERC) ante proyectos de Gas Natural Licuado (GNL)  
**Organización:** Causa Natura Data (POA 2026-2028 | Meta 1 — Entregable 1)  
**Equipo Técnico:**
- **Juan Carlos Barrera (JCB):** Consultor Senior / Especialista Pesquero y Socioambiental
- **Enrique Gorosave (EG):** Analista de Datos y SIG

---

## 1. Resumen Ejecutivo

Este archivo GeoPackage constituye el **1er Entregable Espacial del Proyecto IERC-GNL** para **Causa Natura Data**. Consolida la información geográfica de infraestructura industrial de GNL, trazados de gasoductos, Áreas Naturales Protegidas (CONANP), delimitación de las 3 localidades de estudio prioritarias (**Punta Chueca Comca'ac**, **Puerto Libertad**, **Guaymas**), espacialización del esfuerzo pesquero artesanal PANGAS (Moreno-Báez et al. 2011, 2012) con la clave única `uid_espaciotemporal`, y la grilla hexagonal adaptativa Uber H3 (Res 8 mar abierto / Res 9 zonas portuarias) con la evaluación integrada del IERC y los sub-índices socioeconómicos.

---

## 2. Estructura de Capas Espaciales (7 Capas Vectoriales)

| Nombre de Capa | Tipo Geometría | N° Entidades | Descripción |
|---|---|---|---|
|  `proyectos_gnl` | `Point` | 5 | Ubicación puntual y nivel de riesgo de terminales GNL en el Golfo. |
|  `gasoductos_infraestructura_gnl` | `LineString` | 2 | Trazados conocidos y proyectados de ductos GNL (Sonora, Saguaro, Guaymas). |
|  `localidades_estudio_ierc` | `Point` | 3 | Las 3 localidades prioritarias del POA (Punta Chueca, Puerto Libertad, Guaymas). |
|  `anp_habitats_criticos` | `Polygon` | 2 | Áreas Naturales Protegidas (CONANP) y hábitats marinos críticos. |
|  `zonas_pesqueras_pangas` | `MultiPolygon` | 17 | Polígonos consolidados por sitio pesquero con la clave `uid_espaciotemporal`. |
| ⬡ `grilla_h3_riesgo` | `Polygon` | 5,244 | Grilla hexagonal Uber H3 adaptativa (Res 8 / Res 9) con scores IERC. |
|  `riqueza_relativa_pesquera` | `MultiPolygon` | 11,065 | Malla espacial de riqueza biológica pesquera relativa (PANGAS). |

---

## 3. Estándar de Identificador Único Espacio-Temporal (`uid_espaciotemporal`)

Cada entidad pesquera digitalizada o ingresada en el repositorio incluye el atributo estandarizado:
$$\text{uid\_espaciotemporal} = \text{comunidad} - \text{actor} - \text{pesquería} - \text{arte} - \text{zona} - \text{temporada} - \text{ruta}$$

Ejemplo: `PUNTA_CHUECA-ARTESANAL-MULTIESPECIE-PANGAS-SITIO_01-ANUAL-RUTA_PRINCIPAL`

---

## 4. Instrucciones de Reproducibilidad

Para regenerar o actualizar este archivo GeoPackage ejecute desde la raíz del proyecto:

```bash
uv run --with geopandas --with shapely --with h3 python3 deliverables/v1_geopackage/build_geopackage.py
```
