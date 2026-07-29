#!/usr/bin/env python3
"""
export_pangas_gdb_atlas.py
--------------------------
Script de generación del Catálogo Espacial y Atlas JPG para Fish_Zones_PANGAS.gdb
Autores: Juan Carlos Barrera (JCB - Consultor Senior) & Enrique Gorosave (EG - Analista GIS)
Organización: Causa Natura Data (POA 2026-2028)

Este script:
1. Lee las 7 capas de data/raw/pangas_gdb/Fish_Zones_PANGAS.gdb.
2. Renderiza mapas cartográficos de alta definición (1920x1080, 300 DPI) en formato JPG.
3. Extrae metadatos estructurados (CRS, BBox, recuento de entidades, diccionario de atributos, especies).
4. Exporta el Catálogo de Metadatos en Markdown (docs/metodologia/ATLAS_PANGAS_METADATOS_JCB_EG.md) e HTML (output/atlas_pangas_report.html).
"""

import os
from pathlib import Path
import pyogrio
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import matplotlib.ticker as mticker
import numpy as np

# Configurar estilo estricto sin emojis
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

BASE_DIR = Path(__file__).resolve().parent.parent
GDB_PATH = BASE_DIR / 'data' / 'raw' / 'pangas_gdb' / 'Fish_Zones_PANGAS.gdb'
JPG_OUTPUT_DIR = BASE_DIR / 'output' / 'atlas_pangas_jpg'
MD_OUTPUT_PATH = BASE_DIR / 'docs' / 'metodologia' / 'ATLAS_PANGAS_METADATOS_JCB_EG.md'
HTML_OUTPUT_PATH = BASE_DIR / 'output' / 'atlas_pangas_report.html'

JPG_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MD_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

print("Iniciando procesamiento de capas de Fish_Zones_PANGAS.gdb...")
print(f"Ruta de GDB: {GDB_PATH}")

layers_info = pyogrio.list_layers(GDB_PATH)
layer_names = [name for name, _ in layers_info]
print(f"Capas detectadas ({len(layer_names)}): {layer_names}")

# Descripciones y metadatos conceptuales por capa
LAYER_METADATA = {
    'Riqueza_Relativa': {
        'titulo': 'Malla de Riqueza Biológica Pesquera Relativa',
        'descripcion': 'Polígonos de grilla espacial con acumulación de riqueza de especies de peces y mariscos comerciales del Golfo de California (Estudio PANGAS).',
        'color': 'Blues',
        'artes': 'Todas las artes registradas',
        'responsable': 'EG / JCB'
    },
    'ZPesca_Buceo': {
        'titulo': 'Polígonos de Pesca Comercial por Buceo',
        'descripcion': 'Sitios y caladeros de pesca artesanal extractiva mediante buceo (moluscos, bentónicos, almeja, callo de hacha, erizo, pepino de mar).',
        'color': 'PuBu',
        'artes': 'Buceo autónomo y semiautónomo (Hookah)',
        'responsable': 'EG / JCB'
    },
    'ZPesca_Chinchorro': {
        'titulo': 'Polígonos de Pesca con Chinchorro de Línea',
        'descripcion': 'Zonas de operación pesquera artesanal mediante chinchorros de línea de playa y deriva para especies escamadas.',
        'color': 'YlOrRd',
        'artes': 'Chinchorro de línea / Redes agalleras',
        'responsable': 'EG / JCB'
    },
    'ZPesca_PANGAS': {
        'titulo': 'Base Unificada de Zonas Pesqueras PANGAS',
        'descripcion': 'Capa maestra consolidada de campos pesqueros artesanales del Golfo de California derivada de entrevistas participativas.',
        'color': 'YlGnBu',
        'artes': 'Multiespecie / PANGAS',
        'responsable': 'EG / JCB'
    },
    'ZPesca_Redes': {
        'titulo': 'Polígonos de Pesca con Redes de Enmalle',
        'descripcion': 'Zonas de esfuerzo pesquero artesanal con redes agalleras y agalleras de fondo para peces demersales y pelágicos menores.',
        'color': 'Purples',
        'artes': 'Redes de enmalle / Agalleras',
        'responsable': 'EG / JCB'
    },
    'ZPesca_Redes_Manta_Camaron': {
        'titulo': 'Polígonos de Pesca de Camarón y Redes de Manta',
        'descripcion': 'Caladeros de pesca estacional de camarón con redes de manta y surpera en el litoral de Sonora y Sinaloa.',
        'color': 'Oranges',
        'artes': 'Redes de manta / Surpera / Camarón',
        'responsable': 'EG / JCB'
    },
    'ZPesca_Trampa': {
        'titulo': 'Polígonos de Pesca con Trampas (Jaiba y Peces)',
        'descripcion': 'Sitios de pesca artesanal costera y estuarina mediante trampas y nasas para jaiba azul y especies de rocas.',
        'color': 'Greens',
        'artes': 'Trampas jaiberas / Nasas',
        'responsable': 'EG / JCB'
    }
}

catalog_records = []

for idx, layer in enumerate(layer_names, start=1):
    print(f"\n[{idx}/{len(layer_names)}] Procesando capa '{layer}'...")
    gdf = gpd.read_file(GDB_PATH, layer=layer)
    
    # Asegurar CRS EPSG:4326
    if gdf.crs is not None and gdf.crs.to_epsg() != 4326:
        gdf = gdf.to_crs("EPSG:4326")
    elif gdf.crs is None:
        gdf.set_crs("EPSG:4326", inplace=True)
        
    bounds = gdf.total_bounds # [minx, miny, maxx, maxy]
    bbox_str = f"MinLon: {bounds[0]:.4f}, MinLat: {bounds[1]:.4f}, MaxLon: {bounds[2]:.4f}, MaxLat: {bounds[3]:.4f}"
    
    meta_info = LAYER_METADATA.get(layer, {
        'titulo': f"Capa Espacial {layer}",
        'descripcion': 'Capa vectorial de la base de datos geográfica PANGAS.',
        'color': 'viridis',
        'artes': 'Pesca Artesanal',
        'responsable': 'EG / JCB'
    })
    
    # ── Renderizar Mapa JPG de Alta Calidad ──
    fig, ax = plt.subplots(figsize=(14, 8), dpi=150)
    fig.patch.set_facecolor('#0f172a') # Fondo oscuro elegante
    ax.set_facecolor('#1e293b')

    
    # Determinar columna para colorear
    color_column = None
    if 'all' in gdf.columns:
        color_column = 'all'
    elif 'riqueza_total_especies' in gdf.columns:
        color_column = 'riqueza_total_especies'
    elif 'total_registros_entrevista' in gdf.columns:
        color_column = 'total_registros_entrevista'
    
    if color_column and color_column in gdf.columns:
        gdf.plot(column=color_column, cmap=meta_info['color'], ax=ax, linewidth=0.3, edgecolor='#334155', alpha=0.85, legend=True,
                 legend_kwds={'label': f"Intensidad / Riqueza ({color_column})", 'shrink': 0.6})
    else:
        gdf.plot(ax=ax, color='#0284c7', linewidth=0.4, edgecolor='#38bdf8', alpha=0.65)
        
    # Ajustar límites espaciales con margen
    margin_x = (bounds[2] - bounds[0]) * 0.05 if (bounds[2] - bounds[0]) > 0 else 0.5
    margin_y = (bounds[3] - bounds[1]) * 0.05 if (bounds[3] - bounds[1]) > 0 else 0.5
    ax.set_xlim(bounds[0] - margin_x, bounds[2] + margin_x)
    ax.set_ylim(bounds[1] - margin_y, bounds[3] + margin_y)
    
    # Elementos Cartográficos
    ax.grid(True, linestyle='--', alpha=0.3, color='#94a3b8')
    ax.set_xlabel("Longitud (WGS 84 Grados Decimales)", fontsize=11, color='#e2e8f0', fontweight='bold')
    ax.set_ylabel("Latitud (WGS 84 Grados Decimales)", fontsize=11, color='#e2e8f0', fontweight='bold')
    ax.tick_params(colors='#e2e8f0', labelsize=10)
    
    # Rosa de los Vientos
    ax.text(0.96, 0.93, 'N\n▲', transform=ax.transAxes, fontsize=16, fontweight='bold',
            color='#38bdf8', ha='center', va='center',
            bbox=dict(boxstyle='circle,pad=0.4', facecolor='#0f172a', edgecolor='#38bdf8', linewidth=1.5))
    
    # Título y Créditos
    plt.suptitle(f"CATALOGO ESPACIAL PANGAS — CAPA: {layer.upper()}", fontsize=16, fontweight='bold', color='#f8fafc', y=0.96)
    ax.set_title(f"{meta_info['titulo']} | Entidades: {len(gdf):,} | CRS: EPSG:4326 (WGS84)\nCausa Natura Data (POA 2026) | Autores: JCB (Consultor Senior) & EG (Analista GIS)",
                 fontsize=11, color='#cbd5e1', pad=12)
    
    jpg_filename = f"mapa_{layer}.jpg"
    jpg_path = JPG_OUTPUT_DIR / jpg_filename
    plt.tight_layout()
    plt.savefig(jpg_path, format='jpg', dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()

    print(f"   Mapa JPG generado: {jpg_path}")
    
    # Extraer lista de especies si están presentes
    species_list = []
    if 'spp_code' in gdf.columns:
        species_list = sorted(list(gdf['spp_code'].dropna().unique()))[:20]
        
    # Extraer campos y tipos de datos
    schema_info = [{'campo': col, 'tipo': str(dtype)} for col, dtype in gdf.dtypes.items() if col != 'geometry']
    
    catalog_records.append({
        'layer_name': layer,
        'titulo': meta_info['titulo'],
        'descripcion': meta_info['descripcion'],
        'artes': meta_info['artes'],
        'responsable': meta_info['responsable'],
        'geom_type': str(gdf.geometry.geom_type.iloc[0]) if len(gdf) > 0 else 'Polígono',
        'entity_count': len(gdf),
        'bbox': bbox_str,
        'jpg_filename': jpg_filename,
        'jpg_path_rel': f"../output/atlas_pangas_jpg/{jpg_filename}",
        'schema': schema_info,
        'species': species_list
    })

# ── Generar Documento de Metadatos en Markdown ──
print("\nGenerando documento de metadatos en Markdown...")

md_content = f"""# Catálogo Espacial de Capas de la Base de Datos PANGAS (Fish_Zones_PANGAS.gdb)

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
"""

for rec in catalog_records:
    md_content += f"| `{rec['layer_name']}` | `{rec['geom_type']}` | {rec['entity_count']:,} | {rec['artes']} |\n"

md_content += "\n---\n\n## 3. Fichas Técnicas Detalladas por Capa\n\n"

for rec in catalog_records:
    md_content += f"""### Capa: `{rec['layer_name']}`

**Título:** {rec['titulo']}  
**Tipo de Geometría:** {rec['geom_type']}  
**Número de Entidades:** {rec['entity_count']:,}  
**Sistema de Referencia:** EPSG:4326 (WGS 84 - Coordenadas Geográficas)  
**Extensión Espacial (Bounding Box):** `{rec['bbox']}`  
**Artes de Pesca Asociadas:** {rec['artes']}  
**Responsables del Procesamiento:** {rec['responsable']}  

**Descripción Metodológica:**  
{rec['descripcion']}

**Mapa Cartográfico Renderizado (JPG Alta Resolución):**  
![Mapa {rec['layer_name']}](file://{JPG_OUTPUT_DIR / rec['jpg_filename']})

**Esquema de Atributos ({len(rec['schema'])} Campos):**

| Nombre de Campo | Tipo de Dato | Descripción / Rol |
|---|---|---|
"""
    for col in rec['schema'][:15]: # Limitar a primeros 15 campos para legibilidad
        md_content += f"| `{col['campo']}` | `{col['tipo']}` | Atributo descriptivo de la capa pesquera PANGAS |\n"
        
    if rec['species']:
        spp_str = ", ".join(rec['species'])
        md_content += f"\n**Especies Registradas (Muestra spp_code):** `{spp_str}`\n"
        
    md_content += "\n---\n\n"

MD_OUTPUT_PATH.write_text(md_content, encoding='utf-8')
print(f"Documento Markdown generado en: {MD_OUTPUT_PATH}")

# ── Generar Informe HTML Visual Imprimible ──
print("\nGenerando informe visual en HTML...")

html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Catálogo Espacial PANGAS GDB — Causa Natura Data</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 40px; line-height: 1.6; }}
        h1 {{ color: #38bdf8; border-bottom: 2px solid #0284c7; padding-bottom: 12px; font-size: 28px; }}
        h2 {{ color: #f1f5f9; margin-top: 30px; font-size: 22px; border-bottom: 1px solid #334155; padding-bottom: 8px; }}
        h3 {{ color: #7dd3fc; margin-top: 20px; font-size: 18px; }}
        .header-card {{ background-color: #1e293b; border: 1px solid #334155; padding: 24px; border-radius: 8px; margin-bottom: 30px; }}
        .layer-card {{ background-color: #1e293b; border: 1px solid #334155; padding: 24px; border-radius: 8px; margin-bottom: 40px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3); }}
        .map-img {{ width: 100%; height: auto; border-radius: 6px; border: 1px solid #475569; margin: 16px 0; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 12px; margin-bottom: 16px; background-color: #0f172a; border-radius: 6px; overflow: hidden; }}
        th, td {{ padding: 10px 14px; text-align: left; border-bottom: 1px solid #334155; font-size: 14px; }}
        th {{ background-color: #0284c7; color: #ffffff; font-weight: 600; }}
        tr:nth-child(even) {{ background-color: #1e293b; }}
        .badge {{ background-color: #0369a1; color: #e0f2fe; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; font-family: monospace; }}
    </style>
</head>
<body>

    <div class="header-card">
        <h1>Catálogo Espacial de Capas de la Base de Datos PANGAS (Fish_Zones_PANGAS.gdb)</h1>
        <p><strong>Proyecto:</strong> Índice Espacial de Riesgo Socioeconómico para Comunidades (IERC-GNL)</p>
        <p><strong>Organización:</strong> Causa Natura Data (POA 2026-2028)</p>
        <p><strong>Autores:</strong> Juan Carlos Barrera (JCB - Consultor Senior) & Enrique Gorosave (EG - Analista GIS)</p>
        <p><strong>Propósito:</strong> Fichas técnicas y atlas cartográfico de gabinete para el inventario de la línea base de pesca artesanal en el Golfo de California.</p>
    </div>

    <h2>1. Resumen General de Capas ({len(catalog_records)} Capas)</h2>
    <table>
        <thead>
            <tr>
                <th>Nombre de Capa</th>
                <th>Tipo Geometría</th>
                <th>Entidades</th>
                <th>Artes de Pesca</th>
            </tr>
        </thead>
        <tbody>
"""

for rec in catalog_records:
    html_content += f"""
            <tr>
                <td><span class="badge">{rec['layer_name']}</span></td>
                <td>{rec['geom_type']}</td>
                <td>{rec['entity_count']:,}</td>
                <td>{rec['artes']}</td>
            </tr>
    """

html_content += """
        </tbody>
    </table>

    <h2>2. Fichas Técnicas Cartográficas Detalladas</h2>
"""

for rec in catalog_records:
    html_content += f"""
    <div class="layer-card">
        <h3>Capa: {rec['layer_name']} — {rec['titulo']}</h3>
        <p><strong>Descripción:</strong> {rec['descripcion']}</p>
        <p><strong>Geometría:</strong> {rec['geom_type']} | <strong>Entidades:</strong> {rec['entity_count']:,} | <strong>CRS:</strong> EPSG:4326 (WGS84)</p>
        <p><strong>Bounding Box:</strong> <code>{rec['bbox']}</code></p>
        
        <img class="map-img" src="../output/atlas_pangas_jpg/{rec['jpg_filename']}" alt="Mapa {rec['layer_name']}">
        
        <h4>Esquema de Atributos</h4>
        <table>
            <thead>
                <tr>
                    <th>Nombre de Campo</th>
                    <th>Tipo de Dato</th>
                    <th>Descripción</th>
                </tr>
            </thead>
            <tbody>
    """
    for col in rec['schema'][:12]:
        html_content += f"""
                <tr>
                    <td><code>{col['campo']}</code></td>
                    <td>{col['tipo']}</td>
                    <td>Atributo espacial/pesquero PANGAS</td>
                </tr>
        """
    html_content += """
            </tbody>
        </table>
    </div>
    """

html_content += """
</body>
</html>
"""

HTML_OUTPUT_PATH.write_text(html_content, encoding='utf-8')
print(f"Informe HTML generado en: {HTML_OUTPUT_PATH}")

print("\nProceso de generación del Catálogo Espacial completado exitosamente.")
