# Paquete Geográfico y Metadatos: Capa `ZPesca_Chinchorro`

**Título de la Capa:** Polígonos de Pesca con Chinchorro de Línea  
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

- **Nombre de la Capa en GDB:** `ZPesca_Chinchorro`
- **Tipo de Geometría:** `MultiPolygon`
- **Número Total de Polígonos / Entidades:** `2,209`
- **Sistema de Coordenadas Original:** EPSG:4326 (WGS 84 - Grados Decimales)
- **Proyección de Visualización:** EPSG:3857 (Web Mercator)
- **Extensión Geográfica (Bounding Box WGS84):** `MinLon: -114.9171, MinLat: 27.9883, MaxLon: -111.4621, MaxLat: 31.8624`
- **Artes de Pesca Relacionadas:** Chinchorro de línea / Redes agalleras de playa

---

## 3. Descripción Metodológica

Zonas de operación pesquera artesanal mediante chinchorros de línea de playa y deriva para capturas de peces de escama.

---

## 4. Visualización Cartográfica Georreferenciada

### Mapa Base: OpenStreetMap Estándar (Estilo QGIS)
![Mapa OpenStreetMap](mapa_osm.jpg)

### Mapa Base: Esri World Imagery (Satelital)
![Mapa Satelital Esri](mapa_satelital.jpg)

---

## 5. Diccionario de Atributos (22 Campos)

| Nombre de Campo | Tipo de Dato | Rol / Descripción Metodológica |
|---|---|---|
| `Id` | `int32` | Atributo espacial/pesquero registrado en PANGAS |
| `CODE` | `str` | Atributo espacial/pesquero registrado en PANGAS |
| `M` | `str` | Atributo espacial/pesquero registrado en PANGAS |
| `J` | `str` | Atributo espacial/pesquero registrado en PANGAS |
| `R` | `str` | Atributo espacial/pesquero registrado en PANGAS |
| `G` | `str` | Atributo espacial/pesquero registrado en PANGAS |
| `NAME` | `str` | Atributo espacial/pesquero registrado en PANGAS |
| `ENTREVIS` | `str` | Atributo espacial/pesquero registrado en PANGAS |
| `Int_id` | `int32` | Atributo espacial/pesquero registrado en PANGAS |
| `Ent_num` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `Entvsdr` | `str` | Atributo espacial/pesquero registrado en PANGAS |
| `mes` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `dia` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `ano` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `spp_code` | `str` | Atributo espacial/pesquero registrado en PANGAS |
| `sitio_code` | `str` | Atributo espacial/pesquero registrado en PANGAS |
| `Met_Pesca` | `str` | Atributo espacial/pesquero registrado en PANGAS |
| `HABITAT` | `str` | Atributo espacial/pesquero registrado en PANGAS |
| `CODE_COMP` | `str` | Atributo espacial/pesquero registrado en PANGAS |
| `CODE_FIN` | `str` | Atributo espacial/pesquero registrado en PANGAS |
| `Shape_Length` | `float64` | Atributo espacial/pesquero registrado en PANGAS |
| `Shape_Area` | `float64` | Atributo espacial/pesquero registrado en PANGAS |

### Muestra de Especies Registradas (Códigos SPP):
`ATRNOB, CARANX, CARLIM, CARSPP, CYNOTH, CYNPAR, CYNSPP, DASDIP, DASSPP, GYMMAR, HOPGUE, LITSTY, LUTARG, MICMEG, MUGSPP, MUSCAL, MUSLUN, MUSSPP, MYCJOR, MYLCAL, MYLLON, PARPLE, RHILON, RHIPRO, RHISPP`
