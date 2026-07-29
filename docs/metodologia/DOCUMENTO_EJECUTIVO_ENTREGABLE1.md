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
  - Contiene el diccionario técnico de datos: [`GEOPACKAGE_METADATA.md`](file:///home/gorops/ierc-gnl-project/deliverables/v1_geopackage/GEOPACKAGE_METADATA.md).
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

El archivo `ierc_golfo_california.gpkg` almacena 7 capas vectoriales organizadas bajo un estándar unificado de coordenadas geograficas (`EPSG:4326 - WGS 84`):

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
$$\text{Clave} = \text{comunidad} - \text{actor} - \text{pesquería} - \text{arte} - \text{zona} - \text{temporada} - \text{ruta}$$

> **Explicación Accesible:**  
> Es como el número de CURP o código postal de una actividad de pesca. Nos dice exactamente: *quién pesca* (comunidad y actor), *qué pesca* (especie o pesquería), *con qué herramienta* (arte de pesca), *en dónde* (zona), *en qué época del año* (temporada) y *por dónde navega* (ruta).

---

## 5. Catálogo de Paquetes Cartográficos por Capa (Línea Base PANGAS)

A continuación se presenta el desglose de las 7 capas pesqueras de la base de datos `Fish_Zones_PANGAS.gdb`, atribuidas a la investigación de la **Dra. Marcia Moreno-Báez et al. (2011, 2012)**. Cada paquete cuenta con 2 mapas georreferenciados en proyección Web Mercator (`EPSG:3857`): uno con el mapa base **OpenStreetMap estándar (estilo QGIS)** que muestra nombres de ciudades, carreteras y líneas de costa, y otro con el mapa **satelital Esri World Imagery**.

---

### Paquete 01: `01_Riqueza_Relativa`
**Título:** Malla de Riqueza Biológica Pesquera Relativa  
**Ubicación en Repositorio:** `output/paquetes_capas_pangas/01_Riqueza_Relativa/`  

#### Mapas Georreferenciados
- **Mapa Base OpenStreetMap (Estilo QGIS):** `output/paquetes_capas_pangas/01_Riqueza_Relativa/mapa_osm.jpg`
- **Mapa Base Satelital Esri:** `output/paquetes_capas_pangas/01_Riqueza_Relativa/mapa_satelital.jpg`

#### Ficha de Metadatos y Especificaciones
- **Tipo de Geometría:** Polígonos de Grilla Espacial
- **Número Total de Entidades (Polígonos):** 11,065
- **Sistema de Coordenadas de Origen:** EPSG:4326 (WGS 84 - Grados Decimales)
- **Extensión Geográfica:** Longitud -115.00 a -108.50, Latitud 24.00 a 32.00
- **Artes de Pesca Incluidas:** Múltiples artes de la pesca artesanal
- **Descripción en Lenguaje Cotidiano:** Muestra las zonas del Golfo de California donde los pescadores reportan la mayor concentración combinada de especies comerciales. Los tonos más oscuros representan lugares de alta biodiversidad y productividad pesquera.

---

### Paquete 02: `02_ZPesca_Buceo`
**Título:** Polígonos de Pesca Comercial por Buceo  
**Ubicación en Repositorio:** `output/paquetes_capas_pangas/02_ZPesca_Buceo/`  

#### Mapas Georreferenciados
- **Mapa Base OpenStreetMap (Estilo QGIS):** `output/paquetes_capas_pangas/02_ZPesca_Buceo/mapa_osm.jpg`
- **Mapa Base Satelital Esri:** `output/paquetes_capas_pangas/02_ZPesca_Buceo/mapa_satelital.jpg`

#### Ficha de Metadatos y Especificaciones
- **Tipo de Geometría:** Polígonos Marinos
- **Número Total de Entidades:** 249
- **Sistema de Coordenadas de Origen:** EPSG:4326 (WGS 84)
- **Artes de Pesca Incluidas:** Buceo autónomo y buceo semiautónomo con manguera de aire (Hookah)
- **Especies Principales:** Almeja generosa, callo de hacha, erizo de mar, pepino de mar y caracol.
- **Descripción en Lenguaje Cotidiano:** Delimita las áreas del fondo marino costero donde buzos artesanales se sumergen para extraer moluscos y recursos bentónicos (del fondo marino). Son zonas muy cercanas a la orilla y a mantos rocosos.

---

### Paquete 03: `03_ZPesca_Chinchorro`
**Título:** Polígonos de Pesca con Chinchorro de Línea  
**Ubicación en Repositorio:** `output/paquetes_capas_pangas/03_ZPesca_Chinchorro/`  

#### Mapas Georreferenciados
- **Mapa Base OpenStreetMap (Estilo QGIS):** `output/paquetes_capas_pangas/03_ZPesca_Chinchorro/mapa_osm.jpg`
- **Mapa Base Satelital Esri:** `output/paquetes_capas_pangas/03_ZPesca_Chinchorro/mapa_satelital.jpg`

#### Ficha de Metadatos y Especificaciones
- **Tipo de Geometría:** Polígonos Marinos
- **Número Total de Entidades:** 2,209
- **Sistema de Coordenadas de Origen:** EPSG:4326 (WGS 84)
- **Artes de Pesca Incluidas:** Redes de chinchorro de playa y deriva
- **Especies Principales:** Peces de escama (corvina, curvina reyna, sierra, robalo).
- **Descripción en Lenguaje Cotidiano:** Áreas costeras y esteros donde los pescadores extienden redes flotantes tipo chinchorro para rodear y capturar cardúmenes de peces costeros.

---

### Paquete 04: `04_ZPesca_PANGAS`
**Título:** Base Unificada de Zonas Pesqueras PANGAS  
**Ubicación en Repositorio:** `output/paquetes_capas_pangas/04_ZPesca_PANGAS/`  

#### Mapas Georreferenciados
- **Mapa Base OpenStreetMap (Estilo QGIS):** `output/paquetes_capas_pangas/04_ZPesca_PANGAS/mapa_osm.jpg`
- **Mapa Base Satelital Esri:** `output/paquetes_capas_pangas/04_ZPesca_PANGAS/mapa_satelital.jpg`

#### Ficha de Metadatos y Especificaciones
- **Tipo de Geometría:** Polígonos Marinos
- **Número Total de Entidades:** 4,241
- **Sistema de Coordenadas de Origen:** EPSG:4326 (WGS 84)
- **Artes de Pesca Incluidas:** Multiespecie / Pesca artesanal general
- **Descripción en Lenguaje Cotidiano:** Capa geográfica consolidada que reúne todos los mapas de uso pesquero trazados durante el proyecto histórico PANGAS. Representa la extensión total de operación de la flota de pangas en el Golfo de California.

---

### Paquete 05: `05_ZPesca_Redes`
**Título:** Polígonos de Pesca con Redes de Enmalle  
**Ubicación en Repositorio:** `output/paquetes_capas_pangas/05_ZPesca_Redes/`  

#### Mapas Georreferenciados
- **Mapa Base OpenStreetMap (Estilo QGIS):** `output/paquetes_capas_pangas/05_ZPesca_Redes/mapa_osm.jpg`
- **Mapa Base Satelital Esri:** `output/paquetes_capas_pangas/05_ZPesca_Redes/mapa_satelital.jpg`

#### Ficha de Metadatos y Especificaciones
- **Tipo de Geometría:** Polígonos Marinos
- **Número Total de Entidades:** 1,263
- **Sistema de Coordenadas de Origen:** EPSG:4326 (WGS 84)
- **Artes de Pesca Incluidas:** Redes agalleras de fondo y deriva
- **Especies Principales:** Cazón, tiburón pequeño, raya, huachinango, pargo.
- **Descripción en Lenguaje Cotidiano:** Sitios marinos donde se colocan redes verticales colgadas en el agua para que los peces queden atrapados por las agallas al nadar.

---

### Paquete 06: `06_ZPesca_Redes_Manta_Camaron`
**Título:** Polígonos de Pesca de Camarón y Redes de Manta  
**Ubicación en Repositorio:** `output/paquetes_capas_pangas/06_ZPesca_Redes_Manta_Camaron/`  

#### Mapas Georreferenciados
- **Mapa Base OpenStreetMap (Estilo QGIS):** `output/paquetes_capas_pangas/06_ZPesca_Redes_Manta_Camaron/mapa_osm.jpg`
- **Mapa Base Satelital Esri:** `output/paquetes_capas_pangas/06_ZPesca_Redes_Manta_Camaron/mapa_satelital.jpg`

#### Ficha de Metadatos y Especificaciones
- **Tipo de Geometría:** Polígonos Marinos
- **Número Total de Entidades:** 783
- **Sistema de Coordenadas de Origen:** EPSG:4326 (WGS 84)
- **Artes de Pesca Incluidas:** Redes de manta y red surpera de camarón
- **Especies Principales:** Camarón azul, camarón café y camarón blanco.
- **Descripción en Lenguaje Cotidiano:** Caladeros costeros donde se realiza la pesca de camarón durante la temporada de zafra (otoño e invierno), empleando redes especiales arrastradas suavemente por panga.

---

### Paquete 07: `07_ZPesca_Trampa`
**Título:** Polígonos de Pesca con Trampas (Jaiba y Peces)  
**Ubicación en Repositorio:** `output/paquetes_capas_pangas/07_ZPesca_Trampa/`  

#### Mapas Georreferenciados
- **Mapa Base OpenStreetMap (Estilo QGIS):** `output/paquetes_capas_pangas/07_ZPesca_Trampa/mapa_osm.jpg`
- **Mapa Base Satelital Esri:** `output/paquetes_capas_pangas/07_ZPesca_Trampa/mapa_satelital.jpg`

#### Ficha de Metadatos y Especificaciones
- **Tipo de Geometría:** Polígonos Marinos
- **Número Total de Entidades:** 360
- **Sistema de Coordenadas de Origen:** EPSG:4326 (WGS 84)
- **Artes de Pesca Incluidas:** Trampas metálicas y nasas jaiberas
- **Especies Principales:** Jaiba azul, jaiba café y peces de arrecife.
- **Descripción en Lenguaje Cotidiano:** Zonas protegidas cerca de bahías y estuarios donde los pescadores depositan jaulas o trampas cebadas en el fondo para atrapar crustáceos.

---

## 6. Atribución Académica Formal

Todas las capas del catálogo PANGAS presentadas en este documento proceden de la investigación:
> **Moreno-Báez, M., Cudney-Bueno, R., Shaw, W. W., Cudney-Bueno, S., & Torre-Cosío, J. (2011, 2012).**  
> *Integrating spatial and temporal dimensions of artisanal fishing for management in the Gulf of California, Mexico.*  
> Publicado en: *Ocean & Coastal Management* / *Marine Policy*.  
> Base de Datos Geográfica original del proyecto PANGAS.

---

## 7. Glosario de Términos no Técnicos para Revisores

Para apoyar la lectura de directivos, asesores y representantes comunitarios, a continuación se explican los conceptos clave empleados en este informe:

1. **Sistema de Información Geográfica (SIG):** Un programa de computadora especializado en crear, almacenar y analizar mapas digitales interactivos en lugar de mapas impresos en papel.
2. **GeoPackage (.gpkg):** Un formato de archivo moderno y estándar internacional que permite guardar en un solo archivo ligero de computadora múltiples mapas, líneas, puntos y tablas de datos de manera muy rápida.
3. **Sistema de Coordenadas (CRS) / WGS 84 (EPSG:4326):** El sistema global de latitud y longitud que utiliza el GPS de los teléfonos para saber exactamente en qué parte del planeta Tierra se encuentra un objeto.
4. **Proyección Web Mercator (EPSG:3857):** La forma matemática en que se aplana la esfera terrestre para mostrar mapas en pantallas de computadora y navegadores de internet (como Google Maps u OpenStreetMap).
5. **Bounding Box (Extensión Geográfica):** El marco o rectángulo imaginario definido por las coordenadas mínimas y máximas que encierran a todo un mapa o grupo de datos.
6. **Grilla H3 (Hexágonos de Uber):** Un sistema que divide la superficie del mar en miles de piezas de rompecabezas de seis lados (hexágonos) idénticos en tamaño, lo que permite medir y comparar variables de riesgo sin deformaciones.
7. **Metadatos:** La "ficha de identidad" o etiqueta que describe a un mapa o archivo digital (quién lo hizo, cuándo se creó, qué significan sus variables y con qué precisión fue medido).
8. **Topología:** Reglas matemáticas que aseguran que los mapas digitales no tengan errores como líneas encimadas, polígonos encimados por error o huecos vacíos donde debería haber datos.
9. **R-Tree (Índice Espacial):** Una tecnología interna dentro de las bases de datos geográficas que funciona como el índice de un libro, permitiendo encontrar un polígono o barco en el mapa en una fracción de segundo.
