# Documento Ejecutivo y Catálogo Cartográfico de Avances: Entregable 1 (Meta 1 POA 2026)

**Proyecto:** Índice Espacial de Riesgo Socioeconómico para Comunidades (IERC-GNL)  
**Cliente / Organización:** Causa Natura Center / Causa Natura Data (POA 2026-2028)  
**Equipo Técnico de Autores:**
- **Juan Carlos Barrera (JCB):** Consultor Senior / Especialista Pesquero y Socioambiental
- **Enrique Gorosave (EG):** Analista de Datos y Sistema de Información Geográfica (SIG)  
**Fecha de Publicación:** 19 de Agosto de 2026  
**Versión del Entregable:** GeoPackage v1.1 & v2 (OGC Standard)  
**Repositorio Oficial de Código y Datos:** [https://github.com/Gorodev-lab/ierc-gnl-project](https://github.com/Gorodev-lab/ierc-gnl-project)

---

## 1. Resumen Ejecutivo y Alcance del Entregable 1

Este documento constituye el informe técnico y gráfico detallado para stakeholders sobre los avances alcanzados en la **Meta 1 (Semanas 1 a 4 del Plan Operativo Anual 2026)** del proyecto **IERC-GNL**. Su objetivo es consolidar la arquitectura de información geográfica de gabinete, el motor matemático de cálculo de riesgo socioecológico, las 7 capas base estandarizadas del Golfo de California y las herramientas del Dashboard Web interactivo.

### Hitos Principales Completados
1. **Compilación del GeoPackage OGC v1.1 y v2**: Creación del contenedor espacial estandarizado `deliverables/v1_geopackage/ierc_golfo_california.gpkg` y `v2_geopackage/ierc_golfo_california_v2.gpkg` en CRS global `EPSG:4326 (WGS 84)` con indexación espacial R-Tree.
2. **Implementación de la Malla Hexagonal Uber H3**: Generación de 5,244 celdas hexagonales adaptativas (Resolución 8 en aguas abiertas y Resolución 9 en zonas portuarias/costeras) para cálculo uniforme y sin distorsiones del riesgo.
3. **Formulación y Automatización del Modelo IERC**: Implementación del motor de cálculo en Python (`src/engine/fishing_risk_calculator.py`) basado en la ecuación $R_{i,t} = H_{i,t} \times V_{i,t}$.
4. **Estandarización del Identificador Único Espacio-Temporal (`uid_espaciotemporal`)**: Formato estandarizado `comunidad-actor-pesqueria-arte-zona-temporada-ruta` para vincular encuestas comunitarias con polígonos pesqueros.
5. **Dashboard Web Interactivo Next.js 15**: Desarrollo de la interfaz gráfica web (`dashboard/`) con mapa interactivo en tiempo real, selector de proyectos GNL, desglose de especies críticas y panel explicativo metodológico.
6. **Catálogo Cartográfico Completo**: Paquete con 7 subcarpetas de capas geográficas PANGAS (Dr. Marcia Moreno-Báez et al.), tablas de atributos estilo QGIS (52 campos) y visualizadores HTML para exportación.

> **Nota Explicativa sobre los Datos Presentados:**  
> La información espacial contenida en este reporte representa la **línea base histórica de gabinete (Estudio PANGAS de la Dra. Marcia Moreno-Báez et al.) y la infraestructura del modelo espacial**. Los datos primarios de campo y el mapeo en vivo de exclusiones marinas por obras de GNL serán validados durante la **Meta 2 (Semanas 5 a 8)** en **Punta Chueca (Nación Comca'ac)**, **Puerto Libertad** y **Guaymas**.

---

## 2. Estructura del Repositorio y Entregables

Todos los insumos del proyecto se encuentran estructurados y sincronizados en el repositorio de GitHub:

```bash
ierc-gnl-project/
├── causanaturadata/            # Documentos oficiales del proyecto (POA 2026, Manual Metodológico)
├── dashboard/                  # Dashboard Web Interactivo (Next.js 15, React, Tailwind CSS)
├── data/                       # Insumos geográficos de gabinete (PANGAS, CONANP, GFW, INEGI)
│   └── processed/              # Datasets procesados y resúmenes de riesgo pesquero
├── deliverables/
│   ├── v1_geopackage/          # ENTREGABLE ESPACIAL META 1 (GeoPackage OGC v1.1)
│   └── v2_geopackage/          # GeoPackage v2 optimizado con índices H3
├── docs/                       # Documentación metodológica e inventario de vacíos
│   ├── metodologia/            # Notas técnicas, documentos ejecutivos y guiones de presentación
│   └── auditoria/              # Planes de supervisión y expedientes de dictamen técnico
├── output/                     # Artefactos finales de salida (PDFs, HTMLs y capturas de mapa)
│   ├── atlas_pangas_jpg/       # Capturas JPG de alta resolución por capa y arte de pesca
│   ├── paquetes_capas_pangas/  # Paquetes individuales de capas con metadatos estilo QGIS
│   └── DOCUMENTO_EJECUTIVO_ENTREGABLE1.pdf  # Reporte PDF Nativo para Stakeholders
└── scripts/                    # Scripts de procesamiento, descargas y generación de PDF/GeoPackage
```

---

## 3. Modelo Matemático del Índice Espacial de Riesgo (IERC)

El cálculo del riesgo socioeconómico y ecológico por celda hexagonal $i$ y periodo $t$ se realiza a través de la fórmula multiplicativa:

$$R_{i,t} = H_{i,t} \times V_{i,t}$$

Donde:

1. **$H_{i,t}$ (Amenaza y Exposición Espacial)**:
   $$H_{i,t} = w_1 \cdot \text{DensidadEsfuerzo}_{i,t} + w_2 \cdot \text{ProximidadGNL}_{i} + w_3 \cdot \text{RutaConflicto}_{i}$$
   Mide la presencia y concentración de la actividad pesquera artesanal combinada con la cercanía física a plantas de licuefacción de GNL, monoboyas y rutas marítimas de buques metaneros.

2. **$V_{i,t}$ (Vulnerabilidad Socioecológica y de Gobernanza)**:
   $$V_{i,t} = 0.25 \cdot \text{SensibilidadEcológica} + 0.25 \cdot \text{DependenciaEconómica} + 0.20 \cdot \text{VulnerabilidadBiocultural} + 0.15 \cdot \text{EnfoqueGénero} + 0.15 \cdot (1 - \text{CapacidadAdaptativa})$$
   Evalúa el grado en que las comunidades y ecosistemas costeros carecen de mecanismos de amortiguamiento o alternativas de sustento ante la exclusión de sus zonas tradicionales de pesca.

---

## 4. Matriz de Evaluación de Riesgo Pesquero por Proyecto GNL

Evaluación cruzada de las 5 terminales GNL en el Golfo de California frente a las artes de pesca artesanal:

| Proyecto GNL | Localidad Cercana | Estado | Nivel de Riesgo IERC | Artes de Pesca Más Afectadas | Especies Críticas en Riesgo |
|---|---|---|---|---|---|
| **Saguaro Energía (Mexico Pacific)** | Puerto Libertad, Sonora | Proyectado / En construcción | **Extremo (0.89)** | Buceo, Chinchorro, Redes agalleras | Almeja generosa, Camarón azul, Curvina, Pepino de mar |
| **Amigo LNG (LNG Alliance)** | Guaymas, Sonora | Aprobado / En desarrollo | **Alto (0.76)** | Redes de manta, Trampa de jaiba, Linea | Jaiba azul/café, Sierra, Liza, Pargo |
| **Vista Pacífico LNG (Sempra Infrastructure)** | Topolobampo, Sinaloa | En evaluación ambiental | **Alto (0.71)** | Redes agalleras, Chinchorro | Camarón café, Robalo, Jaiba |
| **ECA LNG (Sempra Infrastructure)** | Ensenada / Costa del Pacífico | Operativo (Fase 1) | **Moderado (0.58)** | Buceo bentónico, Trampa | Erizo rojo, Langosta roja |
| **Salina Cruz LNG (CFE / Pemex)** | Salina Cruz, Oaxaca | En planificación | **Moderado (0.52)** | Chinchorro, Atarraya | Camarón blanco, Huachinango |

---

## 5. Descripción de las 7 Capas Geográficas del GeoPackage OGC (v1.1 / v2)

El archivo maestro `ierc_golfo_california.gpkg` almacena 7 capas geográficas en WGS84 (`EPSG:4326`):

1. **`proyectos_gnl` (Puntos):** 5 plantas y terminales de exportación de GNL con atributos de capacidad de producción (MTPA) y scores IERC.
2. **`gasoductos_infraestructura_gnl` (Líneas):** 2 trazados principales de tuberías de gas (Gasoducto Saguaro y Guaymas-El Oro).
3. **`localidades_estudio_ierc` (Puntos):** 3 asentamientos costeros prioritarios del POA: **Punta Chueca (Nación Comca'ac)**, **Puerto Libertad** y **Guaymas**.
4. **`anp_habitats_criticos` (Polígonos):** 2 Áreas Naturales Protegidas prioritarias (Reserva de la Biosfera Alto Golfo y Delta del Río Colorado, Isla Tiburón).
5. **`zonas_pesqueras_pangas` (Polígonos):** 17 polígonos pesqueros integrados y enriquecidos con la clave `uid_espaciotemporal`.
6. **`grilla_h3_riesgo` (Polígonos Hexagonales):** Malla espacial de 5,244 hexágonos Uber H3 para evaluación del riesgo celda por celda.
7. **`riqueza_relativa_pesquera` (Polígonos):** 11,065 polígonos de riqueza biológica acumulada de especies pesqueras.

---

## 6. Catálogo Cartográfico y Fichas de Capas (Línea Base PANGAS)

### Paquete 01: `01_Riqueza_Relativa`
- **Nombre de Capa:** Malla de Riqueza Biológica Pesquera Relativa
- **Ubicación:** `output/paquetes_capas_pangas/01_Riqueza_Relativa/`
- **Origen:** Moreno-Báez, M., et al. (2011, 2012).
- **Entidades:** 11,065 polígonos | **Campos en Tabla QGIS:** 52
- **Bounding Box:** `MinLon: -114.9307, MinLat: 27.2977, MaxLon: -110.5188, MaxLat: 31.8423`
- **Mapas Georreferenciados:**  
  ![Mapa OSM Riqueza Relativa](output/atlas_pangas_jpg/mapa_Riqueza_Relativa.jpg)

### Paquete 02: `02_ZPesca_Buceo`
- **Nombre de Capa:** Polígonos de Pesca Comercial por Buceo
- **Ubicación:** `output/paquetes_capas_pangas/02_ZPesca_Buceo/`
- **Entidades:** 249 polígonos | **Artes:** Buceo autónomo y Hookah (almeja generosa, callo de hacha, pepino de mar)
- **Mapas Georreferenciados:**  
  ![Mapa OSM Buceo](output/atlas_pangas_jpg/mapa_ZPesca_Buceo.jpg)

### Paquete 03: `03_ZPesca_Chinchorro`
- **Nombre de Capa:** Polígonos de Pesca con Chinchorro de Línea
- **Ubicación:** `output/paquetes_capas_pangas/03_ZPesca_Chinchorro/`
- **Entidades:** 2,209 polígonos | **Artes:** Chinchorro agallero de playa (corvina, sierra, robalo)
- **Mapas Georreferenciados:**  
  ![Mapa OSM Chinchorro](output/atlas_pangas_jpg/mapa_ZPesca_Chinchorro.jpg)

### Paquete 04: `04_ZPesca_PANGAS`
- **Nombre de Capa:** Base Unificada de Zonas Pesqueras PANGAS
- **Ubicación:** `output/paquetes_capas_pangas/04_ZPesca_PANGAS/`
- **Entidades:** 4,241 polígonos | **Artes:** Multiespecie PANGAS
- **Mapas Georreferenciados:**  
  ![Mapa OSM PANGAS](output/atlas_pangas_jpg/mapa_ZPesca_PANGAS.jpg)

### Paquete 05: `05_ZPesca_Redes`
- **Nombre de Capa:** Polígonos de Pesca con Redes de Enmalle
- **Ubicación:** `output/paquetes_capas_pangas/05_ZPesca_Redes/`
- **Entidades:** 1,263 polígonos | **Artes:** Redes agalleras de fondo y deriva (cazón, tiburón, raya, pargo)
- **Mapas Georreferenciados:**  
  ![Mapa OSM Redes](output/atlas_pangas_jpg/mapa_ZPesca_Redes.jpg)

### Paquete 06: `06_ZPesca_Redes_Manta_Camaron`
- **Nombre de Capa:** Polígonos de Pesca de Camarón y Redes de Manta
- **Ubicación:** `output/paquetes_capas_pangas/06_ZPesca_Redes_Manta_Camaron/`
- **Entidades:** 783 polígonos | **Artes:** Red surpera y manta camaronera (camarón azul, café y blanco)
- **Mapas Georreferenciados:**  
  ![Mapa OSM Camarón](output/atlas_pangas_jpg/mapa_ZPesca_Redes_Manta_Camaron.jpg)

### Paquete 07: `07_ZPesca_Trampa`
- **Nombre de Capa:** Polígonos de Pesca con Trampas (Jaiba y Peces)
- **Ubicación:** `output/paquetes_capas_pangas/07_ZPesca_Trampa/`
- **Entidades:** 360 polígonos | **Artes:** Trampas jaiberas y nasas metálicas
- **Mapas Georreferenciados:**  
  ![Mapa OSM Trampa](output/atlas_pangas_jpg/mapa_ZPesca_Trampa.jpg)

---

## 7. Glosario de Términos Técnicos para Stakeholders

1. **GeoPackage (.gpkg):** Formato de archivo geográfico estándar de la Open Geospatial Consortium (OGC) que almacena múltiples capas vectoriales y tablas en una sola base de datos SQLite.
2. **Grilla H3 (Uber H3):** Malla hexagonal discreta global desarrollada por Uber que fragmenta el espacio en celdas regulares para realizar análisis geoespaciales comparativos y eficientes.
3. **WGS 84 (EPSG:4326):** Sistema de Coordenadas Geográficas estándar utilizado mundialmente por sistemas GPS.
4. **`uid_espaciotemporal`:** Clave alfanumérica estandarizada para rastrear una actividad pesquera específica por comunidad, actor, especie, arte de pesca, zona y temporada.
5. **IERC (Índice Espacial de Riesgo Socioeconómico):** Indicador cuantitativo que combina la exposición a amenazas industriales de GNL con la vulnerabilidad social y pesquera.

---

## 8. Matriz de Validación y Firma de Entregable

| Rol / Función | Responsable | Estado | Fecha de Firma |
|---|---|---|---|
| **Especialista Pesquero y Socioambiental** | Juan Carlos Barrera (JCB) | **Aprobado** | 19/08/2026 |
| **Analista GIS y de Datos** | Enrique Gorosave (EG) | **Aprobado** | 19/08/2026 |
| **Coordinación Causa Natura Data** | Dirección POA 2026 | **Recibido Conformidad** | 19/08/2026 |

---
*Causa Natura Data (2026) — Proyecto IERC-GNL. Todos los derechos reservados.*
