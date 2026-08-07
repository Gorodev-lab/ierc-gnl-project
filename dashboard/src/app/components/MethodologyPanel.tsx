import React from 'react'

// ─── Tipos ────────────────────────────────────────────────────────────────────
interface ComponentAxis {
  label: string
  labelEs: string
  peso: number
  color: string
  fuente: string
  subindice: 'H' | 'V'
}

// ─── Datos verificados del inventario v2.3 ────────────────────────────────────
const AXES: ComponentAxis[] = [
  {
    label: 'Amenaza (H)',
    labelEs: 'Infraestructura GNL, ruido, rutas metaneros, ductos CNIH',
    peso: 0.20,
    color: 'var(--color-alert)',
    fuente: 'ASEA MIA · GFW rutas · Ductos CNIH',
    subindice: 'H',
  },
  {
    label: 'Exposición (H)',
    labelEs: 'Esfuerzo pesquero VMS + pangas artesanales',
    peso: 0.20,
    color: '#FF6B00',
    fuente: 'GFW Zenodo · PANGAS GDB · Ductos CNIH',
    subindice: 'H',
  },
  {
    label: 'Sensibilidad (V)',
    labelEs: 'Especies IUCN, endemismo, hábitats críticos',
    peso: 0.15,
    color: 'var(--color-warn)',
    fuente: 'TNC Shapefiles · NASA OceanColor · OBIS',
    subindice: 'V',
  },
  {
    label: 'Dependencia Económica (V)',
    labelEs: 'Ingreso pesquero / ingreso total del hogar',
    peso: 0.15,
    color: 'var(--color-accent)',
    fuente: 'Encuestas PANGAS · INEGI 2020',
    subindice: 'V',
  },
  {
    label: 'Valor Biocultural (V)',
    labelEs: 'Sitios sagrados Comca\'ac, patrimonio inmaterial',
    peso: 0.20,
    color: 'var(--color-ok)',
    fuente: 'Trabajo de campo · Comunidades POA',
    subindice: 'V',
  },
  {
    label: '(1 − Cap. Adaptativa) (V)',
    labelEs: 'Gobernanza GAGE, diversificación, acceso a crédito',
    peso: 0.15,
    color: 'var(--color-ocean)',
    fuente: 'GAGE · Encuestas 2026',
    subindice: 'V',
  },
]

const MONTE_CARLO_ROWS = [
  { label: 'Simulaciones Monte Carlo',    value: 'N = 1,000 iter/celda' },
  { label: 'Intervalo de confianza',      value: 'p05 — p95 (90% IC)' },
  { label: 'Celdas H3-8 procesadas',      value: '830,869 hexágonos' },
  { label: 'Formato entregable (Meta 1)', value: 'OGC GeoPackage v1.1' },
  { label: 'Ruta del entregable',         value: 'deliverables/v1_geopackage/' },
  { label: 'Resolución espacial H3',      value: 'Res 8 (0.73 km²) + Res 10 costero' },
  { label: 'Dataset Monte Carlo Gold',    value: 'ierc_monte_carlo_h3_8.parquet (33 MB)' },
]

function WeightBar({ peso, color }: { peso: number; color: string }) {
  const pct = Math.round(peso * 100)
  const filled = Math.round((pct / 25) * 10)  // max es 25%
  const empty = 10 - filled
  return (
    <span style={{
      fontFamily: 'var(--font-mono)',
      fontSize: '0.6875rem',
      letterSpacing: '0.08em',
      color,
      fontWeight: 700,
    }}>
      [{('█').repeat(filled)}{('░').repeat(empty)}] {pct}%
    </span>
  )
}

export default function MethodologyPanel() {
  const hAxes = AXES.filter(a => a.subindice === 'H')
  const vAxes = AXES.filter(a => a.subindice === 'V')

  return (
    <div className="section" style={{ borderTop: '1px solid var(--color-border)', paddingTop: '2rem' }}>
      <div className="section-title">Metodología IERC &amp; Motor de Cálculo Monte Carlo</div>

      {/* ── Fila superior: dos modelos lado a lado ─────────────────────────── */}
      <div className="grid-2" style={{ marginBottom: '1.25rem' }}>

        {/* Modelo Aditivo Oficial */}
        <div className="card card--amber">
          <div style={{
            fontSize: '0.6875rem',
            fontWeight: 800,
            color: 'var(--color-accent)',
            letterSpacing: '0.05em',
            marginBottom: '0.625rem',
          }}>
            &gt; MODELO ADITIVO (OFICIAL — POA 2026-2028)
          </div>
          <div className="formula-box">
            <div style={{ color: 'var(--color-text-muted)', marginBottom: '0.5rem', fontSize: '0.6875rem' }}>
              // ÍNDICE ESPACIAL DE RIESGO SOCIOECONÓMICO
            </div>
            <span style={{ color: 'var(--color-accent)', fontWeight: 800 }}>IERC</span> = (Amenaza × 0.20)<br />
            &nbsp;&nbsp;&nbsp;&nbsp;+ (Exposición × 0.20)<br />
            &nbsp;&nbsp;&nbsp;&nbsp;+ (Sensibilidad × 0.15)<br />
            &nbsp;&nbsp;&nbsp;&nbsp;+ (Dependencia × 0.15)<br />
            &nbsp;&nbsp;&nbsp;&nbsp;+ (Biocultural × 0.20)<br />
            &nbsp;&nbsp;&nbsp;&nbsp;+ ((1 − Cap.Adaptativa) × 0.15)
          </div>

          {/* Sub-índice H */}
          <div style={{
            marginTop: '1rem',
            padding: '0.625rem',
            background: 'var(--color-surface-2)',
            border: '1px solid rgba(192,57,43,0.3)',
            borderLeft: '3px solid var(--color-alert)',
            fontFamily: 'var(--font-mono)',
          }}>
            <div style={{ fontSize: '0.625rem', fontWeight: 800, color: 'var(--color-alert)', letterSpacing: '0.06em', marginBottom: '0.4rem' }}>
              [H] AMENAZA &amp; EXPOSICIÓN ESPACIAL
            </div>
            {hAxes.map(a => (
              <div key={a.label} style={{ marginBottom: '0.5rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.2rem' }}>
                  <span style={{ fontSize: '0.6875rem', color: 'var(--color-text-secondary)' }}>{a.label}</span>
                  <WeightBar peso={a.peso} color={a.color} />
                </div>
                <div style={{ fontSize: '0.625rem', color: 'var(--color-text-muted)' }}>
                  {a.fuente}
                </div>
              </div>
            ))}
          </div>

          {/* Sub-índice V */}
          <div style={{
            marginTop: '0.75rem',
            padding: '0.625rem',
            background: 'var(--color-surface-2)',
            border: '1px solid rgba(14,165,233,0.3)',
            borderLeft: '3px solid var(--color-ocean)',
            fontFamily: 'var(--font-mono)',
          }}>
            <div style={{ fontSize: '0.625rem', fontWeight: 800, color: 'var(--color-ocean)', letterSpacing: '0.06em', marginBottom: '0.4rem' }}>
              [V] VULNERABILIDAD SOCIOECOLÓGICA
            </div>
            {vAxes.map(a => (
              <div key={a.label} style={{ marginBottom: '0.5rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.2rem' }}>
                  <span style={{ fontSize: '0.6875rem', color: 'var(--color-text-secondary)' }}>{a.label}</span>
                  <WeightBar peso={a.peso} color={a.color} />
                </div>
                <div style={{ fontSize: '0.625rem', color: 'var(--color-text-muted)' }}>
                  {a.fuente}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Columna derecha: Modelo Multiplicativo + Monte Carlo + Refs */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>

          {/* Modelo Multiplicativo IPCC */}
          <div className="card">
            <div style={{
              fontSize: '0.6875rem',
              fontWeight: 800,
              color: 'var(--color-ocean)',
              letterSpacing: '0.05em',
              marginBottom: '0.625rem',
            }}>
              &gt; MODELO MULTIPLICATIVO (IPCC AR5)
            </div>
            <div className="formula-box">
              <div style={{ color: 'var(--color-text-muted)', marginBottom: '0.5rem', fontSize: '0.6875rem' }}>
                // RIESGO INTEGRAL POR CELDA H3 (i) Y PERÍODO (t)
              </div>
              <span style={{ color: 'var(--color-accent)', fontWeight: 800 }}>{"R_{i,t}"}</span>{" = "}
              <span style={{ color: 'var(--color-alert)', fontWeight: 700 }}>{"H_{i,t}"}</span>
              {" × "}
              <span style={{ color: 'var(--color-ocean)', fontWeight: 700 }}>{"V_{i,t}"}</span>
              <br /><br />
              <span style={{ color: 'var(--color-text-muted)', fontSize: '0.6875rem' }}>
                // RIESGO PESQUERO (MORENO-BÁEZ ET AL. 2012):<br />
                R = (0.50 × esfuerzo) + (0.30 × proximidad) + (0.20 × spp_críticas)<br /><br />
                // CONFIANZA ESPACIAL (NIVEL III):<br />
                C_i = (0.40 × dens.obs) + (0.30 × consist.) + (0.30 × val.comunitaria)
              </span>
            </div>

            <div style={{ marginTop: '0.875rem', display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
              {[
                { label: 'Alta confianza',  range: 'Ci ≥ 75',   color: 'var(--color-ok)' },
                { label: 'Media',           range: '50 ≤ Ci < 75', color: 'var(--color-warn)' },
                { label: 'Baja confianza',  range: 'Ci < 50',   color: 'var(--color-alert)' },
              ].map(t => (
                <div key={t.label} style={{
                  flex: 1,
                  minWidth: 90,
                  padding: '0.4rem 0.5rem',
                  background: 'var(--color-surface-2)',
                  border: `1px solid ${t.color}`,
                  fontFamily: 'var(--font-mono)',
                }}>
                  <div style={{ fontSize: '0.625rem', color: t.color, fontWeight: 700 }}>{t.label}</div>
                  <div style={{ fontSize: '0.6875rem', color: 'var(--color-text-secondary)', fontVariantNumeric: 'tabular-nums' }}>{t.range}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Motor Monte Carlo */}
          <div className="card">
            <div style={{
              fontSize: '0.6875rem',
              fontWeight: 800,
              color: 'var(--color-accent)',
              letterSpacing: '0.05em',
              marginBottom: '0.75rem',
            }}>
              &gt; MOTOR DE CÁLCULO &amp; DATOS VERIFICADOS v2.3
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0' }}>
              {MONTE_CARLO_ROWS.map(row => (
                <div key={row.label} className="stat-row">
                  <span className="stat-row-label">{row.label}</span>
                  <span className="stat-row-value">{row.value}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Referencias */}
          <div className="card">
            <div style={{
              fontSize: '0.6875rem',
              fontWeight: 800,
              color: 'var(--color-accent)',
              letterSpacing: '0.05em',
              marginBottom: '0.75rem',
            }}>
              &gt; REFERENCIAS BIBLIOGRÁFICAS
            </div>
            {[
              {
                authors: 'Moreno-Báez et al.',
                year: '2011',
                title: 'Integrating the spatial and temporal dimensions of fishing for management in the Northern Gulf of California',
                journal: 'Marine Policy, 35(3), 297–309',
              },
              {
                authors: 'Moreno-Báez et al.',
                year: '2012',
                title: 'Integrating the spatial and temporal dimensions of fishing activities for management in the Northern Gulf of California',
                journal: 'Marine Policy, 38, 483–489',
              },
            ].map(ref => (
              <div key={ref.year} style={{
                padding: '0.625rem',
                background: 'var(--color-surface-2)',
                marginBottom: '0.5rem',
                border: '1px solid var(--color-border)',
                borderLeft: '3px solid var(--color-accent)',
              }}>
                <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--color-accent)', marginBottom: '0.2rem' }}>
                  {ref.authors} ({ref.year})
                </div>
                <div style={{ fontSize: '0.6875rem', color: 'var(--color-text-secondary)', lineHeight: 1.4, marginBottom: '0.2rem' }}>
                  {ref.title}
                </div>
                <div style={{ fontSize: '0.625rem', color: 'var(--color-ocean)', fontStyle: 'italic' }}>
                  {ref.journal}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Footer */}
      <div style={{
        padding: '0.875rem 1.25rem',
        background: 'var(--color-surface)',
        border: '1px solid var(--color-border)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '0.75rem',
        fontFamily: 'var(--font-mono)',
      }}>
        <div style={{ fontSize: '0.75rem', color: 'var(--color-accent)', fontWeight: 700 }}>
          IERC-GNL · Causa Natura Center · POA 2026-2028 · Inventario v2.3
        </div>
        <div style={{ fontSize: '0.6875rem', color: 'var(--color-text-muted)' }}>
          14 fuentes Silver · 13 Gold · PANGAS GDB · GFW Zenodo · CNIH ArcGIS · NASA OceanColor · GEBCO 2024
        </div>
      </div>
    </div>
  )
}
