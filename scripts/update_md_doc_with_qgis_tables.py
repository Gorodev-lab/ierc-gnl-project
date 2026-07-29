#!/usr/bin/env python3
"""
update_md_doc_with_qgis_tables.py
---------------------------------
Sincroniza DOCUMENTO_EJECUTIVO_ENTREGABLE1.md con las tablas completas de metadatos estilo QGIS para las 7 capas.
"""

import pyogrio
import geopandas as gpd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
GDB_PATH = BASE_DIR / 'data' / 'raw' / 'pangas_gdb' / 'Fish_Zones_PANGAS.gdb'
MD_DOC_PATH = BASE_DIR / 'docs' / 'metodologia' / 'DOCUMENTO_EJECUTIVO_ENTREGABLE1.md'

CITA_ACADEMICA = (
    "Moreno-Báez, M., Cudney-Bueno, R., Shaw, W. W., Cudney-Bueno, S., & Torre-Cosío, J. (2011, 2012). "
    "Integrating spatial and temporal dimensions of artisanal fishing for management in the Gulf of California, Mexico. "
    "Ocean & Coastal Management / Marine Policy. Base de Datos Geográfica PANGAS."
)

FIELD_DESCRIPTIONS = {
    'Id': 'Identificador único numérico del registro de zona pesquera.',
    'CODE': 'Código alfanumérico asignado al polígono de pesca.',
    'M': 'Indicador del mes o temporada (1 = activo, 0 = inactivo).',
    'J': 'Indicador estacional o de pesquería.',
    'R': 'Indicador de región o zona pesquera.',
    'G': 'Indicador de grupo pesquero o gremio.',
    'NAME': 'Nombre geográfico o toponímico del sitio de pesca.',
    'ENTREVIS': 'Código único de la encuesta o entrevista participativa PANGAS.',
    'Int_id': 'Identificador numérico del pescador o informante clave.',
    'Ent_num': 'Número secuencial de la entrevista efectuada.',
    'Entvsdr': 'Iniciales o código del entrevistador de campo.',
    'mes': 'Mes del levantamiento o temporada de pesca (1-12).',
    'dia': 'Día del levantamiento en campo.',
    'ano': 'Año del registro de la información (ej. 2005, 2006).',
    'spp_code': 'Código taxonómico estándar de la especie (ej. LITSTY = Litopenaeus stylirostris).',
    'sitio_code': 'Código corto del campo o comunidad pesquera (ej. SLG, PLO).',
    'Met_Pesca': 'Método o arte de pesca registrado (ej. Chinchorro, Trampa, Buceo).',
    'HABITAT': 'Tipo de sustrato o hábitat bentónico (ej. arena, arrecife, fango).',
    'CODE_COMP': 'Código compuesto de identificación espacial.',
    'CODE_FIN': 'Código final concatenado de sitio, entrevista y especie.',
    'Shape_Length': 'Perímetro total del polígono expresado en metros.',
    'Shape_Area': 'Superficie o área total del polígono expresada en metros cuadrados.',
    'no_comunid': 'Número correlativo de comunidad pesquera.',
    'comunidad': 'Nombre o código corto de la comunidad costera.',
    'ORIG_FID': 'Identificador de registro original en el dataset de origen.',
    'day': 'Día del registro participativo.',
    'month': 'Mes del registro participativo.',
    'year': 'Año del registro participativo.',
    'sitio_nomb': 'Nombre oficial del sitio o Área Natural Protegida.',
    'weight_pc': 'Ponderación porcentual de uso pesquero.',
    'NorSur': 'Orientación geográfica del caladero (1 = Norte, 0 = Sur).',
    'TEMP': 'Código de identificación temporal del polígono.',
    'NAME_ORG': 'Nombre registrado originalmente en las entrevistas.',
    'all': 'Acumulado de riqueza biológica total.',
    'artnob': 'Especie pesquera: Balistes polylepis / Pez ballesta.',
    'atrtub': 'Especie pesquera: Atractoscion nobilis / Seabass.',
    'balpol': 'Especie pesquera: Balistes polylepis / Cochi.',
    'carlim': 'Especie pesquera: Carcharias spp. / Tiburón.',
    'carspp': 'Especie pesquera: Caranx spp. / Jurel.',
    'isofus': 'Especie pesquera: Isostichopus fuscus / Pepino de mar.',
    'litsty': 'Especie pesquera: Litopenaeus stylirostris / Camarón azul.',
    'pinrug': 'Especie pesquera: Pinna rugosa / Hacha de labio.',
    'stegig': 'Especie pesquera: Strombus gigas / Caracol.'
}

LAYER_CONFIG = {
    'Riqueza_Relativa': {
        'num_prefix': '01',
        'titulo': 'Malla de Riqueza Biológica Pesquera Relativa',
        'descripcion': 'Muestra las zonas del Golfo de California donde los pescadores reportan la mayor concentración combinada de especies comerciales. Los tonos más oscuros representan lugares de alta biodiversidad y productividad pesquera.',
        'artes': 'Todas las artes de pesca artesanal registradas en el Golfo de California'
    },
    'ZPesca_Buceo': {
        'num_prefix': '02',
        'titulo': 'Polígonos de Pesca Comercial por Buceo',
        'descripcion': 'Delimita las áreas del fondo marino costero donde buzos artesanales se sumergen para extraer moluscos y recursos bentónicos (almeja generosa, callo de hacha, erizo y pepino de mar).',
        'artes': 'Buceo autónomo y buceo semiautónomo (Hookah)'
    },
    'ZPesca_Chinchorro': {
        'num_prefix': '03',
        'titulo': 'Polígonos de Pesca con Chinchorro de Línea',
        'descripcion': 'Zonas de playa y estuarios donde los pescadores extienden redes flotantes tipo chinchorro para rodear y capturar cardúmenes de peces de escama (corvina, sierra, robalo).',
        'artes': 'Chinchorro de línea / Redes agalleras de playa'
    },
    'ZPesca_PANGAS': {
        'num_prefix': '04',
        'titulo': 'Base Unificada de Zonas Pesqueras PANGAS',
        'descripcion': 'Capa geográfica consolidada que reúne todos los mapas de uso pesquero trazados durante el proyecto histórico PANGAS (Dra. Marcia Moreno-Báez et al.).',
        'artes': 'Multiespecie / PANGAS'
    },
    'ZPesca_Redes': {
        'num_prefix': '05',
        'titulo': 'Polígonos de Pesca con Redes de Enmalle',
        'descripcion': 'Sitios marinos donde se colocan redes agalleras verticales en la columna de agua o en el fondo marino para capturar cazón, tiburón pequeño, raya y pargo.',
        'artes': 'Redes agalleras de fondo y deriva'
    },
    'ZPesca_Redes_Manta_Camaron': {
        'num_prefix': '06',
        'titulo': 'Polígonos de Pesca de Camarón y Redes de Manta',
        'descripcion': 'Caladeros costeros de gran importancia económica donde se realiza la pesca de camarón (azul, café y blanco) durante la temporada de zafra.',
        'artes': 'Red de manta / Red surpera de camarón'
    },
    'ZPesca_Trampa': {
        'num_prefix': '07',
        'titulo': 'Polígonos de Pesca con Trampas (Jaiba y Peces)',
        'descripcion': 'Zonas protegidas cerca de bahías y esteros donde los pescadores depositan jaulas o trampas cebadas en el fondo para jaiba azul, jaiba café y peces de rocas.',
        'artes': 'Trampas metálicas / Nasas jaiberas'
    }
}

layers_list = pyogrio.list_layers(GDB_PATH)
layer_names = [name for name, _ in layers_list]

extracted_layers = []

for layer in layer_names:
    config = LAYER_CONFIG.get(layer, {
        'num_prefix': '99',
        'titulo': f'Capa {layer}',
        'descripcion': 'Capa geográfica PANGAS.',
        'artes': 'Pesca Artesanal'
    })
    
    gdf = gpd.read_file(GDB_PATH, layer=layer)
    folder_name = f"{config['num_prefix']}_{layer}"
    
    schema_fields = []
    for col, dtype in gdf.dtypes.items():
        if col != 'geometry':
            non_nulls = gdf[col].dropna()
            sample_val = str(non_nulls.iloc[0]) if len(non_nulls) > 0 else 'N/A'
            if len(sample_val) > 35:
                sample_val = sample_val[:32] + '...'
            desc = FIELD_DESCRIPTIONS.get(col, f'Atributo espacial registrado en {layer}.')
            schema_fields.append({
                'campo': col,
                'tipo': str(dtype),
                'ejemplo': sample_val,
                'descripcion': desc
            })
            
    bounds = gdf.to_crs(epsg=4326).total_bounds
    bbox_str = f"MinLon: {bounds[0]:.4f}, MinLat: {bounds[1]:.4f}, MaxLon: {bounds[2]:.4f}, MaxLat: {bounds[3]:.4f}"
    
    extracted_layers.append({
        'folder_name': folder_name,
        'layer': layer,
        'titulo': config['titulo'],
        'descripcion': config['descripcion'],
        'artes': config['artes'],
        'entities': len(gdf),
        'bbox': bbox_str,
        'schema_fields': schema_fields
    })

md_text = f"""# Documento Ejecutivo y Catálogo Cartográfico: Entregable 1 (Meta 1)

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
$$\text{{Clave}} = \text{{comunidad}} - \text{{actor}} - \text{{pesquería}} - \text{{arte}} - \text{{zona}} - \text{{temporada}} - \text{{ruta}}$$

> **Explicación Accesible:**  
> Es como el número de CURP o código postal de una actividad de pesca. Nos dice exactamente: *quién pesca* (comunidad y actor), *qué pesca* (especie o pesquería), *con qué herramienta* (arte de pesca), *en dónde* (zona), *en qué época del año* (temporada) y *por dónde navega* (ruta).

---

## 5. Catálogo de Paquetes Cartográficos por Capa (Línea Base PANGAS)

A continuación se presenta el desglose de las 7 capas pesqueras de la base de datos `Fish_Zones_PANGAS.gdb`, atribuidas a la investigación de la **Dra. Marcia Moreno-Báez et al. (2011, 2012)**. Cada paquete cuenta con 2 mapas georreferenciados en proyección Web Mercator (`EPSG:3857`): uno con el mapa base **OpenStreetMap estándar (estilo QGIS)** que muestra nombres de ciudades, carreteras y líneas de costa, y otro con el mapa **satelital Esri World Imagery**.

"""

for item in extracted_layers:
    md_text += f"""### Paquete {item['folder_name'][:2]}: `{item['folder_name']}`
**Título de la Capa:** {item['titulo']}  
**Ubicación en Repositorio:** `output/paquetes_capas_pangas/{item['folder_name']}/`  
**Cita de Origen:** Moreno-Báez, M., et al. (2011, 2012). Ocean & Coastal Management / Marine Policy.  
**Entidades (Polígonos):** {item['entities']:,} | **Artes de Pesca:** {item['artes']}  
**Bounding Box (WGS84):** `{item['bbox']}`  
**Descripción Accesible:** {item['descripcion']}  

#### Mapas Georreferenciados
- **Mapa Base OpenStreetMap (Estilo QGIS):** `output/paquetes_capas_pangas/{item['folder_name']}/mapa_osm.jpg`
- **Mapa Base Satelital Esri:** `output/paquetes_capas_pangas/{item['folder_name']}/mapa_satelital.jpg`

#### Tabla de Atributos Extraídos Estilo QGIS ({len(item['schema_fields'])} Campos)

| Nombre del Campo | Tipo de Dato (QGIS/GDAL) | Valor de Ejemplo | Descripción y Rol Metodológico |
|---|---|---|---|
"""
    for f in item['schema_fields']:
        md_text += f"| `{f['campo']}` | `{f['tipo']}` | `{f['ejemplo']}` | {f['descripcion']} |\n"
    md_text += "\n---\n\n"

md_text += """## 6. Atribución Académica Formal

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
"""

MD_DOC_PATH.write_text(md_text, encoding='utf-8')
print(f"Documento Markdown generado exitosamente en: {MD_DOC_PATH}")
