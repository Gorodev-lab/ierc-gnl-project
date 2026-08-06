'use client'

import React, { useState } from 'react'

interface ExportModalProps {
  isOpen: boolean
  onClose: () => void
}

const LAYERS = [
  { id: 'proyectos_gnl', name: '4 Terminales GNL (11 Features Vectoriales v3)', file: 'terminales_gnl_v3.geojson' },
  { id: 'poligonos_saguaro', name: 'Polígonos Detalle Saguaro MIA 181V', file: 'saguaro_polygons_181v.geojson' },
  { id: 'capas_contexto', name: 'Gasoductos, Sitios Ramsar & ANPs', file: 'capas_contextuales.geojson' },
  { id: 'h3_riesgo', name: 'Malla H3 IERC (Res 8/9, Scores Riesgo)', file: 'grilla_h3_riesgo.geojson' },
  { id: 'gfw_fishing', name: 'GFW Esfuerzo Pesquero (H3, 9,960 Celdas)', file: 'gfw_fishing_h3.geojson' },
  { id: 'pangas', name: 'Zonas Pesqueras Multiespecie PANGAS (4,241)', file: 'zpesca_pangas_sample.geojson' },
  { id: 'riqueza', name: 'Riqueza Relativa Pesquera Acumulada (11,065)', file: 'riqueza_relativa_sample.geojson' },
  { id: 'batimetria', name: 'Contornos Batimétricos GEBCO 2024', file: 'batimetria_golfo.geojson' },
  { id: 'buceo', name: 'Pesca por Buceo Artesanal (249 Polígonos)', file: 'zpesca_buceo_sample.geojson' },
  { id: 'chinchorro', name: 'Chinchorro de Línea (2,209 Polígonos)', file: 'zpesca_chinchorro_sample.geojson' },
  { id: 'redes', name: 'Redes de Enmalle (1,263 Polígonos)', file: 'zpesca_redes_sample.geojson' },
  { id: 'trampa', name: 'Trampas Jaiberas (360 Polígonos)', file: 'zpesca_trampa_sample.geojson' },
]

export default function ExportModal({ isOpen, onClose }: ExportModalProps) {
  const [selectedLayer, setSelectedLayer] = useState('proyectos_gnl')
  const [isExporting, setIsExporting] = useState(false)

  if (!isOpen) return null

  const activeLayerConfig = LAYERS.find((l) => l.id === selectedLayer) || LAYERS[0]

  const handleDownloadGpkg = () => {
    setIsExporting(true)
    const link = document.createElement('a')
    link.href = '/api/export/gpkg'
    link.download = 'ierc_golfo_california_v1.1.gpkg'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    setTimeout(() => setIsExporting(false), 1000)
  }

  const handleDownloadCsv = () => {
    setIsExporting(true)
    const link = document.createElement('a')
    link.href = `/api/export/csv?layer=${selectedLayer}`
    link.download = `ierc_${selectedLayer}_export.csv`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    setTimeout(() => setIsExporting(false), 1000)
  }

  const handleDownloadGeoJson = () => {
    setIsExporting(true)
    const link = document.createElement('a')
    link.href = `/data/${activeLayerConfig.file}`
    link.download = activeLayerConfig.file
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
          maxWidth: '720px',
          width: '100%',
          color: 'var(--color-text-primary, #FFFFFF)',
          fontFamily: 'var(--font-mono, monospace)',
          boxShadow: '0 0 25px rgba(245, 158, 11, 0.15)',
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
              EXPORTAR DATOS ESPACIALES & REPORTES IERC-GNL
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
        <div style={{ padding: '1.25rem', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          {/* Section 1: Official GeoPackage Download */}
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
                  &gt; ENTREGABLE OFICIAL GEOPACKAGE (.GPKG v1.1)
                </h4>
                <p style={{ margin: '4px 0 0 0', fontSize: '0.72rem', color: 'var(--color-text-secondary, #BBBBBB)' }}>
                  Contiene las 7 capas base integradas en formato OGC SQLite estándar (5.9 MB, EPSG:4326).
                </p>
              </div>

              <button
                onClick={handleDownloadGpkg}
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
                {isExporting ? 'DESCARGANDO...' : '↓ DESCARGAR GPKG (5.9 MB)'}
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
              <span>● Proyectos GNL (5 point features)</span>
              <span>● Zonas PANGAS (17 multipolygons)</span>
              <span>● Malla H3 Riesgo (5,244 celdas)</span>
              <span>● Gasoductos (2 linestrings)</span>
              <span>● Riqueza Pesquera (11,065 poly)</span>
              <span>● Localidades POA (3 points)</span>
            </div>
          </div>

          {/* Section 2: Layer-by-Layer Export (CSV / GeoJSON) */}
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
              &gt; EXPORTAR CAPA ESPECÍFICA (TABULAR CSV / GEOJSON)
            </h4>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
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

            {/* Export Buttons */}
            <div style={{ display: 'flex', gap: '0.75rem', marginTop: '0.25rem' }}>
              <button
                onClick={handleDownloadCsv}
                disabled={isExporting}
                style={{
                  flex: 1,
                  background: 'var(--color-surface-3, #1F1F1F)',
                  border: '1px solid var(--color-accent, #F59E0B)',
                  color: 'var(--color-accent, #F59E0B)',
                  padding: '8px 12px',
                  fontWeight: 800,
                  fontSize: '0.75rem',
                  fontFamily: 'monospace',
                  cursor: 'pointer',
                  textAlign: 'center',
                }}
              >
                ↓ EXPORTAR CSV (TABULAR CON BOM)
              </button>

              <button
                onClick={handleDownloadGeoJson}
                disabled={isExporting}
                style={{
                  flex: 1,
                  background: 'var(--color-surface-3, #1F1F1F)',
                  border: '1px solid var(--color-ocean, #38BDF8)',
                  color: 'var(--color-ocean, #38BDF8)',
                  padding: '8px 12px',
                  fontWeight: 800,
                  fontSize: '0.75rem',
                  fontFamily: 'monospace',
                  cursor: 'pointer',
                  textAlign: 'center',
                }}
              >
                ↓ DESCARGAR GEOJSON ORIGINAL
              </button>
            </div>
          </div>

          {/* Section 3: Technical Specifications & Citation */}
          <div
            style={{
              fontSize: '0.68rem',
              color: 'var(--color-text-muted, #888888)',
              background: 'var(--color-surface, #0A0A0A)',
              padding: '0.75rem',
              border: '1px dashed var(--color-border, #333333)',
            }}
          >
            <b>CITACIÓN OFICIAL DE DATOS:</b> Gorosave Meza, E. (2026). <i>Inventario Espacial IERC-GNL v2.1</i>. Causa Natura Center. Golfo de California, México. Proyección EPSG:4326 (WGS84).
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
            CERRAR VENTANA
          </button>
        </div>
      </div>
    </div>
  )
}
