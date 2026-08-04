#!/usr/bin/env python3
"""
Dashboard Folium — IERC-GNL Riesgo Pesquero v2.0
=================================================

Genera un mapa interactivo HTML consolidado con:
- 4 Terminales GNL del Pacífico Mexicano (13 features vectoriales: polígonos, puntos FLNG, subsistemas)
- Estatus diferencial: Propuesto (Red/Orange), En evaluación (Teal/Cyan), CANCELADO (Grey/Dashed)
- Capas contextuales: Gasoducto Sierra Madre, Gasoducto Corredor Norte, Sitio Ramsar Topolobampo, ANP Islas del Golfo
- Zonas pesqueras PANGAS (4,241 zonas), Riqueza Relativa de Especies y Buceo
- Control de capas, leyendas interactivas y tooltips socioambientales (comunicación ONU AL OTH 39/2025)

Output: output/dashboard_riesgo_pesquero.html
"""

import json
import os
from pathlib import Path
import folium
from folium import plugins
from config import get_data_dir, get_causanatura_dir, get_deliverables_dir, get_raw_dir, PROJECT_ROOT

BASE_DIR = PROJECT_ROOT
PUBLIC_DATA_DIR = BASE_DIR / 'dashboard/public/data'
PANGAS_DIR = get_raw_dir("pangas_wgs84")
OUTPUT_DIR = get_deliverables_dir()

# Datos de riesgo pesquero consolidados para los 4 proyectos
RISK_METRICS = {
    'Saguaro Energía GNL': {
        'riesgo_pesquero': 90.3, 'nivel': 'Alto', 'zonas': 525, 'dist_min_km': 1.96,
        'densidad': 1.000, 'especies_score': 1.00, 'capacidad': '30.0 MTPA (3 trenes)'
    },
    'Amigo LNG': {
        'riesgo_pesquero': 93.8, 'nivel': 'Alto', 'zonas': 2828, 'dist_min_km': 0.76,
        'densidad': 1.000, 'especies_score': 0.80, 'capacidad': '7.8 MTPA (T1+T2)'
    },
    'Vista Pacífico LNG': {
        'riesgo_pesquero': 88.5, 'nivel': 'Alto (PROYECTO CANCELADO)', 'zonas': 1240, 'dist_min_km': 0.50,
        'densidad': 0.890, 'especies_score': 0.95, 'capacidad': '5.05 MTPA (CANCELADO Feb 2026)'
    },
    'GNL Cosalá': {
        'riesgo_pesquero': 42.0, 'nivel': 'Moderado', 'zonas': 180, 'dist_min_km': 4.12,
        'densidad': 0.450, 'especies_score': 0.50, 'capacidad': 'Estaciones Compresión/Descompresión'
    }
}


def build_popup_html(props: dict) -> str:
    """Construye una ficha informativa HTML rica para el popup del mapa."""
    t_group = props.get('terminal_grupo', 'Proyecto GNL')
    p_name = props.get('nombre_feature', props.get('id'))
    status_permiso = props.get('estatus_permiso', 'Propuesto')
    is_cancelado = 'CANCELADO' in status_permiso.upper()
    
    rm = RISK_METRICS.get(t_group, {
        'riesgo_pesquero': 50.0, 'nivel': 'Moderado', 'zonas': 0, 'dist_min_km': 0,
        'densidad': 0, 'especies_score': 0, 'capacidad': 'N/A'
    })
    
    header_color = '#546E7A' if is_cancelado else ('#D32F2F' if rm['riesgo_pesquero'] >= 70 else '#F57C00')
    badge_bg = '#78909C' if is_cancelado else ('#D32F2F' if rm['riesgo_pesquero'] >= 70 else '#00ACC1')
    
    notes_html = f"""
    <div style="margin-top:8px; padding:6px; background:#FFF3E0; border-left:3px solid #FF9800; font-size:11px;">
        <b>Impacto Socioambiental:</b><br>{props.get('impacto_notes', '')}
    </div>
    """ if props.get('impacto_notes') else ""

    return f"""
    <div style="font-family: 'Segoe UI', sans-serif; width: 310px; padding: 4px;">
        <div style="background:{header_color}; color:white; padding: 8px 10px; border-radius: 6px 6px 0 0;">
            <div style="font-size:10px; text-transform:uppercase; letter-spacing:1px; opacity:0.9;">{t_group}</div>
            <div style="font-size:13px; font-weight:bold; margin-top:2px;">{p_name}</div>
        </div>
        
        <div style="padding: 10px; background: #FAFAFA; border: 1px solid #E0E0E0; border-top: none; border-radius: 0 0 6px 6px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <span style="background:{badge_bg}; color:white; padding:3px 8px; border-radius:12px; font-size:10px; font-weight:bold;">
                    {status_permiso}
                </span>
                <span style="font-size:11px; color:#666;">
                    {props.get('estado', '')} · {props.get('municipio', '')}
                </span>
            </div>

            <table style="font-size: 11px; width: 100%; border-collapse: collapse; margin-top: 4px;">
                <tr style="background:#F0F4F8;">
                    <td style="padding:4px 6px;"><b>Promovente</b></td>
                    <td style="padding:4px 6px;">{props.get('promovente', 'N/A')}</td>
                </tr>
                <tr>
                    <td style="padding:4px 6px;"><b>Capacidad</b></td>
                    <td style="padding:4px 6px;">{props.get('capacidad_mtpa', 'N/A')} MTPA</td>
                </tr>
                <tr style="background:#F0F4F8;">
                    <td style="padding:4px 6px;"><b>Tipo de Área</b></td>
                    <td style="padding:4px 6px;">{props.get('tipo_area', 'N/A')}</td>
                </tr>
                <tr>
                    <td style="padding:4px 6px;"><b>Riesgo Pesquero</b></td>
                    <td style="padding:4px 6px;"><b>{rm['riesgo_pesquero']:.1f}/100</b> ({rm['nivel']})</td>
                </tr>
                <tr style="background:#F0F4F8;">
                    <td style="padding:4px 6px;"><b>Zonas PANGAS c/u</b></td>
                    <td style="padding:4px 6px;">{rm['zonas']:,} (min {rm['dist_min_km']} km)</td>
                </tr>
                <tr>
                    <td style="padding:4px 6px;"><b>Precisión Geom</b></td>
                    <td style="padding:4px 6px;">{props.get('precision_geom', 'aprox')} ({props.get('fuente_coordenadas', '')})</td>
                </tr>
            </table>

            {notes_html}

            <div style="font-size:9px; color:#888; margin-top:8px; text-align:right;">
                Clave ASEA / Ref: {props.get('clave_proyecto', 'N/A')}
            </div>
        </div>
    </div>
    """


def build_map():
    print("Iniciando construcción del mapa Folium IERC-GNL v2.0...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Centro: Golfo de California / Pacífico Mexicano
    m = folium.Map(
        location=[26.5, -111.0],
        zoom_start=6,
        tiles=None,
        control_scale=True,
    )

    # Capas base tiles
    folium.TileLayer(
        tiles='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
        attr='&copy; CARTO &copy; OpenStreetMap',
        name=' CartoDB Dark (Recomendado)',
        max_zoom=19,
        subdomains='abcd',
    ).add_to(m)

    folium.TileLayer(
        tiles='OpenStreetMap',
        name=' OpenStreetMap',
    ).add_to(m)

    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri Satellite',
        name=' Satélite (ESRI)',
    ).add_to(m)

    # ============================================================
    # CAPA 1: Polígonos y Features de las 4 Terminales GNL (13 features)
    # ============================================================
    gnl_group = folium.FeatureGroup(name=' Terminales y Subconjuntos GNL (13 features)', show=True)
    
    proyectos_file = PUBLIC_DATA_DIR / 'proyectos_gnl.geojson'
    if proyectos_file.exists():
        with open(proyectos_file, 'r', encoding='utf-8') as f:
            p_data = json.load(f)
            
        print(f"Cargando {len(p_data['features'])} features de proyectos GNL...")
        for feat in p_data['features']:
            props = feat['properties']
            p_id = props['id']
            status = props.get('status_code', 'proposed')
            is_cancel = status == 'cancelado'
            
            # Estilos por estatus
            if is_cancel:
                fill_c = '#78909C'
                border_c = '#455A64'
                weight = 2
                dash = '6, 4'
                fill_op = 0.35
            elif status == 'en_evaluacion':
                fill_c = '#00ACC1'
                border_c = '#006064'
                weight = 2
                dash = '0'
                fill_op = 0.55
            else: # proposed
                fill_c = '#E53935'
                border_c = '#B71C1C'
                weight = 2.5
                dash = '0'
                fill_op = 0.60

            popup_content = build_popup_html(props)
            tooltip_txt = f"<b>{props.get('nombre_feature')}</b><br>Estatus: {props.get('estatus_permiso')}"

            # Representación vectorial (Polygon / Point / LineString)
            gtype = feat['geometry']['type']
            
            if gtype in ['Polygon', 'MultiPolygon', 'LineString']:
                folium.GeoJson(
                    feat,
                    style_function=lambda x, fc=fill_c, bc=border_c, w=weight, d=dash, fo=fill_op: {
                        'fillColor': fc,
                        'color': bc,
                        'weight': w,
                        'dashArray': d,
                        'fillOpacity': fo,
                    },
                    popup=folium.Popup(popup_content, max_width=340),
                    tooltip=folium.Tooltip(tooltip_txt, sticky=True)
                ).add_to(gnl_group)
                
            # Marcador de centroide con ícono para rápida visión espacial
            lat, lon = props['latitud'], props['longitud']
            icon_name = 'times-circle' if is_cancel else ('exclamation-triangle' if status == 'proposed' else 'info-circle')
            icon_color = 'gray' if is_cancel else ('red' if status == 'proposed' else 'cadetblue')
            
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_content, max_width=340),
                tooltip=folium.Tooltip(f"<b>{props.get('terminal_grupo')}</b> ({props.get('estatus_permiso')})"),
                icon=folium.Icon(color=icon_color, icon=icon_name, prefix='fa')
            ).add_to(gnl_group)

    gnl_group.add_to(m)

    # ============================================================
    # CAPA 2: Capas Contextuales (Gasoductos, Sitios Ramsar, ANPs)
    # ============================================================
    context_group = folium.FeatureGroup(name=' Capas Contextuales (Gasoductos, Ramsar, ANPs)', show=True)
    
    context_file = PUBLIC_DATA_DIR / 'capas_contextuales.geojson'
    if context_file.exists():
        with open(context_file, 'r', encoding='utf-8') as f:
            c_data = json.load(f)
            
        for feat in c_data['features']:
            cp = feat['properties']
            c_type = cp.get('tipo_capa', '')
            c_color = cp.get('color', '#FF9800')
            fill_c = cp.get('fill_color', c_color)
            fill_op = cp.get('fill_opacity', 0.2)
            w = cp.get('line_weight', 2)
            dash = cp.get('dash_array', '0')
            
            popup_html = f"""
            <div style="font-family:sans-serif; padding:5px; width:250px;">
                <h4 style="margin:0 0 6px 0; color:{c_color};">{cp.get('nombre')}</h4>
                <p style="font-size:11px; margin:2px 0;"><b>Tipo:</b> {c_type}</p>
                <p style="font-size:11px; margin:2px 0;"><b>Estatus:</b> {cp.get('estatus')}</p>
                <p style="font-size:11px; color:#444; margin-top:6px;">{cp.get('descripcion')}</p>
            </div>
            """
            
            folium.GeoJson(
                feat,
                style_function=lambda x, cc=c_color, fc=fill_c, fo=fill_op, lw=w, da=dash: {
                    'color': cc,
                    'fillColor': fc,
                    'fillOpacity': fo,
                    'weight': lw,
                    'dashArray': da
                },
                popup=folium.Popup(popup_html, max_width=280),
                tooltip=folium.Tooltip(f"<b>{cp.get('nombre')}</b> ({c_type})")
            ).add_to(context_group)

    context_group.add_to(m)

    # ============================================================
    # CAPA 3: Zonas Pesqueras PANGAS
    # ============================================================
    pangas_group = folium.FeatureGroup(name=' Zonas Pesqueras PANGAS (4,241 zonas)', show=False)
    pangas_file = PANGAS_DIR / 'ZPesca_PANGAS_wgs84.geojson'
    if pangas_file.exists():
        with open(pangas_file, 'r', encoding='utf-8') as f:
            pangas_data = json.load(f)
            
        sampled = pangas_data['features'][::3]
        print(f"  Añadiendo {len(sampled)} zonas PANGAS...")
        for feat in sampled:
            sitio = feat['properties'].get('sitio_nomb', 'N/A')
            habitat = feat['properties'].get('HABITAT', 'N/A')
            folium.GeoJson(
                feat,
                style_function=lambda x: {
                    'fillColor': '#1976D2', 'color': '#0D47A1', 'weight': 0.5, 'fillOpacity': 0.25
                },
                tooltip=folium.Tooltip(f"<b>PANGAS:</b> {sitio} ({habitat})", sticky=True)
            ).add_to(pangas_group)
            
    pangas_group.add_to(m)

    # Leyenda flotante HTML
    legend_html = """
    <div style="
        position: fixed; bottom: 30px; right: 30px; z-index: 1000;
        background: rgba(20, 25, 35, 0.92); color: white; padding: 14px 18px;
        border-radius: 10px; font-family: 'Segoe UI', sans-serif; font-size: 12px;
        border: 1px solid rgba(255,255,255,0.18); box-shadow: 0 4px 20px rgba(0,0,0,0.6);
        min-width: 220px;
    ">
        <div style="font-size: 14px; font-weight: bold; margin-bottom: 8px; border-bottom: 1px solid rgba(255,255,255,0.2); padding-bottom: 4px;">
            Estatus Proyectos GNL
        </div>
        <div style="margin: 4px 0;"><span style="color: #E53935; font-weight:bold;">■</span> Propuesto / Pre-FID (Saguaro, Amigo)</div>
        <div style="margin: 4px 0;"><span style="color: #00ACC1; font-weight:bold;">■</span> En Evaluación ASEA (GNL Cosalá)</div>
        <div style="margin: 4px 0;"><span style="color: #78909C; font-weight:bold;">■</span> CANCELADO (Vista Pacífico FLNG)</div>
        
        <div style="font-size: 13px; font-weight: bold; margin-top: 10px; margin-bottom: 6px; border-bottom: 1px solid rgba(255,255,255,0.2); padding-bottom: 4px;">
            Capas Contextuales
        </div>
        <div style="margin: 3px 0;"><span style="color: #FF9800;">━ ━</span> Gasoducto Sierra Madre / GCN</div>
        <div style="margin: 3px 0;"><span style="color: #4CAF50;">■</span> Sitio Ramsar Topolobampo / ANPs</div>
        <div style="margin: 3px 0;"><span style="color: #1976D2;">■</span> Zonas Pesqueras PANGAS</div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    # Título flotante
    title_html = """
    <div style="
        position: fixed; top: 15px; left: 50%; transform: translateX(-50%); z-index: 1000;
        background: rgba(15, 20, 30, 0.92); color: white; padding: 10px 24px;
        border-radius: 8px; font-family: 'Segoe UI', sans-serif; font-size: 15px; font-weight: bold;
        border: 1px solid rgba(255,255,255,0.2); box-shadow: 0 4px 20px rgba(0,0,0,0.6); text-align: center;
    ">
        IERC-GNL · Terminales GNL del Pacífico Mexicano v2.0
        <div style="font-size: 10px; font-weight: normal; color: rgba(255,255,255,0.7); margin-top: 2px;">
            4 Terminales (13 Subconjuntos Vectoriales) · Estatus Actualizados 2026 · Contexto Ramsar/ANP/PANGAS
        </div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(title_html))

    folium.LayerControl(collapsed=False, position='topright').add_to(m)
    plugins.MiniMap(toggle_display=True, position='bottomleft').add_to(m)

    output_path = OUTPUT_DIR / 'dashboard_riesgo_pesquero.html'
    m.save(str(output_path))
    print(f" Dashboard Folium guardado exitosamente en: {output_path}")
    return str(output_path)


if __name__ == '__main__':
    path = build_map()
