'use client'

import React, { useEffect, useState } from 'react'

interface ComponentAxis {
  label: string
  labelEs: string
  peso: number
  color: string
  fuente: string
  subindice: 'H' | 'V'
}

interface MonteCarloRow {
  label: string
  value: string
}

interface Reference {
  authors: string
  year: string
  title: string
  journal: string
}

interface MethodologyData {
  axes: ComponentAxis[]
  monteCarloRows: MonteCarloRow[]
  references: Reference[]
}

function WeightBar({ peso, color }: { peso: number; color: string }) {
  const pct = Math.round(peso * 100)
  const filled = Math.round((pct / 25) * 10)
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
  const [data, setData] = useState<MethodologyData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/data/methodology.json')
      .then(r => r.json())
      .then(setData)
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  if (loading || !data) {
    return (
      <div className="section" style={{ borderTop: '1px solid var(--color-border)', paddingTop: '2rem' }}>
        <div className="section-title">Metodología IERC & Motor de Cálculo Monte Carlo</div>
        <div style={{ padding: '2rem', textAlign: 'center', fontFamily: 'var(--font-mono)', color: 'var(--color-text-muted)' }}>
          [ CARGANDO METODOLOGÍA... ]
        </div>
      </div>
    )
  }

  const { axes, monteCarloRows, references } = data
  const hAxes = axes.filter(a => a.subindice === 'H')
  const vAxes = axes.filter(a => a.subindice === 'V')

  return (
    <div className="section" style={{ borderTop: '1px solid var(--color-border)', paddingTop: '2rem' }}>
      <div className="section-title">Metodología IERC & Motor de Cálculo Monte Carlo</div>

      {/* Fila superior: dos modelos lado a lado */}
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
            {' > MODELO ADITIVO (OFICIAL — POA 2026-2028)'}
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
              [H] AMENAZA & EXPOSICIÓN ESPACIAL
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

            {/* Advertencia: datos socioeconómicos constantes */}
            <div style={{
              marginTop: '0.5rem',
              padding: '0.5rem',
              background: 'rgba(243, 156, 18, 0.1)',
              border: '1px solid #F39C12',
              borderRadius: 0,
              fontFamily: 'var(--font-mono)',
              fontSize: '0.625rem',
              color: '#F39C12',
            }}>
              ⚠ Datos socioeconómicos (dependencia, biocultural, género, capacidad) son constantes por celda — V sub-índice no captura varianza espacial real
            </div>
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
              {' > MODELO MULTIPLICATIVO (IPCC AR5)'}
            </div>
            <div className="formula-box">
              <div style={{ color: 'var(--color-text-muted)', marginBottom: '0.5rem', fontSize: '0.6875rem' }}>
                // RIESGO INTEGRAL POR CELDA H3 (i) Y PERÍODO (t)
              </div>
              <span style={{ color: 'var(--color-accent)', fontWeight: 800 }}>R<sub>i,t</sub></span> = 
              <span style={{ color: 'var(--color-alert)', fontWeight: 700 }}>H<sub>i,t</sub></span>
              × 
              <span style={{ color: 'var(--color-ocean)', fontWeight: 700 }}>V<sub>i,t</sub></span>
              <br /><br />
              <span style={{ color: 'var(--color-text-muted)', fontSize: '0.6875rem' }}>
                // RIESGO PESQUERO (MORENO-BÁEZ ET AL. 2012):<br />
                R = (0.50 × esfuerzo) + (0.30 × proximidad) + (0.20 × spp_críticas)<br /><br />
                // CONFIANZA ESPACIAL (NIVEL III):<br />
                C<sub>i</sub> = (0.40 × dens.obs) + (0.30 × consist.) + (0.30 × val.comunitaria)
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
              {' > MOTOR DE CÁLCULO & DATOS VERIFICADOS v2.3'}
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0' }}>
              {monteCarloRows.map(row => (
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
              {' > REFERENCIAS BIBLIOGRÁFICAS'}
            </div>
            {references.map(ref => (
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