'use client'

import React, { useState } from 'react'
import Header from './components/Header'
import RiskMap from './components/RiskMap'
import ZoneCards from './components/ZoneCards'
import SpeciesPanel from './components/SpeciesPanel'
import MethodologyPanel from './components/MethodologyPanel'
import CoverageModal from './components/CoverageModal'

export default function Home() {
  const [isCoverageOpen, setIsCoverageOpen] = useState(false)

  return (
    <div className="main-content">
      <Header onOpenCoverage={() => setIsCoverageOpen(true)} />

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
              <span style={{ color: 'var(--color-amber)', fontWeight: 700 }}>[CAUSA NATURA CENTER]</span>{' '}
              Evaluación espacial del <strong style={{ color: 'var(--color-amber)' }}>Índice Espacial de Riesgo Socioeconómico para Comunidades (IERC)</strong> ante
              proyectos de Gas Natural Licuado (GNL) en el Golfo de California. Datos integrados en el entregable{' '}
              <code style={{ background: 'var(--color-surface-2)', padding: '0.15rem 0.4rem', border: '1px solid var(--color-border-hi)', color: 'var(--color-ocean)' }}>
                ierc_golfo_california.gpkg
              </code>.
            </p>
          </div>

          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '1rem'
          }}>
            <button
              onClick={() => setIsCoverageOpen(true)}
              style={{
                background: 'var(--color-surface-2)',
                border: '1px solid var(--color-amber)',
                color: 'var(--color-amber)',
                padding: '0.5rem 0.875rem',
                fontFamily: 'var(--font-mono)',
                fontSize: '0.75rem',
                fontWeight: 700,
                cursor: 'pointer',
                boxShadow: '0 0 10px rgba(245, 158, 11, 0.2)'
              }}
            >
              📊 VER VACÍOS & COBERTURA DE DATOS
            </button>
          </div>
        </div>
      </div>

      {/* Map Section */}
      <RiskMap />

      {/* Zone Cards */}
      <ZoneCards />

      {/* Species Panel */}
      <SpeciesPanel />

      {/* Methodology */}
      <MethodologyPanel />

      {/* Modal reportes */}
      <CoverageModal isOpen={isCoverageOpen} onClose={() => setIsCoverageOpen(false)} />
    </div>
  )
}
