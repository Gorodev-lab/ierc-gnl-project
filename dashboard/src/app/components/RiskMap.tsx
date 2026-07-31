'use client'

import React, { useEffect, useState } from 'react'
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
  { id: 'sener_gasoductos', name: 'SENER/CNIH Red Gasoductos (WMS)', file: '', color: '#FFB000' },
  { id: 'proyectos_gnl',    name: '11 Proyectos GNL Consolidados',    file: '/data/proyectos_gnl.geojson', color: '#EF4444' },
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
  if (depth >= -20) return { color: '#7DD3FC', weight: 0.9, opacity: 0.8 } // Somero nerítico
  if (depth >= -100) return { color: '#38BDF8', weight: 0.8, opacity: 0.7 } // Plataforma
  if (depth >= -500) return { color: '#0284C7', weight: 0.7, opacity: 0.6 } // Borde plataforma / talud
  if (depth >= -2000) return { color: '#0369A1', weight: 0.6, opacity: 0.5 } // Batiatlántica
  return { color: '#1E3A8A', weight: 0.5, opacity: 0.4 } // Profunda (-5000m)
}

export default function RiskMap() {
  const [layersData, setLayersData]     = useState<Record<string, any>>({})
  const [activeLayers, setActiveLayers] = useState<Record<string, boolean>>({
    sener_gasoductos: true,
    proyectos_gnl: true,
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

  useEffect(() => {
    // Cargar capas GeoJSON pesqueras, GNL y batimetría
    LAYER_CONFIGS.forEach(cfg => {
      if (cfg.file) {
        fetch(cfg.file)
          .then(r => r.json())
          .then(geoJson => {
            setLayersData(prev => ({ ...prev, [cfg.id]: geoJson }))
          })
          .catch(() => console.log(`Notice: Layer file ${cfg.file} notice.`))
      }
    })

    // Setup Leaflet
    import('leaflet').then(L => {
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

  return (
    <div className="section">
      <div className="section-title" style={{ justifyContent: 'space-between' }}>
        <span>VISOR ESPACIAL IERC — ACTIVIDAD PESQUERA & INFRAESTRUCTURA GNL</span>
        <span style={{ fontSize: '0.75rem', color: 'var(--color-ok)', fontFamily: 'var(--font-mono)' }}>
          ● ENTREGABLE GEOPACKAGE V1.1 CONECTADO
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
          <h4 style={{
            fontSize: '0.8125rem',
            color: 'var(--color-amber)',
            borderBottom: '1px solid var(--color-border-hi)',
            paddingBottom: '0.5rem',
            marginBottom: '1rem',
            letterSpacing: '0.05em',
          }}>
            CAPAS VECTORIALES IERC (QGIS)
          </h4>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
            {LAYER_CONFIGS.map(cfg => (
              <label key={cfg.id} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.75rem', cursor: 'pointer', color: 'var(--color-text-primary)' }}>
                <input type="checkbox" checked={!!activeLayers[cfg.id]} onChange={() => toggleLayer(cfg.id)} style={{ accentColor: cfg.color }} />
                <span style={{ display: 'inline-block', width: 10, height: 10, background: cfg.color, border: '1px solid #000', flexShrink: 0 }} />
                <span>{cfg.name}</span>
              </label>
            ))}
          </div>

          <div style={{ marginTop: '1.5rem', borderTop: '1px solid var(--color-border)', paddingTop: '1rem', fontSize: '0.6875rem', color: 'var(--color-text-muted)' }}>
            <strong>GRADIENTE BATIMÉTRICO (GEBCO):</strong>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem', marginTop: '0.4rem' }}>
              <span style={{ color: '#7DD3FC' }}>― -10m a -20m (Zona Somera/Nerítica)</span>
              <span style={{ color: '#38BDF8' }}>― -50m a -100m (Plataforma Continental)</span>
              <span style={{ color: '#0284C7' }}>― -200m a -500m (Talud Superior)</span>
              <span style={{ color: '#0369A1' }}>― -1000m a -2000m (Batiatlántica)</span>
              <span style={{ color: '#1E3A8A' }}>― -5000m (Fosa Profunda)</span>
            </div>
          </div>
        </div>

        {/* Map Container */}
        <div>
          <div className="map-wrapper" style={{ height: '620px' }}>
            {loaded ? (
              <MapContainer
                center={[28.5, -111.8]}
                zoom={6}
                style={{ height: '100%', width: '100%' }}
                attributionControl={true}
              >
                <TileLayer
                  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> | CartoDB'
                  url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                  subdomains="abcd"
                  maxZoom={19}
                />

                {/* SENER / CNIH Official Gas Pipeline WMS Tile Layer */}
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

                {/* Layer Batimetría GEBCO 2024 (Solo contornos marinos < 0m) */}
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

                {/* Layers Pesqueras PANGAS (Simbología QGIS Original) */}
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

                {/* Layer 11 Proyectos GNL Consolidados */}
                {activeLayers.proyectos_gnl && layersData.proyectos_gnl && (
                  <GeoJSON
                    key="proyectos_gnl"
                    data={layersData.proyectos_gnl}
                    pointToLayer={(feat, latlng) => {
                      return new (window as any).L.CircleMarker(latlng, {
                        radius: 9,
                        fillColor: '#EF4444',
                        fillOpacity: 0.95,
                        color: '#FFFFFF',
                        weight: 2
                      })
                    }}
                    onEachFeature={(feat, layer) => {
                      const p = feat.properties || {}
                      layer.bindPopup(
                        `<div style="font-family: monospace; font-size: 0.75rem; min-width: 230px;">
                          <b style="color: #EF4444; font-size: 0.8125rem;">${p.nombre_proyecto}</b><br/>
                          <b>ESTADO:</b> ${p.estado}<br/>
                          <b>TIPO:</b> ${p.tipo_infraestructura}<br/>
                          <b>EMPRESA:</b> ${p.empresa_promovente}<br/>
                          <b>ESTATUS:</b> ${p.estatus_permiso}<br/>
                          <b>FUENTE:</b> <span style="color: #F59E0B;">${p.fuente_oficial}</span>
                        </div>`
                      )
                    }}
                  />
                )}

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
                CARGANDO VISOR ESPACIAL COMPLETO (PANGAS & BATIMETRÍA GEBCO)…
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
            FUENTE: ierc_golfo_california.gpkg (11 Proyectos GNL + 7 Capas PANGAS + Batimetría GEBCO 2024)
          </p>
        </div>
      </div>
    </div>
  )
}
