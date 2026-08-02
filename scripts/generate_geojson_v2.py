#!/usr/bin/env python3
"""
generate_geojson_v2.py — Generador de GeoJSONs v2 para IERC-GNL
============================================================
Lee GeoPackage v2 (/home/gorops/gnl_research/terminales_gnl_pacifico_mexico_v2.gpkg)
y genera:
1. dashboard/public/data/proyectos_gnl.geojson (13 features estandarizados, JSON estricto sin NaN)
2. dashboard/public/data/capas_contextuales.geojson (Gasoductos y Áreas Protegidas Ramsar/ANPs)
3. data/processed/proyectos_gnl_v2.geojson
"""

import json
import math
from pathlib import Path
import geopandas as gpd
from shapely.geometry import Point, Polygon, LineString, mapping

BASE_DIR = Path("/home/gorops/ierc-gnl-project")
RESEARCH_GPKG = Path("/home/gorops/gnl_research/terminales_gnl_pacifico_mexico_v2.gpkg")

OUT_PUBLIC_PROYECTOS = BASE_DIR / "dashboard/public/data/proyectos_gnl.geojson"
OUT_PUBLIC_CONTEXTO = BASE_DIR / "dashboard/public/data/capas_contextuales.geojson"
OUT_PROCESSED_PROYECTOS = BASE_DIR / "data/processed/proyectos_gnl_v2.geojson"


def clean_num(val):
    """Sanitiza números flotantes para evitar NaN o Infinity en JSON estricto."""
    if val is None:
        return None
    try:
        f = float(val)
        if math.isnan(f) or math.isinf(f):
            return None
        return f
    except (ValueError, TypeError):
        return None


def build_proyectos_geojson():
    print(f"Cargando GeoPackage: {RESEARCH_GPKG}")
    gdf = gpd.read_file(RESEARCH_GPKG)
    
    features = []
    
    for idx, row in gdf.iterrows():
        p_id = str(row['proyecto'])
        status_raw = str(row['status'])
        
        # Mapeo de estatus legible
        if 'cancelado' in status_raw.lower():
            estatus_permiso = "CANCELADO"
            status_code = "cancelado"
            color_hex = "#78909C" # Gris neutro/deshabilitado
        elif 'evaluacion' in status_raw.lower():
            estatus_permiso = "En evaluación ASEA"
            status_code = "en_evaluacion"
            color_hex = "#00ACC1" # Cían/Turquesa
        else:
            estatus_permiso = "Propuesto / Pre-FID"
            status_code = "proposed"
            color_hex = "#E53935" # Rojo alerta
            
        # Nombres y metadata enriquecidos
        title_map = {
            'Saguaro_T1': 'Saguaro Energía GNL — Tren 1 (172 ha)',
            'Saguaro_T2': 'Saguaro Energía GNL — Tren 2 (47 ha)',
            'Saguaro_Reserva': 'Saguaro Energía GNL — Área Reserva (1 ha)',
            'Saguaro_Campamentos': 'Saguaro Energía GNL — Campamentos (21 ha)',
            'Saguaro_Caminos': 'Saguaro Energía GNL — Caminos de Acceso (155 vértices)',
            'Amigo_LNG_T1': 'Amigo LNG — Tren 1 (4.2 MTPA)',
            'Amigo_LNG_T2': 'Amigo LNG — Tren 2 (3.6 MTPA)',
            'Vista_Pacifico_FLNG': 'Vista Pacífico GNL — Unidad FLNG Marine (CANCELADO)',
            'Vista_Pacifico_Marina': 'Vista Pacífico GNL — Área Marina 22 ha (CANCELADO)',
            'Vista_Pacifico_Terrestre': 'Vista Pacífico GNL — Predio ASIPONA 1 ha (CANCELADO)',
            'Vista_Pacifico_Jetty': 'Vista Pacífico GNL — Muelle / Jetty (CANCELADO)',
            'GNL_Cosala_Mazatlan': 'GNL Cosalá — Estación Mazatlán (Casas Viejas 1.5 ha)',
            'GNL_Cosala_Zapopan': 'GNL Cosalá — Estación Zapopan (Av. Agujas 0.3 ha)',
        }
        
        terminal_group = {
            'Saguaro': 'Saguaro Energía GNL',
            'Amigo': 'Amigo LNG',
            'Vista': 'Vista Pacífico LNG',
            'Cosala': 'GNL Cosalá'
        }
        
        t_group = "Otro"
        for k, v in terminal_group.items():
            if k in p_id:
                t_group = v
                break
                
        # Detalle ambiental ONU / Ramsar
        impacto_notes = ""
        if t_group == "Vista Pacífico LNG":
            impacto_notes = "CANCELADO Feb 2026. Afectaba Sitio Ramsar Topolobampo (21.9 ha), AICA Bahía Navachiste (21.9 ha), ANP Islas del Golfo (2.15 km W)."
        elif t_group == "Saguaro Energía GNL":
            impacto_notes = "30 MTPA total. Comunicación ONU AL OTH 39/2025. Conexión con Gasoducto Sierra Madre (800 km)."
        elif t_group == "Amigo LNG":
            impacto_notes = "7.8 MTPA total. Contratos SPA 20 años con Sahara Group y Gunvor."
        elif t_group == "GNL Cosalá":
            impacto_notes = "Trámites ASEA 25SI2023G0009, 25SI2025G0030, 14JA2025G0073. Compresión propano y tanques 800 m³."

        # Centroide lat/lon para popups y marcadores
        geom = row['geometry']
        centroid = geom.centroid
        lat = round(float(centroid.y), 6)
        lon = round(float(centroid.x), 6)

        props = {
            'id': p_id,
            'nombre_feature': title_map.get(p_id, p_id),
            'terminal_grupo': t_group,
            'promovente': str(row['promovente']),
            'empresa_madre': str(row['empresa_madre']),
            'estado': str(row['estado']),
            'municipio': str(row['municipio']),
            'localidad': str(row['localidad']),
            'tipo_area': str(row['tipo_area']),
            'estatus_permiso': estatus_permiso,
            'status_code': status_code,
            'color_hex': color_hex,
            'capacidad_mtpa': clean_num(row['capacidad_mtpa']),
            'superficie_ha': clean_num(row['superficie_ha']),
            'precision_geom': str(row['precision']),
            'fuente_coordenadas': str(row['fuente_coordenadas']),
            'clave_proyecto': str(row['clave_proyecto']),
            'impacto_notes': impacto_notes,
            'latitud': lat,
            'longitud': lon
        }
        
        features.append({
            'type': 'Feature',
            'properties': props,
            'geometry': mapping(geom)
        })
        
    fc = {
        'type': 'FeatureCollection',
        'name': 'proyectos_gnl_v2',
        'crs': { 'type': 'name', 'properties': { 'name': 'urn:ogc:def:crs:OGC:1.3:CRS84' } },
        'features': features
    }
    
    OUT_PUBLIC_PROYECTOS.parent.mkdir(parents=True, exist_ok=True)
    OUT_PROCESSED_PROYECTOS.parent.mkdir(parents=True, exist_ok=True)
    
    with open(OUT_PUBLIC_PROYECTOS, 'w', encoding='utf-8') as f:
        json.dump(fc, f, ensure_ascii=False, indent=2)
    print(f" -> Guardado: {OUT_PUBLIC_PROYECTOS} ({len(features)} features)")
    
    with open(OUT_PROCESSED_PROYECTOS, 'w', encoding='utf-8') as f:
        json.dump(fc, f, ensure_ascii=False, indent=2)
    print(f" -> Guardado: {OUT_PROCESSED_PROYECTOS}")


def build_capas_contextuales():
    """Genera capas de gasoductos y zonas de conservación / ANPs."""
    context_features = []
    
    # 1. Gasoducto Sierra Madre (~800 km, Frontera Chihuahua/Sonora -> Puerto Libertad Saguaro)
    sierra_madre_coords = [
        [-108.2000, 31.3000],
        [-109.5000, 30.8000],
        [-110.8000, 30.2000],
        [-112.6880, 29.9058]
    ]
    context_features.append({
        'type': 'Feature',
        'properties': {
            'id': 'gasoducto_sierra_madre',
            'nombre': 'Gasoducto Sierra Madre (~800 km)',
            'tipo_capa': 'Gasoducto',
            'empresa': 'Mexico Pacific Limited',
            'estatus': 'Propuesto / Permiso en trámite',
            'color': '#FF9800',
            'line_weight': 3,
            'dash_array': '5, 5',
            'descripcion': 'Conecta el Hub Permian (EEUU) a través de Chihuahua/Sonora con la Terminal Saguaro Energía en Puerto Libertad (30 MTPA).'
        },
        'geometry': mapping(LineString(sierra_madre_coords))
    })
    
    # 2. Gasoducto Corredor Norte (GCN, ~75 km Ahome -> El Fuerte)
    gcn_coords = [
        [-108.8500, 26.1500],
        [-108.9800, 25.8000],
        [-109.0881, 25.6033]
    ]
    context_features.append({
        'type': 'Feature',
        'properties': {
            'id': 'gasoducto_corredor_norte',
            'nombre': 'Gasoducto Corredor Norte (GCN ~75 km)',
            'tipo_capa': 'Gasoducto',
            'empresa': 'Gasoducto Corredor Norte, S.A.P.I.',
            'estatus': 'Asociado a proyecto Vista Pacífico (CANCELADO)',
            'color': '#78909C',
            'line_weight': 2.5,
            'dash_array': '8, 4',
            'descripcion': 'Gasoducto proyectado para alimentar Vista Pacífico LNG en Topolobampo.'
        },
        'geometry': mapping(LineString(gcn_coords))
    })
    
    # 3. Sitio Ramsar "Lagunas Santa María-Topolobampo-Ohuira"
    ramsar_poly = Polygon([
        [-109.15, 25.52],
        [-108.95, 25.52],
        [-108.95, 25.68],
        [-109.15, 25.68],
        [-109.15, 25.52]
    ])
    context_features.append({
        'type': 'Feature',
        'properties': {
            'id': 'ramsar_topolobampo',
            'nombre': 'Sitio Ramsar Lagunas Santa María-Topolobampo-Ohuira',
            'tipo_capa': 'Área Protegida / Ramsar',
            'estatus': 'Internacional (Ramsar #1978)',
            'color': '#2E7D32',
            'fill_color': '#4CAF50',
            'fill_opacity': 0.18,
            'descripcion': 'Humedal de importancia internacional. 21.9 ha de afectación calculada por el proyecto Vista Pacífico LNG (ONU AL OTH 39/2025).'
        },
        'geometry': mapping(ramsar_poly)
    })
    
    # 4. ANP Islas del Golfo de California
    anp_islas = Polygon([
        [-109.25, 25.50],
        [-109.13, 25.50],
        [-109.13, 25.62],
        [-109.25, 25.62],
        [-109.25, 25.50]
    ])
    context_features.append({
        'type': 'Feature',
        'properties': {
            'id': 'anp_islas_golfo',
            'nombre': 'ANP Federal Islas del Golfo de California (Zona de Influencia)',
            'tipo_capa': 'Área Natural Protegida',
            'estatus': 'Decreto Federal ANP',
            'color': '#1B5E20',
            'fill_color': '#81C784',
            'fill_opacity': 0.15,
            'descripcion': 'Reserva de la biosfera a 2.15 km al oeste de la ubicación FLNG de Vista Pacífico.'
        },
        'geometry': mapping(anp_islas)
    })
    
    fc = {
        'type': 'FeatureCollection',
        'name': 'capas_contextuales_gnl',
        'crs': { 'type': 'name', 'properties': { 'name': 'urn:ogc:def:crs:OGC:1.3:CRS84' } },
        'features': context_features
    }
    
    with open(OUT_PUBLIC_CONTEXTO, 'w', encoding='utf-8') as f:
        json.dump(fc, f, ensure_ascii=False, indent=2)
    print(f" -> Guardado: {OUT_PUBLIC_CONTEXTO} ({len(context_features)} capas contextuales)")


if __name__ == '__main__':
    print("=== Generando GeoJSONs v2 IERC-GNL ===")
    build_proyectos_geojson()
    build_capas_contextuales()
    print("=== Proceso completado exitosamente ===")
