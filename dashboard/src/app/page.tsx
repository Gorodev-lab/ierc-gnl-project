import Header from './components/Header'
import RiskMap from './components/RiskMap'
import ZoneCards from './components/ZoneCards'
import SpeciesPanel from './components/SpeciesPanel'
import MethodologyPanel from './components/MethodologyPanel'

export default function Home() {
  return (
    <div className="main-content">
      <Header />

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
              <span style={{ color: 'var(--color-amber)', fontWeight: 700 }}>[ZOHAR v4 / ESOTERIA v2]</span>{' '}
              Evaluación espacial del <strong style={{ color: 'var(--color-amber)' }}>Índice Espacial de Riesgo Socioeconómico para Comunidades (IERC)</strong> ante
              proyectos de Gas Natural Licuado (GNL) en el Golfo de California. Datos integrados en el entregable{' '}
              <code style={{ background: 'var(--color-surface-2)', padding: '0.15rem 0.4rem', border: '1px solid var(--color-border-hi)', color: 'var(--color-ocean)' }}>
                ierc_golfo_california.gpkg
              </code>.
            </p>
          </div>

          <div style={{
            fontSize: '0.6875rem',
            color: 'var(--color-text-muted)',
            fontFamily: 'var(--font-mono)',
            textAlign: 'right',
          }}>
            RECURSOS: 4 CAPAS VECTORIALES<br />
            MOTOR: MONTE CARLO 1,000 ITER/CELDA
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
    </div>
  )
}
