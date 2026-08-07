'use client'

import React, { useState, useEffect, Suspense } from 'react'
import Header from './components/Header'
import RiskMap from './components/RiskMap'
import ZoneCards from './components/ZoneCards'
import GasInfraPanel from './components/GasInfraPanel'
import SpeciesPanel from './components/SpeciesPanel'
import MethodologyPanel from './components/MethodologyPanel'
import CoverageModal from './components/CoverageModal'
import ExportModal from './components/ExportModal'

const SECTIONS = [
  { id: 'mapa', label: 'VISOR ESPACIAL' },
  { id: 'terminales', label: 'TERMINALES GNL' },
  { id: 'gas', label: 'INFRAESTRUCTURA GAS' },
  { id: 'especies', label: 'ESPECIES' },
  { id: 'metodologia', label: 'METODOLOGÍA' },
] as const

function ScrollToTop() {
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const handleScroll = () => setVisible(window.scrollY > 400)
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const scrollToTop = () => window.scrollTo({ top: 0, behavior: 'smooth' })

  if (!visible) return null

  return (
    <button
      onClick={scrollToTop}
      style={{
        position: 'fixed',
        bottom: 24,
        right: 24,
        zIndex: 100,
        background: 'var(--color-surface-2)',
        border: '1px solid var(--color-accent)',
        color: 'var(--color-accent)',
        padding: '0.5rem 0.75rem',
        fontFamily: 'var(--font-mono)',
        fontSize: '0.6875rem',
        fontWeight: 700,
        cursor: 'pointer',
        borderRadius: 0,
        letterSpacing: '0.04em',
      }}
      onMouseOver={e => e.currentTarget.style.background = 'var(--color-surface-3)'}
      onMouseOut={e => e.currentTarget.style.background = 'var(--color-surface-2)'}
      aria-label="Volver arriba"
    >
      ↑ TOP
    </button>
  )
}

function SectionNav() {
  return (
    <nav style={{
      position: 'sticky',
      top: 80,
      zIndex: 50,
      background: 'var(--color-surface)',
      borderBottom: '1px solid var(--color-border)',
      padding: '0.35rem 1.5rem',
      display: 'flex',
      gap: '1rem',
      flexWrap: 'wrap',
      fontFamily: 'var(--font-mono)',
      fontSize: '0.625rem',
    }}>
      {SECTIONS.map(s => (
        <a
          key={s.id}
          href={`#${s.id}`}
          style={{
            color: 'var(--color-text-secondary)',
            textDecoration: 'none',
            padding: '0.15rem 0.5rem',
            border: '1px solid transparent',
            transition: 'color 0.15s ease, border-color 0.15s ease',
          }}
          onMouseOver={e => {
            e.currentTarget.style.color = 'var(--color-accent)'
            e.currentTarget.style.borderColor = 'var(--color-accent)'
          }}
          onMouseOut={e => {
            e.currentTarget.style.color = 'var(--color-text-secondary)'
            e.currentTarget.style.borderColor = 'transparent'
          }}
        >
          {s.label}
        </a>
      ))}
    </nav>
  )
}

function RiskMapWrapper() {
  return (
    <Suspense fallback={
      <div style={{ height: '680px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--color-text-muted)', fontFamily: 'var(--font-mono)' }}>
        [ CARGANDO MAPA... ]
      </div>
    }>
      <RiskMap />
    </Suspense>
  )
}

export default function Home() {
  const [isCoverageOpen, setIsCoverageOpen] = useState(false)
  const [isExportOpen, setIsExportOpen] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <div className="main-content">
      {sidebarOpen && (
        <div
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'rgba(0, 0, 0, 0.5)',
            zIndex: 40,
            display: 'block',
          }}
          onClick={() => setSidebarOpen(false)}
          aria-hidden="true"
        />
      )}

      <div
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          bottom: 0,
          width: 340,
          background: 'var(--color-surface)',
          borderRight: '1px solid var(--color-border)',
          zIndex: 50,
          transform: sidebarOpen ? 'translateX(0)' : 'translateX(-100%)',
          transition: 'transform 0.25s ease',
          boxShadow: '4px 0 16px rgba(0,0,0,0.3)',
        }}
        aria-hidden={!sidebarOpen}
      >
        <SectionNav />
      </div>

      <main
        style={{
          marginLeft: sidebarOpen ? 340 : 0,
          transition: 'margin-left 0.25s ease',
          minHeight: '100vh',
        }}
      >
        <Header
          onOpenCoverage={() => setIsCoverageOpen(true)}
          onOpenExport={() => setIsExportOpen(true)}
          onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
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
                onMouseOver={e => e.currentTarget.style.background = 'var(--color-surface-3)'}
                onMouseOut={e => e.currentTarget.style.background = 'var(--color-surface-2)'}
              >
                {' > EXPORTAR GPKG / CSV'}
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
                onMouseOver={e => e.currentTarget.style.background = 'var(--color-surface-3)'}
                onMouseOut={e => e.currentTarget.style.background = 'var(--color-surface-2)'}
              >
                {' > MATRIZ DE VACÍOS DE INFORMACIÓN'}
              </button>
            </div>
          </div>
        </div>

        <section id="mapa" style={{ scrollMarginTop: 100 }}>
          <RiskMapWrapper />
        </section>

        <section id="terminales" style={{ scrollMarginTop: 100 }}>
          <ZoneCards />
        </section>

        <section id="gas" style={{ scrollMarginTop: 100 }}>
          <GasInfraPanel />
        </section>

        <section id="especies" style={{ scrollMarginTop: 100 }}>
          <SpeciesPanel />
        </section>

        <section id="metodologia" style={{ scrollMarginTop: 100 }}>
          <MethodologyPanel />
        </section>

        <CoverageModal isOpen={isCoverageOpen} onClose={() => setIsCoverageOpen(false)} />

        <ExportModal isOpen={isExportOpen} onClose={() => setIsExportOpen(false)} />

        <ScrollToTop />
      </main>
    </div>
  )
}