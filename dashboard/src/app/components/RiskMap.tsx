'use client'

import React, { useEffect, useState, useRef } from 'react'
import dynamic from 'next/dynamic'
import MiaInspectorModal from './MiaInspectorModal'
import { getRiskColor } from '@/lib/risk'

const MapContainer   = dynamic(() => import('react-leaflet').then(m => m.MapContainer),   { ssr: false })
const TileLayer      = dynamic(() => import('react-leaflet').then(m => m.TileLayer),      { ssr: false })
const Marker         = dynamic(() => import('react-leaflet').then(m => m.Marker),         { ssr: false })
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
  { id: 'proyectos_gnl',    name: '4 Terminales GNL (11 Features v3)', file: '/data/terminales_gnl_v3.geojson', color: '#EF4444' },
  { id: 'poligonos_saguaro', name: 'Polígonos Detalle Saguaro (MIA 181V)', file: '/data/saguaro_polygons_181v.geojson', color: '#10B981' },
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

interface TerminalQuickJump {
  key: string
  name: string
  location: string
  lat: number
  lon: number
  zoom: number
  precision: string
  precisionColor: string
  status: string
  color: string
}

const TERMINAL_JUMPS: TerminalQuickJump[] = [
  {
    key: 'saguaro',
    name: 'SAGUARO ENERGÍA GNL',
    location: 'Puerto Libertad, Sonora',
    lat: 29.905838,
    lon: -112.688038,
    zoom: 13,
    precision: '[APROXIMADO]',
    precisionColor: '#C0392B',
    status: 'Proposed / Pre-FID',
    color: '#EF4444'
  },
  {
    key: 'amigo',
    name: 'AMIGO LNG',
    location: 'Guaymas, Sonora',
    lat: 27.922867,
    lon: -110.868082,
    zoom: 13,
    precision: '[EXACTO]',
    precisionColor: '#27AE60',
    status: 'Proposed / Pre-FID',
    color: '#27AE60'
  },
  {
    key: 'vista_pacifico',
    name: 'VISTA PACÍFICO (FLNG)',
    location: 'Topolobampo, Sinaloa',
    lat: 25.589100,
    lon: -109.103800,
    zoom: 13,
    precision: '[CALCULADO]',
    precisionColor: '#F39C12',
    status: 'CANCELADO (Feb 2026)',
    color: '#78909C'
  },
  {
    key: 'cosala',
    name: 'GNL COSALÁ',
    location: 'Mazatlán / Zapopan',
    lat: 23.250000,
    lon: -106.420000,
    zoom: 11,
    precision: '[APROXIMADO]',
    precisionColor: '#00ACC1',
    status: 'En Evaluación ASEA',
    color: '#00ACC1'
  }
]

function getBathymetryColor(depth: number): { color: string; weight: number; opacity: number } {
  if (depth >= -20) return { color: '#7DD3FC', weight: 0.9, opacity: 0.8 }
  if (depth >= -100) return { color: '#38BDF8', weight: 0.8, opacity: 0.7 }
  if (depth >= -500) return { color: '#0284C7', weight: 0.7, opacity: 0.6 }
  if (depth >= -2000) return { color: '#0369A1', weight: 0.6, opacity: 0.5 }
  return { color: '#1E3A8A', weight: 0.5, opacity: 0.4 }
}

async function loadLayer(file: string): Promise<any> {
  const response = await fetch(file)
  if (!response.ok) throw new Error(`Failed to load ${file}: ${response.statusText}`)
  return response.json()
}

export default function RiskMap() {
  const [layersData, setLayersData]     = useState<Record<string, any>>({})
  const [activeLayers, setActiveLayers] = useState<Record<string, boolean>>({
    proyectos_gnl: true,
    poligonos_saguaro: true,
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
  const [selectedMiaFeature, setSelectedMiaFeature] = useState<Record<string, any> | null>(null)
  const [isMiaOpen, setIsMiaOpen] = useState(false)
  const [leafletIcons, setLeafletIcons] = useState<Record<string, any>>({})
  const mapRef = useRef<any>(null)

  useEffect(() => {
    // Load all layers in parallel using Promise.all
    const layerPromises = LAYER_CONFIGS
      .filter(cfg => cfg.file)
      .map(async cfg => {
        try {
          const geoJson = await loadLayer(cfg.file)
          return { id: cfg.id, data: geoJson }
        } catch (err) {
          console.error(`Error loading layer ${cfg.file}:`, err)
          return { id: cfg.id, data: null }
        }
      })

    Promise.all(layerPromises).then(results => {
      const newLayers: Record<string, any> = {}
      results.forEach(r => {
        if (r.data) newLayers[r.id] = r.data
      })
      setLayersData(newLayers)
    })

    import('leaflet').then(L => {
      (window as any).L = L
      delete (L.Icon.Default.prototype as any)._getIconUrl
      L.Icon.Default.mergeOptions({
        iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
        iconUrl:       'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
        shadowUrl:     'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
      })

      // Crear custom divIcons estilo Radar Beacon para cada proyecto
      const iconsMap: Record<string, any> = {}
      TERMINAL_JUMPS.forEach(t => {
        iconsMap[t.key] = L.divIcon({
          className: 'custom-radar-beacon-icon',
          html: `
            <div class="radar-beacon-container" style="--beacon-color: ${t.color}">
              <div class="beacon-center"></div>
              <div class="beacon-ring"></div>
              <div class="map-terminal-label" style="--beacon-color: ${t.color}">
                [+] ${t.name}
              </div>
            </div>
          `,
          iconSize: [220, 30],
          iconAnchor: [7, 15]
        })
      })
      setLeafletIcons(iconsMap)
      setLoaded(true)
    })
  }, [])

  const toggleLayer = (id: string) => {
    setActiveLayers(prev => ({ ...prev, [id]: !prev[id] }))
  }

  const focusProyectos = () => {
    if (mapRef.current) {
      mapRef.current.setView([25.8, -109.0], 6)
    }
  }

  const handleOpenMiaModal = (properties: Record<string, any>) => {
    setSelectedMiaFeature(properties)
    setIsMiaOpen(true)
  }

  const handleQuickJump = (t: TerminalQuickJump) => {
    if (mapRef.current) {
      mapRef.current.flyTo([t.lat, t.lon], t.zoom, { duration: 1.2 })
    }
    // Buscar la feature correspondiente en el GeoJSON para abrir su modal
    const features = layersData.proyectos_gnl?.features || []
    const match = features.find((f: any) => {
      const p = f.properties || {}
      const projLower = (p.proyecto || '').toLowerCase()
      if (t.key === 'saguaro' && projLower.includes('saguaro')) return true
      if (t.key === 'amigo' && projLower.includes('amigo')) return true
      if (t.key === 'vista_pacifico' && (projLower.includes('vista') || projLower.includes('pacifico'))) return true
      if (t.key === 'cosala' && (projLower.includes('cosal') || projLower.includes('cosalá'))) return true
      return false
    })

    if (match) {
      handleOpenMiaModal(match.properties)
    } else {
      handleOpenMiaModal({
        proyecto: t.name,
        componente: t.name,
        promovente: t.name,
        estado: t.location,
        municipio: t.location,
        precision_label: t.precision,
        status: t.status,
        fuente_coordenadas: `Navegación Rápida (${t.lat.toFixed(4)}, ${t.lon.toFixed(4)})`
      })
    }
  }

  return (
    <div className="section">
      <div className="section-title" style={{ justifyContent: 'space-between' }}>
        <span>VISOR ESPACIAL IERC — 4 TERMINALES GNL & CONTEXTO SOCIOAMBIENTAL</span>
        <span style={{ fontSize: '0.75rem', color: 'var(--color-ok)', fontFamily: 'var(--font-mono)' }}>
          [●] ENTREGABLE GEOPACKAGE V3 CONECTADO (11 FEATURES + ACCESO RÁPIDO)
        </span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '340px 1fr', gap: '1.25rem', alignItems: 'start' }}>
        
        {/* Layer & Navigation Sidebar */}
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '1rem',
          maxHeight: '680px',
          overflowY: 'auto'
        }}>

          {/* Quick Jump Navigation Panel */}
          <div style={{
            background: 'var(--color-surface)',
            border: '1px solid var(--color-accent)',
            padding: '1rem',
            fontFamily: 'var(--font-mono)',
            borderRadius: 0,
          }}>
            <div style={{
              fontSize: '0.75rem',
              fontWeight: 800,
              color: 'var(--color-accent)',
              marginBottom: '0.75rem',
              letterSpacing: '0.05em',
              borderBottom: '1px solid var(--color-border)',
              paddingBottom: '0.4rem'
            }}>
              &gt; NAVEGACIÓN RÁPIDA A TERMINALES
            </div>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              {TERMINAL_JUMPS.map(t => (
                <button
                  key={t.key}
                  onClick={() => handleQuickJump(t)}
                  style={{
                    background: 'var(--color-surface-2)',
                    border: `1px solid ${t.color}`,
                    color: '#FFFFFF',
                    padding: '0.5rem 0.65rem',
                    cursor: 'pointer',
                    textAlign: 'left',
                    fontFamily: 'var(--font-mono)',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '0.2rem',
                    borderRadius: 0,
                    transition: 'background 0.15s ease'
                  }}
                  onMouseEnter={e => (e.currentTarget.style.background = 'var(--color-surface-3)')}
                  onMouseLeave={e => (e.currentTarget.style.background = 'var(--color-surface-2)')}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontSize: '0.75rem', fontWeight: 800, color: t.color }}>
                      &gt; {t.name}
                    </span>
                    <span style={{ fontSize: '0.625rem', color: t.precisionColor, fontWeight: 800 }}>
                      {t.precision}
                    </span>
                  </div>
                  <div style={{ fontSize: '0.6875rem', color: 'var(--color-text-secondary)' }}>
                    {t.location}
                  </div>
                  <div style={{ fontSize: '0.625rem', color: 'var(--color-text-muted)' }}>
                    Estatus: {t.status}
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Layer Control Panel */}
          <div style={{
            background: 'var(--color-surface)',
            border: '1px solid var(--color-border-hi)',
            padding: '1.25rem',
            fontFamily: 'var(--font-mono)',
            borderRadius: 0,
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h4 style={{
                fontSize: '0.8125rem',
                color: 'var(--color-accent)',
                margin: 0,
                letterSpacing: '0.05em',
                fontWeight: 800,
              }}>
                CAPAS VECTORIALES IERC
              </h4>

              <button
                onClick={focusProyectos}
                style={{
                  background: 'var(--color-surface-2)',
                  border: '1px solid var(--color-accent)',
                  color: 'var(--color-accent)',
                  fontSize: '0.6875rem',
                  padding: '0.25rem 0.5rem',
                  borderRadius: 0,
                  cursor: 'pointer',
                  fontWeight: 'bold',
                  fontFamily: 'var(--font-mono)',
                }}
                title="Centrar mapa en las 4 terminales GNL"
              >
                &gt; CENTRAR GNL
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
          </div>
        </div>

        {/* Map Container */}
        <div>
          <div className="map-wrapper" style={{ height: '680px' }}>
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

                {/* Layer Polígonos Detalle Saguaro (MIA 181V) */}
                {activeLayers.poligonos_saguaro && layersData.poligonos_saguaro && (
                  <GeoJSON
                    key="poligonos_saguaro"
                    data={layersData.poligonos_saguaro}
                    style={(feat) => {
                      const p = feat?.properties || {}
                      const tipo = p.tipo || ''
                      let color = '#10B981' // Reserva green
                      if (tipo.includes('Campamentos')) color = '#F97316' // Naranja
                      else if (tipo.includes('Vial') || tipo.includes('Caminos')) color = '#FACC15' // Amarillo
                      else if (tipo.includes('Terminal')) color = '#3B82F6' // Azul terminal

                      return {
                        color: color,
                        fillColor: color,
                        fillOpacity: 0.45,
                        weight: 2,
                        dashArray: tipo.includes('Vial') ? '4, 4' : '0'
                      }
                    }}
                    onEachFeature={(feat, layer) => {
                      const p = feat?.properties || {}
                      layer.bindPopup(
                        `<div style="font-family: monospace; font-size: 0.75rem; min-width: 240px;">
                          <b style="color: #10B981; font-size: 0.8125rem;">${p.nombre}</b><br/>
                          <b>TIPO:</b> ${p.tipo}<br/>
                          <b>SUPERFICIE:</b> ${p.superficie_ha} ha<br/>
                          <b>N° VÉRTICES MIA:</b> ${p.num_vertices}<br/>
                          <b>ESTATUS MIA:</b> ${p.estatus}<br/>
                          <div style="margin-top: 6px; font-size: 0.6875rem; color: #CCCCCC; border-top: 1px dashed #444; padding-top: 4px;">
                            FUENTE: MIA-R Saguaro / GeoPackage v1.2 (Tablas II.5 - II.9)
                          </div>
                        </div>`
                      )
                    }}
                  />
                )}

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

                {/* Layer 4 Terminales GNL Consolidados (11 Features Vectoriales v3) */}
                {activeLayers.proyectos_gnl && layersData.proyectos_gnl && (
                  <GeoJSON
                    key="proyectos_gnl_v3"
                    data={layersData.proyectos_gnl}
                    style={(feat) => {
                      const p = feat?.properties || {}
                      const isCancel = p.status_code === 'cancelled'
                      const isEval = p.status_code === 'under_review'
                      
                      return {
                        fillColor: isCancel ? '#78909C' : (isEval ? '#00ACC1' : '#EF4444'),
                        fillOpacity: isCancel ? 0.35 : 0.65,
                        color: isCancel ? '#455A64' : (isEval ? '#006064' : '#B71C1C'),
                        weight: 2,
                        dashArray: isCancel ? '6, 4' : '0'
                      }
                    }}
                    onEachFeature={(feat, layer) => {
                      const p = feat.properties || {}
                      layer.on('click', () => {
                        handleOpenMiaModal(p)
                      })
                    }}
                  />
                )}

                {/* High-Visibility Radar Beacon Markers Permanentes en Mapa */}
                {activeLayers.proyectos_gnl && TERMINAL_JUMPS.map(t => {
                  const customIcon = leafletIcons[t.key]
                  if (!customIcon) return null

                  return (
                    <Marker
                      key={`beacon_${t.key}`}
                      position={[t.lat, t.lon]}
                      icon={customIcon}
                      eventHandlers={{
                        click: () => handleQuickJump(t)
                      }}
                    >
                      <Popup>
                        <div style={{ fontFamily: 'monospace', fontSize: '0.75rem', minWidth: 260 }}>
                          <b style={{ color: t.color, fontSize: '0.8125rem' }}>{t.name}</b>
                          <div style={{ margin: '4px 0', display: 'flex', gap: 4 }}>
                            <span style={{ background: t.color, color: '#FFF', padding: '2px 6px', fontSize: '0.6875rem', fontWeight: 'bold' }}>
                              {t.status}
                            </span>
                            <span style={{ border: `1px solid ${t.precisionColor}`, color: t.precisionColor, padding: '2px 6px', fontSize: '0.6875rem', fontWeight: 'bold' }}>
                              {t.precision}
                            </span>
                          </div>
                          <b>UBICACIÓN:</b> {t.location}<br/>
                          <button 
                            onClick={() => handleQuickJump(t)}
                            style={{
                              marginTop: 8, width: '100%', background: '#C0392B', border: 'none', color: 'white', padding: 6, fontFamily: 'monospace', fontSize: '0.6875rem', fontWeight: 'bold', cursor: 'pointer'
                            }}
                          >
                            &gt; ABRIR INSPECTOR DE MIA & PLANOS
                          </button>
                        </div>
                      </Popup>
                    </Marker>
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
            FUENTE: GeoPackage v3 (4 Terminales GNL / 11 Subconjuntos Vectoriales + Navegación Rápida Radar Beacon)
          </p>
        </div>
      </div>

      {/* MIA Inspector Modal */}
      <MiaInspectorModal
        isOpen={isMiaOpen}
        onClose={() => setIsMiaOpen(false)}
        featureProps={selectedMiaFeature}
      />
    </div>
  )
}
