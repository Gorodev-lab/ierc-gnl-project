'use client'

import React, { useState, useEffect } from 'react'

export interface MiaAsset {
  id: string
  proyecto: string
  titulo: string
  tipo_plano: string
  url: string
  fuente_pdf: string
  pagina: number
}

interface MiaInspectorModalProps {
  isOpen: boolean
  onClose: () => void
  featureProps: Record<string, any> | null
}

export default function MiaInspectorModal({ isOpen, onClose, featureProps }: MiaInspectorModalProps) {
  const [manifest, setManifest] = useState<MiaAsset[]>([])
  const [activeCategory, setActiveCategory] = useState<string>('TODOS')
  const [selectedImage, setSelectedImage] = useState<MiaAsset | null>(null)

  useEffect(() => {
    if (isOpen && manifest.length === 0) {
      fetch('/assets/mias/manifest.json')
        .then(res => res.json())
        .then(data => setManifest(data))
        .catch(() => {})
    }
  }, [isOpen, manifest.length])

  if (!isOpen || !featureProps) return null

  // Mapeo de clave de proyecto hacia clave de assets en manifest.json
  const projNameLower = (featureProps.proyecto || '').toLowerCase()
  let projKey = 'saguaro'
  if (projNameLower.includes('amigo')) projKey = 'amigo'
  else if (projNameLower.includes('vista') || projNameLower.includes('pacifico')) projKey = 'vista_pacifico'
  else if (projNameLower.includes('cosal') || projNameLower.includes('cosalá')) projKey = 'cosala'
  else if (projNameLower.includes('saguaro')) projKey = 'saguaro'

  const projectAssets = manifest.filter(item => item.proyecto === projKey)

  const filteredAssets = activeCategory === 'TODOS'
    ? projectAssets
    : projectAssets.filter(item => {
        if (activeCategory === 'MACROLOCALIZACION') return item.tipo_plano === 'macrolocalizacion' || item.tipo_plano === 'microlocalizacion'
        if (activeCategory === 'DISTRIBUCION') return item.tipo_plano === 'distribucion_planta'
        if (activeCategory === 'TABLAS') return item.tipo_plano === 'tabla_coordenadas'
        if (activeCategory === 'AMBIENTAL') return item.tipo_plano === 'ambiental'
        return true
      })

  // Determinar color y etiqueta de precisión
  const precisionLabel = featureProps.precision_label || '[APROXIMADO]'
  let precisionColor = '#C0392B' // Accent alert
  if (precisionLabel.includes('EXACTO')) precisionColor = '#27AE60'
  else if (precisionLabel.includes('CALCULADO')) precisionColor = '#F39C12'

  return (
    <div style={{
      position: 'fixed',
      top: 0, left: 0, right: 0, bottom: 0,
      background: 'rgba(10, 10, 10, 0.92)',
      zIndex: 9999,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '1.5rem',
      fontFamily: "'IBM Plex Mono', monospace"
    }}>
      <div style={{
        background: '#111111',
        border: '1px solid #222222',
        width: '100%',
        maxWidth: '1050px',
        maxHeight: '90vh',
        display: 'flex',
        flexDirection: 'column',
        boxSizing: 'border-box'
      }}>
        {/* Top Header */}
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          padding: '1rem 1.25rem',
          borderBottom: '1px solid #222222',
          background: '#0A0A0A'
        }}>
          <div>
            <div style={{ fontSize: '0.75rem', color: 'var(--color-accent, #C0392B)', fontWeight: 600, letterSpacing: '0.05em' }}>
              &gt; INSPECTOR DE MANIFESTACIÓN DE IMPACTO AMBIENTAL (MIA / ASEA)
            </div>
            <h2 style={{ fontSize: '1.25rem', color: '#FFFFFF', margin: '0.25rem 0 0 0', fontWeight: 700 }}>
              {featureProps.proyecto || 'TERMINAL GNL'} — {featureProps.componente || ''}
            </h2>
          </div>
          <button
            onClick={onClose}
            style={{
              background: '#111111',
              border: '1px solid #222222',
              color: '#FFFFFF',
              padding: '0.4rem 0.8rem',
              cursor: 'pointer',
              fontFamily: "'IBM Plex Mono', monospace",
              fontSize: '0.8125rem',
              fontWeight: 700
            }}
          >
            [X] CERRAR
          </button>
        </div>

        {/* Modal Body Grid */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: '320px 1fr',
          flex: 1,
          overflow: 'hidden'
        }}>
          {/* Metadata Sidebar */}
          <div style={{
            padding: '1.25rem',
            borderRight: '1px solid #222222',
            background: '#0A0A0A',
            overflowY: 'auto',
            display: 'flex',
            flexDirection: 'column',
            gap: '1rem',
            fontSize: '0.75rem'
          }}>
            <div>
              <span style={{ color: '#666666', display: 'block', marginBottom: '0.25rem' }}>MATRIZ DE PRECISIÓN GEOMÉTRICA</span>
              <span style={{
                display: 'inline-block',
                padding: '0.25rem 0.5rem',
                background: '#111111',
                border: `1px solid ${precisionColor}`,
                color: precisionColor,
                fontWeight: 700
              }}>
                {precisionLabel}
              </span>
            </div>

            <div>
              <span style={{ color: '#666666', display: 'block' }}>ESTATUS PROYECTO</span>
              <span style={{ color: '#FFFFFF', fontWeight: 600 }}>{featureProps.status || 'No especificado'}</span>
            </div>

            <div>
              <span style={{ color: '#666666', display: 'block' }}>PROMOVENTE / EMPRESA</span>
              <span style={{ color: '#AAAAAA' }}>{featureProps.promovente || featureProps.empresa_madre || 'N/A'}</span>
            </div>

            <div>
              <span style={{ color: '#666666', display: 'block' }}>UBICACIÓN INSTITUCIONAL</span>
              <span style={{ color: '#AAAAAA' }}>
                {featureProps.municipio}, {featureProps.estado} ({featureProps.localidad})
              </span>
            </div>

            <div>
              <span style={{ color: '#666666', display: 'block' }}>CAPACIDAD DE LICUEFACCIÓN</span>
              <span style={{ color: '#FFFFFF', fontWeight: 700, fontSize: '0.875rem' }}>
                {featureProps.capacidad_mtpa ? `${featureProps.capacidad_mtpa} MTPA` : 'N/A / No aplica'}
              </span>
            </div>

            <div>
              <span style={{ color: '#666666', display: 'block' }}>SUPERFICIE / ÁREA</span>
              <span style={{ color: '#AAAAAA' }}>
                {featureProps.superficie_ha ? `${featureProps.superficie_ha} ha` : 'No especificada'}
              </span>
            </div>

            <div>
              <span style={{ color: '#666666', display: 'block' }}>CLAVE EXPEDIENTE ASEA / GACETA</span>
              <span style={{ color: '#C0392B', fontWeight: 500, wordBreak: 'break-all' }}>
                {featureProps.clave_asea || 'En trámite / Reservado'}
              </span>
            </div>

            <div style={{ borderTop: '1px solid #222222', paddingTop: '0.75rem' }}>
              <span style={{ color: '#666666', display: 'block', marginBottom: '0.25rem' }}>FUENTE DE COORDENADAS</span>
              <p style={{ color: '#AAAAAA', margin: 0, lineHeight: 1.5 }}>
                {featureProps.fuente_coordenadas || 'Documentos oficiales ASEA / Gaceta Ecológica'}
              </p>
            </div>
          </div>

          {/* MIA Image Gallery Content */}
          <div style={{
            padding: '1.25rem',
            overflowY: 'auto',
            display: 'flex',
            flexDirection: 'column',
            gap: '1rem'
          }}>
            {/* Category Tabs */}
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', borderBottom: '1px solid #222222', paddingBottom: '0.75rem' }}>
              {[
                { id: 'TODOS', label: 'TODOS LOS PLANOS' },
                { id: 'MACROLOCALIZACION', label: 'MACRO/MICRO LOCALIZACIÓN' },
                { id: 'DISTRIBUCION', label: 'DISTRIBUCIÓN DE PLANTA' },
                { id: 'TABLAS', label: 'TABLAS DE COORDENADAS' },
                { id: 'AMBIENTAL', label: 'RESERVA AMBIENTAL' }
              ].map(tab => (
                <button
                  key={tab.id}
                  onClick={() => setActiveCategory(tab.id)}
                  style={{
                    background: activeCategory === tab.id ? '#C0392B' : '#0A0A0A',
                    border: '1px solid #222222',
                    color: activeCategory === tab.id ? '#FFFFFF' : '#AAAAAA',
                    padding: '0.35rem 0.65rem',
                    fontSize: '0.6875rem',
                    fontFamily: "'IBM Plex Mono', monospace",
                    cursor: 'pointer',
                    fontWeight: activeCategory === tab.id ? 700 : 400
                  }}
                >
                  {tab.label}
                </button>
              ))}
            </div>

            {/* Assets Grid */}
            {filteredAssets.length > 0 ? (
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
                gap: '1rem'
              }}>
                {filteredAssets.map(asset => (
                  <div
                    key={asset.id}
                    onClick={() => setSelectedImage(asset)}
                    style={{
                      background: '#0A0A0A',
                      border: '1px solid #222222',
                      padding: '0.75rem',
                      cursor: 'pointer',
                      display: 'flex',
                      flexDirection: 'column',
                      gap: '0.5rem'
                    }}
                  >
                    <div style={{
                      width: '100%',
                      height: '160px',
                      background: '#111111',
                      border: '1px solid #222222',
                      overflow: 'hidden',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center'
                    }}>
                      <img
                        src={asset.url}
                        alt={asset.titulo}
                        style={{ maxWidth: '100%', maxHeight: '100%', objectFit: 'contain' }}
                      />
                    </div>
                    <div>
                      <div style={{ fontSize: '0.6875rem', color: '#C0392B', fontWeight: 600 }}>
                        &gt; {asset.tipo_plano.toUpperCase()} (PÁG. {asset.pagina})
                      </div>
                      <div style={{ fontSize: '0.75rem', color: '#FFFFFF', fontWeight: 600, marginTop: '0.2rem' }}>
                        {asset.titulo}
                      </div>
                      <div style={{ fontSize: '0.65rem', color: '#666666', marginTop: '0.2rem' }}>
                        Fuente: {asset.fuente_pdf}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div style={{
                padding: '3rem',
                textAlign: 'center',
                color: '#666666',
                background: '#0A0A0A',
                border: '1px solid #222222',
                fontSize: '0.8125rem'
              }}>
                No se encontraron planos registrados en esta categoría para la MIA del proyecto {featureProps.proyecto}.
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div style={{
          padding: '0.75rem 1.25rem',
          borderTop: '1px solid #222222',
          background: '#0A0A0A',
          fontSize: '0.6875rem',
          color: '#666666',
          display: 'flex',
          justifyContent: 'space-between'
        }}>
          <span>ESOTERIA INTEL / IERC-GNL VISOR ESPACIAL v3</span>
          <span>SISTEMA DE AUDITORÍA SOCIOAMBIENTAL — GOLFO DE CALIFORNIA</span>
        </div>
      </div>

      {/* Lightbox Modal for Selected Image */}
      {selectedImage && (
        <div
          onClick={() => setSelectedImage(null)}
          style={{
            position: 'fixed',
            top: 0, left: 0, right: 0, bottom: 0,
            background: 'rgba(0,0,0,0.95)',
            zIndex: 10000,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '2rem'
          }}
        >
          <div
            onClick={e => e.stopPropagation()}
            style={{
              background: '#111111',
              border: '1px solid #222222',
              maxWidth: '95vw',
              maxHeight: '90vh',
              padding: '1rem',
              display: 'flex',
              flexDirection: 'column',
              gap: '1rem'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '0.875rem', color: '#FFFFFF', fontWeight: 700 }}>
                &gt; {selectedImage.titulo} ({selectedImage.fuente_pdf} - Pág. {selectedImage.pagina})
              </span>
              <button
                onClick={() => setSelectedImage(null)}
                style={{
                  background: '#0A0A0A',
                  border: '1px solid #222222',
                  color: '#FFFFFF',
                  padding: '0.3rem 0.6rem',
                  fontFamily: "'IBM Plex Mono', monospace",
                  cursor: 'pointer'
                }}
              >
                [X] CERRAR VISTA
              </button>
            </div>
            <div style={{ overflow: 'auto', textAlign: 'center', maxHeight: '78vh' }}>
              <img
                src={selectedImage.url}
                alt={selectedImage.titulo}
                style={{ maxWidth: '100%', maxHeight: '75vh', objectFit: 'contain' }}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
