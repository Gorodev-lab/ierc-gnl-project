'use client'

import React, { useState } from 'react'
import Header from './components/Header'
import RiskMap from './components/RiskMap'
import ZoneCards from './components/ZoneCards'
import GasInfraPanel from './components/GasInfraPanel'
import SpeciesPanel from './components/SpeciesPanel'
import MethodologyPanel from './components/MethodologyPanel'
import CoverageModal from './components/CoverageModal'
import ExportModal from './components/ExportModal'

export default function Home() {
  const [isCoverageOpen, setIsCoverageOpen] = useState(false)
  const [isExportOpen, setIsExportOpen] = useState(false)

  return (
    <div className="main-content">
      <Header
        onOpenCoverage={() => setIsCoverageOpen(true)}
        onOpenExport={() => setIsExportOpen(true)}
      />

      {/* Terminal Intro Banner */}
      <div style={{
        background: 'var(--color-surface)',
        borderBottom: '1px solid var(--color-border)',
        padding: '1.25rem 1.5rem',
      }}>
        <div style={{ maxWidth: 1400, margin: '0 auto', display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '1rem', flexWrap: 'wrap' }}>
          <div style={{ maxWidth: 850 }}>
            <p style={{
              fontSize: '0.8125rem',
              color: 'var(--color-text-secondary)',
              lineHeight: 1.6,
              fontFamily: 'var(--font-mono)',
            }}>
              <span style={{ color: 'var(--color-accent)', fontWeight: 800 }}>[CAUSA NATURA CENTER]</span>{' '}
              Evaluación espacial e instrumento metodológico del <strong style={{ color: 'var(--color-accent)' }}>Índice Espacial de Riesgo Socioeconómico para Comunidades (IERC)</strong> ante
              proyectos de Gas Natural Licuado (GNL) en el Golfo de California. Entregable geográfico OGC v1.1:{' '}
              <code style={{ background: 'var(--color-surface-2)', padding: '0.15rem 0.45rem', border: '1px solid var(--color-border-hi)', color: 'var(--color-ocean)', borderRadius: 0 }}>
                deliverables/v1_geopackage/ierc_golfo_california.gpkg
              </code>.
            </p>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <button
              onClick={() => setIsExportOpen(true)}
              style={{
                background: 'var(--color-surface-2)',
                border: '1px solid var(--color-ok)',
                color: 'var(--color-ok)',
                padding: '0.5rem 0.875rem',
                fontFamily: 'var(--font-mono)',
                fontSize: '0.75rem',
                fontWeight: 800,
                cursor: 'pointer',
                borderRadius: 0,
                letterSpacing: '0.04em',
                transition: 'background 0.15s ease',
              }}
              onMouseOver={(e) => e.currentTarget.style.background = 'var(--color-surface-3)'}
              onMouseOut={(e) => e.currentTarget.style.background = 'var(--color-surface-2)'}
            >
              &gt; EXPORTAR GPKG / CSV
            </button>

            <button
              onClick={() => setIsCoverageOpen(true)}
              style={{
                background: 'var(--color-surface-2)',
                border: '1px solid var(--color-accent)',
                color: 'var(--color-accent)',
                padding: '0.5rem 0.875rem',
                fontFamily: 'var(--font-mono)',
                fontSize: '0.75rem',
                fontWeight: 800,
                cursor: 'pointer',
                borderRadius: 0,
                letterSpacing: '0.04em',
                transition: 'background 0.15s ease',
              }}
              onMouseOver={(e) => e.currentTarget.style.background = 'var(--color-surface-3)'}
              onMouseOut={(e) => e.currentTarget.style.background = 'var(--color-surface-2)'}
            >
              &gt; MATRIZ DE VACÍOS DE INFORMACIÓN
            </button>
          </div>
        </div>
      </div>

      {/* Visor Espacial Interactivo Map Section */}
      <RiskMap />

      {/* Terminales & Polígonos Pesqueros PANGAS */}
      <ZoneCards />

      {/* Infraestructura Gas Natural — SISTRANGAS & CNIH/SENER */}
      <GasInfraPanel />

      {/* Especies & Biodiversidad */}
      <SpeciesPanel />

      {/* Metodología & Formulación Matemática */}
      <MethodologyPanel />

      {/* Modal de cobertura */}
      <CoverageModal isOpen={isCoverageOpen} onClose={() => setIsCoverageOpen(false)} />

      {/* Modal de exportación */}
      <ExportModal isOpen={isExportOpen} onClose={() => setIsExportOpen(false)} />
    </div>
  )
}
