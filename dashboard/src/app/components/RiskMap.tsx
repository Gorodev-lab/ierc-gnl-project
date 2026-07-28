'use client'

import React, { useEffect, useState } from 'react'
import dynamic from 'next/dynamic'

const MapContainer   = dynamic(() => import('react-leaflet').then(m => m.MapContainer),   { ssr: false })
const TileLayer      = dynamic(() => import('react-leaflet').then(m => m.TileLayer),      { ssr: false })
const CircleMarker   = dynamic(() => import('react-leaflet').then(m => m.CircleMarker),   { ssr: false })
const Popup          = dynamic(() => import('react-leaflet').then(m => m.Popup),          { ssr: false })
const GeoJSON        = dynamic(() => import('react-leaflet').then(m => m.GeoJSON),        { ssr: false })

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

function getRiskColor(nivel: string): string {
  if (nivel === 'Alto')     return '#E74C3C'
  if (nivel === 'Moderado') return '#F39C12'
  if (nivel === 'Bajo')     return '#2ECC71'
  return '#0ea5e9'
}

function getRiskRadius(score: number): number {
  return Math.max(10, Math.min(26, score / 4))
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function fishZoneStyle(feature: any) {
  const crit = feature?.properties?.critical_species ?? 0
  let fillColor = '#0ea5e9'
  if (crit >= 5)      fillColor = '#FFB000'
  else if (crit >= 3) fillColor = '#F39C12'

  return {
    fillColor,
    fillOpacity: 0.35,
    color: fillColor,
    weight: 1,
    opacity: 0.6,
  }
}

export default function RiskMap() {
  const [riskData, setRiskData]   = useState<RiskData | null>(null)
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [fishZones, setFishZones] = useState<any>(null)
  const [loaded, setLoaded]       = useState(false)
  const [gpkgConnected, setGpkgConnected] = useState(false)

  useEffect(() => {
    // Intentar consultar API de GeoPackage primero
    fetch('/api/geopackage?layer=proyectos_gnl')
      .then(r => r.json())
      .then(res => {
        if (res.status === 'success' && res.features?.length > 0) {
          setGpkgConnected(true)
        }
      })
      .catch(() => setGpkgConnected(false))

    // Load risk JSON
    fetch('/data/riesgo_proyectos.json')
      .then(r => r.json())
      .then(setRiskData)
      .catch(console.error)

    // Load fish zones sample
    fetch('/data/fish_zones_sample.geojson')
      .then(r => r.json())
      .then(setFishZones)
      .catch(console.error)

    // Leaflet icon setup
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

  return (
    <div className="section">
      <div className="section-title" style={{ justifyContent: 'space-between' }}>
        <span>MAPA DE RIESGO PESQUERO & INFRAESTRUCTURA GNL</span>
        <span style={{ fontSize: '0.6875rem', color: gpkgConnected ? 'var(--color-ok)' : 'var(--color-amber)' }}>
          {gpkgConnected ? '● CONECTADO A GEOPACKAGE (SQLITE)' : '○ MODO CACHE GEOJSON'}
        </span>
      </div>

      {/* Legend */}
      <div style={{
        display: 'flex',
        gap: '1.5rem',
        marginBottom: '1rem',
        flexWrap: 'wrap',
        fontSize: '0.75rem',
        color: 'var(--color-text-secondary)',
        fontFamily: 'var(--font-mono)',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <span style={{ display: 'inline-block', width: 10, height: 10, borderRadius: '50%', background: '#E74C3C' }} />
          ALTO RIESGO GNL
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <span style={{ display: 'inline-block', width: 10, height: 10, borderRadius: '50%', background: '#F39C12' }} />
          MODERADO
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <span style={{ display: 'inline-block', width: 12, height: 8, borderRadius: 2, background: '#FFB000', opacity: 0.7 }} />
          SITIO PANGAS (≥5 SP. CRÍTICAS)
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <span style={{ display: 'inline-block', width: 12, height: 8, borderRadius: 2, background: '#0ea5e9', opacity: 0.6 }} />
          SITIO PANGAS (PESCA ARTESANAL)
        </div>
      </div>

      <div className="map-wrapper" style={{ height: '520px' }}>
        {loaded ? (
          <MapContainer
            center={[29.5, -113.0]}
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

            {/* Fish zones GeoJSON */}
            {fishZones && (
              <GeoJSON
                data={fishZones}
                style={fishZoneStyle}
                onEachFeature={(feature, layer) => {
                  const { sitio, total_records, critical_species, habitat } = feature.properties ?? {}
                  layer.bindTooltip(
                    `<b>SITIO: ${sitio}</b><br/>Entrevistas: ${total_records}<br/>Especies Críticas: ${critical_species}<br/>Hábitat: ${habitat}`,
                    { sticky: true }
                  )
                }}
              />
            )}

            {/* Project markers */}
            {projects.map(p => {
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
                    <div style={{ minWidth: 220, fontFamily: 'var(--font-mono)' }}>
                      <p style={{ fontWeight: 700, fontSize: '0.875rem', color: 'var(--color-amber)', marginBottom: 4 }}>
                        {p.proyecto_nombre}
                      </p>
                      <p style={{ fontSize: '0.6875rem', color: 'var(--color-text-muted)', marginBottom: 8 }}>
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
                      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                        <span style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>ZONAS EN RADIO</span>
                        <span style={{ fontSize: '0.75rem' }}>{p.num_zonas_encontradas.toLocaleString()}</span>
                      </div>
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
            gap: '0.5rem',
            fontFamily: 'var(--font-mono)',
          }}>
            <span className="blink" style={{
              width: 8, height: 8, borderRadius: '50%',
              background: 'var(--color-amber)',
              display: 'inline-block',
            }} />
            INICIALIZANDO MAPA ESOTERIA…
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
          CÁLCULO: {riskData.fecha_calculo} · FUENTE: ierc_golfo_california.gpkg (EPSG:4326)
        </p>
      )}
    </div>
  )
}
