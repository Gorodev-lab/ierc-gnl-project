'use client'

import React, { useState } from 'react'

interface ExportModalProps {
  isOpen: boolean
  onClose: () => void
}

const LAYERS = [
  { id: 'proyectos_gnl', name: '4 Terminales GNL (11 Features Vectoriales v3)', file: 'terminales_gnl_v3.geojson', desc: 'Puntos: Saguaro, Amigo, Vista Pacífico, Cosalá + buffers' },
  { id: 'poligonos_saguaro', name: 'Polígonos Detalle Saguaro MIA 181V', file: 'saguaro_polygons_181v.geojson', desc: '5 polígonos: Terminal, Campamentos, Viales, Áreas de influencia' },
  { id: 'capas_contexto', name: 'Gasoductos, Sitios Ramsar & ANPs', file: 'capas_contextuales.geojson', desc: 'LineStrings + Polygons: ductos, humedales, áreas protegidas' },
  { id: 'h3_riesgo', name: 'Malla H3 IERC (Res 8/9, Scores Riesgo)', file: 'grilla_h3_riesgo.geojson', desc: 'Hexágonos con score IERC, confianza, amenaza, exposición' },
  { id: 'gfw_fishing', name: 'GFW Esfuerzo Pesquero (H3, 9,960 Celdas)', file: 'gfw_fishing_h3.geojson', desc: 'Heatmap effort pesquero 2016-2020 por arte/bandera/año/mes' },
  { id: 'pangas', name: 'Zonas Pesqueras Multiespecie PANGAS (4,241)', file: 'zpesca_pangas_sample.geojson', desc: 'Polígonos pesca artesanal multiespecie con riqueza' },
  { id: 'riqueza', name: 'Riqueza Relativa Pesquera Acumulada (11,065)', file: 'riqueza_relativa_sample.geojson', desc: 'Índice acumulado de riqueza pesquera por zona' },
  { id: 'batimetria', name: 'Contornos Batimétricos GEBCO 2024', file: 'batimetria_golfo.geojson', desc: 'Isobatas -200m a -3000m, resolución 0.5km' },
  { id: 'buceo', name: 'Pesca por Buceo Artesanal (249 Polígonos)', file: 'zpesca_buceo_sample.geojson', desc: 'Zonas de buceo: pulpo, caracol, langosta' },
  { id: 'chinchorro', name: 'Chinchorro de Línea (2,209 Polígonos)', file: 'zpesca_chinchorro_sample.geojson', desc: 'Arte chinchorro: sierra, curvina, robalo' },
  { id: 'redes', name: 'Redes de Enmalle (1,263 Polígonos)', file: 'zpesca_redes_sample.geojson', desc: 'Redes fijas: tiburón, rayas, peces de fondo' },
  { id: 'trampa', name: 'Trampas Jaiberas (360 Polígonos)', file: 'zpesca_trampa_sample.geojson', desc: 'Trampas: jaiba, langosta, camarón profundo' },
]

export default function ExportModal({ isOpen, onClose }: ExportModalProps) {
  const [selectedLayer, setSelectedLayer] = useState('proyectos_gnl')
  const [isExporting, setIsExporting] = useState(false)
  const [exportFormat, setExportFormat] = useState<'csv' | 'geojson' | 'gpkg'>('csv')

  if (!isOpen) return null

  const activeLayerConfig = LAYERS.find((l) => l.id === selectedLayer) || LAYERS[0]

  const handleDownload = (format: 'csv' | 'geojson' | 'gpkg') => {
    setIsExporting(true)
    let url: string
    let filename: string

    if (format === 'gpkg') {
      url = '/api/export/gpkg'
      filename = 'ierc_golfo_california_v1.1.gpkg'
    } else if (format === 'csv') {
      url = `/api/export/csv?layer=${selectedLayer}`
      filename = `ierc_${selectedLayer}_export.csv`
    } else {
      url = `/data/${activeLayerConfig.file}`
      filename = activeLayerConfig.file
    }

    const link = document.createElement('a')
    link.href = url
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    setTimeout(() => setIsExporting(false), 1000)
  }

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.85)',
        zIndex: 1000,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '1.5rem',
        backdropFilter: 'blur(3px)',
      }}
    >
      <div
        style={{
          background: 'var(--color-surface, #0A0A0A)',
          border: '1px solid var(--color-accent, #F59E0B)',
          maxWidth: '760px',
          width: '100%',
          color: 'var(--color-text-primary, #FFFFFF)',
          fontFamily: 'var(--font-mono, monospace)',
          boxShadow: '0 0 32px rgba(245, 158, 11, 0.15)',
        }}
      >
        {/* Modal Header */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '1rem 1.25rem',
            borderBottom: '1px solid var(--color-border-hi, #333333)',
            background: 'var(--color-surface-2, #141414)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <span
              style={{
                background: 'var(--color-ok, #27AE60)',
                color: '#000000',
                fontWeight: 800,
                fontSize: '0.7rem',
                padding: '2px 6px',
              }}
            >
              [OGC GPKG v1.1]
            </span>
            <h3
              style={{
                fontSize: '0.95rem',
                fontWeight: 800,
                margin: 0,
                letterSpacing: '0.04em',
                color: 'var(--color-text-primary, #FFFFFF)',
              }}
            >
              EXPORTAR DATOS IERC-GNL — CAPAS & ENTREGABLES
            </h3>
          </div>

          <button
            onClick={onClose}
            style={{
              background: 'transparent',
              border: '1px solid var(--color-border, #444)',
              color: 'var(--color-text-secondary, #AAAAAA)',
              padding: '2px 8px',
              cursor: 'pointer',
              fontFamily: 'monospace',
              fontSize: '0.85rem',
            }}
          >
            [X]
          </button>
        </div>

        {/* Modal Body */}
        <div style={{ padding: '1.25rem', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {/* Section 1: Official GeoPackage */}
          <div
            style={{
              border: '1px solid var(--color-ok, #27AE60)',
              background: 'rgba(39, 174, 96, 0.05)',
              padding: '1rem',
              display: 'flex',
              flexDirection: 'column',
              gap: '0.75rem',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <h4 style={{ margin: 0, fontSize: '0.85rem', color: 'var(--color-ok, #27AE60)', fontWeight: 800 }}>
                  {'>'} ENTREGABLE OFICIAL: GPKG v1.1 (OGC GeoPackage)
                </h4>
                <p style={{ margin: '4px 0 0 0', fontSize: '0.72rem', color: 'var(--color-text-secondary, #BBBBBB)' }}>
                  7 capas base integradas · 5.9 MB · EPSG:4326 · SQLite OGC estándar
                </p>
              </div>

              <button
                onClick={() => handleDownload('gpkg')}
                disabled={isExporting}
                style={{
                  background: 'var(--color-ok, #27AE60)',
                  color: '#000000',
                  border: 'none',
                  padding: '8px 16px',
                  fontWeight: 800,
                  fontSize: '0.78rem',
                  fontFamily: 'monospace',
                  cursor: 'pointer',
                  whiteSpace: 'nowrap',
                }}
              >
                {isExporting ? 'DESCARGANDO...' : '↓ DESCARGAR GPKG OFICIAL (5.9 MB)'}
              </button>
            </div>

            <div
              style={{
                fontSize: '0.68rem',
                color: 'var(--color-text-muted, #888888)',
                borderTop: '1px dashed rgba(39, 174, 96, 0.3)',
                paddingTop: '6px',
                display: 'grid',
                gridTemplateColumns: 'repeat(3, 1fr)',
                gap: '0.5rem',
              }}
            >
              <span>● 4 Terminales GNL (11 features)</span>
              <span>● Malla H3 Riesgo (5,244 celdas)</span>
              <span>● Gasoductos (24 tramos, 6.4k km)</span>
              <span>● Zonas PANGAS (4,241 polígonos)</span>
              <span>● Riqueza Pesquera (11,065)</span>
              <span>● Batimetría GEBCO (1,146 contornos)</span>
            </div>
          </div>

          {/* Section 2: Layer Export */}
          <div
            style={{
              border: '1px solid var(--color-border-hi, #333333)',
              background: 'var(--color-surface-2, #141414)',
              padding: '1rem',
              display: 'flex',
              flexDirection: 'column',
              gap: '1rem',
            }}
          >
            <h4 style={{ margin: 0, fontSize: '0.85rem', color: 'var(--color-accent, #F59E0B)', fontWeight: 800 }}>
              {'>'} EXPORTAR CAPA INDIVIDUAL (CSV / GEOJSON)
            </h4>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              <label style={{ fontSize: '0.72rem', color: 'var(--color-text-secondary, #AAAAAA)' }}>
                SELECCIONAR CAPA DE DATOS:
              </label>
              <select
                value={selectedLayer}
                onChange={(e) => setSelectedLayer(e.target.value)}
                style={{
                  background: 'var(--color-surface, #0A0A0A)',
                  border: '1px solid var(--color-accent, #F59E0B)',
                  color: '#FFFFFF',
                  padding: '8px',
                  fontFamily: 'monospace',
                  fontSize: '0.78rem',
                  borderRadius: 0,
                  outline: 'none',
                }}
              >
                {LAYERS.map((layer) => (
                  <option key={layer.id} value={layer.id}>
                    {layer.name}
                  </option>
                ))}
              </select>
            </div>

            <div style={{ fontSize: '0.68rem', color: 'var(--color-text-muted, #888888)', marginTop: '0.25rem', padding: '0.5rem', background: 'var(--color-surface, #0A0A0A)', border: '1px solid var(--color-border, #333333)' }}>
              <strong>{activeLayerConfig.name}</strong><br/>
              {activeLayerConfig.desc}
            </div>

            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
                <input
                  type="radio"
                  value="csv"
                  checked={exportFormat === 'csv'}
                  onChange={() => setExportFormat('csv')}
                  style={{ accentColor: 'var(--color-accent, #F59E0B)' }}
                />
                <span style={{ fontSize: '0.72rem', color: 'var(--color-text-secondary)' }}>CSV (tabular con BOM)</span>
              </label>
              <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
                <input
                  type="radio"
                  value="geojson"
                  checked={exportFormat === 'geojson'}
                  onChange={() => setExportFormat('geojson')}
                  style={{ accentColor: 'var(--color-ocean, #38BDF8)' }}
                />
                <span style={{ fontSize: '0.72rem', color: 'var(--color-text-secondary)' }}>GeoJSON (geometrías)</span>
              </label>
            </div>

            <div style={{ display: 'flex', gap: '0.75rem', marginTop: '0.5rem' }}>
              <button
                onClick={() => handleDownload(exportFormat)}
                disabled={isExporting}
                style={{
                  flex: 1,
                  background: exportFormat === 'csv' ? 'var(--color-accent, #F59E0B)' : 'var(--color-ocean, #38BDF8)',
                  color: '#000000',
                  border: 'none',
                  padding: '8px 12px',
                  fontWeight: 800,
                  fontSize: '0.75rem',
                  fontFamily: 'monospace',
                  cursor: 'pointer',
                  textAlign: 'center',
                }}
              >
                {isExporting ? 'EXPORTANDO...' : exportFormat === 'csv' ? '↓ EXPORTAR CSV' : '↓ EXPORTAR GEOJSON'}
              </button>

              <button
                onClick={() => handleDownload('gpkg')}
                disabled={isExporting}
                style={{
                  flex: 1,
                  background: 'var(--color-ok, #27AE60)',
                  color: '#000000',
                  border: 'none',
                  padding: '8px 12px',
                  fontWeight: 800,
                  fontSize: '0.75rem',
                  fontFamily: 'monospace',
                  cursor: 'pointer',
                  textAlign: 'center',
                }}
              >
                ↓ GPKG COMPLETO
              </button>
            </div>
          </div>

          {/* Section 3: Metadata & Citation */}
          <div
            style={{
              fontSize: '0.68rem',
              color: 'var(--color-text-muted, #888888)',
              background: 'var(--color-surface, #0A0A0A)',
              padding: '0.75rem',
              border: '1px dashed var(--color-border, #333333)',
            }}
          >
            <b>ESPECIFICACIONES TÉCNICAS:</b> Proyección EPSG:4326 (WGS84) · Codificación UTF-8 con BOM (CSV) · RFC 7946 (GeoJSON) · OGC GeoPackage v1.1 (GPKG).
            <br/><br/>
            <b>CITACIÓN REQUERIDA:</b> Gorosave Meza, E. (2026). <i>Inventario Espacial IERC-GNL v2.3</i>. Causa Natura Center. Golfo de California, México.
            <br/><br/>
            <b>METADATOS:</b> 14 fuentes Silver · 13 productos Gold · PANGAS GDB · GFW Zenodo · CNIH ArcGIS · NASA OceanColor · GEBCO 2024.
            <br/><br/>
            <b>VERSIÓN:</b> Inventario v2.3 · POA 2026-2028 · Entregable OGC v1.1.
          </div>
        </div>

        {/* Modal Footer */}
        <div
          style={{
            padding: '0.75rem 1.25rem',
            borderTop: '1px solid var(--color-border-hi, #333333)',
            background: 'var(--color-surface-2, #141414)',
            display: 'flex',
            justifyContent: 'flex-end',
            gap: '0.5rem',
          }}
        >
          <button
            onClick={onClose}
            style={{
              background: 'var(--color-surface-3, #222222)',
              border: '1px solid var(--color-border-hi, #444444)',
              color: '#FFFFFF',
              padding: '6px 14px',
              fontFamily: 'monospace',
              fontSize: '0.75rem',
              fontWeight: 700,
              cursor: 'pointer',
            }}
          >
            CERRAR
          </button>
        </div>
      </div>
    </div>
  )
}