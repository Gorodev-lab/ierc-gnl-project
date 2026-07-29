'use client'

import React, { useEffect, useState } from 'react'
import dynamic from 'next/dynamic'

const MapContainer   = dynamic(() => import('react-leaflet').then(m => m.MapContainer),   { ssr: false })
const TileLayer      = dynamic(() => import('react-leaflet').then(m => m.TileLayer),      { ssr: false })
const CircleMarker   = dynamic(() => import('react-leaflet').then(m => m.CircleMarker),   { ssr: false })
const Popup          = dynamic(() => import('react-leaflet').then(m => m.Popup),          { ssr: false })
const GeoJSON        = dynamic(() => import('react-leaflet').then(m => m.GeoJSON),        { ssr: false })
const WMSTileLayer   = dynamic(() => import('react-leaflet').then(m => m.WMSTileLayer),   { ssr: false })

interface Project {
  proyecto_id: string
  proyecto_nombre: string
  latitud: number
  longitud: number
  estado: string
  estatus: string
  riesgo_pesquero: number
  nivel_riesgo: string
  num_zonas_encontradas: number
  zona_mas_cercana_km: number | null
  artes_de_pesca: string[]
  nota: string
}

interface RiskData {
  fecha_calculo: string
  proyectos: Project[]
}

const LAYER_CONFIGS = [
  { id: 'sener_gasoductos', name: 'SENER/CNIH Red Gasoductos (WMS)', file: '', color: '#FFB000' },
  { id: 'pangas',    name: 'PANGAS Multiespecie (4,241)', file: '/data/zpesca_pangas_sample.geojson', color: '#8D6E63' },
  { id: 'buceo',     name: 'Pesca por Buceo (249)',       file: '/data/zpesca_buceo_sample.geojson',  color: '#E91E63' },
  { id: 'chinchorro',name: 'Chinchorro de Línea (2,209)',  file: '/data/zpesca_chinchorro_sample.geojson', color: '#C0392B' },
  { id: 'redes',     name: 'Redes de Enmalle (1,263)',    file: '/data/zpesca_redes_sample.geojson',      color: '#27AE60' },
  { id: 'manta',     name: 'Camarón / Manta (783)',       file: '/data/zpesca_redes_manta_camaron_sample.geojson', color: '#D35400' },
  { id: 'trampa',    name: 'Trampas Jaiberas (360)',      file: '/data/zpesca_trampa_sample.geojson',     color: '#8E44AD' },
  { id: 'riqueza',   name: 'Riqueza Relativa (11,065)',   file: '/data/riqueza_relativa_sample.geojson',  color: '#2C3E50' }
]

function getRiskColor(nivel: string): string {
  if (nivel === 'Alto')     return '#C0392B'
  if (nivel === 'Moderado') return '#F39C12'
  if (nivel === 'Bajo')     return '#27AE60'
  return '#0EA5E9'
}

function getRiskRadius(score: number): number {
  return Math.max(10, Math.min(26, score / 4))
}

export default function RiskMap() {
  const [riskData, setRiskData]         = useState<RiskData | null>(null)
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [layersData, setLayersData]     = useState<Record<string, any>>({})
  const [activeLayers, setActiveLayers] = useState<Record<string, boolean>>({
    sener_gasoductos: true,
    pangas: true,
    buceo: false,
    chinchorro: false,
    redes: false,
    manta: false,
    trampa: false,
    riqueza: false,
    proyectos: true,
  })

  const [loaded, setLoaded]             = useState(false)
  const [gpkgConnected, setGpkgConnected] = useState(false)

  // Filters
  const [selectedQuincena, setSelectedQuincena] = useState<string>('TODAS')
  const [selectedArte, setSelectedArte]         = useState<string>('TODAS')

  useEffect(() => {
    // Check API GeoPackage
    fetch('/api/geopackage?layer=proyectos_gnl')
      .then(r => r.json())
      .then(res => {
        if (res.status === 'success' && res.features?.length > 0) setGpkgConnected(true)
      })
      .catch(() => setGpkgConnected(false))

    // Load projects risk JSON
    fetch('/data/riesgo_proyectos.json')
      .then(r => r.json())
      .then(setRiskData)
      .catch(console.error)

    // Load PANGAS GeoJSON layers
    LAYER_CONFIGS.forEach(cfg => {
      fetch(cfg.file)
        .then(r => r.json())
        .then(geoJson => {
          setLayersData(prev => ({ ...prev, [cfg.id]: geoJson }))
        })
        .catch(console.error)
    })

    // Setup Leaflet
    import('leaflet').then(L => {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      delete (L.Icon.Default.prototype as any)._getIconUrl
      L.Icon.Default.mergeOptions({
        iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
        iconUrl:       'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
        shadowUrl:     'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
      })
      setLoaded(true)
    })
  }, [])

  const projects = riskData?.proyectos ?? []

  const toggleLayer = (id: string) => {
    setActiveLayers(prev => ({ ...prev, [id]: !prev[id] }))
  }

  return (
    <div className="section">
      <div className="section-title" style={{ justifyContent: 'space-between' }}>
        <span>VISOR ESPACIAL IERC — SIMBOLOGÍA IDÉNTICA A QGIS</span>
        <span style={{ fontSize: '0.75rem', color: gpkgConnected ? 'var(--color-ok)' : 'var(--color-warn)' }}>
          {gpkgConnected ? '● GEOPACKAGE v2 (SQLITE) CONECTADO' : '○ MODO CACHE GEOJSON'}
        </span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '320px 1fr', gap: '1.25rem', alignItems: 'start' }}>
        
        {/* Layer Control Sidebar */}
        <div style={{
          background: 'var(--color-surface)',
          border: '1px solid var(--color-border-hi)',
          borderRadius: 0,
          padding: '1.25rem',
          fontFamily: 'var(--font-mono)',
        }}>
          <h4 style={{
            fontSize: '0.8125rem',
            color: 'var(--color-text-primary)',
            borderBottom: '1px solid var(--color-border-hi)',
            paddingBottom: '0.5rem',
            marginBottom: '1rem',
            letterSpacing: '0.05em',
          }}>
            capas vectoriales (100% qgis)
          </h4>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem', marginBottom: '1.5rem' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.75rem', cursor: 'pointer', color: 'var(--color-text-primary)' }}>
              <input type="checkbox" checked={activeLayers['proyectos']} onChange={() => toggleLayer('proyectos')} style={{ accentColor: 'var(--color-accent)' }} />
              Terminales GNL (5)
            </label>

            {LAYER_CONFIGS.map(cfg => (
              <label key={cfg.id} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.75rem', cursor: 'pointer', color: 'var(--color-text-primary)' }}>
                <input type="checkbox" checked={!!activeLayers[cfg.id]} onChange={() => toggleLayer(cfg.id)} style={{ accentColor: cfg.color }} />
                <span style={{ display: 'inline-block', width: 10, height: 10, background: cfg.color, border: '1px solid #000', borderRadius: 0 }} />
                {cfg.name}
              </label>
            ))}
          </div>

          <h4 style={{
            fontSize: '0.8125rem',
            color: 'var(--color-text-primary)',
            borderBottom: '1px solid var(--color-border-hi)',
            paddingBottom: '0.5rem',
            marginBottom: '1rem',
            letterSpacing: '0.05em',
          }}>
            filtros temporales & artes
          </h4>

          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', fontSize: '0.6875rem', color: 'var(--color-text-muted)', marginBottom: '0.35rem' }}>
              TEMPORADA QUINCENAL:
            </label>
            <select
              value={selectedQuincena}
              onChange={e => setSelectedQuincena(e.target.value)}
              style={{
                width: '100%',
                background: 'var(--color-surface-2)',
                color: 'var(--color-text-primary)',
                border: '1px solid var(--color-border-hi)',
                borderRadius: 0,
                padding: '0.4rem',
                fontSize: '0.75rem',
                fontFamily: 'var(--font-mono)',
              }}
            >
              <option value="TODAS">TODAS LAS QUINCENAS (ANUAL)</option>
              <option value="Q12">Q12 — JUNIO II (PICO CURVINA)</option>
              <option value="Q15">Q15 — AGOSTO II (PICO CAMARÓN)</option>
              <option value="Q18">Q18 — SEPTIEMBRE II (PICO JAIBA)</option>
            </select>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.6875rem', color: 'var(--color-text-muted)', marginBottom: '0.35rem' }}>
              ARTE DE PESCA:
            </label>
            <select
              value={selectedArte}
              onChange={e => setSelectedArte(e.target.value)}
              style={{
                width: '100%',
                background: 'var(--color-surface-2)',
                color: 'var(--color-text-primary)',
                border: '1px solid var(--color-border-hi)',
                borderRadius: 0,
                padding: '0.4rem',
                fontSize: '0.75rem',
                fontFamily: 'var(--font-mono)',
              }}
            >
              <option value="TODAS">TODAS LAS ARTES</option>
              <option value="CHINCHORRO">CHINCHORRO DE LÍNEA</option>
              <option value="BUCEO">BUCEO AUTÓNOMO / HOOKAH</option>
              <option value="REDES">REDES DE ENMALLE</option>
              <option value="TRAMPA">TRAMPAS JAIBERAS</option>
              <option value="SURPERA">SURPERA / MANTA CAMARÓN</option>
            </select>
          </div>
        </div>

        {/* Map Container */}
        <div>
          <div className="map-wrapper" style={{ height: '580px' }}>
            {loaded ? (
              <MapContainer
                center={[29.3, -112.8]}
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

                {/* Render PANGAS Atlas Layers with exact QGIS styling */}
                {LAYER_CONFIGS.map(cfg => {
                  if (!activeLayers[cfg.id] || !layersData[cfg.id]) return null

                  return (
                    <GeoJSON
                      key={cfg.id}
                      data={layersData[cfg.id]}
                      style={{
                        fillColor: cfg.color,
                        fillOpacity: cfg.id === 'riqueza' ? 0.25 : 0.45,
                        color: '#000000',
                        weight: cfg.id === 'riqueza' ? 0.3 : 0.8,
                        opacity: 0.8,
                      }}
                      onEachFeature={(feature, layer) => {
                        const p = feature.properties ?? {}
                        const imgPath = p.layer_imagen || `/atlas_pangas_jpg/mapa_${cfg.id}.jpg`

                        layer.bindPopup(
                          `<div style="min-width: 280px; max-width: 320px; font-family: 'IBM Plex Mono', monospace;">
                            <div style="font-weight: 700; font-size: 0.8125rem; color: #FFFFFF; border-bottom: 1px solid #333; padding-bottom: 4px; margin-bottom: 8px;">
                              ${p.layer_titulo || cfg.name}
                            </div>
                            <img src="${imgPath}" alt="Mapa Atlas" style="width: 100%; height: 120px; object-fit: cover; border: 1px solid #333; margin-bottom: 8px; border-radius: 0px;" />
                            <div style="font-size: 0.75rem; color: #AAAAAA; margin-bottom: 6px;">
                              <b>SITIO:</b> ${p.sitio}<br/>
                              <b>ARTES:</b> ${p.layer_artes || 'Multiespecie'}<br/>
                              <b>HÁBITAT:</b> ${p.habitat || 'No especificado'}<br/>
                              <b>CÓDIGO SPP:</b> <span style="color: #FFB000;">${p.spp_code || 'VARIOS'}</span>
                            </div>
                            <div style="font-size: 0.6875rem; color: #666666; border-top: 1px dashed #333; padding-top: 6px;">
                              FUENTE: Atlas PANGAS / ierc_golfo_california_v2.gpkg
                            </div>
                          </div>`,
                          { maxWidth: 340 }
                        )
                      }}
                    />
                  )
                })}

                {/* Project markers */}
                {activeLayers['proyectos'] && projects.map(p => {
                  const color  = getRiskColor(p.nivel_riesgo)
                  const radius = getRiskRadius(p.riesgo_pesquero)
                  return (
                    <CircleMarker
                      key={p.proyecto_id}
                      center={[p.latitud, p.longitud]}
                      radius={radius}
                      pathOptions={{
                        fillColor: color,
                        fillOpacity: 0.85,
                        color: '#FFF',
                        weight: 2,
                      }}
                    >
                      <Popup>
                        <div style={{ minWidth: 240, fontFamily: 'var(--font-mono)' }}>
                          <p style={{ fontWeight: 700, fontSize: '0.875rem', color: '#FFF', marginBottom: 4 }}>
                            {p.proyecto_nombre}
                          </p>
                          <p style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)', marginBottom: 8 }}>
                            {p.estado} · {p.estatus}
                          </p>
                          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                            <span style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>RIESGO PESQUERO</span>
                            <strong style={{ color }}>
                              {p.riesgo_pesquero > 0 ? `${p.riesgo_pesquero}/100` : 'Sin datos'}
                            </strong>
                          </div>
                          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                            <span style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>NIVEL</span>
                            <span style={{ color, fontWeight: 700, fontSize: '0.75rem' }}>{p.nivel_riesgo.toUpperCase()}</span>
                          </div>
                          {p.zona_mas_cercana_km !== null && (
                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                              <span style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>ZONA MÁS CERCANA</span>
                              <span style={{ fontSize: '0.75rem' }}>{p.zona_mas_cercana_km} km</span>
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
                color: 'var(--color-text-primary)',
                fontSize: '0.875rem',
                fontFamily: 'var(--font-mono)',
              }}>
                CARGANDO VISOR ESPACIAL SIMBOLOGÍA QGIS…
              </div>
            )}
          </div>

          {riskData && (
            <p style={{
              marginTop: '0.75rem',
              fontSize: '0.6875rem',
              color: 'var(--color-text-muted)',
              textAlign: 'right',
              fontFamily: 'var(--font-mono)',
            }}>
              FUENTE: ierc_golfo_california_v2.gpkg & Atlas PANGAS (Moreno-Báez et al. 2011/2012)
            </p>
          )}
        </div>
      </div>
    </div>
  )
}
