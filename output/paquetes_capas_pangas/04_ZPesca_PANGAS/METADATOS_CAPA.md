# Paquete Geográfico y Metadatos: Capa `ZPesca_PANGAS`

**Título de la Capa:** Base Unificada de Zonas Pesqueras PANGAS  
**Base de Datos de Origen:** `Fish_Zones_PANGAS.gdb` (Estudio PANGAS)  

---

## 1. Atribución Académica y Cita Oficial

**Autora Principal de la Base de Datos:** Dra. Marcia Moreno-Báez et al.  
**Cita Académica Completa:**  
> Moreno-Báez, M., Cudney-Bueno, R., Shaw, W. W., Cudney-Bueno, S., & Torre-Cosío, J. (2011, 2012). Integrating spatial and temporal dimensions of artisanal fishing for management in the Gulf of California, Mexico. Ocean & Coastal Management / Marine Policy. Base de Datos Geográfica PANGAS.

**Uso y Adaptación Metodológica:**  
Esta capa constituye la línea base histórica del estudio PANGAS utilizada por **Juan Carlos Barrera (JCB - Consultor Senior)** y **Enrique Gorosave (EG - Analista GIS)** para el proyecto **IERC-GNL** de **Causa Natura Data (POA 2026-2028)**. Se utiliza para calibrar la exposición y sensibilidad de las comunidades pesqueras ante la infraestructura de Gas Natural Licuado en el Golfo de California.

---

## 2. Ficha Técnica Espacial

- **Nombre de la Capa en GDB:** `ZPesca_PANGAS`
- **Tipo de Geometría:** `MultiPolygon`
- **Número Total de Polígonos / Entidades:** `4,241`
- **Sistema de Coordenadas Original:** EPSG:4326 (WGS 84 - Grados Decimales)
- **Proyección de Visualización:** EPSG:3857 (Web Mercator)
- **Extensión Geográfica (Bounding Box WGS84):** `MinLon: -114.9492, MinLat: 27.9883, MaxLon: -111.5713, MaxLat: 31.8958`
- **Artes de Pesca Relacionadas:** Multiespecie / PANGAS

---

## 3. Descripción Metodológica

Capa geográfica consolidada de campos pesqueros artesanales del Golfo de California basada en el mapeo participativo original de la Dra. Marcia Moreno-Báez.

---

## 4. Visualización Cartográfica Georreferenciada

### Mapa Base: OpenStreetMap Estándar (Estilo QGIS)
![Mapa OpenStreetMap](mapa_osm.jpg)

### Mapa Base: Esri World Imagery (Satelital)
![Mapa Satelital Esri](mapa_satelital.jpg)

---

## 5. Tabla de Atributos Extraídos Estilo QGIS (19 Campos)

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

### Muestra de Especies Registradas (Códigos SPP):
`ATRNOB, ATRTUB, BALPOL, CALBEL, CARANX, CARLIM, CARSPP, CYNOTH, CYNPAR, CYNSPP, DASSPP, DOSPON, EPIACA, EPIANA, EPISPP, GYMMAR, HEXNIG, HOPGUE, ISOFUS, LITSTY, LUTARG, LUTPER, MICMEG, MUGSPP, MUSCAL`
