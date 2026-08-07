import React from 'react'

export default function Header({
  onOpenCoverage,
  onOpenExport,
  onToggleSidebar,
}: {
  onOpenCoverage?: () => void
  onOpenExport?: () => void
  onToggleSidebar?: () => void
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
            <span style={{ color: 'var(--color-text-primary)', fontWeight: 600 }}>ONLINE</span>
          </div>
          <span>|</span>
          <div className="system-ticker-item">
            <span>GPKG:</span>
            <span style={{ color: 'var(--color-ocean)' }}>v1.1</span>
          </div>
          <span>|</span>
          <div className="system-ticker-item">
            <span>INVENTARIO:</span>
            <span style={{ color: 'var(--color-accent)', fontWeight: 700 }}>v2.3</span>
          </div>
          <span>|</span>
          <div className="system-ticker-item">
            <span>H3:</span>
            <span style={{ color: 'var(--color-accent)', fontVariantNumeric: 'tabular-nums' }}>830K CELDAS</span>
          </div>
          <span>|</span>
          <div className="system-ticker-item">
            <span>CI:</span>
            <span style={{ color: 'var(--color-ok)' }}>45 TESTS · 5 JOBS</span>
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

            {onToggleSidebar && (
              <button
                onClick={onToggleSidebar}
                style={{
                  background: 'var(--color-surface-2)',
                  border: '1px solid var(--color-border)',
                  color: 'var(--color-text-primary)',
                  borderRadius: 0,
                  padding: '5px 10px',
                  fontSize: '0.72rem',
                  fontWeight: 700,
                  cursor: 'pointer',
                  fontFamily: 'var(--font-mono)',
                  letterSpacing: '0.04em',
                  transition: 'background 0.15s ease',
                }}
                onMouseOver={(e) => e.currentTarget.style.background = 'var(--color-surface-3)'}
                onMouseOut={(e) => e.currentTarget.style.background = 'var(--color-surface-2)'}
                aria-label="Toggle sidebar"
              >
                ☰
              </button>
            )}
          </div>
        </div>

        {/* Esoteria Metrics Strip — datos verificados v2.3 */}
        <div style={{
          borderTop: '1px solid var(--color-border)',
          background: 'var(--color-surface-2)',
        }}>
          <div style={{
            maxWidth: 1400,
            margin: '0 auto',
            padding: '0.45rem 1.5rem',
            display: 'flex',
            gap: '1.75rem',
            overflowX: 'auto',
            scrollbarWidth: 'none',
            fontFamily: 'var(--font-mono)',
          } as React.CSSProperties}>
            {[
              { label: 'FUENTES SILVER',    value: '14 DATASETS',      sub: '165 Parquets · ZSTD' },
              { label: 'PRODUCTOS GOLD',    value: '13 ANALÍTICOS',    sub: '6 IERC + 6 gas + 1 env', color: 'var(--color-ok)' },
              { label: 'CELDAS H3-8 GOLD', value: '830,869',           sub: 'IERC score 0–1' },
              { label: 'ZONAS PANGAS',      value: '263,796 FILAS',    sub: '7 artes de pesca', color: 'var(--color-ocean)' },
              { label: 'SCRIPTS PYTHON',    value: '44 OPS',           sub: 'ETL · Gold · API' },
              { label: 'DUCTOS CNIH/SENER', value: '24 TRAMOS',        sub: '6,399 km · EPSG:4326', color: 'var(--color-warn)' },
              { label: 'TERMINALES GNL',    value: '4 PROYECTOS',      sub: 'Saguaro · Amigo · Vista · Cosalá', color: 'var(--color-alert)' },
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
