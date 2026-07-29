# Catálogo Espacial de Capas de la Base de Datos PANGAS (Fish_Zones_PANGAS.gdb)

**Proyecto:** Índice Espacial de Riesgo Socioeconómico para Comunidades (IERC-GNL)  
**Organización:** Causa Natura Data (POA 2026-2028)  
**Entregable:** Inventario y Catálogo Cartográfico de Gabinete (Meta 1)  
**Autores del Equipo Técnico:**
- **Juan Carlos Barrera (JCB):** Consultor Senior / Especialista Pesquero y Socioambiental
- **Enrique Gorosave (EG):** Analista de Datos y SIG

---

## 1. Resumen Ejecutivo de la Base de Conocimiento PANGAS

El presente Catálogo Espacial compila y documenta las 7 capas geográficas contenidas en la base de datos `Fish_Zones_PANGAS.gdb`. Constituye la línea base histórica del esfuerzo pesquero artesanal en el Golfo de California (Moreno-Báez et al. 2011, 2012) utilizada para orientar la fase de campo y calibrar los sub-índices de exposición y sensibilidad del IERC.

---

## 2. Índice General de Capas

| Capa GDB | Tipo Geometría | N° Entidades | Artes de Pesca / Categoría |
|---|---|---|---|
| `Riqueza_Relativa` | `MultiPolygon` | 11,065 | Todas las artes registradas |
| `ZPesca_Buceo` | `MultiPolygon` | 249 | Buceo autónomo y semiautónomo (Hookah) |
| `ZPesca_Chinchorro` | `MultiPolygon` | 2,209 | Chinchorro de línea / Redes agalleras |
| `ZPesca_PANGAS` | `MultiPolygon` | 4,241 | Multiespecie / PANGAS |
| `ZPesca_Redes` | `MultiPolygon` | 1,263 | Redes de enmalle / Agalleras |
| `ZPesca_Redes_Manta_Camaron` | `MultiPolygon` | 783 | Redes de manta / Surpera / Camarón |
| `ZPesca_Trampa` | `MultiPolygon` | 360 | Trampas jaiberas / Nasas |

---

## 3. Fichas Técnicas Detalladas por Capa

### Capa: `Riqueza_Relativa`

**Título:** Malla de Riqueza Biológica Pesquera Relativa  
**Tipo de Geometría:** MultiPolygon  
**Número de Entidades:** 11,065  
**Sistema de Referencia:** EPSG:4326 (WGS 84 - Coordenadas Geográficas)  
**Extensión Espacial (Bounding Box):** `MinLon: -114.9307, MinLat: 27.2977, MaxLon: -110.5188, MaxLat: 31.8423`  
**Artes de Pesca Asociadas:** Todas las artes registradas  
**Responsables del Procesamiento:** EG / JCB  

**Descripción Metodológica:**  
Polígonos de grilla espacial con acumulación de riqueza de especies de peces y mariscos comerciales del Golfo de California (Estudio PANGAS).

**Mapa Cartográfico Renderizado (JPG Alta Resolución):**  
![Mapa Riqueza_Relativa](file:///home/gorops/ierc-gnl-project/output/atlas_pangas_jpg/mapa_Riqueza_Relativa.jpg)

**Esquema de Atributos (52 Campos):**

| Nombre de Campo | Tipo de Dato | Descripción / Rol |
|---|---|---|
| `artnob` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `atrtub` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `balpol` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `calbel` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `carlim` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `carspp` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `cynoth` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `cynpar` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `cynspp` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `dasdip` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `dasspp` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `dospon` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `epiaca` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `epiana` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `epispp` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |

---

### Capa: `ZPesca_Buceo`

**Título:** Polígonos de Pesca Comercial por Buceo  
**Tipo de Geometría:** MultiPolygon  
**Número de Entidades:** 249  
**Sistema de Referencia:** EPSG:4326 (WGS 84 - Coordenadas Geográficas)  
**Extensión Espacial (Bounding Box):** `MinLon: -114.1083, MinLat: 27.4209, MaxLon: -111.7763, MaxLat: 31.5724`  
**Artes de Pesca Asociadas:** Buceo autónomo y semiautónomo (Hookah)  
**Responsables del Procesamiento:** EG / JCB  

**Descripción Metodológica:**  
Sitios y caladeros de pesca artesanal extractiva mediante buceo (moluscos, bentónicos, almeja, callo de hacha, erizo, pepino de mar).

**Mapa Cartográfico Renderizado (JPG Alta Resolución):**  
![Mapa ZPesca_Buceo](file:///home/gorops/ierc-gnl-project/output/atlas_pangas_jpg/mapa_ZPesca_Buceo.jpg)

**Esquema de Atributos (5 Campos):**

| Nombre de Campo | Tipo de Dato | Descripción / Rol |
|---|---|---|
| `no_comunid` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `comunidad` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `ORIG_FID` | `int32` | Atributo descriptivo de la capa pesquera PANGAS |
| `Shape_Length` | `float64` | Atributo descriptivo de la capa pesquera PANGAS |
| `Shape_Area` | `float64` | Atributo descriptivo de la capa pesquera PANGAS |

---

### Capa: `ZPesca_Chinchorro`

**Título:** Polígonos de Pesca con Chinchorro de Línea  
**Tipo de Geometría:** MultiPolygon  
**Número de Entidades:** 2,209  
**Sistema de Referencia:** EPSG:4326 (WGS 84 - Coordenadas Geográficas)  
**Extensión Espacial (Bounding Box):** `MinLon: -114.9171, MinLat: 27.9883, MaxLon: -111.4621, MaxLat: 31.8624`  
**Artes de Pesca Asociadas:** Chinchorro de línea / Redes agalleras  
**Responsables del Procesamiento:** EG / JCB  

**Descripción Metodológica:**  
Zonas de operación pesquera artesanal mediante chinchorros de línea de playa y deriva para especies escamadas.

**Mapa Cartográfico Renderizado (JPG Alta Resolución):**  
![Mapa ZPesca_Chinchorro](file:///home/gorops/ierc-gnl-project/output/atlas_pangas_jpg/mapa_ZPesca_Chinchorro.jpg)

**Esquema de Atributos (22 Campos):**

| Nombre de Campo | Tipo de Dato | Descripción / Rol |
|---|---|---|
| `Id` | `int32` | Atributo descriptivo de la capa pesquera PANGAS |
| `CODE` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `M` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `J` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `R` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `G` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `NAME` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `ENTREVIS` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `Int_id` | `int32` | Atributo descriptivo de la capa pesquera PANGAS |
| `Ent_num` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `Entvsdr` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `mes` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `dia` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `ano` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `spp_code` | `str` | Atributo descriptivo de la capa pesquera PANGAS |

**Especies Registradas (Muestra spp_code):** `ATRNOB, CARANX, CARLIM, CARSPP, CYNOTH, CYNPAR, CYNSPP, DASDIP, DASSPP, GYMMAR, HOPGUE, LITSTY, LUTARG, MICMEG, MUGSPP, MUSCAL, MUSLUN, MUSSPP, MYCJOR, MYLCAL`

---

### Capa: `ZPesca_PANGAS`

**Título:** Base Unificada de Zonas Pesqueras PANGAS  
**Tipo de Geometría:** MultiPolygon  
**Número de Entidades:** 4,241  
**Sistema de Referencia:** EPSG:4326 (WGS 84 - Coordenadas Geográficas)  
**Extensión Espacial (Bounding Box):** `MinLon: -114.9492, MinLat: 27.9883, MaxLon: -111.5713, MaxLat: 31.8958`  
**Artes de Pesca Asociadas:** Multiespecie / PANGAS  
**Responsables del Procesamiento:** EG / JCB  

**Descripción Metodológica:**  
Capa maestra consolidada de campos pesqueros artesanales del Golfo de California derivada de entrevistas participativas.

**Mapa Cartográfico Renderizado (JPG Alta Resolución):**  
![Mapa ZPesca_PANGAS](file:///home/gorops/ierc-gnl-project/output/atlas_pangas_jpg/mapa_ZPesca_PANGAS.jpg)

**Esquema de Atributos (19 Campos):**

| Nombre de Campo | Tipo de Dato | Descripción / Rol |
|---|---|---|
| `Id` | `int32` | Atributo descriptivo de la capa pesquera PANGAS |
| `CODE` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `M` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `J` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `R` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `G` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `ENTREVIS` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `Ent_num` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `Entvsdr` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `spp_code` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `sitio_code` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `HABITAT` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `day` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `month` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `year` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |

**Especies Registradas (Muestra spp_code):** `ATRNOB, ATRTUB, BALPOL, CALBEL, CARANX, CARLIM, CARSPP, CYNOTH, CYNPAR, CYNSPP, DASSPP, DOSPON, EPIACA, EPIANA, EPISPP, GYMMAR, HEXNIG, HOPGUE, ISOFUS, LITSTY`

---

### Capa: `ZPesca_Redes`

**Título:** Polígonos de Pesca con Redes de Enmalle  
**Tipo de Geometría:** MultiPolygon  
**Número de Entidades:** 1,263  
**Sistema de Referencia:** EPSG:4326 (WGS 84 - Coordenadas Geográficas)  
**Extensión Espacial (Bounding Box):** `MinLon: -114.9402, MinLat: 27.9883, MaxLon: -111.6857, MaxLat: 31.8724`  
**Artes de Pesca Asociadas:** Redes de enmalle / Agalleras  
**Responsables del Procesamiento:** EG / JCB  

**Descripción Metodológica:**  
Zonas de esfuerzo pesquero artesanal con redes agalleras y agalleras de fondo para peces demersales y pelágicos menores.

**Mapa Cartográfico Renderizado (JPG Alta Resolución):**  
![Mapa ZPesca_Redes](file:///home/gorops/ierc-gnl-project/output/atlas_pangas_jpg/mapa_ZPesca_Redes.jpg)

**Esquema de Atributos (24 Campos):**

| Nombre de Campo | Tipo de Dato | Descripción / Rol |
|---|---|---|
| `Id` | `int32` | Atributo descriptivo de la capa pesquera PANGAS |
| `CODE` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `M` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `J` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `R` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `G` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `NAME` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `ENTREVIS` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `Int_id` | `int32` | Atributo descriptivo de la capa pesquera PANGAS |
| `Ent_num` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `Entvsdr` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `mes` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `dia` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `ano` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `spp_code` | `str` | Atributo descriptivo de la capa pesquera PANGAS |

**Especies Registradas (Muestra spp_code):** `GYMMAR, LITSTY, MUSCAL, MUSLUN, MUSSPP, MYLCAL, MYLLON, RHILON, RHIPRO, RHISPP`

---

### Capa: `ZPesca_Redes_Manta_Camaron`

**Título:** Polígonos de Pesca de Camarón y Redes de Manta  
**Tipo de Geometría:** MultiPolygon  
**Número de Entidades:** 783  
**Sistema de Referencia:** EPSG:4326 (WGS 84 - Coordenadas Geográficas)  
**Extensión Espacial (Bounding Box):** `MinLon: -114.9402, MinLat: 28.6917, MaxLon: -111.8732, MaxLat: 31.8724`  
**Artes de Pesca Asociadas:** Redes de manta / Surpera / Camarón  
**Responsables del Procesamiento:** EG / JCB  

**Descripción Metodológica:**  
Caladeros de pesca estacional de camarón con redes de manta y surpera en el litoral de Sonora y Sinaloa.

**Mapa Cartográfico Renderizado (JPG Alta Resolución):**  
![Mapa ZPesca_Redes_Manta_Camaron](file:///home/gorops/ierc-gnl-project/output/atlas_pangas_jpg/mapa_ZPesca_Redes_Manta_Camaron.jpg)

**Esquema de Atributos (24 Campos):**

| Nombre de Campo | Tipo de Dato | Descripción / Rol |
|---|---|---|
| `Id` | `int32` | Atributo descriptivo de la capa pesquera PANGAS |
| `CODE` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `M` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `J` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `R` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `G` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `NAME` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `ENTREVIS` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `Int_id` | `int32` | Atributo descriptivo de la capa pesquera PANGAS |
| `Ent_num` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `Entvsdr` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `mes` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `dia` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `ano` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `spp_code` | `str` | Atributo descriptivo de la capa pesquera PANGAS |

**Especies Registradas (Muestra spp_code):** `GYMMAR, LITSTY, MYLCAL, MYLLON`

---

### Capa: `ZPesca_Trampa`

**Título:** Polígonos de Pesca con Trampas (Jaiba y Peces)  
**Tipo de Geometría:** MultiPolygon  
**Número de Entidades:** 360  
**Sistema de Referencia:** EPSG:4326 (WGS 84 - Coordenadas Geográficas)  
**Extensión Espacial (Bounding Box):** `MinLon: -114.7043, MinLat: 28.3656, MaxLon: -111.5806, MaxLat: 31.6367`  
**Artes de Pesca Asociadas:** Trampas jaiberas / Nasas  
**Responsables del Procesamiento:** EG / JCB  

**Descripción Metodológica:**  
Sitios de pesca artesanal costera y estuarina mediante trampas y nasas para jaiba azul y especies de rocas.

**Mapa Cartográfico Renderizado (JPG Alta Resolución):**  
![Mapa ZPesca_Trampa](file:///home/gorops/ierc-gnl-project/output/atlas_pangas_jpg/mapa_ZPesca_Trampa.jpg)

**Esquema de Atributos (22 Campos):**

| Nombre de Campo | Tipo de Dato | Descripción / Rol |
|---|---|---|
| `Id` | `int32` | Atributo descriptivo de la capa pesquera PANGAS |
| `CODE` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `M` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `J` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `R` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `G` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `NAME` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `ENTREVIS` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `Int_id` | `int32` | Atributo descriptivo de la capa pesquera PANGAS |
| `Ent_num` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `Entvsdr` | `str` | Atributo descriptivo de la capa pesquera PANGAS |
| `mes` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `dia` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `ano` | `int16` | Atributo descriptivo de la capa pesquera PANGAS |
| `spp_code` | `str` | Atributo descriptivo de la capa pesquera PANGAS |

**Especies Registradas (Muestra spp_code):** `BALPOL, CALBEL, PARSPP`

---

