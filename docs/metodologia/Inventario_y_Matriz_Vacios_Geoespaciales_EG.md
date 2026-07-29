# Inventario de Información Geoespacial y Matriz de Vacíos (EG - Causa Natura Data)

**Proyecto:** Índice Espacial de Riesgo Socioeconómico para Comunidades (IERC-GNL)  
**Elaborado por:** Enrique Gorosave (EG - Analista de Datos y SIG)  
**Revisado por:** Juan Carlos Barrera (JCB - Consultor Senior)  
**Fecha:** Julio 2026 | **Entregable:** Meta 1 — POA 2026  

---

## 1. Inventario de Capas de Gabinete Disponibles

| Categoría | Nombre de Capa | Fuente | Formato Original | Estado / Cobertura | Coordenadas |
|---|---|---|---|---|---|
| **Infraestructura GNL** | Terminales GNL Golfo | SENER / MIA / Gabinete | GeoJSON / CSV | 5 Terminales (Puerto Libertad, Guaymas, San Felipe, NFE, Amigo LNG) | EPSG:4326 |
| **Infraestructura GNL** | Gasoductos Sonora / Guaymas | SENER / CENAGAS | SHP / GeoJSON | Trazados principales de ductos de gas natural | EPSG:4326 |
| **Pesca Artesanal** | Campos Pesqueros PANGAS | Moreno-Báez et al. (2011, 2012) | GDB / GeoJSON | 17 sitios de pesca artesanal consolidados | EPSG:4326 |
| **Pesca Artesanal** | Riqueza Relativa Pesquera | PANGAS / UCSD | GeoJSON | 11,065 polígonos de riqueza acumulada | EPSG:4326 |
| **Tráfico Marítimo** | Tráfico Industrial / Pesquero | Global Fishing Watch (GFW) | CSV / Raster | Densidad de esfuerzo pesquero y buques metaneros | EPSG:4326 |
| **Ecosistemas** | Áreas Naturales Protegidas (ANP) | CONANP | SHP / GeoJSON | ANP Federales y Estatales en Golfo de California | EPSG:4326 |
| **Ecosistemas** | Manglares, Pastos y Arrecifes | CONABIO / TNC | SHP / GeoJSON | Cobertura de hábitats marinos críticos | EPSG:4326 |
| **Socioeconomía** | Localidades y Censo INEGI | INEGI (2020) | SHP / Tabular | Localidades costeras de Sonora y Baja California | EPSG:4326 |

---

## 2. Matriz de Vacíos de Información Espacio-Temporal (Para Levantar en Campo)

| Vacío de Información | Dimensión Afectada | Localidades Objetivo | Método de Captura en Campo (JCB / EG) | Prioridad |
|---|---|---|---|---|
| **Rutas Pesqueras Quincenales** | Exposición Pesquera | Punta Chueca, Puerto Libertad, Guaymas | Cartografía participativa con GPS / Digitalización de rutas quincenales |  Alta |
| **Zonas Secundarias y de Contingencia** | Exposición / Sensibilidad | Punta Chueca, Puerto Libertad | Talleres comunitarios y mapeo participativo de zonas alternas |  Alta |
| **Calendarios Pesqueros por Arte y Especie** | Exposición Temporal | Punta Chueca, Puerto Libertad, Guaymas | Matriz explícita de estacionalidad y especies objetivo quincenales |  Alta |
| **Sitios Bioculturales Comca'ac** | Patrimonio Biocultural | Punta Chueca | Mapeo intercultural con la comunidad Comca'ac (bajo CPLI) |  Alta |
| **Cadenas de Valor y Roles de Género** | Vulnerabilidad Social | Guaymas, Puerto Libertad | Entrevistas a mujeres desconchadoras / trabajadoras postcaptura | 🟡 Media |
| **Puntos de Fondeo y Conflictos con GNL** | Amenaza GNL | Puerto Libertad, Guaymas | Superposición de trazas AIS de metaneros vs rutas de pangas |  Alta |

---

## 3. Plan de Estandarización del Repositorio GeoPackage

El repositorio espacial `deliverables/v1_geopackage/ierc_golfo_california.gpkg` integra todas las capas bajo las siguientes reglas:
1. **Sistema de Coordenadas:** EPSG:4326 (WGS 84 - Grados Decimales).
2. **Índices Espaciales:** R-Tree habilitado en SQLite para cada tabla de geometría.
3. **Clave Única Espacio-Temporal:** Atributo `uid_espaciotemporal` en todas las capas vectoriales pesqueras.
