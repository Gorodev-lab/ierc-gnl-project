# Paquete Geográfico y Metadatos: Capa `Riqueza_Relativa`

**Título de la Capa:** Malla de Riqueza Biológica Pesquera Relativa  
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

- **Nombre de la Capa en GDB:** `Riqueza_Relativa`
- **Tipo de Geometría:** `MultiPolygon`
- **Número Total de Polígonos / Entidades:** `11,065`
- **Sistema de Coordenadas Original:** EPSG:4326 (WGS 84 - Grados Decimales)
- **Proyección de Visualización:** EPSG:3857 (Web Mercator)
- **Extensión Geográfica (Bounding Box WGS84):** `MinLon: -114.9307, MinLat: 27.2977, MaxLon: -110.5188, MaxLat: 31.8423`
- **Artes de Pesca Relacionadas:** Todas las artes de pesca artesanal registradas en el Golfo de California

---

## 3. Descripción Metodológica

Polígonos de grilla espacial con acumulación de riqueza biológica pesquera derivada de las entrevistas del estudio PANGAS.

---

## 4. Visualización Cartográfica Georreferenciada

### Mapa Base: OpenStreetMap Estándar (Estilo QGIS)
![Mapa OpenStreetMap](mapa_osm.jpg)

### Mapa Base: Esri World Imagery (Satelital)
![Mapa Satelital Esri](mapa_satelital.jpg)

---

## 5. Diccionario de Atributos (52 Campos)

| Nombre de Campo | Tipo de Dato | Rol / Descripción Metodológica |
|---|---|---|
| `artnob` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `atrtub` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `balpol` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `calbel` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `carlim` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `carspp` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `cynoth` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `cynpar` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `cynspp` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `dasdip` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `dasspp` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `dospon` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `epiaca` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `epiana` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `epispp` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `gymmar` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `hexnig` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `hopgue` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `isofus` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `litsty` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `lutarg` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `lutper` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `micmeg` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `mugspp` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `muscal` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `muslun` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `musspp` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `mycjor` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `mycpri` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `mycros` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `mylcal` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `myllon` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `octspp` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `pangen` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `paninf` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `paraur` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `parmac` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `parple` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `parspp` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `phyery` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `pinrug` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `rhilon` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `rhipro` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `rhispp` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `scospp` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `sphspp` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `spocal` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `squcal` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `stegig` | `int16` | Atributo espacial/pesquero registrado en PANGAS |
| `all` | `float64` | Atributo espacial/pesquero registrado en PANGAS |
| `Shape_Length` | `float64` | Atributo espacial/pesquero registrado en PANGAS |
| `Shape_Area` | `float64` | Atributo espacial/pesquero registrado en PANGAS |
