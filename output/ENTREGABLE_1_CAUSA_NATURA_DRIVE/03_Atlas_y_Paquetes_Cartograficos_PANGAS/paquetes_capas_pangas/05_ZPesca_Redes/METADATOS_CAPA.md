# Paquete Geográfico y Metadatos: Capa `ZPesca_Redes`

**Título de la Capa:** Polígonos de Pesca con Redes de Enmalle  
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

- **Nombre de la Capa en GDB:** `ZPesca_Redes`
- **Tipo de Geometría:** `MultiPolygon`
- **Número Total de Polígonos / Entidades:** `1,263`
- **Sistema de Coordenadas Original:** EPSG:4326 (WGS 84 - Grados Decimales)
- **Proyección de Visualización:** EPSG:3857 (Web Mercator)
- **Extensión Geográfica (Bounding Box WGS84):** `MinLon: -114.9402, MinLat: 27.9883, MaxLon: -111.6857, MaxLat: 31.8724`
- **Artes de Pesca Relacionadas:** Redes de enmalle / Agalleras de fondo y deriva

---

## 3. Descripción Metodológica

Zonas de esfuerzo pesquero artesanal con redes agalleras de fondo y deriva para especies demersales y pelágicas.

---

## 4. Visualización Cartográfica Georreferenciada

### Mapa Base: OpenStreetMap Estándar (Estilo QGIS)
![Mapa OpenStreetMap](mapa_osm.jpg)

### Mapa Base: Esri World Imagery (Satelital)
![Mapa Satelital Esri](mapa_satelital.jpg)

---

## 5. Tabla de Atributos Extraídos Estilo QGIS (24 Campos)

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

### Muestra de Especies Registradas (Códigos SPP):
`GYMMAR, LITSTY, MUSCAL, MUSLUN, MUSSPP, MYLCAL, MYLLON, RHILON, RHIPRO, RHISPP`
