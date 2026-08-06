import React from 'react'

export default function Header({
  onOpenCoverage,
  onOpenExport,
}: {
  onOpenCoverage?: () => void
  onOpenExport?: () => void
}) {
  return (
    <>
      <header style={{
        background: 'var(--color-surface)',
        borderBottom: '1px solid var(--color-border-hi)',
        position: 'sticky',
        top: 0,
        zIndex: 100,
      }}>
        {/* System Ticker Bar */}
        <div className="system-ticker-bar">
          <div className="system-ticker-item">
            <span className="system-ticker-dot" />
            <span style={{ color: 'var(--color-text-primary)', fontWeight: 600 }}>SYSTEM: ONLINE</span>
          </div>
          <span>|</span>
          <div className="system-ticker-item">
            <span>GEOPACKAGE:</span>
            <span style={{ color: 'var(--color-ocean)' }}>ierc_golfo_california.gpkg (v1.1)</span>
          </div>
          <span>|</span>
          <div className="system-ticker-item">
            <span>COORDINATES:</span>
            <span style={{ color: 'var(--color-text-secondary)', fontVariantNumeric: 'tabular-nums' }}>27.5000° N, 110.5000° W</span>
          </div>
          <span>|</span>
          <div className="system-ticker-item">
            <span>H3 GRID:</span>
            <span style={{ color: 'var(--color-accent)', fontVariantNumeric: 'tabular-nums' }}>5,244 HEX (RES 8/9)</span>
          </div>
        </div>

        {/* Primary Header Bar */}
        <div style={{
          maxWidth: 1400,
          margin: '0 auto',
          padding: '0.85rem 1.5rem',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '1rem',
          flexWrap: 'wrap',
        }}>
          {/* Brand */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.875rem' }}>
            <div style={{
              width: 36,
              height: 36,
              borderRadius: 0,
              background: 'var(--color-surface-2)',
              border: '1px solid var(--color-accent)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '1.1rem',
              fontWeight: 800,
              color: 'var(--color-accent)',
              flexShrink: 0,
              fontFamily: 'var(--font-mono)',
            }}>
              &gt;
            </div>

            <div>
              <h1 style={{
                fontSize: '1.125rem',
                fontWeight: 800,
                color: 'var(--color-text-primary)',
                lineHeight: 1.2,
                letterSpacing: '0.04em',
                fontFamily: 'var(--font-mono)',
              }}>
                IERC-GNL <span style={{ color: 'var(--color-accent)' }}>[CAUSA NATURA CENTER]</span>
              </h1>
              <p style={{
                fontSize: '0.72rem',
                color: 'var(--color-text-secondary)',
                marginTop: 2,
                letterSpacing: '0.02em',
                fontFamily: 'var(--font-mono)',
              }}>
                Índice Espacial de Riesgo Socioeconómico · Golfo de California, México
              </p>
            </div>
          </div>

          {/* Controls & Actions */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.875rem', flexWrap: 'wrap' }}>
            {onOpenExport && (
              <button
                onClick={onOpenExport}
                style={{
                  background: 'var(--color-surface-2)',
                  border: '1px solid var(--color-ok)',
                  color: 'var(--color-ok)',
                  borderRadius: 0,
                  padding: '5px 12px',
                  fontSize: '0.72rem',
                  fontWeight: 700,
                  cursor: 'pointer',
                  fontFamily: 'var(--font-mono)',
                  letterSpacing: '0.04em',
                  transition: 'background 0.15s ease',
                }}
                onMouseOver={(e) => e.currentTarget.style.background = 'var(--color-surface-3)'}
                onMouseOut={(e) => e.currentTarget.style.background = 'var(--color-surface-2)'}
              >
                &gt; EXPORT GPKG / CSV
              </button>
            )}

            {onOpenCoverage && (
              <button
                onClick={onOpenCoverage}
                style={{
                  background: 'var(--color-surface-2)',
                  border: '1px solid var(--color-accent)',
                  color: 'var(--color-accent)',
                  borderRadius: 0,
                  padding: '5px 12px',
                  fontSize: '0.72rem',
                  fontWeight: 700,
                  cursor: 'pointer',
                  fontFamily: 'var(--font-mono)',
                  letterSpacing: '0.04em',
                  transition: 'background 0.15s ease',
                }}
                onMouseOver={(e) => e.currentTarget.style.background = 'var(--color-surface-3)'}
                onMouseOut={(e) => e.currentTarget.style.background = 'var(--color-surface-2)'}
              >
                &gt; INSPECT GAPS &amp; MATRIX
              </button>
            )}

            <div style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.4rem',
              padding: '4px 10px',
              border: '1px solid var(--color-ok)',
              borderRadius: 0,
              fontSize: '0.72rem',
              color: 'var(--color-ok)',
              fontWeight: 700,
              letterSpacing: '0.05em',
              fontFamily: 'var(--font-mono)',
              background: 'rgba(39, 174, 96, 0.1)'
            }}>
              [ OGC GPKG v1.1 ]
            </div>
          </div>
        </div>

        {/* Esoteria Metrics Strip */}
        <div style={{
          borderTop: '1px solid var(--color-border)',
          background: 'var(--color-surface-2)',
        }}>
          <div style={{
            maxWidth: 1400,
            margin: '0 auto',
            padding: '0.45rem 1.5rem',
            display: 'flex',
            gap: '2.5rem',
            overflowX: 'auto',
            fontFamily: 'var(--font-mono)',
          }}>
            {[
              { label: 'PROYECTOS GNL', value: '5 TERMINALES', sub: 'Moreno-Báez et al.' },
              { label: 'ALTO RIESGO', value: '3 ZONAS', sub: 'Score > 0.65', color: 'var(--color-alert)' },
              { label: 'GRILLA HEXAGONAL', value: '5,244 CELDAS', sub: 'Uber H3 Res 8/9' },
              { label: 'ZONAS PESQUERAS', value: '17 POLÍGONOS', sub: 'PANGAS / Pescadores', color: 'var(--color-ocean)' },
              { label: 'CRS ESPACIAL', value: 'EPSG:4326', sub: 'WGS84 Datum' },
            ].map(m => (
              <div key={m.label} style={{ flexShrink: 0 }}>
                <div style={{
                  fontSize: '0.8125rem',
                  fontWeight: 700,
                  color: m.color ?? 'var(--color-accent)',
                  fontVariantNumeric: 'tabular-nums',
                  letterSpacing: '0.02em',
                }}>
                  {m.value}
                </div>
                <div style={{ fontSize: '0.625rem', color: 'var(--color-text-muted)', whiteSpace: 'nowrap' }}>
                  {m.label} · {m.sub}
                </div>
              </div>
            ))}
          </div>
        </div>
      </header>
    </>
  )
}
