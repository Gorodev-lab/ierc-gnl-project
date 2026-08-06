# Reporte Detallado del Repositorio GeoPackage e Inventario de Base de Datos

**Proyecto:** IERC-GNL — Índice Espacial de Riesgo Socioeconómico para Comunidades  
**Organización:** Causa Natura Center  
**Analista de Datos y SIG:** Enrique Gorosave Meza  
**Fecha del reporte:** 2026-08-04  
**Estándar:** OGC GeoPackage v1.1 / EPSG:4326 (WGS 84)

---

## 1. Resumen Ejecutivo

El repositorio IERC-GNL contiene **7 archivos GeoPackage** distribuidos en cuatro ubicaciones funcionales: entregables versionados, datos de procesamiento intermedio, datos del dashboard y copias de respaldo. El GeoPackage principal de producción es `ierc_golfo_california.gpkg` (v1, 5.7 MB, 9 capas) ubicado en `deliverables/v1_geopackage/`. Existe una v2 con 12 capas (5.0 MB) en `deliverables/v2_geopackage/` que incluye capas adicionales de campo (rutas pesqueras, sitios bioculturales, puntos de desembarque y zonas de interacción con fondeaderos GNL).

**Totales:**
- 7 archivos GeoPackage
- 25 capas vectoriales únicas
- ~25,000 entidades geográficas totales
- 1 CRS único: EPSG:4326 (WGS 84)

---

## 2. Inventario de Archivos GeoPackage

### 2.1 Entregables Versionados

| # | Archivo | Ruta | Tamaño | Modificado | Capas | Estado |
|---|---------|------|--------|------------|-------|--------|
| 1 | `ierc_golfo_california.gpkg` | `deliverables/v1_geopackage/` | 5.7 MB | 2026-08-02 | 9 | Producción (v1.1) |
| 2 | `ierc_golfo_california_v2.gpkg` | `deliverables/v2_geopackage/` | 5.0 MB | 2026-07-29 | 12 | Producción (v2) |
| 3 | `ierc_golfo_california.gpkg` | `output/ENTREGABLE_1_CAUSA_NATURA_DRIVE/02_Base_de_Datos_GeoPackage/` | 5.3 MB | 2026-07-28 | 7 | Respaldo (Entregable 1) |

### 2.2 Datos de Procesamiento Intermedio

| # | Archivo | Ruta | Tamaño | Modificado | Capas | Estado |
|---|---------|------|--------|------------|-------|--------|
| 4 | `IERC_GNL_Data.gpkg` | `causanaturadata/output/` | 1.9 MB | 2026-07-30 | 4 | Intermedio |
| 5 | `proyectos_gnl_consolidados.gpkg` | `causanaturadata/output/` | 96 KB | 2026-07-30 | 1 | Intermedio |
| 6 | `GEBCO_Batimetria_Golfo.gpkg` | `causanaturadata/output/` | 784 KB | 2026-07-30 | 1 | Fuente (GEBCO 2024) |

### 2.3 Datos del Dashboard

| # | Archivo | Ruta | Tamaño | Modificado | Capas | Estado |
|---|---------|------|--------|------------|-------|--------|
| 7 | `terminales_gnl_v3.gpkg` | `dashboard/public/data/` | 108 KB | 2026-08-01 | 1 | Dashboard |

---

## 3. Inventario Detallado de Capas

### 3.1 GeoPackage Principal v1 — `ierc_golfo_california.gpkg` (5.7 MB, 9 capas)

#### Capa 1: `proyectos_gnl`
- **Geometría:** Punto
- **Entidades:** 11
- **Extensión:** (-114.800, 19.450) — (-96.400, 32.450)
- **Descripción:** Proyectos de infraestructura GNL en el Golfo de California y costa del Pacífico
- **Esquema de atributos:**

| Campo | Tipo | Descripción |
|-------|------|-------------|
| nombre_proyecto | String | Nombre del proyecto GNL |
| estado | String | Estado federativo |
| municipio | String | Municipio |
| tipo_infraestructura | String | Tipo (terminal, planta, etc.) |
| empresa_promovente | String | Empresa promovente |
| estatus_permiso | String | Estatus del permiso |
| fuente_oficial | String | Fuente de datos |
| capacidad_mtpa | Real | Capacidad en millones de toneladas/año |
| latitud | Real | Latitud |
| longitud | Real | Longitud |

#### Capa 2: `gasoductos_infraestructura_gnl`
- **Geometría:** LineString
- **Entidades:** 3
- **Extensión:** (-112.684, 24.890) — (-108.010, 31.300)
- **Descripción:** Gasoductos asociados a infraestructura GNL
- **Esquema:**

| Campo | Tipo |
|-------|------|
| ducto_id | String |
| nombre | String |
| operador | String |
| estatus | String |
| longitud_km | Real |

#### Capa 3: `localidades_estudio_ierc`
- **Geometría:** Punto
- **Entidades:** 3
- **Extensión:** (-112.684, 27.918) — (-110.904, 29.911)
- **Descripción:** Localidades pesqueras artesanales de estudio
- **Esquema:**

| Campo | Tipo |
|-------|------|
| localidad_id | String |
| nombre | String |
| municipio | String |
| estado | String |
| tipo_comunidad | String |
| poblacion_pesquera_est | Integer64 |
| prioridad_poa | String |
| latitud | Real |
| longitud | Real |

#### Capa 4: `anp_habitats_criticos`
- **Geometría:** Polígono
- **Entidades:** 2
- **Extensión:** (-114.800, 29.000) — (-112.000, 31.800)
- **Descripción:** Áreas Naturales Protegidas y hábitats críticos
- **Esquema:**

| Campo | Tipo |
|-------|------|
| anp_id | String |
| nombre | String |
| categoria | String |
| administracion | String |
| superficie_ha | Real |

#### Capa 5: `zonas_pesqueras_pangas`
- **Geometría:** MultiPolígono
- **Entidades:** 17
- **Extensión:** (-114.861, 28.362) — (-112.225, 31.601)
- **Descripción:** Zonas de pesca artesanal en pangas por localidad
- **Esquema:**

| Campo | Tipo |
|-------|------|
| uid_espaciotemporal | String |
| sitio_code | String |
| nombre_sitio | String |
| comunidad | String |
| actor | String |
| pesqueria | String |
| arte | String |
| zona | String |
| temporada | String |
| ruta | String |
| habitat | String |
| total_registros_entrevista | Integer64 |
| riqueza_total_especies | Integer64 |
| especies_criticas_iucn_count | Integer64 |
| tiene_especies_amenazadas | Integer64 |

#### Capa 6: `riqueza_relativa_pesquera`
- **Geometría:** MultiPolígono
- **Entidades:** 11,065
- **Extensión:** (-114.931, 27.298) — (-110.519, 31.842)
- **Descripción:** Riqueza relativa de especies pesqueras (modelo de distribución)
- **Esquema:** 51 campos de especies (abundancia relativa por especie, códigos de 6 letras) + campo `all` (riqueza agregada). Especies incluidas:

| Código | Especie (referencia) |
|--------|---------------------|
| artnob | Artedidraco sp. |
| atrtub | Atractoscion nobilis |
| balpol | Balaenoptera polynomials |
| calbel | Calamus brachysomus |
| carlim | Caranx limon |
| carspp | Caranx spp. |
| cynoth | Cynoscion othonopterus |
| cynpar | Cynoscion parvipinnis |
| cynspp | Cynoscion spp. |
| dasdip | Dasyatis diploptera |
| dasspp | Dasyatis spp. |
| dospon | Dosidicus gigas |
| epiaca | Epinephelus acanthistius |
| epiana | Epinephelus analogus |
| epispp | Epinephelus spp. |
| gymmar | Gymnothorax mordax |
| hexnig | Hexagrammos nigricans |
| hopgue | Hoplostethus guezeni |
| isofus | Iso fuscovittatus |
| litsty | Lithodytes stylophorus |
| lutarg | Lutjanus argentiventris |
| lutper | Lutjanus peru |
| micmeg | Micromesistius megastoma |
| mugspp | Mugil spp. |
| muscal | Mustelus californicus |
| muslun | Mustelus lunulatus |
| musspp | Mustelus spp. |
| mycjor | Mycteroperca jordani |
| mycpri | Mycteroperca prionura |
| mycros | Mycteroperca rosacea |
| mylcal | Myliobatis californica |
| myllon | Myliobatis longirostris |
| octspp | Octopus spp. |
| pangen | Panulirus geminus |
| paninf | Panulirus inflatus |
| paraur | Paralabrax auriclineatus |
| parmac | Paralabrax maculatofasciatus |
| parple | Paralabrax sexfasciatus |
| parspp | Paralabrax spp. |
| phyery | Physalaemus erythrostictus |
| pinrug | Pinguipes rugosus |
| rhilon | Rhinobatos lionotus |
| rhipro | Rhinobatos productus |
| rhispp | Rhinobatos spp. |
| scospp | Scomberomorus spp. |
| sphspp | Sphoeroides spp. |
| spocal | Sphyraena californica |
| squcal | Squatina californica |
| stegig | Stegostoma giganteum |
| all | Riqueza agregada (Real) |

#### Capa 7: `batimetria_contornos_gebco`
- **Geometría:** LineString
- **Entidades:** 1,146
- **Extensión:** (-114.008, 22.992) — (-106.207, 31.652)
- **Descripción:** Contornos batimétricos derivados de GEBCO 2024
- **Esquema:**

| Campo | Tipo |
|-------|------|
| profundidad_m | Real |
| clase_profundidad | String |
| fuente | String |

#### Capa 8: `poligonos_detalle_saguaro`
- **Geometría:** desconocida
- **Entidades:** variable
- **Descripción:** Polígonos de detalle del proyecto Saguaro
- **Esquema:**

| Campo | Tipo |
|-------|------|
| sitio_id | String |
| nombre | String |
| tipo | String |
| superficie_ha | Real |
| num_vertices | Integer64 |
| estatus | String |

#### Capa 9: `grilla_h3_riesgo`
- **Geometría:** Polígono
- **Entidades:** 5,244
- **Extensión:** (-115.038, 27.866) — (-110.850, 31.238)
- **Descripción:** Grilla H3 (resolución 8/9) con índice IERC calculado
- **Esquema:**

| Campo | Tipo |
|-------|------|
| h3_index | String |
| resolucion | Integer64 |
| latitud_centroide | Real |
| longitud_centroide | Real |
| ierc_score | Real |
| nivel_riesgo | String |
| amenaza_score | Real |
| exposicion_score | Real |
| sensibilidad_score | Real |
| dependencia_score | Real |
| biocultural_score | Real |
| capacidad_adaptativa_score | Real |
| distancia_proyecto_mas_cercano_km | Real |

---

### 3.2 GeoPackage v2 — `ierc_golfo_california_v2.gpkg` (5.0 MB, 12 capas)

Incluye las capas de v1 (excepto batimetría_contornos_gebco y poligonos_detalle_saguaro) más **5 capas adicionales de campo**:

#### Capa 10: `campo_rutas_pesqueras`
- **Geometría:** LineString
- **Descripción:** Rutas de pesca artesanal desde localidades de origen
- **Esquema:**

| Campo | Tipo |
|-------|------|
| uid_espaciotemporal | String |
| localidad_origen | String |
| pesqueria | String |
| arte_pesca | String |
| quincena | String |
| distancia_km | Real |

#### Capa 11: `campo_zonas_pesca_quincenales`
- **Geometría:** Polígono
- **Descripción:** Zonas de pesca por quincena con costos de viaje
- **Esquema:**

| Campo | Tipo |
|-------|------|
| uid_espaciotemporal | String |
| localidad_origen | String |
| tipo_zona | String |
| especie_grupo | String |
| arte_pesca | String |
| mes_quincena | String |
| temporada | String |
| costo_viaje_mxn | Real |
| presencia_mujeres | Integer64 |
| grado_confianza | String |

#### Capa 12: `campo_sitios_bioculturales_comcaac`
- **Geometría:** Punto
- **Descripción:** Sitios bioculturales del pueblo Comcaac (Seri)
- **Esquema:**

| Campo | Tipo |
|-------|------|
| sitio_id | String |
| nombre_sitio | String |
| localidad | String |
| categoria_patrimonio | String |
| relevancia | String |

#### Capa 13: `campo_puntos_desembarque_costo`
- **Geometría:** Punto
- **Descripción:** Puntos de desembarque pesquero con costos de combustible
- **Esquema:**

| Campo | Tipo |
|-------|------|
| sitio_id | String |
| nombre_playa | String |
| localidad | String |
| num_pangas_activas | Integer64 |
| precio_gasolina_l_mxn | Real |

#### Capa 14: `campo_interaccion_fondeaderos_gnl`
- **Geometría:** Polígono
- **Descripción:** Zonas de interacción entre fondeaderos pesqueros y terminales GNL
- **Esquema:**

| Campo | Tipo |
|-------|------|
| fondeadero_id | String |
| terminal_asociada | String |
| estatus_conflictividad | String |
| radio_seguridad_m | Real |

#### Diferencias en `proyectos_gnl` (v2 vs v1):
- v2 tiene **5 entidades** (solo Golfo de California) vs v1 con **11 entidades** (incluye Pacífico)
- v2 tiene esquema extendido con scores de riesgo: `riesgo_pesquero_score`, `nivel_riesgo`, `densidad_esfuerzo`, `proximidad_normalizada`, `especies_criticas_score`, `num_zonas_50km`, `distancia_zona_cercana_km`, `artes_pesca`, `nota`

#### Diferencias en `grilla_h3_riesgo` (v2 vs v1):
- v2 tiene **5,244 entidades** (rango más amplio)
- v1 tiene campos adicionales: `dependencia_score`, `biocultural_score`, `capacidad_adaptativa_score` (no presentes en v2)

---

### 3.3 Datos Auxiliares

#### `IERC_GNL_Data.gpkg` (1.9 MB, 4 capas)

| Capa | Geometría | Entidades | Extensión | Descripción |
|------|-----------|-----------|-----------|-------------|
| `asea_proyectos_filtrados` | Punto | 2 | Golfo de California | Proyectos ASEA filtrados para IERC |
| `asea_proyectos_todos` | Punto | 10 | Nacional | Todos los proyectos ASEA |
| `gnl_proyectos_consolidados` | Punto | 11 | (-111.0, 19.3) — (-96.4, 29.5) | Proyectos GNL consolidados |
| `batimetria_golfo_california` | Sin geometría | 2,732 | N/A | Datos batimétricos tabulares |

**Esquema `asea_proyectos_*`:**

| Campo | Tipo |
|-------|------|
| folio | String |
| nombre | String |
| razon_social | String |
| estado | String |
| estado_codigo | String |
| estatus_evaluacion | String |
| mia_pdf | String |
| todos_pdfs | String |
| fuente | String |

**Esquema `gnl_proyectos_consolidados`:**

| Campo | Tipo |
|-------|------|
| nombre | String |
| folio | String |
| estado | String |
| tipo | String |
| empresa | String |
| estatus | String |
| lat | Real |
| lon | Real |
| fuente | String |

#### `proyectos_gnl_consolidados.gpkg` (96 KB, 1 capa)

| Capa | Geometría | Entidades | Descripción |
|------|-----------|-----------|-------------|
| `proyectos_gnl_11_consolidados` | Mixta | 11 | 11 proyectos GNL consolidados (mismo esquema que v1 proyectos_gnl) |

#### `GEBCO_Batimetria_Golfo.gpkg` (784 KB, 1 capa)

| Capa | Geometría | Entidades | Descripción |
|------|-----------|-----------|-------------|
| `batimetria_gebco_2024` | LineString | 1,146 | Contornos batimétricos GEBCO 2024 |

#### `terminales_gnl_v3.gpkg` (108 KB, 1 capa)

| Capa | Geometría | Entidades | Extensión | Descripción |
|------|-----------|-----------|-----------|-------------|
| `terminales_gnl_v3` | Polígono | 11 | (-112.696, 20.699) — (-103.419, 29.917) | Polígonos de terminales GNL para dashboard |

**Esquema `terminales_gnl_v3` (18 campos):**

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | String | Identificador único |
| proyecto | String | Nombre del proyecto |
| componente | String | Componente de la terminal |
| promovente | String | Empresa promovente |
| empresa_madre | String | Empresa matriz |
| estado | String | Estado federativo |
| municipio | String | Municipio |
| localidad | String | Localidad |
| tipo_area | String | Tipo de área |
| capacidad_mtpa | Real | Capacidad Mt/año |
| fase | String | Fase del proyecto |
| superficie_ha | Real | Superficie hectáreas |
| status | String | Estatus general |
| status_code | String | Código de estatus |
| precision_level | String | Nivel de precisión |
| precision_label | String | Etiqueta de precisión |
| clave_asea | String | Clave ASEA |
| fuente_coordenadas | String | Fuente de coordenadas |

---

### 3.4 Respaldo (Entregable 1)

#### `output/ENTREGABLE_1_CAUSA_NATURA_DRIVE/02_Base_de_Datos_GeoPackage/ierc_golfo_california.gpkg` (5.3 MB, 7 capas)

Versión anterior (2026-07-28) con 7 capas: proyectos_gnl, gasoductos_infraestructura_gnl, localidades_estudio_ierc, anp_habitats_criticos, zonas_pesqueras_pangas, riqueza_relativa_pesquera, grilla_h3_riesgo. Es el primer entregable formal para Causa Natura Center.

---

## 4. Análisis Comparativo v1 vs v2

| Aspecto | v1 (5.7 MB) | v2 (5.0 MB) |
|---------|-------------|-------------|
| Capas totales | 9 | 12 |
| Proyectos GNL | 11 (nacional) | 5 (solo Golfo) |
| Gasoductos | 3 | 2 |
| Batimetría | 1,146 contornos | No incluida |
| Polígonos Saguaro | Sí | No incluida |
| Capas de campo | No | 5 capas nuevas |
| Scores en grilla H3 | 6 scores | 3 scores |
| Scores en proyectos | Básico | Extendido (riesgo pesquero) |
| Fecha modificación | 2026-08-02 | 2026-07-29 |

**Observación:** v1 es la versión más reciente y completa para análisis IERC. v2 incluye capas de campo etnográfico que v1 no tiene. Recomendación: consolidar ambas versiones en una v3 que combine las 9 capas de v1 + las 5 capas de campo de v2.

---

## 5. Cobertura Geográfica

| Dataset | Extensión (Lon, Lat) | Región |
|---------|----------------------|--------|
| Proyectos GNL (v1) | (-114.8, 19.5) — (-96.4, 32.5) | Golfo de California + Pacífico |
| Proyectos GNL (v2) | (-116.6, 27.9) — (-110.9, 31.9) | Solo Golfo de California |
| Terminales GNL v3 | (-112.7, 20.7) — (-103.4, 29.9) | Golfo + Pacífico Sur |
| Zonas pesqueras pangas | (-114.9, 28.4) — (-112.2, 31.6) | Norte del Golfo |
| Riqueza pesquera | (-114.9, 27.3) — (-110.5, 31.8) | Golfo de California |
| Grilla H3 riesgo | (-115.0, 27.9) — (-110.8, 31.2) | Norte del Golfo |
| Batimetría GEBCO | (-114.0, 23.0) — (-106.2, 31.7) | Golfo de California |

---

## 6. Calidad de Datos y Observaciones

1. **Todos los GeoPackage usan EPSG:4326 (WGS 84)** — consistencia CRS correcta.
2. **riqueza_relativa_pesquera** es la capa más pesada (11,065 polígonos, 51 especies) — puede optimizar consultas con índices espaciales.
3. **3 copias del mismo GeoPackage** (v1, respaldo Entregable 1, proyectos_consolidados) — recomendar consolidar y usar control de versiones.
4. **batimetria_golfo_california** en IERC_GNL_Data.gpkg no tiene geometría asignada pero tiene 2,732 registros — posible tabla atributiva sin geometría.
5. **proyectos_gnl en v2** tiene solo 5 entidades (Golfo) vs 11 en v1 (nacional) — decidir alcance definitivo.
6. **grilla_h3_riesgo en v1** tiene 6 scores de riesgo vs 3 en v2 — v1 es más completa para análisis IERC.
7. **terminales_gnl_v3** tiene el esquema más rico (18 campos) con metadatos de precisión y fuente — recomendado como estándar para futuras capas de proyectos.

---

## 7. Recomendaciones de Siguientes Pasos

1. **Consolidar v1 + v2 en v3** — combinar 9 capas de v1 + 5 capas de campo de v2 + batimetría = 15 capas en un solo entregable.
2. **Crear índices espaciales R-Tree** en capas pesadas (riqueza_relativa, grilla_h3) para mejorar performance.
3. **Validar consistencia de esquemas** entre proyectos_gnl (v1 con 10 campos vs v2 con 15 campos) y unificar.
4. **Migrar campos de precision/fuente** de terminales_gnl_v3 al esquema de proyectos_gnl principal.
5. **Generar metadatos XML** por capa siguiendo estándar ISO 19115 para cumplimiento institucional Causa Natura.
6. **Eliminar duplicados** — proyecto_gnl_consolidados.gpkg e IERC_GNL_Data.gpkg son subconjuntos del entregable principal.
7. **Documentar fuentes** — la capa de riqueza_relativa_pesquera necesita metadatos de origen (modelo de distribución, año base, método).

---

*Reporte generado por Hermes Agent para Enrique Gorosave Meza, Analista de Datos y SIG, Causa Natura Center.*
