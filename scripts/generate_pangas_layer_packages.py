#!/usr/bin/env python3
"""
generate_pangas_layer_packages.py
---------------------------------
Generación de paquetes cartográficos individuales georreferenciados para las 7 capas de Fish_Zones_PANGAS.gdb.
Línea Base Pesquera Histórica: Dra. Marcia Moreno-Báez et al. (2011, 2012)
Uso y Adaptación para Causa Natura Data: Juan Carlos Barrera (JCB - Consultor Senior) & Enrique Gorosave (EG - Analista GIS)

Este script:
1. Lee cada una de las 7 capas de Fish_Zones_PANGAS.gdb.
2. Reproyecta temporalmente a EPSG:3857 (Web Mercator) para alineación exacta con capas base XYZ.
3. Genera 2 mapas JPG georreferenciados por capa:
   - mapa_osm.jpg (OpenStreetMap estilo QGIS con ciudades, costas y carreteras)
   - mapa_satelital.jpg (Esri World Imagery Satelital para detalle de litoral)
4. Genera una carpeta independiente por capa en output/paquetes_capas_pangas/ con su archivo METADATOS_CAPA.md.
5. Compila el reporte maestro HTML output/paquetes_capas_pangas/ATLAS_PAQUETES_COMPLETO.html.
"""

import os
import re
from pathlib import Path
import pyogrio
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx

BASE_DIR = Path(__file__).resolve().parent.parent
GDB_PATH = BASE_DIR / 'data' / 'raw' / 'pangas_gdb' / 'Fish_Zones_PANGAS.gdb'
OUTPUT_PACKAGES_DIR = BASE_DIR / 'output' / 'paquetes_capas_pangas'
HTML_MASTER_PATH = OUTPUT_PACKAGES_DIR / 'ATLAS_PAQUETES_COMPLETO.html'

OUTPUT_PACKAGES_DIR.mkdir(parents=True, exist_ok=True)

# Cita académica oficial completa
CITA_ACADEMICA = (
    "Moreno-Báez, M., Cudney-Bueno, R., Shaw, W. W., Cudney-Bueno, S., & Torre-Cosío, J. (2011, 2012). "
    "Integrating spatial and temporal dimensions of artisanal fishing for management in the Gulf of California, Mexico. "
    "Ocean & Coastal Management / Marine Policy. Base de Datos Geográfica PANGAS."
)

LAYER_CONFIG = {
    'Riqueza_Relativa': {
        'num_prefix': '01',
        'titulo': 'Malla de Riqueza Biológica Pesquera Relativa',
        'descripcion': 'Polígonos de grilla espacial con acumulación de riqueza biológica pesquera derivada de las entrevistas del estudio PANGAS.',
        'artes': 'Todas las artes de pesca artesanal registradas en el Golfo de California',
        'color': '#0284c7',
        'edge_color': '#0369a1'
    },
    'ZPesca_Buceo': {
        'num_prefix': '02',
        'titulo': 'Polígonos de Pesca Comercial por Buceo',
        'descripcion': 'Campos y caladeros de pesca artesanal por buceo autónomo y hookah (moluscos, bentónicos, almeja, callo de hacha, erizo, pepino de mar).',
        'artes': 'Buceo autónomo y semiautónomo (Hookah)',
        'color': '#ec4899',
        'edge_color': '#be185d'
    },
    'ZPesca_Chinchorro': {
        'num_prefix': '03',
        'titulo': 'Polígonos de Pesca con Chinchorro de Línea',
        'descripcion': 'Zonas de operación pesquera artesanal mediante chinchorros de línea de playa y deriva para capturas de peces de escama.',
        'artes': 'Chinchorro de línea / Redes agalleras de playa',
        'color': '#b91c1c',
        'edge_color': '#7f1d1d'
    },
    'ZPesca_PANGAS': {
        'num_prefix': '04',
        'titulo': 'Base Unificada de Zonas Pesqueras PANGAS',
        'descripcion': 'Capa geográfica consolidada de campos pesqueros artesanales del Golfo de California basada en el mapeo participativo original de la Dra. Marcia Moreno-Báez.',
        'artes': 'Multiespecie / PANGAS',
        'color': '#b45309',
        'edge_color': '#78350f'
    },
    'ZPesca_Redes': {
        'num_prefix': '05',
        'titulo': 'Polígonos de Pesca con Redes de Enmalle',
        'descripcion': 'Zonas de esfuerzo pesquero artesanal con redes agalleras de fondo y deriva para especies demersales y pelágicas.',
        'artes': 'Redes de enmalle / Agalleras de fondo y deriva',
        'color': '#15803d',
        'edge_color': '#14532d'
    },
    'ZPesca_Redes_Manta_Camaron': {
        'num_prefix': '06',
        'titulo': 'Polígonos de Pesca de Camarón y Redes de Manta',
        'descripcion': 'Caladeros de pesca estacional de camarón mediante redes de manta y surpera en el litoral marino costero de Sonora y Sinaloa.',
        'color': '#6b21a8',
        'edge_color': '#581c87'
    },
    'ZPesca_Trampa': {
        'num_prefix': '07',
        'titulo': 'Polígonos de Pesca con Trampas (Jaiba y Peces)',
        'descripcion': 'Sitios de pesca artesanal costera y estuarina mediante trampas y nasas para jaiba azul, jaiba café y especies de rocas.',
        'color': '#0f766e',
        'edge_color': '#134e4a'
    }
}

layers_list = pyogrio.list_layers(GDB_PATH)
layer_names = [name for name, _ in layers_list]

print(f"Iniciando generación de paquetes georreferenciados para {len(layer_names)} capas...")

package_summary = []

for layer in layer_names:
    config = LAYER_CONFIG.get(layer, {
        'num_prefix': '99',
        'titulo': f'Capa {layer}',
        'descripcion': 'Capa geográfica del estudio PANGAS.',
        'artes': 'Pesca Artesanal',
        'color': '#0284c7',
        'edge_color': '#0369a1'
    })
    
    folder_name = f"{config['num_prefix']}_{layer}"
    pkg_dir = OUTPUT_PACKAGES_DIR / folder_name
    pkg_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nProcesando paquete: {folder_name}...")
    gdf = gpd.read_file(GDB_PATH, layer=layer)
    
    # Reproyectar a EPSG:3857 para contexto geográfico Web Mercator
    gdf_3857 = gdf.to_crs(epsg=3857)
    bounds_4326 = gdf.to_crs(epsg=4326).total_bounds
    bbox_str = f"MinLon: {bounds_4326[0]:.4f}, MinLat: {bounds_4326[1]:.4f}, MaxLon: {bounds_4326[2]:.4f}, MaxLat: {bounds_4326[3]:.4f}"
    
    # ── 1. Renderizar Mapa 1: OpenStreetMap Estándar (Estilo QGIS) ──
    fig, ax = plt.subplots(figsize=(14, 9), dpi=150)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    
    gdf_3857.plot(ax=ax, color=config['color'], edgecolor=config['edge_color'], alpha=0.55, linewidth=0.5)
    
    try:
        ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
    except Exception as e:
        print(f"   Aviso: no se pudo cargar OSM tile online: {e}")
        
    ax.set_title(f"ESTUDIO PANGAS (Dra. Marcia Moreno-Báez et al.) — CAPA: {layer.upper()}\n"
                 f"Mapa Base Georreferenciado: OpenStreetMap Standard (EPSG:3857) | Entidades: {len(gdf):,}\n"
                 f"Uso por Causa Natura Data: JCB (Consultor Senior) & EG (Analista GIS)",
                 fontsize=11, color='#0f172a', fontweight='bold', pad=12)
    ax.set_xlabel("Coordenadas Web Mercator X (m)", fontsize=10, color='#334155')
    ax.set_ylabel("Coordenadas Web Mercator Y (m)", fontsize=10, color='#334155')
    ax.grid(True, linestyle=':', alpha=0.5, color='#94a3b8')
    
    osm_jpg_path = pkg_dir / "mapa_osm.jpg"
    plt.tight_layout()
    plt.savefig(osm_jpg_path, format='jpg', dpi=150, facecolor='#ffffff', edgecolor='none')
    plt.close()
    print(f"   Mapa OSM (estilo QGIS) generado: {osm_jpg_path}")
    
    # ── 2. Renderizar Mapa 2: Esri World Imagery (Satelital) ──
    fig, ax = plt.subplots(figsize=(14, 9), dpi=150)
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')
    
    gdf_3857.plot(ax=ax, color='#f59e0b', edgecolor='#fef08a', alpha=0.65, linewidth=0.6)
    
    try:
        ctx.add_basemap(ax, source=ctx.providers.Esri.WorldImagery)
    except Exception as e:
        print(f"   Aviso: no se pudo cargar Esri Satelital online: {e}")
        
    ax.set_title(f"ESTUDIO PANGAS (Dra. Marcia Moreno-Báez et al.) — CAPA: {layer.upper()}\n"
                 f"Mapa Base Georreferenciado: Esri World Imagery Satelital | Entidades: {len(gdf):,}\n"
                 f"Uso por Causa Natura Data: JCB (Consultor Senior) & EG (Analista GIS)",
                 fontsize=11, color='#f8fafc', fontweight='bold', pad=12)
    ax.set_xlabel("Coordenadas Web Mercator X (m)", fontsize=10, color='#cbd5e1')
    ax.set_ylabel("Coordenadas Web Mercator Y (m)", fontsize=10, color='#cbd5e1')
    ax.grid(True, linestyle=':', alpha=0.3, color='#64748b')
    ax.tick_params(colors='#f8fafc')
    
    sat_jpg_path = pkg_dir / "mapa_satelital.jpg"
    plt.tight_layout()
    plt.savefig(sat_jpg_path, format='jpg', dpi=150, facecolor='#0f172a', edgecolor='none')
    plt.close()
    print(f"   Mapa Satelital generado: {sat_jpg_path}")
    
    # ── 3. Extraer Metadatos y Especies ──
    schema_fields = [{'campo': col, 'tipo': str(dtype)} for col, dtype in gdf.dtypes.items() if col != 'geometry']
    species_list = []
    if 'spp_code' in gdf.columns:
        species_list = sorted(list(gdf['spp_code'].dropna().unique()))[:25]
        
    # ── 4. Generar METADATOS_CAPA.md ──
    meta_md_path = pkg_dir / "METADATOS_CAPA.md"
    md_text = f"""# Paquete Geográfico y Metadatos: Capa `{layer}`

**Título de la Capa:** {config['titulo']}  
**Base de Datos de Origen:** `Fish_Zones_PANGAS.gdb` (Estudio PANGAS)  

---

## 1. Atribución Académica y Cita Oficial

**Autora Principal de la Base de Datos:** Dra. Marcia Moreno-Báez et al.  
**Cita Académica Completa:**  
> {CITA_ACADEMICA}

**Uso y Adaptación Metodológica:**  
Esta capa constituye la línea base histórica del estudio PANGAS utilizada por **Juan Carlos Barrera (JCB - Consultor Senior)** y **Enrique Gorosave (EG - Analista GIS)** para el proyecto **IERC-GNL** de **Causa Natura Data (POA 2026-2028)**. Se utiliza para calibrar la exposición y sensibilidad de las comunidades pesqueras ante la infraestructura de Gas Natural Licuado en el Golfo de California.

---

## 2. Ficha Técnica Espacial

- **Nombre de la Capa en GDB:** `{layer}`
- **Tipo de Geometría:** `{gdf.geometry.geom_type.iloc[0] if len(gdf) > 0 else 'MultiPolygon'}`
- **Número Total de Polígonos / Entidades:** `{len(gdf):,}`
- **Sistema de Coordenadas Original:** EPSG:4326 (WGS 84 - Grados Decimales)
- **Proyección de Visualización:** EPSG:3857 (Web Mercator)
- **Extensión Geográfica (Bounding Box WGS84):** `{bbox_str}`
- **Artes de Pesca Relacionadas:** {config['artes']}

---

## 3. Descripción Metodológica

{config['descripcion']}

---

## 4. Visualización Cartográfica Georreferenciada

### Mapa Base: OpenStreetMap Estándar (Estilo QGIS)
![Mapa OpenStreetMap](mapa_osm.jpg)

### Mapa Base: Esri World Imagery (Satelital)
![Mapa Satelital Esri](mapa_satelital.jpg)

---

## 5. Diccionario de Atributos ({len(schema_fields)} Campos)

| Nombre de Campo | Tipo de Dato | Rol / Descripción Metodológica |
|---|---|---|
"""
    for f_info in schema_fields:
        md_text += f"| `{f_info['campo']}` | `{f_info['tipo']}` | Atributo espacial/pesquero registrado en PANGAS |\n"

    if species_list:
        md_text += f"\n### Muestra de Especies Registradas (Códigos SPP):\n`{', '.join(species_list)}`\n"

    meta_md_path.write_text(md_text, encoding='utf-8')
    print(f"   Ficha de metadatos generada: {meta_md_path}")
    
    package_summary.append({
        'folder_name': folder_name,
        'layer': layer,
        'titulo': config['titulo'],
        'entities': len(gdf),
        'artes': config['artes'],
        'bbox': bbox_str,
        'schema_count': len(schema_fields)
    })

# ── 5. Generar Informe Maestro HTML Consolidado ──
print("\nGenerando informe maestro HTML ATLAS_PAQUETES_COMPLETO.html...")

html_master = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Atlas de Paquetes Geográficos PANGAS — Causa Natura Data</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 40px; line-height: 1.6; }}
        h1 {{ color: #38bdf8; border-bottom: 2px solid #0284c7; padding-bottom: 12px; font-size: 26px; }}
        h2 {{ color: #f1f5f9; margin-top: 32px; font-size: 20px; border-bottom: 1px solid #334155; padding-bottom: 6px; }}
        h3 {{ color: #7dd3fc; font-size: 18px; margin-top: 24px; }}
        .citation-box {{ background-color: #1e293b; border-left: 4px solid #38bdf8; padding: 16px; margin: 20px 0; border-radius: 4px; font-style: italic; color: #cbd5e1; }}
        .card {{ background-color: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 24px; margin-bottom: 40px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.4); }}
        .grid-maps {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0; }}
        .grid-maps img {{ width: 100%; border-radius: 6px; border: 1px solid #475569; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 12px; background-color: #0f172a; border-radius: 6px; overflow: hidden; }}
        th, td {{ padding: 10px 14px; text-align: left; border-bottom: 1px solid #334155; font-size: 14px; }}
        th {{ background-color: #0284c7; color: #ffffff; }}
        tr:nth-child(even) {{ background-color: #1e293b; }}
        .badge {{ background-color: #0369a1; color: #e0f2fe; padding: 4px 8px; border-radius: 4px; font-family: monospace; font-size: 13px; }}
        .btn {{ display: inline-block; background-color: #0284c7; color: white; padding: 8px 16px; text-decoration: none; border-radius: 4px; font-weight: bold; margin-top: 10px; }}
        .btn:hover {{ background-color: #0369a1; }}
    </style>
</head>
<body>

    <h1>Catálogo Espacial de Paquetes Geográficos PANGAS (Fish_Zones_PANGAS.gdb)</h1>
    <p><strong>Proyecto:</strong> Índice Espacial de Riesgo Socioeconómico para Comunidades (IERC-GNL)</p>
    <p><strong>Organización:</strong> Causa Natura Data (POA 2026-2028)</p>
    <p><strong>Equipo Técnico:</strong> Juan Carlos Barrera (JCB - Consultor Senior) & Enrique Gorosave (EG - Analista GIS)</p>

    <div class="citation-box">
        <strong>Atribución y Cita Académica Oficial:</strong><br>
        {CITA_ACADEMICA}
    </div>

    <h2>Resumen General de Paquetes ({len(package_summary)} Capas)</h2>
    <table>
        <thead>
            <tr>
                <th>Carpeta de Paquete</th>
                <th>Capa en GDB</th>
                <th>Entidades</th>
                <th>Artes de Pesca</th>
                <th>Acciones</th>
            </tr>
        </thead>
        <tbody>
"""

for pkg in package_summary:
    html_master += f"""
            <tr>
                <td><span class="badge">{pkg['folder_name']}</span></td>
                <td><code>{pkg['layer']}</code></td>
                <td>{pkg['entities']:,}</td>
                <td>{pkg['artes']}</td>
                <td><a class="btn" href="./{pkg['folder_name']}/METADATOS_CAPA.md">Ver Ficha Markdown</a></td>
            </tr>
    """

html_master += """
        </tbody>
    </table>

    <h2>Paquetes Cartográficos Detallados con Mapas Georreferenciados</h2>
"""

for pkg in package_summary:
    html_master += f"""
    <div class="card">
        <h3>Paquete: {pkg['folder_name']} — {pkg['titulo']}</h3>
        <p><strong>Capa GDB:</strong> <code>{pkg['layer']}</code> | <strong>Entidades:</strong> {pkg['entities']:,} | <strong>CRS:</strong> EPSG:4326 (WGS84)</p>
        <p><strong>Bounding Box:</strong> <code>{pkg['bbox']}</code></p>
        
        <div class="grid-maps">
            <div>
                <h4>Mapa OpenStreetMap Estándar (Estilo QGIS)</h4>
                <img src="./{pkg['folder_name']}/mapa_osm.jpg" alt="Mapa OSM {pkg['layer']}">
            </div>
            <div>
                <h4>Mapa Esri World Imagery (Satelital)</h4>
                <img src="./{pkg['folder_name']}/mapa_satelital.jpg" alt="Mapa Satelital {pkg['layer']}">
            </div>
        </div>
    </div>
    """

html_master += """
</body>
</html>
"""

HTML_MASTER_PATH.write_text(html_master, encoding='utf-8')
print(f"\nInforme Maestro HTML generado exitosamente en: {HTML_MASTER_PATH}")
print("Generación completa de paquetes por capa finalizada con éxito.")
