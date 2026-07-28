#!/usr/bin/env python3
"""
Dashboard Folium — IERC-GNL Riesgo Pesquero
============================================

Genera un mapa interactivo HTML con:
  - Proyectos GNL (marcadores coloreados por riesgo)
  - Zonas pesqueras PANGAS (polígonos por arte de pesca)
  - Capa de riqueza relativa de especies
  - Control de capas, leyenda y tooltips informativos

Output: output/dashboard_riesgo_pesquero.html
"""

import json
import os
from pathlib import Path
import folium
from folium import plugins

# ================================================================
# Resultados de riesgo pesquero calculados
# ================================================================
RESULTS = [
    {
        'proyecto_id': 'NFE_Puerto_Libertad',
        'proyecto_nombre': 'New Fortress Energy\nPuerto Libertad',
        'latitud': 29.9107, 'longitud': -112.6835,
        'estado': 'Sonora', 'estatus': 'Propuesto',
        'riesgo_pesquero': 90.3, 'nivel_riesgo': 'Alto',
        'num_zonas_encontradas': 525, 'zona_mas_cercana_km': 1.96,
        'densidad_esfuerzo_pesquero': 1.0,
        'proximidad_normalizada': 0.676,
        'especies_criticas_score': 1.0,
    },
    {
        'proyecto_id': 'Bazan_San_Felipe',
        'proyecto_nombre': 'Terminal GNL\nSan Felipe',
        'latitud': 31.0833, 'longitud': -114.85,
        'estado': 'Baja California', 'estatus': 'Propuesto',
        'riesgo_pesquero': 97.8, 'nivel_riesgo': 'Alto',
        'num_zonas_encontradas': 2369, 'zona_mas_cercana_km': 0.39,
        'densidad_esfuerzo_pesquero': 1.0,
        'proximidad_normalizada': 0.925,
        'especies_criticas_score': 1.0,
    },
    {
        'proyecto_id': 'Guaymas_Terminal',
        'proyecto_nombre': 'Terminal GNL\nGuaymas',
        'latitud': 27.9179, 'longitud': -110.9039,
        'estado': 'Sonora', 'estatus': 'Propuesto',
        'riesgo_pesquero': 93.8, 'nivel_riesgo': 'Alto',
        'num_zonas_encontradas': 2828, 'zona_mas_cercana_km': 0.76,
        'densidad_esfuerzo_pesquero': 1.0,
        'proximidad_normalizada': 0.927,
        'especies_criticas_score': 0.8,
    },
    {
        'proyecto_id': 'Sempra_Ensenada',
        'proyecto_nombre': 'Sempra Energy\nEnsenada LNG',
        'latitud': 31.8667, 'longitud': -116.6333,
        'estado': 'Baja California', 'estatus': 'Operacional',
        'riesgo_pesquero': 0.0, 'nivel_riesgo': 'Sin datos PANGAS',
        'num_zonas_encontradas': 0, 'zona_mas_cercana_km': None,
        'densidad_esfuerzo_pesquero': 0,
        'proximidad_normalizada': 0,
        'especies_criticas_score': 0,
    },
    {
        'proyecto_id': 'Sempra_Costa_Azul',
        'proyecto_nombre': 'Sempra LNG\nCosta Azul (Expansión)',
        'latitud': 31.715, 'longitud': -116.57,
        'estado': 'Baja California', 'estatus': 'Propuesto (expansión)',
        'riesgo_pesquero': 0.0, 'nivel_riesgo': 'Sin datos PANGAS',
        'num_zonas_encontradas': 0, 'zona_mas_cercana_km': None,
        'densidad_esfuerzo_pesquero': 0,
        'proximidad_normalizada': 0,
        'especies_criticas_score': 0,
    },
]


def risk_color(risk_score: float) -> str:
    """Retorna color hex basado en nivel de riesgo."""
    if risk_score >= 70:
        return '#d32f2f'   # rojo oscuro - Alto
    elif risk_score >= 40:
        return '#f57c00'   # naranja - Moderado
    elif risk_score > 0:
        return '#388e3c'   # verde - Bajo
    else:
        return '#78909c'   # gris - Sin datos


def risk_icon(risk_score: float) -> str:
    """Retorna ícono FontAwesome según nivel de riesgo."""
    if risk_score >= 70:
        return 'exclamation-triangle'
    elif risk_score > 0:
        return 'exclamation-circle'
    else:
        return 'question-circle'


def build_popup(r: dict) -> str:
    """Genera HTML para el popup de cada proyecto GNL."""
    color = risk_color(r['riesgo_pesquero'])
    dist_str = f"{r['zona_mas_cercana_km']} km" if r['zona_mas_cercana_km'] else 'N/A'

    bar_w = int(r['riesgo_pesquero'])
    bar_color = color

    return f"""
<div style="font-family: 'Segoe UI', sans-serif; width: 280px; padding: 5px;">
  <h4 style="margin: 0 0 8px 0; color: {color}; border-bottom: 2px solid {color}; padding-bottom: 4px;">
    🏭 {r['proyecto_id'].replace('_', ' ')}
  </h4>
  <p style="margin: 2px 0; font-size: 12px; color: #555;">{r['estado']} · {r['estatus']}</p>

  <div style="margin: 10px 0;">
    <b>Riesgo Pesquero</b>
    <div style="background:#eee; border-radius:4px; height:20px; margin-top:4px; position:relative;">
      <div style="background:{bar_color}; width:{bar_w}%; height:100%; border-radius:4px;"></div>
      <span style="position:absolute; right:6px; top:2px; font-size:11px; font-weight:bold; color:{'white' if bar_w > 40 else '#333'};">
        {r['riesgo_pesquero']:.1f}/100 — {r['nivel_riesgo']}
      </span>
    </div>
  </div>

  <table style="font-size: 11px; width: 100%; border-collapse: collapse;">
    <tr style="background:#f5f5f5;">
      <td style="padding: 3px 5px;"><b>📍 Coordenadas</b></td>
      <td style="padding: 3px 5px;">{r['latitud']:.4f}°N, {r['longitud']:.4f}°E</td>
    </tr>
    <tr>
      <td style="padding: 3px 5px;"><b>🎣 Zonas pesqueras</b></td>
      <td style="padding: 3px 5px;">{r['num_zonas_encontradas']:,}</td>
    </tr>
    <tr style="background:#f5f5f5;">
      <td style="padding: 3px 5px;"><b>📏 Zona más cercana</b></td>
      <td style="padding: 3px 5px;">{dist_str}</td>
    </tr>
    <tr>
      <td style="padding: 3px 5px;"><b>📊 Densidad esfuerzo</b></td>
      <td style="padding: 3px 5px;">{r['densidad_esfuerzo_pesquero']:.3f}</td>
    </tr>
    <tr style="background:#f5f5f5;">
      <td style="padding: 3px 5px;"><b>🐟 Especies críticas</b></td>
      <td style="padding: 3px 5px;">{r['especies_criticas_score']:.2f}</td>
    </tr>
  </table>

  <p style="font-size: 10px; color: #777; margin-top: 8px; border-top: 1px solid #eee; padding-top: 4px;">
    Fuente: Fish_Zones_PANGAS (Moreno-Báez et al. 2011, 2012)
  </p>
</div>
"""


def build_map():
    """Construye el mapa Folium interactivo."""
    base_dir = Path('/home/gorops/ierc-gnl-project')
    pangas_dir = base_dir / 'data/raw/pangas_wgs84'
    output_dir = base_dir / 'output'
    output_dir.mkdir(exist_ok=True)

    # Centro del mapa: Alto Golfo de California
    m = folium.Map(
        location=[29.5, -113.0],
        zoom_start=7,
        tiles=None,
        control_scale=True,
    )

    # Capas base
    folium.TileLayer(
        tiles='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        name='🗺️ Mapa Oscuro (CARTO Dark)',
        max_zoom=19,
        subdomains='abcd',
    ).add_to(m)

    folium.TileLayer(
        tiles='OpenStreetMap',
        name='🗺️ OpenStreetMap',
    ).add_to(m)

    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
        name='🛰️ Satélite (ESRI)',
    ).add_to(m)

    # ============================================================
    # CAPA 1: Zonas pesqueras PANGAS (ZPesca_PANGAS)
    # ============================================================
    pangas_layer = folium.FeatureGroup(name='🎣 Zonas Pesqueras PANGAS (4,241 zonas)', show=True)

    pangas_file = pangas_dir / 'ZPesca_PANGAS_wgs84.geojson'
    if pangas_file.exists():
        with open(pangas_file, 'r') as f:
            pangas_data = json.load(f)

        # Muestrear para no saturar el mapa (tomar 1 de cada 3 features)
        sampled = pangas_data['features'][::3]
        print(f"  Añadiendo {len(sampled)} zonas PANGAS (muestra 1:3)...")

        for feat in sampled:
            try:
                habitat = feat['properties'].get('HABITAT', 'N/A')
                sitio = feat['properties'].get('sitio_nomb', 'N/A')
                spp = feat['properties'].get('spp_code', 'N/A')
                folium.GeoJson(
                    feat,
                    style_function=lambda x: {
                        'fillColor': '#1976D2',
                        'color': '#0D47A1',
                        'weight': 0.5,
                        'fillOpacity': 0.25,
                    },
                    tooltip=folium.Tooltip(
                        f"<b>Sitio:</b> {sitio}<br><b>Hábitat:</b> {habitat}<br><b>Especie:</b> {spp}",
                        sticky=True
                    )
                ).add_to(pangas_layer)
            except Exception:
                continue
    pangas_layer.add_to(m)

    # ============================================================
    # CAPA 2: Riqueza Relativa de Especies
    # ============================================================
    riqueza_layer = folium.FeatureGroup(name='🐟 Riqueza Relativa de Especies (11,065 celdas)', show=False)

    riqueza_file = pangas_dir / 'Riqueza_Relativa_wgs84.geojson'
    if riqueza_file.exists():
        with open(riqueza_file, 'r') as f:
            riqueza_data = json.load(f)

        # Muestra 1:20 para rendimiento del mapa
        sampled_r = riqueza_data['features'][::20]
        print(f"  Añadiendo {len(sampled_r)} celdas de riqueza (muestra 1:20)...")

        for feat in sampled_r:
            try:
                all_val = feat['properties'].get('all', 0) or 0
                # Color basado en riqueza: azul claro → verde oscuro
                opacity = min(0.7, float(all_val) * 0.3 + 0.1)
                folium.GeoJson(
                    feat,
                    style_function=lambda x, v=all_val: {
                        'fillColor': '#2e7d32' if v > 5 else '#66bb6a' if v > 2 else '#a5d6a7',
                        'color': '#1b5e20',
                        'weight': 0.3,
                        'fillOpacity': 0.35,
                    },
                    tooltip=folium.Tooltip(
                        f"<b>Riqueza total:</b> {all_val:.1f}",
                        sticky=True
                    )
                ).add_to(riqueza_layer)
            except Exception:
                continue
    riqueza_layer.add_to(m)

    # ============================================================
    # CAPA 3: Zonas de Buceo
    # ============================================================
    buceo_layer = folium.FeatureGroup(name='🤿 Zonas de Buceo (249 zonas)', show=False)
    buceo_file = pangas_dir / 'ZPesca_Buceo_wgs84.geojson'
    if buceo_file.exists():
        folium.GeoJson(
            str(buceo_file),
            name='Buceo',
            style_function=lambda x: {
                'fillColor': '#00acc1',
                'color': '#006064',
                'weight': 1,
                'fillOpacity': 0.4,
            },
            tooltip=folium.GeoJsonTooltip(
                fields=['comunidad', 'HABITAT'] if True else [],
                aliases=['Comunidad', 'Hábitat'],
            )
        ).add_to(buceo_layer)
    buceo_layer.add_to(m)

    # ============================================================
    # CAPA 4: Proyectos GNL (marcadores principales)
    # ============================================================
    gnl_layer = folium.FeatureGroup(name='🏭 Proyectos GNL (5 proyectos)', show=True)

    for r in RESULTS:
        color = risk_color(r['riesgo_pesquero'])

        # Círculo de radio de búsqueda (referencia visual)
        if r['riesgo_pesquero'] > 0:
            folium.Circle(
                location=[r['latitud'], r['longitud']],
                radius=50000,  # 50 km en metros
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.05,
                weight=1,
                dash_array='5',
                tooltip=f"Radio de análisis: 50 km",
            ).add_to(gnl_layer)

        # Marcador principal
        folium.Marker(
            location=[r['latitud'], r['longitud']],
            popup=folium.Popup(build_popup(r), max_width=300),
            tooltip=folium.Tooltip(
                f"<b>{r['proyecto_id'].replace('_', ' ')}</b><br>"
                f"Riesgo: {r['riesgo_pesquero']:.1f}/100 ({r['nivel_riesgo']})",
                sticky=False,
            ),
            icon=folium.Icon(
                color='red' if r['riesgo_pesquero'] >= 70 else 'orange' if r['riesgo_pesquero'] >= 40 else 'gray',
                icon=risk_icon(r['riesgo_pesquero']),
                prefix='fa',
            )
        ).add_to(gnl_layer)

        # Etiqueta de nombre y riesgo
        folium.Marker(
            location=[r['latitud'] + 0.08, r['longitud']],
            icon=folium.DivIcon(
                html=f"""<div style="
                    font-family: 'Segoe UI', sans-serif;
                    font-size: 10px;
                    font-weight: bold;
                    color: {color};
                    text-shadow: 1px 1px 2px black;
                    white-space: nowrap;
                    pointer-events: none;
                ">{r['proyecto_id'].replace('_', '<br>').replace('GNL', '').strip()}<br>
                {'⚠️' if r['riesgo_pesquero'] >= 70 else '!'} {r['riesgo_pesquero']:.0f}/100</div>""",
                icon_size=(120, 40),
                icon_anchor=(0, 0)
            )
        ).add_to(gnl_layer)

    gnl_layer.add_to(m)

    # ============================================================
    # LEYENDA HTML
    # ============================================================
    legend_html = """
    <div style="
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 1000;
        background: rgba(20, 20, 30, 0.92);
        color: white;
        padding: 14px 18px;
        border-radius: 10px;
        font-family: 'Segoe UI', sans-serif;
        font-size: 12px;
        border: 1px solid rgba(255,255,255,0.15);
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        min-width: 200px;
    ">
        <div style="font-size: 14px; font-weight: bold; margin-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.2); padding-bottom: 6px;">
            🎣 Riesgo Pesquero GNL
        </div>
        <div style="margin: 5px 0;">
            <span style="background: #d32f2f; padding: 2px 10px; border-radius: 3px; margin-right: 6px;">●</span> Alto ≥ 70
        </div>
        <div style="margin: 5px 0;">
            <span style="background: #f57c00; padding: 2px 10px; border-radius: 3px; margin-right: 6px;">●</span> Moderado 40-69
        </div>
        <div style="margin: 5px 0;">
            <span style="background: #388e3c; padding: 2px 10px; border-radius: 3px; margin-right: 6px;">●</span> Bajo < 40
        </div>
        <div style="margin: 5px 0;">
            <span style="background: #78909c; padding: 2px 10px; border-radius: 3px; margin-right: 6px;">●</span> Sin datos
        </div>
        <div style="margin-top: 10px; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 6px;">
            <div style="margin: 3px 0;"><span style="color: #1976D2;">■</span> Zonas PANGAS</div>
            <div style="margin: 3px 0;"><span style="color: #2e7d32;">■</span> Riqueza de especies</div>
            <div style="margin: 3px 0;"><span style="color: #00acc1;">■</span> Buceo</div>
        </div>
        <div style="margin-top: 8px; font-size: 9px; color: rgba(255,255,255,0.5);">
            Moreno-Báez et al. (2011, 2012)<br>
            Fish_Zones_PANGAS GDB · EPSG:4326
        </div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    # ============================================================
    # TÍTULO
    # ============================================================
    title_html = """
    <div style="
        position: fixed;
        top: 15px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1000;
        background: rgba(20, 20, 30, 0.90);
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        font-family: 'Segoe UI', sans-serif;
        font-size: 15px;
        font-weight: bold;
        border: 1px solid rgba(255,255,255,0.15);
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        text-align: center;
        pointer-events: none;
    ">
        🌊 IERC-GNL · Riesgo Pesquero — Alto Golfo de California
        <div style="font-size: 10px; font-weight: normal; color: rgba(255,255,255,0.6); margin-top: 2px;">
            Índice Espacial de Riesgo Socioeconómico · Moreno-Báez et al. (2011, 2012)
        </div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(title_html))

    # Control de capas
    folium.LayerControl(
        collapsed=False,
        position='topright',
    ).add_to(m)

    # Mini mapa
    plugins.MiniMap(toggle_display=True, position='bottomleft').add_to(m)

    # Guardar
    output_path = output_dir / 'dashboard_riesgo_pesquero.html'
    m.save(str(output_path))
    print(f"\n✅ Dashboard guardado: {output_path}")
    return str(output_path)


if __name__ == '__main__':
    print("Generando dashboard Folium — IERC-GNL...")
    path = build_map()
    print(f"\nAbre en tu navegador:")
    print(f"  file://{path}")
