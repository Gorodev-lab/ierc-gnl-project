'use client'

import React, { useEffect, useState } from 'react'
import dynamic from 'next/dynamic'

const MapContainer   = dynamic(() => import('react-leaflet').then(m => m.MapContainer),   { ssr: false })
const TileLayer      = dynamic(() => import('react-leaflet').then(m => m.TileLayer),      { ssr: false })
const CircleMarker   = dynamic(() => import('react-leaflet').then(m => m.CircleMarker),   { ssr: false })
const Popup          = dynamic(() => import('react-leaflet').then(m => m.Popup),          { ssr: false })
const GeoJSON        = dynamic(() => import('react-leaflet').then(m => m.GeoJSON),        { ssr: false })
const WMSTileLayer   = dynamic(() => import('react-leaflet').then(m => m.WMSTileLayer),   { ssr: false })

interface GnlProject {
  nombre_proyecto: string
  estado: string
  municipio: string
  tipo_infraestructura: string
  empresa_promovente: string
  estatus_permiso: string
  fuente_oficial: string
  latitud: number
  longitud: number
}

const LAYER_CONFIGS = [
  { id: 'sener_gasoductos', name: 'SENER/CNIH Red Gasoductos (WMS)', file: '', color: '#FFB000' },
  { id: 'proyectos_gnl',    name: '11 Proyectos GNL Consolidados',    file: '/data/proyectos_gnl.geojson', color: '#EF4444' },
  { id: 'batimetria',       name: 'Contornos Batimétricos GEBCO 2024',file: '/data/batimetria_golfo.geojson', color: '#0EA5E9' },
  { id: 'h3_riesgo',        name: 'Malla H3 IERC (Res 8/9)',          file: '/data/grilla_h3_riesgo.geojson', color: '#F59E0B' },
  { id: 'pangas',           name: 'Zonas Pesqueras PANGAS',          file: '/data/zpesca_pangas_sample.geojson', color: '#8D6E63' },
  { id: 'riqueza',          name: 'Riqueza Relativa Pesquera',       file: '/data/riqueza_relativa_sample.geojson', color: '#2C3E50' }
]

function getRiskColor(score: number): string {
  if (score >= 75.0) return '#EF4444'
  if (score >= 50.0) return '#F59E0B'
  return '#10B981'
}

export default function RiskMap() {
  const [layersData, setLayersData]     = useState<Record<string, any>>({})
  const [activeLayers, setActiveLayers] = useState<Record<string, boolean>>({
    sener_gasoductos: true,
    proyectos_gnl: true,
    batimetria: true,
    h3_riesgo: true,
    pangas: true,
    riqueza: false,
  })

  const [loaded, setLoaded] = useState(false)

  useEffect(() => {
    // Load GeoJSON layers
    LAYER_CONFIGS.forEach(cfg => {
      if (cfg.file) {
        fetch(cfg.file)
          .then(r => r.json())
          .then(geoJson => {
            setLayersData(prev => ({ ...prev, [cfg.id]: geoJson }))
          })
          .catch(() => console.log(`Notice: Layer file ${cfg.file} handled.`))
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
        <span>VISOR ESPACIAL IERC — BATIMETRÍA GEBCO 2024 & PROYECTOS GNL CONSOLIDADOS</span>
        <span style={{ fontSize: '0.75rem', color: 'var(--color-ok)', fontFamily: 'var(--font-mono)' }}>
          ● ENTREGABLE GEOPACKAGE V1.1 CONECTADO
        </span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '320px 1fr', gap: '1.25rem', alignItems: 'start' }}>
        
        {/* Layer Control Sidebar */}
        <div style={{
          background: 'var(--color-surface)',
          border: '1px solid var(--color-border-hi)',
          padding: '1.25rem',
          fontFamily: 'var(--font-mono)',
        }}>
          <h4 style={{
            fontSize: '0.8125rem',
            color: 'var(--color-amber)',
            borderBottom: '1px solid var(--color-border-hi)',
            paddingBottom: '0.5rem',
            marginBottom: '1rem',
            letterSpacing: '0.05em',
          }}>
            CAPAS VECTORIALES IERC
          </h4>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {LAYER_CONFIGS.map(cfg => (
              <label key={cfg.id} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.75rem', cursor: 'pointer', color: 'var(--color-text-primary)' }}>
                <input type="checkbox" checked={!!activeLayers[cfg.id]} onChange={() => toggleLayer(cfg.id)} style={{ accentColor: cfg.color }} />
                <span style={{ display: 'inline-block', width: 10, height: 10, background: cfg.color, border: '1px solid #000' }} />
                {cfg.name}
              </label>
            ))}
          </div>

          <div style={{ marginTop: '1.5rem', borderTop: '1px solid var(--color-border)', paddingTop: '1rem', fontSize: '0.6875rem', color: 'var(--color-text-muted)' }}>
            <strong>SIMBOLOGÍA DE RIESGO IERC:</strong>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.35rem', marginTop: '0.5rem' }}>
              <span style={{ color: '#EF4444' }}>■ ALTO RIESGO (&gt;= 75)</span>
              <span style={{ color: '#F59E0B' }}>■ MODERADO (50 - 75)</span>
              <span style={{ color: '#10B981' }}>■ BAJO (&lt; 50)</span>
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

                {/* Layer 1: Batimetría GEBCO */}
                {activeLayers.batimetria && layersData.batimetria && (
                  <GeoJSON
                    key="batimetria"
                    data={layersData.batimetria}
                    style={(feature) => ({
                      color: '#0EA5E9',
                      weight: 0.8,
                      opacity: 0.6
                    })}
                    onEachFeature={(feat, layer) => {
                      const p = feat.properties || {}
                      layer.bindPopup(
                        `<div style="font-family: monospace; font-size: 0.75rem;">
                          <b>PROFUNDIDAD:</b> ${p.profundidad_m} m<br/>
                          <b>CLASE:</b> ${p.clase_profundidad}<br/>
                          <b>FUENTE:</b> ${p.fuente || 'GEBCO 2024 / ETOPO1'}
                        </div>`
                      )
                    }}
                  />
                )}

                {/* Layer 2: Malla H3 IERC */}
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

                {/* Layer 3: Proyectos GNL Consolidados (11) */}
                {activeLayers.proyectos_gnl && layersData.proyectos_gnl && (
                  <GeoJSON
                    key="proyectos_gnl"
                    data={layersData.proyectos_gnl}
                    pointToLayer={(feat, latlng) => {
                      return new (window as any).L.CircleMarker(latlng, {
                        radius: 8,
                        fillColor: '#EF4444',
                        fillOpacity: 0.9,
                        color: '#FFFFFF',
                        weight: 2
                      })
                    }}
                    onEachFeature={(feat, layer) => {
                      const p = feat.properties || {}
                      layer.bindPopup(
                        `<div style="font-family: monospace; font-size: 0.75rem; min-width: 220px;">
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
                CARGANDO VISOR ESPACIAL IERC & CAPAS BATIMÉTRICAS GEBCO…
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
            FUENTE: ierc_golfo_california.gpkg (11 Proyectos GNL + Batimetría GEBCO 2024 / ETOPO1)
          </p>
        </div>
      </div>
    </div>
  )
}
