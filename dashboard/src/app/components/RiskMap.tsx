'use client'

import React, { useEffect, useState, useRef, useMemo, useCallback } from 'react'
import dynamic from 'next/dynamic'
import { useSearchParams, useRouter, usePathname } from 'next/navigation'
import MiaInspectorModal from './MiaInspectorModal'
import { getRiskColor } from '@/lib/risk'
import Tooltip from './Tooltip'

const MapContainer   = dynamic(() => import('react-leaflet').then(m => m.MapContainer),   { ssr: false })
const TileLayer      = dynamic(() => import('react-leaflet').then(m => m.TileLayer),      { ssr: false })
const Marker         = dynamic(() => import('react-leaflet').then(m => m.Marker),         { ssr: false })
const Popup          = dynamic(() => import('react-leaflet').then(m => m.Popup),          { ssr: false })
const GeoJSON        = dynamic(() => import('react-leaflet').then(m => m.GeoJSON),        { ssr: false })
const WMSTileLayer   = dynamic(() => import('react-leaflet').then(m => m.WMSTileLayer),   { ssr: false })
import Heatmap from './Heatmap'

// Leaflet only available client-side
const getLeaflet = () => {
  if (typeof window !== 'undefined') {
    return (window as any).L
  }
  return null
}

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
  { id: 'ductos_cnih',      name: 'Ductos CNIH/SENER (24 tramos, 6.4k km)', file: '/data/ductos_cnih.geojson', color: '#FF6B00' },
  { id: 'sener_gasoductos', name: 'SENER/CNIH Red Gasoductos (WMS)', file: '', color: '#FFB000' },
  { id: 'batimetria',       name: 'Contornos Batimétricos GEBCO 2024',file: '/data/batimetria_golfo.geojson', color: '#38BDF8' },
  { id: 'h3_riesgo',        name: 'Malla H3 IERC (Res 8/9)',          file: '/data/grilla_h3_riesgo.geojson', color: '#F59E0B' },
  { id: 'gfw_fishing',      name: 'GFW Esfuerzo Pesquero (H3, 9960 celdas)', file: '/data/gfw_fishing_h3.geojson', color: '#6366F1' },
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

function LayerToggle({ cfg, isActive, featureCount, onClick,extras }: {
  cfg: LayerConfig
  isActive: boolean
  featureCount: number | null
  onClick: () => void
  extras?: React.ReactNode
}) {
  return (
    <div
      style={{
        display: 'flex', alignItems: 'center', gap: '0.5rem',
        padding: '0.3rem 0.25rem',
        borderBottom: '1px solid var(--color-border)',
        cursor: 'pointer',
        opacity: isActive ? 1 : 0.55,
        transition: 'opacity 0.15s ease',
      }}
      onClick={onClick}
    >
      <span style={{
        display: 'inline-block', width: 10, height: 10, flexShrink: 0,
        background: cfg.id === 'sener_gasoductos' ? 'transparent' : cfg.color,
        border: cfg.id === 'sener_gasoductos' ? `2px solid ${cfg.color}` : 'none',
        opacity: isActive ? 1 : 0.4,
      }} />
      <span style={{
        fontSize: '0.625rem', fontWeight: 800, fontFamily: 'var(--font-mono)', flexShrink: 0,
        color: !isActive ? 'var(--color-text-disabled)' : 'var(--color-ok)',
      }}>
        {isActive ? '[ON]' : '[--]'}
      </span>
      <span style={{
        fontSize: '0.6875rem', flex: 1, lineHeight: 1.3,
        color: isActive ? 'var(--color-text-primary)' : 'var(--color-text-muted)',
      }}>
        {cfg.name}
        {extras}
      </span>
      {featureCount !== null && (
        <span style={{
          fontSize: '0.5625rem', color: 'var(--color-text-muted)',
          fontVariantNumeric: 'tabular-nums', flexShrink: 0,
        }}>
          {featureCount.toLocaleString()}
        </span>
      )}
    </div>
  )
}

function getBathymetryColor(depth: number): { color: string; weight: number; opacity: number } {
  if (depth >= -20) return { color: '#7DD3FC', weight: 0.9, opacity: 0.8 }
  if (depth >= -100) return { color: '#38BDF8', weight: 0.8, opacity: 0.7 }
  if (depth >= -500) return { color: '#0284C7', weight: 0.7, opacity: 0.6 }
  if (depth >= -2000) return { color: '#0369A1', weight: 0.6, opacity: 0.5 }
  return { color: '#1E3A8A', weight: 0.5, opacity: 0.4 }
}

function toGeoJSON(data: any): any {
  if (!data) return null
  if (data.type === 'FeatureCollection') return data
  if (data.features && Array.isArray(data.features)) {
    const features = data.features.map((item: any) => {
      if (item.type === 'Feature') return item
      const { geometry, ...properties } = item
      return {
        type: 'Feature',
        geometry: typeof geometry === 'string' ? JSON.parse(geometry) : (geometry || null),
        properties
      }
    })
    return { type: 'FeatureCollection', features }
  }
  if (Array.isArray(data)) {
    const features = data.map((item: any) => {
      const { geometry, ...properties } = item
      return {
        type: 'Feature',
        geometry: typeof geometry === 'string' ? JSON.parse(geometry) : (geometry || null),
        properties
      }
    })
    return { type: 'FeatureCollection', features }
  }
  return data
}

async function loadLayer(id: string, file: string): Promise<any> {
  if (file) {
    try {
      const response = await fetch(file)
      if (response.ok) {
        const json = await response.json()
        return toGeoJSON(json)
      }
    } catch {
      // Fallthrough to API fallback
    }
  }

  const tableMap: Record<string, string> = {
    proyectos_gnl: 'proyectos_gnl',
    h3_riesgo: 'grilla_h3_riesgo',
    pangas: 'zonas_pesqueras_pangas',
    riqueza: 'riqueza_relativa_pesquera',
    capas_contexto: 'gasoductos_infraestructura_gnl',
    ductos_cnih: 'ductos_cnih',
  }

  const table = tableMap[id] || id
  const apiRes = await fetch(`/api/geopackage?layer=${table}&limit=5000`)
  if (!apiRes.ok) throw new Error(`Failed to load layer ${id}`)
  const data = await apiRes.json()
  return toGeoJSON(data)
}

export default function RiskMap() {
  const [layersData, setLayersData]     = useState<Record<string, any>>({})
  const [confidenceThreshold, setConfidenceThreshold] = useState<number>(0.0)
  const [activeLayers, setActiveLayers] = useState<Record<string, boolean>>({
    proyectos_gnl: true,
    poligonos_saguaro: true,
    capas_contexto: true,
    ductos_cnih: false,
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
    gfw_fishing: false,
  })

  const [gfwFilters, setGfwFilters] = useState({
    year: 'all' as string,
    month: 'all' as string,
    geartype: 'all' as string,
    flag: 'all' as string,
  })

  // Heatmap intensity controls
  const [heatmapOptions, setHeatmapOptions] = useState({
    radius: 25,
    blur: 15,
    max: 2,
    minOpacity: 0.25,
  })

  // Vessel intelligence report data
  const [vesselReport, setVesselReport] = useState<{
    totalVessels: number
    totalHours: number
    uniqueMMSI: number
    topFlags: { flag: string; count: number }[]
    topGearTypes: { gear: string; hours: number }[]
    yearsAvailable: number[]
    monthsAvailable: number[]
    timeRange: { start: string; end: string }
    lastUpdated: string
  } | null>(null)

  const [loaded, setLoaded] = useState(false)
  const [gfwLoading, setGfwLoading] = useState(false)
  const [gfwError, setGfwError] = useState<string | null>(null)
  const [selectedMiaFeature, setSelectedMiaFeature] = useState<Record<string, any> | null>(null)
  const [isMiaOpen, setIsMiaOpen] = useState(false)
  const [leafletIcons, setLeafletIcons] = useState<Record<string, any>>({})
  const [mapZoom, setMapZoom] = useState<number>(5)
  const mapRef = useRef<any>(null)

  // URL state synchronization
  const searchParams = useSearchParams()
  const { replace } = useRouter()
  const pathname = usePathname()

  // Initialize state from URL params
  useEffect(() => {
    const params = new URLSearchParams(searchParams.toString())
    if (params.has('lat') && params.has('lng') && params.has('z')) {
      mapRef.current?.setView([parseFloat(params.get('lat')!), parseFloat(params.get('lng')!)], parseInt(params.get('z')!))
    }
    if (params.has('layers')) {
      const layerIds = params.get('layers')!.split(',')
      setActiveLayers(prev => {
        const next = { ...prev }
        Object.keys(next).forEach(k => { next[k] = layerIds.includes(k) })
        return next
      })
    }
  }, [searchParams])

  const syncUrl = useCallback(() => {
    if (!mapRef.current) return
    const center = mapRef.current.getCenter()
    const zoom = mapRef.current.getZoom()
    const activeLayerIds = Object.entries(activeLayers).filter(([, v]) => v).map(([k]) => k).join(',')
    const params = new URLSearchParams()
    params.set('lat', center.lat.toFixed(4))
    params.set('lng', center.lng.toFixed(4))
    params.set('z', zoom.toString())
    if (activeLayerIds) params.set('layers', activeLayerIds)
    replace(`${pathname}?${params.toString()}`)
  }, [activeLayers, pathname, replace])

  // Sync URL when map moves or layers change
  useEffect(() => {
    if (!mapRef.current) return
    const handleMoveEnd = () => syncUrl()
    mapRef.current.on('moveend', handleMoveEnd)
    syncUrl()
    return () => mapRef.current?.off('moveend', syncUrl)
  }, [syncUrl])

  useEffect(() => {
    // Load all layers in parallel using Promise.all
    // Skip gfw_fishing initially since it's large (2.3 MB) and disabled by default
    const layersToLoad = LAYER_CONFIGS.filter(cfg => cfg.id !== 'gfw_fishing')
    const layerPromises = layersToLoad
      .map(async cfg => {
        try {
          const geoJson = await loadLayer(cfg.id, cfg.file)
          return { id: cfg.id, data: geoJson }
        } catch (err) {
          console.error(`Error loading layer ${cfg.id}:`, err)
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

    // Lazy load gfw_fishing — usa formato compacto (330 KB) en lugar del GeoJSON bruto (2.1 MB)
    const loadGfwFishing = async () => {
      setGfwLoading(true)
      setGfwError(null)
      try {
        const res = await fetch('/data/gfw_compact.json')
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        const compact = await res.json()
        // Decodificar formato compacto → GeoJSON FeatureCollection
        const { flags, geartypes, rows } = compact as {
          flags: string[]
          geartypes: string[]
          rows: number[][]
        }
        const geoJson = {
          type: 'FeatureCollection' as const,
          features: rows.map((r: number[]) => ({
            type: 'Feature' as const,
            properties: {
              hours:         r[2],
              fishing_hours: r[2], // duplicar para compatibilidad con popups y zoom alto
              year:          r[3],
              month:         r[4],
              flag:          flags[r[5]],
              geartype:      geartypes[r[6]],
            },
            geometry: { type: 'Point' as const, coordinates: [r[0], r[1]] }
          }))
        }
        setLayersData(prev => ({ ...prev, gfw_fishing: geoJson }))

        // Generate vessel intelligence report from loaded data
        const features = geoJson.features
        const totalHours = features.reduce((sum, f) => sum + (f.properties.hours || 0), 0)
        const uniqueMMSI = features.length
        const flagCounts: Record<string, number> = {}
        const gearHours: Record<string, number> = {}
        const yearsSet = new Set<number>()
        const monthsSet = new Set<number>()

        features.forEach(f => {
          const p = f.properties
          flagCounts[p.flag] = (flagCounts[p.flag] || 0) + 1
          gearHours[p.geartype] = (gearHours[p.geartype] || 0) + (p.hours || 0)
          yearsSet.add(p.year)
          monthsSet.add(p.month)
        })

        const topFlags = Object.entries(flagCounts)
          .sort(([,a], [,b]) => b - a)
          .slice(0, 5)
          .map(([flag, count]) => ({ flag, count }))

        const topGearTypes = Object.entries(gearHours)
          .sort(([,a], [,b]) => b - a)
          .slice(0, 5)
          .map(([gear, hours]) => ({ gear, hours: Number(hours.toFixed(1)) }))

        const yearsAvailable = Array.from(yearsSet).sort()
        const monthsAvailable = Array.from(monthsSet).sort((a,b) => a-b)

        setVesselReport({
          totalVessels: uniqueMMSI || features.length,
          totalHours: Number(totalHours.toFixed(1)),
          uniqueMMSI,
          topFlags,
          topGearTypes,
          yearsAvailable,
          monthsAvailable,
          timeRange: {
            start: `${yearsAvailable[0]}-${String(monthsAvailable[0]).padStart(2,'0')}`,
            end: `${yearsAvailable[yearsAvailable.length-1]}-${String(monthsAvailable[monthsAvailable.length-1]).padStart(2,'0')}`
          },
          lastUpdated: new Date().toISOString().split('T')[0]
        })
      } catch (err: any) {
        console.error('Error loading gfw_fishing:', err)
        setGfwError(err.message ?? 'Error desconocido')
        setActiveLayers(prev => ({ ...prev, gfw_fishing: false }))
      } finally {
        setGfwLoading(false)
      }
    }

    // Store loader for later use
    ;(window as any).loadGfwFishing = loadGfwFishing

    import('leaflet').then(async L => {
      (window as any).L = L
      // @ts-ignore
      await import('leaflet.heat')
      return L
    }).then(L => {
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

  useEffect(() => {
    const handleFocusMapNode = (e: Event) => {
      const customEvent = e as CustomEvent<{ lat: number; lng: number; label: string; layerId?: string }>
      const { lat, lng, label, layerId } = customEvent.detail
      
      if (mapRef.current) {
        // 1. Activar la capa de gasoductos/infraestructura de gas si es necesario
        if (layerId === 'capas_contexto') {
          setActiveLayers(prev => ({ ...prev, capas_contexto: true }))
        }
        
        // 2. Centrar mapa y hacer zoom
        mapRef.current.setView([lat, lng], 11)

        // 3. Abrir popup de Leaflet de forma dinámica en la posición del nodo
        const L = (window as any).L
        if (L) {
          L.popup()
            .setLatLng([lat, lng])
            .setContent(
              `<div style="font-family: monospace; font-size: 0.75rem; min-width: 180px; color: #fff; background: #000; padding: 4px;">
                <b style="color: var(--color-accent); font-size: 0.8125rem;">[NODO GAS SISTRANGAS]</b><br/>
                <span style="font-weight: 700; color: #fff;">${label}</span><br/>
                <span style="color: var(--color-text-muted); font-size: 0.625rem; display: block; margin-top: 4px;">Coordenadas: ${lat.toFixed(4)}N · ${Math.abs(lng).toFixed(4)}W</span>
              </div>`
            )
            .openOn(mapRef.current)
        }
      }
    }

    window.addEventListener('focus-map-node', handleFocusMapNode)
    return () => {
      window.removeEventListener('focus-map-node', handleFocusMapNode)
    }
  }, [])


  // Filtered GFW data (memoized)
  const filteredGfwData = useMemo(() => {
    if (!layersData.gfw_fishing) return null
    const features = layersData.gfw_fishing.features as Array<{ properties: Record<string, any> }>
    return {
      ...layersData.gfw_fishing,
      features: features.filter(f => {
        const p = f.properties
        return (gfwFilters.year === 'all' || String(p.year) === gfwFilters.year) &&
               (gfwFilters.month === 'all' || String(p.month) === gfwFilters.month) &&
               (gfwFilters.geartype === 'all' || p.geartype === gfwFilters.geartype) &&
               (gfwFilters.flag === 'all' || p.flag === gfwFilters.flag)
      })
    }
  }, [layersData.gfw_fishing, gfwFilters])

  const toggleLayer = (id: string) => {
    setActiveLayers(prev => ({ ...prev, [id]: !prev[id] }))
    // Lazy load gfw_fishing on first enable
    if (id === 'gfw_fishing' && !layersData.gfw_fishing) {
      ;(window as any).loadGfwFishing?.()
    }
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
          <div
            data-tour="terminal-jumps"
            style={{
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

          {/* Spatial Confidence Filter Panel */}
          <div style={{
            background: 'var(--color-surface)',
            border: '1px solid var(--color-ocean)',
            padding: '1rem',
            fontFamily: 'var(--font-mono)',
            borderRadius: 0,
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
              <span style={{ fontSize: '0.72rem', fontWeight: 800, color: 'var(--color-ocean)', letterSpacing: '0.05em' }}>
                &gt; FILTRO CONFIANZA ESPACIAL
              </span>
              <span style={{ fontSize: '0.75rem', fontWeight: 800, color: confidenceThreshold > 0 ? 'var(--color-accent)' : 'var(--color-text-muted)' }}>
                ≥ {(confidenceThreshold * 100).toFixed(0)}%
              </span>
            </div>
            
            <input
              type="range"
              min="0.0"
              max="0.95"
              step="0.05"
              value={confidenceThreshold}
              onChange={(e) => setConfidenceThreshold(parseFloat(e.target.value))}
              style={{
                width: '100%',
                accentColor: 'var(--color-ocean)',
                cursor: 'pointer',
              }}
            />
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.62rem', color: 'var(--color-text-muted)', marginTop: '4px' }}>
              <span>0% (Todos)</span>
              <span>50% (Media)</span>
              <span>95% (Alta)</span>
            </div>
          </div>

          {/* Layer Control Panel — con grupos, color swatches y contadores */}
          <div
            data-tour="layer-panel"
            style={{
            background: 'var(--color-surface)',
            border: '1px solid var(--color-border-hi)',
            padding: '1rem',
            fontFamily: 'var(--font-mono)',
            borderRadius: 0,
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.875rem' }}>
              <h4 style={{
                fontSize: '0.75rem',
                color: 'var(--color-accent)',
                margin: 0,
                letterSpacing: '0.05em',
                fontWeight: 800,
              }}>
                &gt; CAPAS VECTORIALES (15)
              </h4>
              <button
                onClick={focusProyectos}
                style={{
                  background: 'var(--color-surface-2)',
                  border: '1px solid var(--color-accent)',
                  color: 'var(--color-accent)',
                  fontSize: '0.6rem',
                  padding: '0.2rem 0.45rem',
                  borderRadius: 0,
                  cursor: 'pointer',
                  fontWeight: 800,
                  fontFamily: 'var(--font-mono)',
                }}
                title="Centrar mapa en las 4 terminales GNL"
              >
                &gt; CENTRAR GNL
              </button>
            </div>

            {/* GRUPO 1: Infraestructura GNL */}
            <div style={{ marginBottom: '0.75rem' }}>
              <div style={{
                fontSize: '0.6rem', fontWeight: 800, color: 'var(--color-alert)',
                letterSpacing: '0.08em', textTransform: 'uppercase',
                marginBottom: '0.4rem', paddingBottom: '0.2rem',
                borderBottom: '1px solid rgba(192,57,43,0.25)',
              }}>
                [INFRAESTRUCTURA GNL]
              </div>
              {LAYER_CONFIGS.filter(l => ['proyectos_gnl','poligonos_saguaro','capas_contexto','ductos_cnih','sener_gasoductos'].includes(l.id)).map(cfg => (
                <LayerToggle key={cfg.id} cfg={cfg} isActive={activeLayers[cfg.id]} featureCount={layersData[cfg.id]?.features?.length ?? null} onClick={() => toggleLayer(cfg.id)} />
              ))}
            </div>

            {/* GRUPO 2: Pesquería Artesanal */}
            <div style={{ marginBottom: '0.75rem' }}>
              <div style={{
                fontSize: '0.6rem', fontWeight: 800, color: 'var(--color-ocean)',
                letterSpacing: '0.08em', textTransform: 'uppercase',
                marginBottom: '0.4rem', paddingBottom: '0.2rem',
                borderBottom: '1px solid rgba(14,165,233,0.25)',
              }}>
                [PESQUERÍA ARTESANAL]
              </div>
              {LAYER_CONFIGS.filter(l => ['pangas','buceo','chinchorro','redes','manta','trampa','riqueza','gfw_fishing'].includes(l.id)).map(cfg => {
                const isGfwLoading = cfg.id === 'gfw_fishing' && gfwLoading
                const hasGfwError = cfg.id === 'gfw_fishing' && gfwError
                const featureCount = cfg.id === 'gfw_fishing'
                  ? (filteredGfwData?.features?.length ?? null)
                  : (layersData[cfg.id]?.features?.length ?? null)
                return (
                  <LayerToggle
                    key={cfg.id} cfg={cfg}
                    isActive={activeLayers[cfg.id]}
                    featureCount={isGfwLoading ? null : featureCount}
                    onClick={() => !isGfwLoading && toggleLayer(cfg.id)}
                    extras={
                      <>
                        {isGfwLoading && <span style={{ fontSize: '0.5625rem', color: 'var(--color-warn)', fontFamily: 'var(--font-mono)', marginLeft: 4 }}>CARGANDO 2.1 MB…</span>}
                        {hasGfwError && <span style={{ fontSize: '0.5625rem', color: 'var(--color-alert)', fontFamily: 'var(--font-mono)', marginLeft: 4 }}>{gfwError}</span>}
                      </>
                    }
                  />
                )
              })}
            </div>

            {/* GRUPO 3: Ambiental */}
            <div>
              <div style={{
                fontSize: '0.6rem', fontWeight: 800, color: 'var(--color-ok)',
                letterSpacing: '0.08em', textTransform: 'uppercase',
                marginBottom: '0.4rem', paddingBottom: '0.2rem',
                borderBottom: '1px solid rgba(39,174,96,0.25)',
              }}>
                [AMBIENTAL / RIESGO]
              </div>
              {LAYER_CONFIGS.filter(l => ['batimetria','h3_riesgo'].includes(l.id)).map(cfg => (
                <LayerToggle key={cfg.id} cfg={cfg} isActive={activeLayers[cfg.id]} featureCount={layersData[cfg.id]?.features?.length ?? null} onClick={() => toggleLayer(cfg.id)} />
              ))}
            </div>

            {/* GFW Filter Controls (conditional) */}
            {activeLayers.gfw_fishing && (
              <div
                data-tour="gfw-filters"
                style={{
                background: 'var(--color-surface-2)',
                border: '1px solid #6366F1',
                padding: '0.75rem',
                marginTop: '0.75rem',
                fontFamily: 'var(--font-mono)',
                borderRadius: 0,
              }}>
                <div style={{ fontSize: '0.6875rem', fontWeight: 800, color: '#6366F1', marginBottom: '0.5rem', letterSpacing: '0.05em' }}>
                  {'>'} FILTROS GFW PESQUERO
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
                  <Tooltip content="Filtrar por año de captura GFW (2016 o 2020).">
                    <div>
                      <label style={{ display: 'block', fontSize: '0.625rem', color: 'var(--color-text-secondary)', marginBottom: '0.2rem' }}>AÑO</label>
                      <select value={gfwFilters.year} onChange={e => setGfwFilters(prev => ({ ...prev, year: e.target.value }))} style={{ width: '100%', background: 'var(--color-surface)', border: '1px solid var(--color-border)', color: 'var(--color-text-primary)', fontSize: '0.6875rem', padding: '0.3rem', fontFamily: 'var(--font-mono)' }}>
                        <option value="all">Todos</option>
                        <option value="2016">2016</option>
                        <option value="2020">2020</option>
                      </select>
                    </div>
                  </Tooltip>
                  <Tooltip content="Filtrar por mes (1-12).">
                    <div>
                      <label style={{ display: 'block', fontSize: '0.625rem', color: 'var(--color-text-secondary)', marginBottom: '0.2rem' }}>MES</label>
                      <select value={gfwFilters.month} onChange={e => setGfwFilters(prev => ({ ...prev, month: e.target.value }))} style={{ width: '100%', background: 'var(--color-surface)', border: '1px solid var(--color-border)', color: 'var(--color-text-primary)', fontSize: '0.6875rem', padding: '0.3rem', fontFamily: 'var(--font-mono)' }}>
                        <option value="all">Todos</option>
                        {Array.from({length: 12}, (_, i) => i + 1).map(m => <option key={m} value={String(m)}>{String(m).padStart(2,'0')}</option>)}
                      </select>
                    </div>
                  </Tooltip>
                  <Tooltip content="Filtrar por tipo de arte de pesca (cerco, arrastre, palangre, etc.).">
                    <div>
                      <label style={{ display: 'block', fontSize: '0.625rem', color: 'var(--color-text-secondary)', marginBottom: '0.2rem' }}>ARTE</label>
                      <select value={gfwFilters.geartype} onChange={e => setGfwFilters(prev => ({ ...prev, geartype: e.target.value }))} style={{ width: '100%', background: 'var(--color-surface)', border: '1px solid var(--color-border)', color: 'var(--color-text-primary)', fontSize: '0.6875rem', padding: '0.3rem', fontFamily: 'var(--font-mono)' }}>
                        <option value="all">Todos</option>
                        <option value="tuna_purse_seines">Tuna Purse Seines</option>
                        <option value="fishing">Fishing (Generic)</option>
                        <option value="pole_and_line">Pole and Line</option>
                        <option value="trawlers">Trawlers</option>
                        <option value="other_purse_seines">Other Purse Seines</option>
                        <option value="set_gillnets">Set Gillnets</option>
                      </select>
                    </div>
                  </Tooltip>
                  <Tooltip content="Filtrar por bandera del país de la embarcación.">
                    <div>
                      <label style={{ display: 'block', fontSize: '0.625rem', color: 'var(--color-text-secondary)', marginBottom: '0.2rem' }}>BANDERA</label>
                      <select value={gfwFilters.flag} onChange={e => setGfwFilters(prev => ({ ...prev, flag: e.target.value }))} style={{ width: '100%', background: 'var(--color-surface)', border: '1px solid var(--color-border)', color: 'var(--color-text-primary)', fontSize: '0.6875rem', padding: '0.3rem', fontFamily: 'var(--font-mono)' }}>
                        <option value="all">Todos</option>
                        <option value="MEX">MEX</option>
                        <option value="BMU">BMU</option>
                        <option value="USA">USA</option>
                        <option value="UNKNOWN-MEX">UNKNOWN-MEX</option>
                        <option value="JAM">JAM</option>
                        <option value="CAN">CAN</option>
                      </select>
                    </div>
                  </Tooltip>
                </div>
                <div style={{ fontSize: '0.625rem', color: 'var(--color-text-muted)', marginTop: '0.5rem', fontFamily: 'var(--font-mono)' }}>
                  {filteredGfwData ? filteredGfwData.features.length : 0} / {layersData.gfw_fishing?.features.length || 0} celdas
                </div>

                {/* Heatmap Intensity Controls */}
                <div style={{ borderTop: '1px solid #6366F1', paddingTop: '0.75rem', marginTop: '0.75rem' }}>
                  <div style={{ fontSize: '0.6875rem', fontWeight: 800, color: '#6366F1', marginBottom: '0.5rem', letterSpacing: '0.05em' }}>
                    {'>'} INTENSIDAD HEATMAP
                  </div>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
                    <Tooltip content="Radio de influencia de cada punto de calor (px). Mayor = áreas más difusas.">
                      <div>
                        <label style={{ display: 'block', fontSize: '0.625rem', color: 'var(--color-text-secondary)', marginBottom: '0.2rem' }}>RADIO</label>
                        <input
                          type="range"
                          min="5"
                          max="50"
                          step="1"
                          value={heatmapOptions.radius}
                          onChange={e => setHeatmapOptions(prev => ({ ...prev, radius: parseInt(e.target.value) }))}
                          style={{ width: '100%', accentColor: '#6366F1', cursor: 'pointer' }}
                        />
                        <div style={{ fontSize: '0.5625rem', color: 'var(--color-text-muted)', textAlign: 'right' }}>{heatmapOptions.radius}px</div>
                      </div>
                    </Tooltip>
                    <Tooltip content="Desenfoque del borde de cada punto (px). Mayor = transición más suave.">
                      <div>
                        <label style={{ display: 'block', fontSize: '0.625rem', color: 'var(--color-text-secondary)', marginBottom: '0.2rem' }}>BLUR</label>
                        <input
                          type="range"
                          min="5"
                          max="30"
                          step="1"
                          value={heatmapOptions.blur}
                          onChange={e => setHeatmapOptions(prev => ({ ...prev, blur: parseInt(e.target.value) }))}
                          style={{ width: '100%', accentColor: '#6366F1', cursor: 'pointer' }}
                        />
                        <div style={{ fontSize: '0.5625rem', color: 'var(--color-text-muted)', textAlign: 'right' }}>{heatmapOptions.blur}px</div>
                      </div>
                    </Tooltip>
                    <Tooltip content="Valor máximo de intensidad para normalizar colores. Ajusta según rango de horas de pesca.">
                      <div>
                        <label style={{ display: 'block', fontSize: '0.625rem', color: 'var(--color-text-secondary)', marginBottom: '0.2rem' }}>MAX VALOR</label>
                        <input
                          type="range"
                          min="0.5"
                          max="10"
                          step="0.1"
                          value={heatmapOptions.max}
                          onChange={e => setHeatmapOptions(prev => ({ ...prev, max: parseFloat(e.target.value) }))}
                          style={{ width: '100%', accentColor: '#6366F1', cursor: 'pointer' }}
                        />
                        <div style={{ fontSize: '0.5625rem', color: 'var(--color-text-muted)', textAlign: 'right' }}>{heatmapOptions.max.toFixed(1)}</div>
                      </div>
                    </Tooltip>
                    <Tooltip content="Opacidad mínima visible (0-50%). Evita que zonas de bajo valor desaparezcan.">
                      <div>
                        <label style={{ display: 'block', fontSize: '0.625rem', color: 'var(--color-text-secondary)', marginBottom: '0.2rem' }}>OPACIDAD MÍN</label>
                        <input
                          type="range"
                          min="0.05"
                          max="0.5"
                          step="0.01"
                          value={heatmapOptions.minOpacity}
                          onChange={e => setHeatmapOptions(prev => ({ ...prev, minOpacity: parseFloat(e.target.value) }))}
                          style={{ width: '100%', accentColor: '#6366F1', cursor: 'pointer' }}
                        />
                        <div style={{ fontSize: '0.5625rem', color: 'var(--color-text-muted)', textAlign: 'right' }}>{(heatmapOptions.minOpacity * 100).toFixed(0)}%</div>
                      </div>
                    </Tooltip>
                  </div>
                </div>

                {/* Vessel Intelligence Report */}
                {vesselReport && (
                  <div style={{ borderTop: '1px solid #6366F1', paddingTop: '0.75rem', marginTop: '0.75rem' }}>
                    <div style={{ fontSize: '0.6875rem', fontWeight: 800, color: '#6366F1', marginBottom: '0.5rem', letterSpacing: '0.05em' }}>
                      {'>'} INTELIGENCIA DE EMBARCACIONES (GFW)
                    </div>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.3rem', fontSize: '0.625rem' }}>
                      <div><span style={{ color: 'var(--color-text-muted)' }}>Total Celdas:</span> <span style={{ color: 'var(--color-text-primary)', fontWeight: 700 }}>{vesselReport.totalVessels.toLocaleString()}</span></div>
                      <div><span style={{ color: 'var(--color-text-muted)' }}>Horas Pesca Totales:</span> <span style={{ color: 'var(--color-text-primary)', fontWeight: 700 }}>{vesselReport.totalHours.toLocaleString()}</span></div>
                      <div><span style={{ color: 'var(--color-text-muted)' }}>Embarcaciones Únicas:</span> <span style={{ color: 'var(--color-text-primary)', fontWeight: 700 }}>{vesselReport.uniqueMMSI.toLocaleString()}</span></div>
                      <div><span style={{ color: 'var(--color-text-muted)' }}>Rango Temporal:</span> <span style={{ color: 'var(--color-text-primary)', fontWeight: 700 }}>{vesselReport.timeRange.start} → {vesselReport.timeRange.end}</span></div>
                      <div><span style={{ color: 'var(--color-text-muted)' }}>Años Disponibles:</span> <span style={{ color: 'var(--color-text-primary)', fontWeight: 700 }}>{vesselReport.yearsAvailable.join(', ')}</span></div>
                      <div><span style={{ color: 'var(--color-text-muted)' }}>Actualizado:</span> <span style={{ color: 'var(--color-text-primary)', fontWeight: 700 }}>{vesselReport.lastUpdated}</span></div>
                    </div>
                    <div style={{ marginTop: '0.5rem', fontSize: '0.5625rem', color: 'var(--color-text-secondary)' }}>
                      <div style={{ fontWeight: 800, color: 'var(--color-ocean)', marginBottom: '0.2rem' }}>TOP BANDERAS:</div>
                      {vesselReport.topFlags.map((f, i) => (
                        <div key={i} style={{ display: 'flex', justifyContent: 'space-between', padding: '0.1rem 0' }}>
                          <span>{f.flag}</span>
                          <span style={{ fontWeight: 700, color: 'var(--color-text-primary)' }}>{f.count.toLocaleString()}</span>
                        </div>
                      ))}
                    </div>
                    <div style={{ marginTop: '0.5rem', fontSize: '0.5625rem', color: 'var(--color-text-secondary)' }}>
                      <div style={{ fontWeight: 800, color: 'var(--color-ocean)', marginBottom: '0.2rem' }}>TOP ARTES DE PESCA (HORAS):</div>
                      {vesselReport.topGearTypes.map((g, i) => (
                        <div key={i} style={{ display: 'flex', justifyContent: 'space-between', padding: '0.1rem 0' }}>
                          <span>{g.gear}</span>
                          <span style={{ fontWeight: 700, color: 'var(--color-text-primary)' }}>{g.hours.toLocaleString()}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Map Container */}
        <div>
          <div className="map-wrapper" style={{ height: '680px' }}>
            {/* Leyenda flotante — capas activas y escala IERC */}
            {(() => {
              const activeCfgs = LAYER_CONFIGS.filter(cfg => activeLayers[cfg.id] && cfg.id !== 'sener_gasoductos')
              if (activeCfgs.length === 0 && !activeLayers.h3_riesgo) return null
              return (
                <div style={{
                  position: 'absolute',
                  bottom: 36,
                  left: 10,
                  zIndex: 500,
                  background: 'rgba(10,10,10,0.92)',
                  border: '1px solid var(--color-border-hi)',
                  padding: '0.5rem 0.75rem',
                  fontFamily: 'var(--font-mono)',
                  minWidth: 180,
                  maxWidth: 225,
                }}>
                  {activeCfgs.length > 0 && (
                    <>
                      <div style={{ fontSize: '0.55rem', fontWeight: 800, color: 'var(--color-accent)', letterSpacing: '0.08em', marginBottom: '0.35rem' }}>
                        &gt; CAPAS ACTIVAS
                      </div>
                      {activeCfgs.map(cfg => (
                        <div key={cfg.id} style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', padding: '0.1rem 0' }}>
                          <span style={{ display: 'inline-block', width: 8, height: 8, flexShrink: 0, background: cfg.color }} />
                          <span style={{ fontSize: '0.5625rem', color: 'var(--color-text-secondary)', lineHeight: 1.3 }}>
                            {cfg.name.length > 30 ? cfg.name.slice(0, 30) + '…' : cfg.name}
                          </span>
                        </div>
                      ))}
                      <div style={{ borderTop: '1px dashed var(--color-border-hi)', margin: '0.5rem 0' }} />
                    </>
                  )}

                  {/* Rampa de color del IERC fija */}
                  <div style={{ fontSize: '0.55rem', fontWeight: 800, color: 'var(--color-accent)', letterSpacing: '0.08em', marginBottom: '0.35rem' }}>
                    &gt; RANGO DE RIESGO IERC
                  </div>
                  {[
                    { label: 'CRÍTICO (≥ 70.0)',  color: 'var(--color-alert)' },
                    { label: 'ALTO (50.0–69.9)',    color: 'var(--color-warn)' },
                    { label: 'MODERADO (30.0–49.9)',color: 'var(--color-amber)' },
                    { label: 'BAJO (< 30.0)',     color: 'var(--color-ok)' },
                  ].map(item => (
                    <div key={item.label} style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', padding: '0.1rem 0' }}>
                      <span style={{ display: 'inline-block', width: 8, height: 8, flexShrink: 0, background: item.color }} />
                      <span style={{ fontSize: '0.5625rem', color: 'var(--color-text-secondary)', lineHeight: 1.3 }}>
                        {item.label}
                      </span>
                    </div>
                  ))}
                </div>
              )
            })()}

            {loaded ? (
              <MapContainer
                center={[27.5, -111.8]}
                zoom={5}
                ref={mapRef}
                style={{ height: '100%', width: '100%' }}
                attributionControl={true}
                whenReady={() => {
                  if (mapRef.current) {
                    mapRef.current.invalidateSize()
                    setTimeout(() => {
                      mapRef.current?.invalidateSize()
                    }, 250)
                  }
                  mapRef.current?.on('zoomend', () => setMapZoom(mapRef.current?.getZoom() ?? 5))
                }}
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

                {/* Layer Ductos CNIH/SENER (Real ductos from CNIH ArcGIS) */}
                {activeLayers.ductos_cnih && layersData.ductos_cnih && (
                  <GeoJSON
                    key="ductos_cnih"
                    data={layersData.ductos_cnih}
                    style={(feat) => {
                      const p = feat?.properties || {}
                      const source = p.source_dataset || ''
                      // Color by source
                      let color = '#FF6B00'
                      if (source.includes('integrados')) color = '#FF6B00'
                      else if (source.includes('no_integrados')) color = '#FFB000'
                      else if (source.includes('poliductos')) color = '#00D4AA'
                      else if (source.includes('pacific')) color = '#A855F7'
                      
                      return {
                        color,
                        weight: 2.5,
                        opacity: 0.9,
                        dashArray: source.includes('pacific') ? '8, 4' : '0'
                      }
                    }}
                    onEachFeature={(feat, layer) => {
                      const p = feat?.properties || {}
                      const source = p.source_dataset || ''
                      const longitud = p.longitud_km ? `${Number(p.longitud_km).toFixed(1)} km` : 'N/A'
                      const capacidad = p.capacidad ? `${Number(p.capacidad).toLocaleString()}` : 'N/A'
                      
                      layer.bindPopup(
                        `<div style="font-family: monospace; font-size: 0.75rem; min-width: 260px;">
                          <b style="color: #FF6B00; font-size: 0.8125rem;">${p.nombre || p.ducto || 'Ducto CNIH'}</b><br/>
                          <b>FUENTE:</b> ${source.replace('_', ' ')}<br/>
                          <b>TIPO:</b> ${p.tipo || 'N/A'}<br/>
                          <b>LONGITUD:</b> ${longitud}<br/>
                          <b>CAPACIDAD:</b> ${capacidad} m³/d<br/>
                          <b>PROYECTO:</b> ${p.proyecto || 'N/A'}<br/>
                          <b>TRAMO:</b> ${p.tramo || 'N/A'}<br/>
                          <b>PERMISO:</b> ${p.permiso || 'N/A'}<br/>
                          <b>EMPRESA:</b> ${p.empresa || 'N/A'}<br/>
                          <div style="margin-top: 6px; font-size: 0.6875rem; color: #CCCCCC; border-top: 1px dashed #444; padding-top: 4px;">
                            FUENTE: CNIH/SENER ArcGIS (Capas: integrados, no_integrados, poliductos, Pacific Limited)
                          </div>
                        </div>`,
                        { maxWidth: 320 }
                      )
                    }}
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

                {/* Layer GFW Fishing Effort H3 - Heatmap at low zoom, circles at high zoom */}
                {activeLayers.gfw_fishing && filteredGfwData && mapZoom <= 7 && (
                  <Heatmap
                    latLngs={filteredGfwData.features.map((f: any) => [
                      f.geometry.coordinates[1],
                      f.geometry.coordinates[0],
                      f.properties?.hours || 0
                    ])}
                    options={heatmapOptions}
                  />
                )}
                {activeLayers.gfw_fishing && filteredGfwData && mapZoom > 7 && (
                  <GeoJSON
                    key="gfw_fishing"
                    data={filteredGfwData}
                    pointToLayer={(feature, latlng) => {
                      const L = getLeaflet()
                      if (!L) return null
                      const hours = feature.properties?.fishing_hours || 0
                      const intensity = Math.min(hours / 2, 1) // Ajustado para mayor visibilidad a zoom alto
                      const radius = 3 + intensity * 5
                      return L.circleMarker(latlng, {
                        radius,
                        fillColor: '#F97316', // Naranja brillante para contraste
                        fillOpacity: 0.3 + intensity * 0.5,
                        color: '#000000',
                        weight: 0.5,
                        opacity: 0.6,
                      })
                    }}
                    onEachFeature={(feature, layer) => {
                      const p = feature.properties ?? {}
                      layer.bindPopup(
                        `<div style="min-width: 240px; font-family: 'IBM Plex Mono', monospace;">
                          <div style="font-weight: 700; font-size: 0.8125rem; color: #FFFFFF; border-bottom: 1px solid #333; padding-bottom: 4px; margin-bottom: 8px;">
                            GFW Esfuerzo Pesquero (H3)
                          </div>
                          <div style="font-size: 0.75rem; color: #AAAAAA; margin-bottom: 6px;">
                            <b>H3 CELL:</b> ${p.h3_cell}<br/>
                            <b>HORAS PESCA:</b> ${Number(p.fishing_hours).toFixed(2)}<br/>
                            <b>HORAS TOTALES:</b> ${Number(p.hours).toFixed(2)}<br/>
                            <b>FLAG:</b> ${p.flag}<br/>
                            <b>ARTES:</b> ${p.geartype}<br/>
                            <b>AÑO:</b> ${p.year}<br/>
                            <b>MES:</b> ${p.month}
                          </div>
                          <div style="font-size: 0.6875rem; color: #666666; border-top: 1px dashed #333; padding-top: 6px;">
                            FUENTE: GFW Fleet Daily (Zenodo) / H3 Res 8 / 2016-2020
                          </div>
                        </div>`,
                        { maxWidth: 300 }
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
                    key={`h3_riesgo_conf_${confidenceThreshold}`}
                    data={layersData.h3_riesgo}
                    style={(feat) => {
                      const score = feat?.properties?.ierc_score || 50
                      const conf = feat?.properties?.confidence_score ?? 0.85
                      const isFiltered = confidenceThreshold > 0 && conf < confidenceThreshold

                      return {
                        fillColor: isFiltered ? '#1A1A1A' : getRiskColor(score),
                        fillOpacity: isFiltered ? 0.05 : 0.35,
                        color: isFiltered ? '#333333' : getRiskColor(score),
                        weight: isFiltered ? 0.2 : 0.5,
                        opacity: isFiltered ? 0.2 : 0.8
                      }
                    }}
                    onEachFeature={(feat, layer) => {
                      const p = feat.properties || {}
                      const conf = p.confidence_score ?? 0.85
                      layer.bindPopup(
                        `<div style="font-family: monospace; font-size: 0.75rem;">
                          <b>CELDA H3:</b> ${p.h3_index || p.h3_cell}<br/>
                          <b>SCORE IERC:</b> <strong style="color: ${getRiskColor(p.ierc_score)}">${p.ierc_score}</strong> (${p.nivel_riesgo || 'N/A'})<br/>
                          <b>CONFIANZA ESPACIAL:</b> <span style="color: ${conf >= 0.7 ? '#27AE60' : '#F39C12'};">${(conf * 100).toFixed(0)}%</span><br/>
                          <b>AMENAZA:</b> ${p.amenaza_score || 'N/A'}<br/>
                          <b>EXPOSICIÓN:</b> ${p.exposicion_score || 'N/A'}<br/>
                          <b>DIST. PROYECTO MÁS CERCANO:</b> ${p.distancia_proyecto_mas_cercano_km ?? 'N/A'} km
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
