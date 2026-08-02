'use client'

import React, { useEffect, useState, useRef } from 'react'
import dynamic from 'next/dynamic'

const MapContainer   = dynamic(() => import('react-leaflet').then(m => m.MapContainer),   { ssr: false })
const TileLayer      = dynamic(() => import('react-leaflet').then(m => m.TileLayer),      { ssr: false })
const CircleMarker   = dynamic(() => import('react-leaflet').then(m => m.CircleMarker),   { ssr: false })
const Popup          = dynamic(() => import('react-leaflet').then(m => m.Popup),          { ssr: false })
const GeoJSON        = dynamic(() => import('react-leaflet').then(m => m.GeoJSON),        { ssr: false })
const WMSTileLayer   = dynamic(() => import('react-leaflet').then(m => m.WMSTileLayer),   { ssr: false })

interface LayerConfig {
  id: string
  name: string
  file: string
  color: string
}

const LAYER_CONFIGS: LayerConfig[] = [
  { id: 'proyectos_gnl',    name: '4 Terminales GNL (13 Features Vectoriales)', file: '/data/proyectos_gnl.geojson', color: '#EF4444' },
  { id: 'capas_contexto',   name: 'Gasoductos, Sitios Ramsar & ANPs',  file: '/data/capas_contextuales.geojson', color: '#FF9800' },
  { id: 'sener_gasoductos', name: 'SENER/CNIH Red Gasoductos (WMS)', file: '', color: '#FFB000' },
  { id: 'batimetria',       name: 'Contornos Batimétricos GEBCO 2024',file: '/data/batimetria_golfo.geojson', color: '#38BDF8' },
  { id: 'h3_riesgo',        name: 'Malla H3 IERC (Res 8/9)',          file: '/data/grilla_h3_riesgo.geojson', color: '#F59E0B' },
  { id: 'pangas',           name: 'PANGAS Multiespecie (4,241)',      file: '/data/zpesca_pangas_sample.geojson', color: '#8D6E63' },
  { id: 'buceo',            name: 'Pesca por Buceo (249)',            file: '/data/zpesca_buceo_sample.geojson', color: '#E91E63' },
  { id: 'chinchorro',       name: 'Chinchorro de Línea (2,209)',      file: '/data/zpesca_chinchorro_sample.geojson', color: '#C0392B' },
  { id: 'redes',            name: 'Redes de Enmalle (1,263)',        file: '/data/zpesca_redes_sample.geojson', color: '#27AE60' },
  { id: 'manta',            name: 'Camarón / Manta (783)',           file: '/data/zpesca_redes_manta_camaron_sample.geojson', color: '#D35400' },
  { id: 'trampa',           name: 'Trampas Jaiberas (360)',          file: '/data/zpesca_trampa_sample.geojson', color: '#8E44AD' },
  { id: 'riqueza',          name: 'Riqueza Relativa Pesquera (11,065)', file: '/data/riqueza_relativa_sample.geojson', color: '#2C3E50' }
]

function getRiskColor(score: number): string {
  if (score >= 75.0) return '#EF4444'
  if (score >= 50.0) return '#F59E0B'
  return '#10B981'
}

function getBathymetryColor(depth: number): { color: string; weight: number; opacity: number } {
  if (depth >= -20) return { color: '#7DD3FC', weight: 0.9, opacity: 0.8 }
  if (depth >= -100) return { color: '#38BDF8', weight: 0.8, opacity: 0.7 }
  if (depth >= -500) return { color: '#0284C7', weight: 0.7, opacity: 0.6 }
  if (depth >= -2000) return { color: '#0369A1', weight: 0.6, opacity: 0.5 }
  return { color: '#1E3A8A', weight: 0.5, opacity: 0.4 }
}

export default function RiskMap() {
  const [layersData, setLayersData]     = useState<Record<string, any>>({})
  const [activeLayers, setActiveLayers] = useState<Record<string, boolean>>({
    proyectos_gnl: true,
    capas_contexto: true,
    sener_gasoductos: false,
    batimetria: true,
    h3_riesgo: false,
    pangas: true,
    buceo: false,
    chinchorro: false,
    redes: false,
    manta: false,
    trampa: false,
    riqueza: true,
  })

  const [loaded, setLoaded] = useState(false)
  const mapRef = useRef<any>(null)

  useEffect(() => {
    LAYER_CONFIGS.forEach(cfg => {
      if (cfg.file) {
        fetch(cfg.file)
          .then(r => r.json())
          .then(geoJson => {
            setLayersData(prev => ({ ...prev, [cfg.id]: geoJson }))
          })
          .catch(err => console.error(`Error loading layer ${cfg.file}:`, err))
      }
    })

    import('leaflet').then(L => {
      (window as any).L = L
      delete (L.Icon.Default.prototype as any)._getIconUrl
      L.Icon.Default.mergeOptions({
        iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
        iconUrl:       'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
        shadowUrl:     'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
      })
      setLoaded(true)
    })
  }, [])

  const toggleLayer = (id: string) => {
    setActiveLayers(prev => ({ ...prev, [id]: !prev[id] }))
  }

  const focusProyectos = () => {
    if (mapRef.current) {
      // Ajustar la vista al polígono completo del Golfo de California y proyectos
      mapRef.current.setView([25.8, -109.0], 6)
    }
  }

  const proyectosFeatures = layersData.proyectos_gnl?.features || []

  return (
    <div className="section">
      <div className="section-title" style={{ justifyContent: 'space-between' }}>
        <span>VISOR ESPACIAL IERC — 4 TERMINALES GNL & CONTEXTO SOCIOAMBIENTAL</span>
        <span style={{ fontSize: '0.75rem', color: 'var(--color-ok)', fontFamily: 'var(--font-mono)' }}>
          ● ENTREGABLE GEOPACKAGE V2 CONECTADO (13 FEATURES)
        </span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '340px 1fr', gap: '1.25rem', alignItems: 'start' }}>
        
        {/* Layer Control Sidebar */}
        <div style={{
          background: 'var(--color-surface)',
          border: '1px solid var(--color-border-hi)',
          padding: '1.25rem',
          fontFamily: 'var(--font-mono)',
          maxHeight: '620px',
          overflowY: 'auto'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h4 style={{
              fontSize: '0.8125rem',
              color: 'var(--color-amber)',
              margin: 0,
              letterSpacing: '0.05em',
            }}>
              CAPAS VECTORIALES IERC
            </h4>

            <button
              onClick={focusProyectos}
              style={{
                background: 'var(--color-surface-2)',
                border: '1px solid var(--color-amber)',
                color: 'var(--color-amber)',
                fontSize: '0.6875rem',
                padding: '0.25rem 0.5rem',
                borderRadius: 4,
                cursor: 'pointer',
                fontWeight: 'bold'
              }}
              title="Centrar mapa en las 4 terminales GNL"
            >
              🎯 CENTRAR GNL
            </button>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
            {LAYER_CONFIGS.map(cfg => (
              <label key={cfg.id} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.75rem', cursor: 'pointer', color: 'var(--color-text-primary)' }}>
                <input type="checkbox" checked={!!activeLayers[cfg.id]} onChange={() => toggleLayer(cfg.id)} style={{ accentColor: cfg.color }} />
                <span style={{ display: 'inline-block', width: 10, height: 10, background: cfg.color, border: '1px solid #000', flexShrink: 0 }} />
                <span>{cfg.name}</span>
              </label>
            ))}
          </div>

          <div style={{ marginTop: '1.25rem', borderTop: '1px solid var(--color-border)', paddingTop: '0.85rem', fontSize: '0.6875rem' }}>
            <strong style={{ color: 'var(--color-amber)' }}>ESTATUS PROYECTOS GNL:</strong>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem', marginTop: '0.4rem', color: 'var(--color-text-muted)' }}>
              <span style={{ color: '#EF4444' }}>■ Propuesto / Pre-FID (Saguaro, Amigo)</span>
              <span style={{ color: '#00ACC1' }}>■ En Evaluación ASEA (GNL Cosalá)</span>
              <span style={{ color: '#78909C' }}>■ CANCELADO (Vista Pacífico FLNG Feb 2026)</span>
            </div>
          </div>

          <div style={{ marginTop: '1rem', borderTop: '1px solid var(--color-border)', paddingTop: '0.85rem', fontSize: '0.6875rem', color: 'var(--color-text-muted)' }}>
            <strong>BATIMETRÍA GEBCO:</strong>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem', marginTop: '0.4rem' }}>
              <span style={{ color: '#7DD3FC' }}>― -10m a -20m (Somera/Nerítica)</span>
              <span style={{ color: '#38BDF8' }}>― -50m a -100m (Plataforma)</span>
              <span style={{ color: '#0284C7' }}>― -200m a -500m (Talud)</span>
              <span style={{ color: '#0369A1' }}>― -1000m a -2000m (Batiatlántica)</span>
            </div>
          </div>
        </div>

        {/* Map Container */}
        <div>
          <div className="map-wrapper" style={{ height: '620px' }}>
            {loaded ? (
              <MapContainer
                center={[25.8, -109.0]}
                zoom={6}
                ref={mapRef}
                style={{ height: '100%', width: '100%' }}
                attributionControl={true}
              >
                <TileLayer
                  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> | CartoDB'
                  url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                  subdomains="abcd"
                  maxZoom={19}
                />

                {/* SENER / CNIH WMS Tile Layer */}
                {activeLayers.sener_gasoductos && (
                  <WMSTileLayer
                    url="https://mapa-hidrocarburos.energia.gob.mx/mapserver/mapserv.exe?map=C:/inetpub/wwwroot/iicnihmap/ms/wms/prod/es_mx/grp_gas.map"
                    layers="ifr_gas_dts_nointegrados,ifr_gas_dts_integrados,ifr_ductos_imp,ift_gas_pts_internacion"
                    format="image/png"
                    transparent={true}
                    version="1.3.0"
                    attribution="&copy; SENER / CNIH SIG Hidrocarburos"
                  />
                )}

                {/* Layer Capas Contextuales (Gasoductos, Sitios Ramsar, ANPs) */}
                {activeLayers.capas_contexto && layersData.capas_contexto && (
                  <GeoJSON
                    key="capas_contexto"
                    data={layersData.capas_contexto}
                    style={(feat) => {
                      const p = feat?.properties || {}
                      return {
                        color: p.color || '#FF9800',
                        fillColor: p.fill_color || p.color || '#FF9800',
                        fillOpacity: p.fill_opacity ?? 0.2,
                        weight: p.line_weight || 2,
                        dashArray: p.dash_array || '0'
                      }
                    }}
                    onEachFeature={(feat, layer) => {
                      const p = feat.properties || {}
                      layer.bindPopup(
                        `<div style="font-family: monospace; font-size: 0.75rem; min-width: 240px;">
                          <b style="color: ${p.color || '#FF9800'}; font-size: 0.8125rem;">${p.nombre}</b><br/>
                          <b>TIPO:</b> ${p.tipo_capa}<br/>
                          <b>ESTATUS:</b> ${p.estatus}<br/>
                          <div style="margin-top: 6px; font-size: 0.6875rem; color: #CCCCCC; border-top: 1px dashed #444; padding-top: 4px;">
                            ${p.descripcion}
                          </div>
                        </div>`
                      )
                    }}
                  />
                )}

                {/* Layer Batimetría GEBCO 2024 */}
                {activeLayers.batimetria && layersData.batimetria && (
                  <GeoJSON
                    key="batimetria"
                    data={layersData.batimetria}
                    style={(feat) => {
                      const depth = feat?.properties?.profundidad_m || -100
                      const style = getBathymetryColor(depth)
                      return {
                        color: style.color,
                        weight: style.weight,
                        opacity: style.opacity
                      }
                    }}
                    onEachFeature={(feat, layer) => {
                      const p = feat.properties || {}
                      layer.bindPopup(
                        `<div style="font-family: monospace; font-size: 0.75rem;">
                          <b style="color: #38BDF8;">BATIMETRÍA MARÍTIMA GEBCO</b><br/>
                          <b>PROFUNDIDAD:</b> ${p.profundidad_m} m<br/>
                          <b>CLASE:</b> ${p.clase_profundidad}<br/>
                          <b>FUENTE:</b> ${p.fuente || 'GEBCO 2024 / ETOPO1'}
                        </div>`
                      )
                    }}
                  />
                )}

                {/* Layers Pesqueras PANGAS */}
                {['pangas', 'buceo', 'chinchorro', 'redes', 'manta', 'trampa', 'riqueza'].map(id => {
                  const cfg = LAYER_CONFIGS.find(c => c.id === id)
                  if (!cfg || !activeLayers[id] || !layersData[id]) return null

                  return (
                    <GeoJSON
                      key={id}
                      data={layersData[id]}
                      style={{
                        fillColor: cfg.color,
                        fillOpacity: id === 'riqueza' ? 0.25 : 0.45,
                        color: '#000000',
                        weight: id === 'riqueza' ? 0.3 : 0.8,
                        opacity: 0.8,
                      }}
                      onEachFeature={(feature, layer) => {
                        const p = feature.properties ?? {}
                        const imgPath = p.layer_imagen || `/atlas_pangas_jpg/mapa_${id}.jpg`

                        layer.bindPopup(
                          `<div style="min-width: 280px; max-width: 320px; font-family: 'IBM Plex Mono', monospace;">
                            <div style="font-weight: 700; font-size: 0.8125rem; color: #FFFFFF; border-bottom: 1px solid #333; padding-bottom: 4px; margin-bottom: 8px;">
                              ${p.layer_titulo || cfg.name}
                            </div>
                            <img src="${imgPath}" alt="Mapa Atlas" style="width: 100%; height: 120px; object-fit: cover; border: 1px solid #333; margin-bottom: 8px;" />
                            <div style="font-size: 0.75rem; color: #AAAAAA; margin-bottom: 6px;">
                              <b>SITIO:</b> ${p.sitio || p.sitio_nomb || 'No especificado'}<br/>
                              <b>ARTES:</b> ${p.layer_artes || cfg.name}<br/>
                              <b>HÁBITAT:</b> ${p.habitat || 'No especificado'}<br/>
                              <b>CÓDIGO SPP:</b> <span style="color: #FFB000;">${p.spp_code || 'MULTIESPECIE'}</span>
                            </div>
                            <div style="font-size: 0.6875rem; color: #666666; border-top: 1px dashed #333; padding-top: 6px;">
                              FUENTE: Atlas PANGAS (Moreno-Báez et al.) / GeoPackage v1.1
                            </div>
                          </div>`,
                          { maxWidth: 340 }
                        )
                      }}
                    />
                  )
                })}

                {/* Layer Malla H3 IERC */}
                {activeLayers.h3_riesgo && layersData.h3_riesgo && (
                  <GeoJSON
                    key="h3_riesgo"
                    data={layersData.h3_riesgo}
                    style={(feat) => {
                      const score = feat?.properties?.ierc_score || 50
                      return {
                        fillColor: getRiskColor(score),
                        fillOpacity: 0.35,
                        color: getRiskColor(score),
                        weight: 0.5,
                        opacity: 0.8
                      }
                    }}
                    onEachFeature={(feat, layer) => {
                      const p = feat.properties || {}
                      layer.bindPopup(
                        `<div style="font-family: monospace; font-size: 0.75rem;">
                          <b>CELDA H3:</b> ${p.h3_index}<br/>
                          <b>SCORE IERC:</b> <strong style="color: ${getRiskColor(p.ierc_score)}">${p.ierc_score}</strong> (${p.nivel_riesgo})<br/>
                          <b>AMENAZA:</b> ${p.amenaza_score}<br/>
                          <b>EXPOSICIÓN:</b> ${p.exposicion_score}<br/>
                          <b>DIST. PROYECTO MÁS CERCANO:</b> ${p.distancia_proyecto_mas_cercano_km} km
                        </div>`
                      )
                    }}
                  />
                )}

                {/* Layer 4 Terminales GNL Consolidados (13 Features Vectoriales Polígonos) */}
                {activeLayers.proyectos_gnl && layersData.proyectos_gnl && (
                  <GeoJSON
                    key="proyectos_gnl_polys"
                    data={layersData.proyectos_gnl}
                    style={(feat) => {
                      const p = feat?.properties || {}
                      const isCancel = p.status_code === 'cancelado'
                      const isEval = p.status_code === 'en_evaluacion'
                      
                      return {
                        fillColor: isCancel ? '#78909C' : (isEval ? '#00ACC1' : '#EF4444'),
                        fillOpacity: isCancel ? 0.35 : 0.65,
                        color: isCancel ? '#455A64' : (isEval ? '#006064' : '#B71C1C'),
                        weight: 2,
                        dashArray: isCancel ? '6, 4' : '0'
                      }
                    }}
                    pointToLayer={(feat, latlng) => {
                      const L_ref = (window as any).L
                      const p = feat?.properties || {}
                      const isCancel = p.status_code === 'cancelado'
                      const isEval = p.status_code === 'en_evaluacion'
                      const fillColor = isCancel ? '#78909C' : (isEval ? '#00ACC1' : '#EF4444')
                      
                      if (L_ref && L_ref.circleMarker) {
                        return L_ref.circleMarker(latlng, {
                          radius: 12,
                          fillColor: fillColor,
                          fillOpacity: 0.95,
                          color: '#FFFFFF',
                          weight: 2
                        })
                      }
                      return null as any
                    }}
                    onEachFeature={(feat, layer) => {
                      const p = feat.properties || {}
                      const isCancel = p.status_code === 'cancelado'
                      const badgeColor = isCancel ? '#78909C' : (p.status_code === 'en_evaluacion' ? '#00ACC1' : '#EF4444')
                      
                      layer.bindPopup(
                        `<div style="font-family: monospace; font-size: 0.75rem; min-width: 270px; max-width: 320px;">
                          <div style="font-size: 0.8125rem; font-weight: bold; color: ${badgeColor}; border-bottom: 1px solid #444; padding-bottom: 4px; margin-bottom: 6px;">
                            ${p.nombre_feature || p.id}
                          </div>
                          
                          <div style="margin-bottom: 6px;">
                            <span style="background: ${badgeColor}; color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.6875rem; font-weight: bold;">
                              ${p.estatus_permiso}
                            </span>
                          </div>

                          <b>GRUPO:</b> ${p.terminal_grupo}<br/>
                          <b>PROMOVENTE:</b> ${p.promovente}<br/>
                          <b>UBICACIÓN:</b> ${p.estado}, ${p.municipio}<br/>
                          <b>CAPACIDAD:</b> ${p.capacidad_mtpa ? p.capacidad_mtpa + ' MTPA' : 'N/A'}<br/>
                          <b>TIPO ÁREA:</b> ${p.tipo_area}<br/>
                          <b>PRECISIÓN GEOM:</b> ${p.precision_geom}<br/>

                          ${p.impacto_notes ? `<div style="margin-top:6px; padding:4px; background:#222; border-left:2px solid ${badgeColor}; font-size:0.6875rem; color:#DDD;">${p.impacto_notes}</div>` : ''}

                          <div style="font-size: 0.6875rem; color: #888888; border-top: 1px dashed #444; padding-top: 4px; margin-top: 6px;">
                            CLAVE ASEA / REF: ${p.clave_proyecto || 'N/A'}
                          </div>
                        </div>`
                      )
                    }}
                  />
                )}

                {/* CircleMarkers Destacados en Centroides para Alta Visibilidad a Cualquier Nivel de Zoom */}
                {activeLayers.proyectos_gnl && proyectosFeatures.map((feat: any) => {
                  const p = feat.properties || {}
                  const lat = p.latitud
                  const lon = p.longitud
                  if (!lat || !lon) return null
                  const isCancel = p.status_code === 'cancelado'
                  const isEval = p.status_code === 'en_evaluacion'
                  const badgeColor = isCancel ? '#78909C' : (isEval ? '#00ACC1' : '#EF4444')

                  return (
                    <CircleMarker
                      key={`marker_${p.id}`}
                      center={[lat, lon]}
                      radius={10}
                      pathOptions={{
                        fillColor: badgeColor,
                        fillOpacity: 0.95,
                        color: '#FFFFFF',
                        weight: 2
                      }}
                    >
                      <Popup>
                        <div style={{ fontFamily: 'monospace', fontSize: '0.75rem', minWidth: 260 }}>
                          <b style={{ color: badgeColor, fontSize: '0.8125rem' }}>{p.nombre_feature || p.id}</b>
                          <div style={{ margin: '4px 0' }}>
                            <span style={{ background: badgeColor, color: '#FFF', padding: '2px 6px', borderRadius: 4, fontSize: '0.6875rem', fontWeight: 'bold' }}>
                              {p.estatus_permiso}
                            </span>
                          </div>
                          <b>PROMOVENTE:</b> {p.promovente}<br/>
                          <b>CAPACIDAD:</b> {p.capacidad_mtpa ? `${p.capacidad_mtpa} MTPA` : 'N/A'}<br/>
                          <b>UBICACIÓN:</b> {p.estado}, {p.municipio}<br/>
                          {p.impacto_notes && (
                            <div style={{ marginTop: 6, padding: 4, background: '#222', borderLeft: `2px solid ${badgeColor}`, fontSize: '0.6875rem', color: '#DDD' }}>
                              {p.impacto_notes}
                            </div>
                          )}
                        </div>
                      </Popup>
                    </CircleMarker>
                  )
                })}

              </MapContainer>
            ) : (
              <div style={{
                height: '100%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                background: 'var(--color-surface)',
                color: 'var(--color-amber)',
                fontSize: '0.875rem',
                fontFamily: 'var(--font-mono)',
              }}>
                CARGANDO VISOR ESPACIAL (4 TERMINALES GNL & CAPAS CONTEXTUALES)…
              </div>
            )}
          </div>

          <p style={{
            marginTop: '0.75rem',
            fontSize: '0.6875rem',
            color: 'var(--color-text-muted)',
            textAlign: 'right',
            fontFamily: 'var(--font-mono)',
          }}>
            FUENTE: GeoPackage v2 (4 Terminales GNL / 13 Subconjuntos Vectoriales + Gasoductos + Sitios Ramsar / ANPs + PANGAS)
          </p>
        </div>
      </div>
    </div>
  )
}
