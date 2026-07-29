# Documento Ejecutivo y Catálogo Cartográfico: Entregable 1 (Meta 1)

**Proyecto:** Índice Espacial de Riesgo Socioeconómico para Comunidades (IERC-GNL)  
**Cliente / Organización:** Causa Natura Center / Causa Natura Data (POA 2026-2028)  
**Equipo Técnico de Autores:**
- **Juan Carlos Barrera (JCB):** Consultor Senior / Especialista Pesquero y Socioambiental
- **Enrique Gorosave (EG):** Analista de Datos y Sistema de Información Geográfica (SIG)
**Fecha de Publicación:** 19 de Agosto de 2026  
**Repositorio Oficial de Código y Datos:** [https://github.com/Gorodev-lab/ierc-gnl-project](https://github.com/Gorodev-lab/ierc-gnl-project)

---

## 1. Resumen Ejecutivo y Alcance del Entregable 1

Este documento constituye la memoria técnica y gráfica del **Primer Entregable (Meta 1 - Semanas 1 a 4 del POA)** para el proyecto IERC-GNL. Su objetivo es presentar la arquitectura geográfica de gabinete, las capas base históricas del Golfo de California y la estructura de metadatos que servirán de cimiento para evaluar el impacto de la infraestructura de Gas Natural Licuado (GNL) en las comunidades pesqueras artesanales.

> **Nota Explicativa sobre los Datos Presentados:**  
> La información contenida en este documento representa la **línea base histórica de gabinete (Estudio PANGAS de la Dra. Marcia Moreno-Báez et al.) y el marco estructural del proyecto**. Los datos primarios oficiales y el mapeo definitivo de la infraestructura de Gas Natural Licuado (polígonos de obras, rutas de ductos, áreas de exclusión marina y zonas de pesca comunitaria actualizadas) serán recolectados directamente en campo durante la **Meta 2 (Semanas 5 a 8)** en las comunidades de **Punta Chueca (Nación Comca'ac)**, **Puerto Libertad** y **Guaymas**.

---

## 2. Estructura del Proyecto y Ubicación de Archivos en el Repositorio

Para facilitar la consulta de revisores técnicos y directivos, todos los insumos de este entregable se encuentran organizados y sincronizados en el repositorio público de GitHub en las siguientes rutas:

### Estructura General de Carpetas
- **`deliverables/v1_geopackage/`**
  - Contiene el archivo contenedor de datos espaciales: [`ierc_golfo_california.gpkg`](file:///home/gorops/ierc-gnl-project/deliverables/v1_geopackage/ierc_golfo_california.gpkg).
  - Contiene el diccionario técnico de datos: [`GEOPACKAGE_METADATOS.md`](file:///home/gorops/ierc-gnl-project/deliverables/v1_geopackage/GEOPACKAGE_METADATOS.md).
- **`output/paquetes_capas_pangas/`**
  - Contiene 7 carpetas individuales con los paquetes de capas geográficas (`01_Riqueza_Relativa`, `02_ZPesca_Buceo`, `03_ZPesca_Chinchorro`, `04_ZPesca_PANGAS`, `05_ZPesca_Redes`, `06_ZPesca_Redes_Manta_Camaron`, `07_ZPesca_Trampa`).
  - Contiene los visores interactivos en HTML: [`ATLAS_PAQUETES_COMPLETO.html`](file:///home/gorops/ierc-gnl-project/output/paquetes_capas_pangas/ATLAS_PAQUETES_COMPLETO.html) y [`DOCUMENTO_EJECUTIVO_ENTREGABLE1_PDF.html`](file:///home/gorops/ierc-gnl-project/output/DOCUMENTO_EJECUTIVO_ENTREGABLE1_PDF.html).
- **`docs/metodologia/`**
  - Contiene la Nota Metodológica Ajustada: [`Nota_Metodologica_Ajustada_JCB_EG.md`](file:///home/gorops/ierc-gnl-project/docs/metodologia/Nota_Metodologica_Ajustada_JCB_EG.md).
  - Contiene la Matriz de Vacíos de Información: [`Inventario_y_Matriz_Vacios_Geoespaciales_EG.md`](file:///home/gorops/ierc-gnl-project/docs/metodologia/Inventario_y_Matriz_Vacios_Geoespaciales_EG.md).
  - Contiene el Guion de Presentación Ejecutiva: [`PRESENTACION_EJECUTIVA_ENTREGABLE1.md`](file:///home/gorops/ierc-gnl-project/docs/metodologia/PRESENTACION_EJECUTIVA_ENTREGABLE1.md).
- **`docs/auditoria/`**
  - Contiene el plan de supervisión técnica: [`PLAN_DE_AUDITORIA_Y_SUPERVISION_IERC.md`](file:///home/gorops/ierc-gnl-project/docs/auditoria/PLAN_DE_AUDITORIA_Y_SUPERVISION_IERC.md).
  - Contiene el expediente de dictamen del entregable: [`AUDITORIA_META1_ENTREGABLE1.md`](file:///home/gorops/ierc-gnl-project/docs/auditoria/AUDITORIA_META1_ENTREGABLE1.md).

> **Explicación Accesible:**  
> Imagine el **repositorio** como una biblioteca digital organizada donde cada archivo tiene una dirección exacta. El archivo **GeoPackage** funciona como una caja fuerte digital que guarda múltiples mapas y tablas en un solo archivo ligero.

---

## 3. Descripción Explicativa de las Capas Geográficas (GeoPackage OGC v1.1)

El archivo `ierc_golfo_california.gpkg` almacena 7 capas vectoriales organizadas bajo un estándar unificado de coordenadas geográficas (`EPSG:4326 - WGS 84`):

1. **`proyectos_gnl` (Puntos):** Muestra la ubicación preliminar de 5 terminales o plantas de Gas Natural Licuado evaluadas en el Golfo de California (ej. Saguaro Energía en Puerto Libertad, Amigo LNG en Guaymas).
2. **`gasoductos_infraestructura_gnl` (Líneas):** Trazado de las tuberías y gasoductos terrestres y marinos que transportan gas natural hacia las plantas de licuefacción.
3. **`localidades_estudio_ierc` (Puntos):** Ubicación exacta de los tres centros de población costeros seleccionados para la evaluación del riesgo socioeconómico: **Punta Chueca (Nación Comca'ac)**, **Puerto Libertad** y **Guaymas**.
4. **`anp_habitats_criticos` (Polígonos):** Delimitación de las Áreas Naturales Protegidas por el gobierno federal y hábitats marinos prioritarios para la conservación de especies.
5. **`zonas_pesqueras_pangas` (Polígonos):** Campos de pesca utilizados por los pescadores artesanales en sus pangas o embarcaciones menores, vinculados con una clave única espacio-temporal.
6. **`grilla_h3_riesgo` (Polígonos de Hexágonos):** Una red o malla espacial compuesta por 5,244 hexágonos pequeños (similares a un panal de abejas) que divide todo el mar en celdas de tamaño uniforme (0.73 km² en mar abierto y 0.10 km² cerca de puertos y costas) para calcular el nivel de riesgo de forma precisa.
7. **`riqueza_relativa_pesquera` (Polígonos):** Mapa de calor espacial que resalta las zonas del mar donde se concentra la mayor cantidad y diversidad de especies pesqueras de importancia comercial.

---

## 4. Estandarización de la Clave Única Espacio-Temporal

Para identificar de forma inconfundible cada zona de pesca en el tiempo y el espacio, se diseñó la clave `uid_espaciotemporal`.

### Estructura de la Clave
$$	ext{Clave} = 	ext{comunidad} - 	ext{actor} - 	ext{pesquería} - 	ext{arte} - 	ext{zona} - 	ext{temporada} - 	ext{ruta}$$

> **Explicación Accesible:**  
> Es como el número de CURP o código postal de una actividad de pesca. Nos dice exactamente: *quién pesca* (comunidad y actor), *qué pesca* (especie o pesquería), *con qué herramienta* (arte de pesca), *en dónde* (zona), *en qué época del año* (temporada) y *por dónde navega* (ruta).

---

## 5. Catálogo de Paquetes Cartográficos por Capa (Línea Base PANGAS)

A continuación se presenta el desglose de las 7 capas pesqueras de la base de datos `Fish_Zones_PANGAS.gdb`, atribuidas a la investigación de la **Dra. Marcia Moreno-Báez et al. (2011, 2012)**. Cada paquete cuenta con 2 mapas georreferenciados en proyección Web Mercator (`EPSG:3857`): uno con el mapa base **OpenStreetMap estándar (estilo QGIS)** que muestra nombres de ciudades, carreteras y líneas de costa, y otro con el mapa **satelital Esri World Imagery**.

### Paquete 01: `01_Riqueza_Relativa`
**Título de la Capa:** Malla de Riqueza Biológica Pesquera Relativa  
**Ubicación en Repositorio:** `output/paquetes_capas_pangas/01_Riqueza_Relativa/`  
**Cita de Origen:** Moreno-Báez, M., et al. (2011, 2012). Ocean & Coastal Management / Marine Policy.  
**Entidades (Polígonos):** 11,065 | **Artes de Pesca:** Todas las artes de pesca artesanal registradas en el Golfo de California  
**Bounding Box (WGS84):** `MinLon: -114.9307, MinLat: 27.2977, MaxLon: -110.5188, MaxLat: 31.8423`  
**Descripción Accesible:** Muestra las zonas del Golfo de California donde los pescadores reportan la mayor concentración combinada de especies comerciales. Los tonos más oscuros representan lugares de alta biodiversidad y productividad pesquera.  

#### Mapas Georreferenciados
- **Mapa Base OpenStreetMap (Estilo QGIS):** `output/paquetes_capas_pangas/01_Riqueza_Relativa/mapa_osm.jpg`
- **Mapa Base Satelital Esri:** `output/paquetes_capas_pangas/01_Riqueza_Relativa/mapa_satelital.jpg`

#### Tabla de Atributos Extraídos Estilo QGIS (52 Campos)

| Nombre del Campo | Tipo de Dato (QGIS/GDAL) | Valor de Ejemplo | Descripción y Rol Metodológico |
|---|---|---|---|
| `artnob` | `int16` | `0` | Especie pesquera: Balistes polylepis / Pez ballesta. |
| `atrtub` | `int16` | `0` | Especie pesquera: Atractoscion nobilis / Seabass. |
| `balpol` | `int16` | `0` | Especie pesquera: Balistes polylepis / Cochi. |
| `calbel` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `carlim` | `int16` | `0` | Especie pesquera: Carcharias spp. / Tiburón. |
| `carspp` | `int16` | `0` | Especie pesquera: Caranx spp. / Jurel. |
| `cynoth` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `cynpar` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `cynspp` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `dasdip` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `dasspp` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `dospon` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `epiaca` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `epiana` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `epispp` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `gymmar` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `hexnig` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `hopgue` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `isofus` | `int16` | `0` | Especie pesquera: Isostichopus fuscus / Pepino de mar. |
| `litsty` | `int16` | `0` | Especie pesquera: Litopenaeus stylirostris / Camarón azul. |
| `lutarg` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `lutper` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `micmeg` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `mugspp` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `muscal` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `muslun` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `musspp` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `mycjor` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `mycpri` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `mycros` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `mylcal` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `myllon` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `octspp` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `pangen` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `paninf` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `paraur` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `parmac` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `parple` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `parspp` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `phyery` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `pinrug` | `int16` | `0` | Especie pesquera: Pinna rugosa / Hacha de labio. |
| `rhilon` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `rhipro` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `rhispp` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `scospp` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `sphspp` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `spocal` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `squcal` | `int16` | `0` | Atributo espacial registrado en Riqueza_Relativa. |
| `stegig` | `int16` | `0` | Especie pesquera: Strombus gigas / Caracol. |
| `all` | `float64` | `0.0` | Acumulado de riqueza biológica total. |
| `Shape_Length` | `float64` | `11112.0` | Perímetro total del polígono expresado en metros. |
| `Shape_Area` | `float64` | `7717284.0` | Superficie o área total del polígono expresada en metros cuadrados. |

---

### Paquete 02: `02_ZPesca_Buceo`
**Título de la Capa:** Polígonos de Pesca Comercial por Buceo  
**Ubicación en Repositorio:** `output/paquetes_capas_pangas/02_ZPesca_Buceo/`  
**Cita de Origen:** Moreno-Báez, M., et al. (2011, 2012). Ocean & Coastal Management / Marine Policy.  
**Entidades (Polígonos):** 249 | **Artes de Pesca:** Buceo autónomo y buceo semiautónomo (Hookah)  
**Bounding Box (WGS84):** `MinLon: -114.1083, MinLat: 27.4209, MaxLon: -111.7763, MaxLat: 31.5724`  
**Descripción Accesible:** Delimita las áreas del fondo marino costero donde buzos artesanales se sumergen para extraer moluscos y recursos bentónicos (almeja generosa, callo de hacha, erizo y pepino de mar).  

#### Mapas Georreferenciados
- **Mapa Base OpenStreetMap (Estilo QGIS):** `output/paquetes_capas_pangas/02_ZPesca_Buceo/mapa_osm.jpg`
- **Mapa Base Satelital Esri:** `output/paquetes_capas_pangas/02_ZPesca_Buceo/mapa_satelital.jpg`

#### Tabla de Atributos Extraídos Estilo QGIS (5 Campos)

| Nombre del Campo | Tipo de Dato (QGIS/GDAL) | Valor de Ejemplo | Descripción y Rol Metodológico |
|---|---|---|---|
| `no_comunid` | `int16` | `1` | Número correlativo de comunidad pesquera. |
| `comunidad` | `str` | `PPE, , , , , , , ,` | Nombre o código corto de la comunidad costera. |
| `ORIG_FID` | `int32` | `0` | Identificador de registro original en el dataset de origen. |
| `Shape_Length` | `float64` | `240636.40965902145` | Perímetro total del polígono expresado en metros. |
| `Shape_Area` | `float64` | `557068833.8007089` | Superficie o área total del polígono expresada en metros cuadrados. |

---

### Paquete 03: `03_ZPesca_Chinchorro`
**Título de la Capa:** Polígonos de Pesca con Chinchorro de Línea  
**Ubicación en Repositorio:** `output/paquetes_capas_pangas/03_ZPesca_Chinchorro/`  
**Cita de Origen:** Moreno-Báez, M., et al. (2011, 2012). Ocean & Coastal Management / Marine Policy.  
**Entidades (Polígonos):** 2,209 | **Artes de Pesca:** Chinchorro de línea / Redes agalleras de playa  
**Bounding Box (WGS84):** `MinLon: -114.9171, MinLat: 27.9883, MaxLon: -111.4621, MaxLat: 31.8624`  
**Descripción Accesible:** Zonas de playa y estuarios donde los pescadores extienden redes flotantes tipo chinchorro para rodear y capturar cardúmenes de peces de escama (corvina, sierra, robalo).  

#### Mapas Georreferenciados
- **Mapa Base OpenStreetMap (Estilo QGIS):** `output/paquetes_capas_pangas/03_ZPesca_Chinchorro/mapa_osm.jpg`
- **Mapa Base Satelital Esri:** `output/paquetes_capas_pangas/03_ZPesca_Chinchorro/mapa_satelital.jpg`

#### Tabla de Atributos Extraídos Estilo QGIS (22 Campos)

| Nombre del Campo | Tipo de Dato (QGIS/GDAL) | Valor de Ejemplo | Descripción y Rol Metodológico |
|---|---|---|---|
| `Id` | `int32` | `2` | Identificador único numérico del registro de zona pesquera. |
| `CODE` | `str` | `B` | Código alfanumérico asignado al polígono de pesca. |
| `M` | `str` | `0` | Indicador del mes o temporada (1 = activo, 0 = inactivo). |
| `J` | `str` | `0` | Indicador estacional o de pesquería. |
| `R` | `str` | `0` | Indicador de región o zona pesquera. |
| `G` | `str` | `0` | Indicador de grupo pesquero o gremio. |
| `NAME` | `str` | `El Bajo Macho` | Nombre geográfico o toponímico del sitio de pesca. |
| `ENTREVIS` | `str` | `SLG04SP030506` | Código único de la encuesta o entrevista participativa PANGAS. |
| `Int_id` | `int32` | `0` | Identificador numérico del pescador o informante clave. |
| `Ent_num` | `int16` | `4` | Número secuencial de la entrevista efectuada. |
| `Entvsdr` | `str` | `SP` | Iniciales o código del entrevistador de campo. |
| `mes` | `int16` | `0` | Mes del levantamiento o temporada de pesca (1-12). |
| `dia` | `int16` | `0` | Día del levantamiento en campo. |
| `ano` | `int16` | `0` | Año del registro de la información (ej. 2005, 2006). |
| `spp_code` | `str` | `LITSTY` | Código taxonómico estándar de la especie (ej. LITSTY = Litopenaeus stylirostris). |
| `sitio_code` | `str` | `SLG` | Código corto del campo o comunidad pesquera (ej. SLG, PLO). |
| `Met_Pesca` | `str` | `Chinchorro` | Método o arte de pesca registrado (ej. Chinchorro, Trampa, Buceo). |
| `HABITAT` | `str` | `arena` | Tipo de sustrato o hábitat bentónico (ej. arena, arrecife, fango). |
| `CODE_COMP` | `str` | `SLG04SP030506_B` | Código compuesto de identificación espacial. |
| `CODE_FIN` | `str` | `SLG04SP030506_B_LITSTY` | Código final concatenado de sitio, entrevista y especie. |
| `Shape_Length` | `float64` | `52970.66149454901` | Perímetro total del polígono expresado en metros. |
| `Shape_Area` | `float64` | `199078841.69311696` | Superficie o área total del polígono expresada en metros cuadrados. |

---

### Paquete 04: `04_ZPesca_PANGAS`
**Título de la Capa:** Base Unificada de Zonas Pesqueras PANGAS  
**Ubicación en Repositorio:** `output/paquetes_capas_pangas/04_ZPesca_PANGAS/`  
**Cita de Origen:** Moreno-Báez, M., et al. (2011, 2012). Ocean & Coastal Management / Marine Policy.  
**Entidades (Polígonos):** 4,241 | **Artes de Pesca:** Multiespecie / PANGAS  
**Bounding Box (WGS84):** `MinLon: -114.9492, MinLat: 27.9883, MaxLon: -111.5713, MaxLat: 31.8958`  
**Descripción Accesible:** Capa geográfica consolidada que reúne todos los mapas de uso pesquero trazados durante el proyecto histórico PANGAS (Dra. Marcia Moreno-Báez et al.).  

#### Mapas Georreferenciados
- **Mapa Base OpenStreetMap (Estilo QGIS):** `output/paquetes_capas_pangas/04_ZPesca_PANGAS/mapa_osm.jpg`
- **Mapa Base Satelital Esri:** `output/paquetes_capas_pangas/04_ZPesca_PANGAS/mapa_satelital.jpg`

#### Tabla de Atributos Extraídos Estilo QGIS (19 Campos)

| Nombre del Campo | Tipo de Dato (QGIS/GDAL) | Valor de Ejemplo | Descripción y Rol Metodológico |
|---|---|---|---|
| `Id` | `int32` | `1` | Identificador único numérico del registro de zona pesquera. |
| `CODE` | `str` | `-` | Código alfanumérico asignado al polígono de pesca. |
| `M` | `str` | `1` | Indicador del mes o temporada (1 = activo, 0 = inactivo). |
| `J` | `str` | `1` | Indicador estacional o de pesquería. |
| `R` | `str` | `0` | Indicador de región o zona pesquera. |
| `G` | `str` | `0` | Indicador de grupo pesquero o gremio. |
| `ENTREVIS` | `str` | `SLG04SP030506` | Código único de la encuesta o entrevista participativa PANGAS. |
| `Ent_num` | `int16` | `4` | Número secuencial de la entrevista efectuada. |
| `Entvsdr` | `str` | `SP` | Iniciales o código del entrevistador de campo. |
| `spp_code` | `str` | `LITSTY` | Código taxonómico estándar de la especie (ej. LITSTY = Litopenaeus stylirostris). |
| `sitio_code` | `str` | `SLG` | Código corto del campo o comunidad pesquera (ej. SLG, PLO). |
| `HABITAT` | `str` | `arena` | Tipo de sustrato o hábitat bentónico (ej. arena, arrecife, fango). |
| `day` | `int16` | `5` | Día del registro participativo. |
| `month` | `int16` | `3` | Mes del registro participativo. |
| `year` | `int16` | `2006` | Año del registro participativo. |
| `sitio_nomb` | `str` | `Reserva de la Biosfera AGC-DRC` | Nombre oficial del sitio o Área Natural Protegida. |
| `CODE_COMP` | `str` | `SLG04SP030506_LITSTY_-` | Código compuesto de identificación espacial. |
| `Shape_Length` | `float64` | `6982.154519027305` | Perímetro total del polígono expresado en metros. |
| `Shape_Area` | `float64` | `3567391.412694994` | Superficie o área total del polígono expresada en metros cuadrados. |

---

### Paquete 05: `05_ZPesca_Redes`
**Título de la Capa:** Polígonos de Pesca con Redes de Enmalle  
**Ubicación en Repositorio:** `output/paquetes_capas_pangas/05_ZPesca_Redes/`  
**Cita de Origen:** Moreno-Báez, M., et al. (2011, 2012). Ocean & Coastal Management / Marine Policy.  
**Entidades (Polígonos):** 1,263 | **Artes de Pesca:** Redes agalleras de fondo y deriva  
**Bounding Box (WGS84):** `MinLon: -114.9402, MinLat: 27.9883, MaxLon: -111.6857, MaxLat: 31.8724`  
**Descripción Accesible:** Sitios marinos donde se colocan redes agalleras verticales en la columna de agua o en el fondo marino para capturar cazón, tiburón pequeño, raya y pargo.  

#### Mapas Georreferenciados
- **Mapa Base OpenStreetMap (Estilo QGIS):** `output/paquetes_capas_pangas/05_ZPesca_Redes/mapa_osm.jpg`
- **Mapa Base Satelital Esri:** `output/paquetes_capas_pangas/05_ZPesca_Redes/mapa_satelital.jpg`

#### Tabla de Atributos Extraídos Estilo QGIS (24 Campos)

| Nombre del Campo | Tipo de Dato (QGIS/GDAL) | Valor de Ejemplo | Descripción y Rol Metodológico |
|---|---|---|---|
| `Id` | `int32` | `1` | Identificador único numérico del registro de zona pesquera. |
| `CODE` | `str` | ` ` | Código alfanumérico asignado al polígono de pesca. |
| `M` | `str` | `1` | Indicador del mes o temporada (1 = activo, 0 = inactivo). |
| `J` | `str` | `1` | Indicador estacional o de pesquería. |
| `R` | `str` | `0` | Indicador de región o zona pesquera. |
| `G` | `str` | `0` | Indicador de grupo pesquero o gremio. |
| `NAME` | `str` | ` ` | Nombre geográfico o toponímico del sitio de pesca. |
| `ENTREVIS` | `str` | `SLG04SP030506` | Código único de la encuesta o entrevista participativa PANGAS. |
| `Int_id` | `int32` | `0` | Identificador numérico del pescador o informante clave. |
| `Ent_num` | `int16` | `4` | Número secuencial de la entrevista efectuada. |
| `Entvsdr` | `str` | `SP` | Iniciales o código del entrevistador de campo. |
| `mes` | `int16` | `0` | Mes del levantamiento o temporada de pesca (1-12). |
| `dia` | `int16` | `0` | Día del levantamiento en campo. |
| `ano` | `int16` | `0` | Año del registro de la información (ej. 2005, 2006). |
| `spp_code` | `str` | `LITSTY` | Código taxonómico estándar de la especie (ej. LITSTY = Litopenaeus stylirostris). |
| `sitio_code` | `str` | `SLG` | Código corto del campo o comunidad pesquera (ej. SLG, PLO). |
| `Met_Pesca` | `str` | `Chinchorro` | Método o arte de pesca registrado (ej. Chinchorro, Trampa, Buceo). |
| `HABITAT` | `str` | `arena` | Tipo de sustrato o hábitat bentónico (ej. arena, arrecife, fango). |
| `weight_pc` | `float64` | `0.0` | Ponderación porcentual de uso pesquero. |
| `NorSur` | `int16` | `1` | Orientación geográfica del caladero (1 = Norte, 0 = Sur). |
| `TEMP` | `str` | `SLG04SP030506_LITSTY_` | Código de identificación temporal del polígono. |
| `NAME_ORG` | `str` | ` ` | Nombre registrado originalmente en las entrevistas. |
| `Shape_Length` | `float64` | `6982.154519027305` | Perímetro total del polígono expresado en metros. |
| `Shape_Area` | `float64` | `3567391.412694994` | Superficie o área total del polígono expresada en metros cuadrados. |

---

### Paquete 06: `06_ZPesca_Redes_Manta_Camaron`
**Título de la Capa:** Polígonos de Pesca de Camarón y Redes de Manta  
**Ubicación en Repositorio:** `output/paquetes_capas_pangas/06_ZPesca_Redes_Manta_Camaron/`  
**Cita de Origen:** Moreno-Báez, M., et al. (2011, 2012). Ocean & Coastal Management / Marine Policy.  
**Entidades (Polígonos):** 783 | **Artes de Pesca:** Red de manta / Red surpera de camarón  
**Bounding Box (WGS84):** `MinLon: -114.9402, MinLat: 28.6917, MaxLon: -111.8732, MaxLat: 31.8724`  
**Descripción Accesible:** Caladeros costeros de gran importancia económica donde se realiza la pesca de camarón (azul, café y blanco) durante la temporada de zafra.  

#### Mapas Georreferenciados
- **Mapa Base OpenStreetMap (Estilo QGIS):** `output/paquetes_capas_pangas/06_ZPesca_Redes_Manta_Camaron/mapa_osm.jpg`
- **Mapa Base Satelital Esri:** `output/paquetes_capas_pangas/06_ZPesca_Redes_Manta_Camaron/mapa_satelital.jpg`

#### Tabla de Atributos Extraídos Estilo QGIS (24 Campos)

| Nombre del Campo | Tipo de Dato (QGIS/GDAL) | Valor de Ejemplo | Descripción y Rol Metodológico |
|---|---|---|---|
| `Id` | `int32` | `1` | Identificador único numérico del registro de zona pesquera. |
| `CODE` | `str` | ` ` | Código alfanumérico asignado al polígono de pesca. |
| `M` | `str` | `1` | Indicador del mes o temporada (1 = activo, 0 = inactivo). |
| `J` | `str` | `1` | Indicador estacional o de pesquería. |
| `R` | `str` | `0` | Indicador de región o zona pesquera. |
| `G` | `str` | `0` | Indicador de grupo pesquero o gremio. |
| `NAME` | `str` | ` ` | Nombre geográfico o toponímico del sitio de pesca. |
| `ENTREVIS` | `str` | `SLG04SP030506` | Código único de la encuesta o entrevista participativa PANGAS. |
| `Int_id` | `int32` | `0` | Identificador numérico del pescador o informante clave. |
| `Ent_num` | `int16` | `4` | Número secuencial de la entrevista efectuada. |
| `Entvsdr` | `str` | `SP` | Iniciales o código del entrevistador de campo. |
| `mes` | `int16` | `0` | Mes del levantamiento o temporada de pesca (1-12). |
| `dia` | `int16` | `0` | Día del levantamiento en campo. |
| `ano` | `int16` | `0` | Año del registro de la información (ej. 2005, 2006). |
| `spp_code` | `str` | `LITSTY` | Código taxonómico estándar de la especie (ej. LITSTY = Litopenaeus stylirostris). |
| `sitio_code` | `str` | `SLG` | Código corto del campo o comunidad pesquera (ej. SLG, PLO). |
| `Met_Pesca` | `str` | `Chinchorro` | Método o arte de pesca registrado (ej. Chinchorro, Trampa, Buceo). |
| `HABITAT` | `str` | `arena` | Tipo de sustrato o hábitat bentónico (ej. arena, arrecife, fango). |
| `weight_pc` | `float64` | `0.0` | Ponderación porcentual de uso pesquero. |
| `NorSur` | `int16` | `1` | Orientación geográfica del caladero (1 = Norte, 0 = Sur). |
| `TEMP` | `str` | `SLG04SP030506_LITSTY_` | Código de identificación temporal del polígono. |
| `NAME_ORG` | `str` | ` ` | Nombre registrado originalmente en las entrevistas. |
| `Shape_Length` | `float64` | `6982.154519027305` | Perímetro total del polígono expresado en metros. |
| `Shape_Area` | `float64` | `3567391.412694994` | Superficie o área total del polígono expresada en metros cuadrados. |

---

### Paquete 07: `07_ZPesca_Trampa`
**Título de la Capa:** Polígonos de Pesca con Trampas (Jaiba y Peces)  
**Ubicación en Repositorio:** `output/paquetes_capas_pangas/07_ZPesca_Trampa/`  
**Cita de Origen:** Moreno-Báez, M., et al. (2011, 2012). Ocean & Coastal Management / Marine Policy.  
**Entidades (Polígonos):** 360 | **Artes de Pesca:** Trampas metálicas / Nasas jaiberas  
**Bounding Box (WGS84):** `MinLon: -114.7043, MinLat: 28.3656, MaxLon: -111.5806, MaxLat: 31.6367`  
**Descripción Accesible:** Zonas protegidas cerca de bahías y esteros donde los pescadores depositan jaulas o trampas cebadas en el fondo para jaiba azul, jaiba café y peces de rocas.  

#### Mapas Georreferenciados
- **Mapa Base OpenStreetMap (Estilo QGIS):** `output/paquetes_capas_pangas/07_ZPesca_Trampa/mapa_osm.jpg`
- **Mapa Base Satelital Esri:** `output/paquetes_capas_pangas/07_ZPesca_Trampa/mapa_satelital.jpg`

#### Tabla de Atributos Extraídos Estilo QGIS (22 Campos)

| Nombre del Campo | Tipo de Dato (QGIS/GDAL) | Valor de Ejemplo | Descripción y Rol Metodológico |
|---|---|---|---|
| `Id` | `int32` | `848` | Identificador único numérico del registro de zona pesquera. |
| `CODE` | `str` | `B` | Código alfanumérico asignado al polígono de pesca. |
| `M` | `str` | `0` | Indicador del mes o temporada (1 = activo, 0 = inactivo). |
| `J` | `str` | `0` | Indicador estacional o de pesquería. |
| `R` | `str` | `0` | Indicador de región o zona pesquera. |
| `G` | `str` | `0` | Indicador de grupo pesquero o gremio. |
| `NAME` | `str` | `Lizos` | Nombre geográfico o toponímico del sitio de pesca. |
| `ENTREVIS` | `str` | `PLO08OM121605` | Código único de la encuesta o entrevista participativa PANGAS. |
| `Int_id` | `int32` | `163` | Identificador numérico del pescador o informante clave. |
| `Ent_num` | `int16` | `8` | Número secuencial de la entrevista efectuada. |
| `Entvsdr` | `str` | `OM` | Iniciales o código del entrevistador de campo. |
| `mes` | `int16` | `12` | Mes del levantamiento o temporada de pesca (1-12). |
| `dia` | `int16` | `16` | Día del levantamiento en campo. |
| `ano` | `int16` | `2005` | Año del registro de la información (ej. 2005, 2006). |
| `spp_code` | `str` | `BALPOL` | Código taxonómico estándar de la especie (ej. LITSTY = Litopenaeus stylirostris). |
| `sitio_code` | `str` | `PLO` | Código corto del campo o comunidad pesquera (ej. SLG, PLO). |
| `Met_Pesca` | `str` | `Piola y trampa` | Método o arte de pesca registrado (ej. Chinchorro, Trampa, Buceo). |
| `HABITAT` | `str` | `arrecife` | Tipo de sustrato o hábitat bentónico (ej. arena, arrecife, fango). |
| `CODE_COMP` | `str` | `PLO08OM121605_B` | Código compuesto de identificación espacial. |
| `CODE_FIN` | `str` | `PLO08OM121605_B_BALPOL` | Código final concatenado de sitio, entrevista y especie. |
| `Shape_Length` | `float64` | `24247.542109495957` | Perímetro total del polígono expresado en metros. |
| `Shape_Area` | `float64` | `43907156.74350939` | Superficie o área total del polígono expresada en metros cuadrados. |

---

## 6. Atribución Académica Formal

Todas las capas del catálogo PANGAS presentadas en este documento proceden de la investigación:
> **Moreno-Báez, M., Cudney-Bueno, R., Shaw, W. W., Cudney-Bueno, S., & Torre-Cosío, J. (2011, 2012).**  
> *Integrating spatial and temporal dimensions of artisanal fishing for management in the Gulf of California, Mexico.*  
> Publicado en: *Ocean & Coastal Management* / *Marine Policy*.  
> Base de Datos Geográfica original del proyecto PANGAS.

---

## 7. Glosario de Términos no Técnicos para Revisores

Para apoyar la lectura de directivos, asesores y representantes comunitarios, a continuación se definen los términos técnicos clave empleados en este informe:

1. **Sistema de Información Geográfica (SIG):** Un programa de computadora especializado en crear, almacenar y analizar mapas digitales interactivos en lugar de mapas impresos en papel.
2. **GeoPackage (.gpkg):** Un formato de archivo moderno y estándar internacional que permite guardar en un solo archivo ligero de computadora múltiples mapas, líneas, puntos y tablas de datos de manera muy rápida.
3. **Sistema de Coordenadas (CRS) / WGS 84 (EPSG:4326):** El sistema global de latitud y longitud que utiliza el GPS de los teléfonos para saber exactamente en qué parte del planeta Tierra se encuentra un objeto.
4. **Proyección Web Mercator (EPSG:3857):** La forma matemática en que se aplana la esfera terrestre para mostrar mapas en pantallas de computadora y navegadores de internet (como Google Maps u OpenStreetMap).
5. **Bounding Box (Extensión Geográfica):** El marco o rectángulo imaginario definido por las coordenadas mínimas y máximas que encierran a todo un mapa o grupo de datos.
6. **Grilla H3 (Hexágonos de Uber):** Un sistema que divide la superficie del mar en miles de piezas de rompecabezas de seis lados (hexágonos) idénticos en tamaño, lo que permite medir y comparar variables de riesgo sin deformaciones.
7. **Metadatos:** La "ficha de identidad" o etiqueta que describe a un mapa o archivo digital (quién lo hizo, cuándo se creó, qué significan sus variables y con qué precisión fue medido).
8. **Topología:** Reglas matemáticas que aseguran que los mapas digitales no tengan errores como líneas encimadas, polígonos encimados por error o huecos vacíos donde debería haber datos.
9. **R-Tree (Índice Espacial):** Una tecnología interna dentro de las bases de datos geográficas que funciona como el índice de un libro, permitiendo encontrar un polígono o barco en el mapa en una fracción de segundo.
