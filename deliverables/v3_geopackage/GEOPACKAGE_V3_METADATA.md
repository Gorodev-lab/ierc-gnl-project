# Metadata Entregable GeoPackage v3.0 (IERC-GNL)

**Proyecto**: Índice Espacial de Riesgo Socioeconómico para Comunidades (IERC) ante proyectos de GNL en el Golfo de California  
**Organización**: Causa Natura Center (POA 2026)  
**Versión GeoPackage**: v3.0  
**Fecha de generación**: 2026-08-06 16:56:13  
**Archivo**: `deliverables/v3_geopackage/ierc_golfo_california_v3.gpkg`  
**CRS**: EPSG:4326 (WGS 84 - Coordenadas Geográficas)  

---

## 📦 Capas Incluidas en el GeoPackage v3.0

| N° | Nombre Capa | Tipo Geometría | Entidades | Descripción |
|---|---|---|---|---|
| 1 | `proyectos_gnl` | Point | 5 | Ubicación de las 4 terminales GNL en el Golfo de California (11 features detalladas). |
| 2 | `gasoductos_infraestructura_gnl` | LineString | 2 | Trazados de gasoductos (Samalayuca-Saguaro, Guaymas-Sásabe). |
| 3 | `localidades_estudio_ierc` | Point | 3 | Localidades prioritarias de estudio (Punta Chueca, Puerto Libertad, Guaymas). |
| 4 | `anp_habitats_criticos` | Polygon | 2 | Áreas Naturales Protegidas (CONANP) e Hábitats Críticos. |
| 5 | `zonas_pesqueras_pangas` | Polygon | 17 | Sitios históricos de pesca artesanal PANGAS con estándar `uid_espaciotemporal`. |
| 6 | `riqueza_relativa_pesquera` | Polygon | 11065 | Polígonos de riqueza relativa de especies pesqueras acumuladas. |
| 7 | `grilla_h3_riesgo` | Polygon | 830,869 | **Grilla H3_8 con datos reales del Lakehouse Gold** (Amenaza $H$, Vulnerabilidad $V$, IERC $R$, Confianza y Monte Carlo). |
| 8 | `campo_rutas_pesqueras` | LineString | 1 | Plantilla estandarizada para rutas pesqueras de campo 2026. |
| 9 | `campo_zonas_pesca_quincenales` | Polygon | 1 | Plantilla estandarizada para zonas pesqueras quincenales. |
| 10 | `campo_sitios_bioculturales_comcaac` | Point | 1 | Plantilla estandarizada para patrimonio biocultural Comca'ac. |
| 11 | `campo_puntos_desembarque_costo` | Point | 1 | Plantilla estandarizada para puntos de desembarque y costos por viaje. |
| 12 | `campo_interaccion_fondeaderos_gnl` | Polygon | 1 | Plantilla estandarizada para interacción y zonas de exclusión con buques GNL. |

---

## 🧮 Esquema de Atributos - `grilla_h3_riesgo` (Gold Layer)

- `h3_index` (String): Identificador único de celda H3 Resolución 8.
- `resolucion` (Integer): Nivel de resolución espacial H3 (8 = ~0.74 km²).
- `latitud_centroide` / `longitud_centroide` (Float): Coordenadas del centroide.
- `ierc_score` (Float): Puntaje de riesgo multiplicativo ($R = H \times V / 100$) en escala [0, 100].
- `nivel_riesgo` (String): Categoría discreta (`Bajo`, `Moderado`, `Alto`, `Crítico`).
- `confidence_score` (Float): Índice de Confianza y Calidad Espacial Nivel III en escala [0.0, 1.0].
- `amenaza_score` (Float): Subíndice de Amenaza y Exposición Espacial ($H$).
- `vulnerabilidad_score` (Float): Subíndice de Vulnerabilidad Socioecológica ($V$).
- `densidad_pesquera_pangas` (Float): Densidad observada de esfuerzo pesquero artesanal PANGAS.
- `gfw_fishing_hours` (Float): Horas de esfuerzo pesquero industrial observadas por Global Fishing Watch.
- `distancia_gnl_km` (Float): Distancia euclidiana en km a la terminal de GNL más cercana.
- `mc_mean` / `mc_std` / `ci_lower_95` / `ci_upper_95` (Float): Métricas de incertidumbre de la Simulación Monte Carlo.

---

*GeoPackage generado automáticamente mediante `scripts/build_geopackage_v3.py`*
