'use client'

import React, { useEffect, useState } from 'react'

interface NodoGas {
  punto: string
  descripcion: string
  total_gj_inyectado_all?: number
  total_gj_all_years?: number
  avg_daily_gj_inyectado?: number
  avg_daily_gj?: number
  days_with_data_iny?: number
  days_with_data?: number
  origen_principal_iny?: string
}

interface DuctoCnih {
  nombre: string
  fuente_capa: string
  longitud_km: number
  empresa: string
  tipo: string
  integrado_sistrangas: boolean
}

interface EnvRiskNodo {
  punto: string
  descripcion: string
  total_sitios: number
  env_risk_score: number
  total_gj_all_years?: number
  total_gj_inyectado_all?: number
}

// Coordenadas geográficas estáticas para centrado rápido de nodos principales
const NODE_COORDINATES: Record<string, { lat: number; lng: number }> = {
  'inj-01': { lat: 25.962, lng: -109.001 }, // El Oro
  'V001':   { lat: 25.962, lng: -109.001 },
  'inj-02': { lat: 27.876, lng: -110.865 }, // Guaymas
  'V007':   { lat: 27.876, lng: -110.865 },
  'inj-03': { lat: 31.332, lng: -111.089 }, // San Isidro
  'inj-04': { lat: 29.904, lng: -112.693 }, // Puerto Libertad
  'V022':   { lat: 29.904, lng: -112.693 },
  'inj-05': { lat: 25.590, lng: -109.052 }, // Topolobampo
  'V029':   { lat: 25.590, lng: -109.052 },
}

function AsciiVolumeBar({ value, max, color }: { value: number; max: number; color: string }) {
  const pct = Math.round((value / max) * 100)
  const filled = Math.round((pct / 100) * 12)
  const empty = 12 - filled
  return (
    <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6875rem', letterSpacing: '0.06em', color, fontWeight: 700 }}>
      [{('█').repeat(filled)}{('░').repeat(empty)}]
    </span>
  )
}

function DuctoColorDot({ fuente }: { fuente: string }) {
  const COLOR: Record<string, string> = {
    integrados:    '#FF6B00',
    no_integrados: '#FFB000',
    pacific:       '#A855F7',
    poliductos:    '#00D4AA',
  }
  return (
    <span style={{
      display: 'inline-block',
      width: 10, height: 10,
      background: COLOR[fuente] ?? '#888',
      flexShrink: 0,
      border: '1px solid rgba(255,255,255,0.2)',
    }} />
  )
}

type Tab = 'inyecciones' | 'ductos' | 'env_risk'

export default function GasInfraPanel() {
  const [tab, setTab] = useState<Tab>('inyecciones')
  const [inyecciones, setInyecciones] = useState<NodoGas[]>([])
  const [ductos, setDuctos] = useState<DuctoCnih[]>([])
  const [envRisk, setEnvRisk] = useState<EnvRiskNodo[]>([])
  const [loading, setLoading] = useState(true)
  const [dataSource, setDataSource] = useState('Cargando...')

  useEffect(() => {
    fetch('/api/gas-infra')
      .then(r => r.json())
      .then(res => {
        setInyecciones(res.inyecciones || [])
        setDuctos(res.ductos || [])
        setEnvRisk(res.env_risk || [])
        setDataSource(res.data_source || 'Unknown')
        setLoading(false)
      })
      .catch(err => {
        console.error('Error loading gas-infra API:', err)
        setLoading(false)
      })
  }, [])

  const handleFocusNode = (nodeId: string, label: string) => {
    const coords = NODE_COORDINATES[nodeId]
    if (coords) {
      // Disparar evento personalizado global para que RiskMap.tsx reaccione
      const event = new CustomEvent('focus-map-node', {
        detail: {
          lat: coords.lat,
          lng: coords.lng,
          label,
          layerId: 'capas_contexto'
        }
      })
      window.dispatchEvent(event)
    }
  }

  const getMaxIny = () => {
    if (inyecciones.length === 0) return 1
    return Math.max(...inyecciones.map(n => n.total_gj_inyectado_all ?? n.total_gj_all_years ?? 1))
  }

  const getMaxEnvRisk = () => {
    if (envRisk.length === 0) return 1
    return Math.max(...envRisk.map(n => n.env_risk_score))
  }

  const maxGj = getMaxIny()
  const maxEnvRisk = getMaxEnvRisk()

  return (
    <div className="section" style={{ borderTop: '1px solid var(--color-border)', paddingTop: '2rem' }}>
      <div className="section-title" style={{ justifyContent: 'space-between' }}>
        <span>INFRAESTRUCTURA GAS NATURAL · SISTRANGAS &amp; CNIH/SENER</span>
        <span style={{ fontSize: 10, color: 'var(--color-warn)', fontFamily: 'var(--font-mono)', letterSpacing: '0.04em' }}>
          ORIGEN: {dataSource.toUpperCase()}
        </span>
      </div>

      {/* KPI summary strip */}
      <div style={{
        display: 'flex',
        gap: '1rem',
        marginBottom: '1.25rem',
        flexWrap: 'wrap',
      }}>
        {[
          { label: 'NODOS INYECCIÓN',   value: inyecciones.length || '33',       color: 'var(--color-accent)',  sub: 'master_inyecciones.parquet' },
          { label: 'NODOS EXTRACCIÓN',  value: '225',                            color: 'var(--color-warn)',    sub: 'master_extracciones.parquet' },
          { label: 'DUCTOS CNIH/SENER', value: ductos.length ? `${ductos.length} tramos` : '24 tramos', color: '#FF6B00',            sub: '6,399.3 km · EPSG:4326' },
          { label: 'NODOS ENV. RISK',   value: envRisk.length || '33',           color: 'var(--color-alert)',   sub: 'sitios contaminados join' },
          { label: 'TARIFAS SISTRANGAS',value: '63 zonas',                       color: 'var(--color-ocean)',   sub: 'tarifas_zone_summary.parquet' },
        ].map(k => (
          <div key={k.label} style={{
            flex: '1 1 140px',
            padding: '0.625rem 0.875rem',
            background: 'var(--color-surface)',
            border: `1px solid ${k.color}20`,
            borderLeft: `3px solid ${k.color}`,
            fontFamily: 'var(--font-mono)',
          }}>
            <div style={{ fontSize: '1rem', fontWeight: 800, color: k.color, fontVariantNumeric: 'tabular-nums' }}>
              {k.value}
            </div>
            <div style={{ fontSize: '0.625rem', color: 'var(--color-text-muted)', marginTop: 2 }}>
              {k.label}
            </div>
            <div style={{ fontSize: '0.5625rem', color: 'var(--color-text-disabled)', marginTop: 1 }}>
              {k.sub}
            </div>
          </div>
        ))}
      </div>

      {/* Tab selector */}
      <div style={{ display: 'flex', gap: '0', marginBottom: '1rem', borderBottom: '1px solid var(--color-border)' }}>
        {([
          { id: 'inyecciones', label: '> INYECCIONES SISTRANGAS' },
          { id: 'ductos',      label: '> DUCTOS CNIH/SENER' },
          { id: 'env_risk',    label: '> RIESGO AMBIENTAL' },
        ] as { id: Tab; label: string }[]).map(t => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            style={{
              background: tab === t.id ? 'var(--color-surface-2)' : 'transparent',
              border: 'none',
              borderBottom: tab === t.id ? '2px solid var(--color-accent)' : '2px solid transparent',
              color: tab === t.id ? 'var(--color-accent)' : 'var(--color-text-muted)',
              padding: '0.5rem 1rem',
              fontSize: '0.6875rem',
              fontWeight: 700,
              cursor: 'pointer',
              fontFamily: 'var(--font-mono)',
              letterSpacing: '0.04em',
              transition: 'color 0.15s ease',
            }}
          >
            {t.label}
          </button>
        ))}
      </div>

      {loading && (
        <div style={{ padding: '2rem', textAlign: 'center', fontFamily: 'var(--font-mono)', color: 'var(--color-text-muted)', fontSize: '0.75rem' }}>
          [ CARGANDO DATOS DOCKDB / PARQUET... ]
        </div>
      )}

      {/* Tab: Top inyecciones */}
      {!loading && tab === 'inyecciones' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0' }}>
          <div style={{
            display: 'grid',
            gridTemplateColumns: '2fr 1.2fr 1.2fr 1.2fr 2fr 1fr',
            gap: '0.5rem',
            padding: '0.35rem 0.75rem',
            background: 'var(--color-surface-2)',
            borderBottom: '1px solid var(--color-border-hi)',
            fontFamily: 'var(--font-mono)',
            fontSize: '0.6rem',
            color: 'var(--color-text-muted)',
            fontWeight: 700,
            letterSpacing: '0.06em',
            textTransform: 'uppercase',
          }}>
            <span>NODO SISTRANGAS</span>
            <span>TOTAL GJ</span>
            <span>PROM. DIARIO</span>
            <span>DÍAS ACTIVO</span>
            <span>VOLUMEN RELATIVO</span>
            <span>GEOLOCALIZAR</span>
          </div>
          {inyecciones.map((n, i) => {
            const nodeId = n.punto || `inj-0${i+1}`
            const val = n.total_gj_inyectado_all ?? n.total_gj_all_years ?? 0
            const avg = n.avg_daily_gj_inyectado ?? n.avg_daily_gj ?? 0
            const days = n.days_with_data_iny ?? n.days_with_data ?? 0
            const hasCoords = !!NODE_COORDINATES[nodeId]

            return (
              <div key={nodeId} style={{
                display: 'grid',
                gridTemplateColumns: '2fr 1.2fr 1.2fr 1.2fr 2fr 1fr',
                gap: '0.5rem',
                padding: '0.5rem 0.75rem',
                borderBottom: '1px solid var(--color-border)',
                fontFamily: 'var(--font-mono)',
                alignItems: 'center',
                background: i % 2 === 0 ? 'var(--color-surface)' : 'var(--color-surface-2)',
              }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--color-text-primary)', fontWeight: 600 }}>{n.descripcion}</span>
                <span style={{ fontSize: '0.75rem', color: 'var(--color-accent)', fontVariantNumeric: 'tabular-nums', fontWeight: 700 }}>
                  {(val / 1_000_000).toFixed(2)}M
                </span>
                <span style={{ fontSize: '0.75rem', color: 'var(--color-text-secondary)', fontVariantNumeric: 'tabular-nums' }}>
                  {avg.toLocaleString()}
                </span>
                <span style={{ fontSize: '0.75rem', color: 'var(--color-text-secondary)', fontVariantNumeric: 'tabular-nums' }}>
                  {days.toLocaleString()}
                </span>
                <AsciiVolumeBar value={val} max={maxGj} color="var(--color-accent)" />
                
                {hasCoords ? (
                  <button
                    onClick={() => handleFocusNode(nodeId, n.descripcion)}
                    style={{
                      background: 'transparent',
                      border: '1px solid var(--color-ok)',
                      color: 'var(--color-ok)',
                      padding: '2px 6px',
                      fontSize: '0.5625rem',
                      fontFamily: 'var(--font-mono)',
                      fontWeight: 800,
                      cursor: 'pointer',
                      textAlign: 'center',
                    }}
                  >
                    MAP
                  </button>
                ) : (
                  <span style={{ fontSize: '0.5625rem', color: 'var(--color-text-disabled)', fontFamily: 'var(--font-mono)', textAlign: 'center' }}>[N/A]</span>
                )}
              </div>
            )
          })}
          <div style={{
            padding: '0.4rem 0.75rem',
            fontSize: '0.625rem',
            color: 'var(--color-text-muted)',
            fontFamily: 'var(--font-mono)',
            borderTop: '1px solid var(--color-border)',
          }}>
            FUENTE: gas_infrastructure_master_inyecciones.parquet · CENEGAS/SISTRANGAS · 2015-01-01 — 2024-12-31
          </div>
        </div>
      )}

      {/* Tab: Ductos CNIH/SENER */}
      {!loading && tab === 'ductos' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0' }}>
          <div style={{
            display: 'grid',
            gridTemplateColumns: '30px 2fr 1.2fr 1.2fr 1fr 1fr',
            gap: '0.5rem',
            padding: '0.35rem 0.75rem',
            background: 'var(--color-surface-2)',
            borderBottom: '1px solid var(--color-border-hi)',
            fontFamily: 'var(--font-mono)',
            fontSize: '0.6rem',
            color: 'var(--color-text-muted)',
            fontWeight: 700,
            letterSpacing: '0.06em',
            textTransform: 'uppercase',
          }}>
            <span></span>
            <span>DUCTO CNIH</span>
            <span>LONGITUD</span>
            <span>EMPRESA</span>
            <span>TIPO</span>
            <span>SISTRANGAS</span>
          </div>
          {ductos.map((d, i) => (
            <div key={d.nombre + i} style={{
              display: 'grid',
              gridTemplateColumns: '30px 2fr 1.2fr 1.2fr 1fr 1fr',
              gap: '0.5rem',
              padding: '0.5rem 0.75rem',
              borderBottom: '1px solid var(--color-border)',
              fontFamily: 'var(--font-mono)',
              alignItems: 'center',
              background: i % 2 === 0 ? 'var(--color-surface)' : 'var(--color-surface-2)',
            }}>
              <DuctoColorDot fuente={d.fuente_capa} />
              <span style={{ fontSize: '0.75rem', color: 'var(--color-text-primary)', fontWeight: 600 }}>{d.nombre}</span>
              <span style={{ fontSize: '0.75rem', color: '#FF6B00', fontVariantNumeric: 'tabular-nums', fontWeight: 700 }}>
                {d.longitud_km.toFixed(1)} km
              </span>
              <span style={{ fontSize: '0.6875rem', color: 'var(--color-text-secondary)' }}>{d.empresa}</span>
              <span style={{ fontSize: '0.6875rem', color: 'var(--color-text-muted)' }}>{d.tipo}</span>
              <span style={{
                fontSize: '0.625rem',
                fontWeight: 700,
                color: d.integrado_sistrangas ? 'var(--color-ok)' : 'var(--color-text-disabled)',
                fontFamily: 'var(--font-mono)',
              }}>
                {d.integrado_sistrangas ? '[SI]' : '[NO]'}
              </span>
            </div>
          ))}
          {/* Leyenda colores */}
          <div style={{
            display: 'flex',
            gap: '1.25rem',
            padding: '0.5rem 0.75rem',
            borderTop: '1px solid var(--color-border)',
            flexWrap: 'wrap',
          }}>
            {[
              { fuente: 'integrados',    label: 'Integrados SISTRANGAS (10)' },
              { fuente: 'no_integrados', label: 'No Integrados (6)' },
              { fuente: 'pacific',       label: 'Pacific Limited (1)' },
              { fuente: 'poliductos',    label: 'Poliductos (5)' },
            ].map(l => (
              <div key={l.fuente} style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: 'var(--color-text-muted)' }}>
                <DuctoColorDot fuente={l.fuente} />
                {l.label}
              </div>
            ))}
            <span style={{ fontSize: '0.625rem', color: 'var(--color-text-muted)', fontFamily: 'var(--font-mono)', marginLeft: 'auto' }}>
              FUENTE: CNIH/SENER ArcGIS FeatureServer · 24 LineStrings · 6,399.3 km total
            </span>
          </div>
        </div>
      )}

      {/* Tab: Riesgo Ambiental */}
      {!loading && tab === 'env_risk' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0' }}>
          <div style={{
            display: 'grid',
            gridTemplateColumns: '2fr 1fr 1fr 1.2fr 2fr 1fr',
            gap: '0.5rem',
            padding: '0.35rem 0.75rem',
            background: 'var(--color-surface-2)',
            borderBottom: '1px solid var(--color-border-hi)',
            fontFamily: 'var(--font-mono)',
            fontSize: '0.6rem',
            color: 'var(--color-text-muted)',
            fontWeight: 700,
            letterSpacing: '0.06em',
            textTransform: 'uppercase',
          }}>
            <span>NODO / TERMINAL GNL</span>
            <span>SITIOS CONT.</span>
            <span>RISK SCORE</span>
            <span>VOLUMEN GJ</span>
            <span>RIESGO RELATIVO</span>
            <span>GEOLOCALIZAR</span>
          </div>
          {envRisk.map((n, i) => {
            const nodeId = n.punto
            const riskColor = n.env_risk_score >= 70 ? 'var(--color-alert)' : n.env_risk_score >= 50 ? 'var(--color-warn)' : 'var(--color-ok)'
            const hasCoords = !!NODE_COORDINATES[nodeId]
            const gjVal = n.total_gj_all_years ?? n.total_gj_inyectado_all ?? 0

            return (
              <div key={nodeId} style={{
                display: 'grid',
                gridTemplateColumns: '2fr 1fr 1fr 1.2fr 2fr 1fr',
                gap: '0.5rem',
                padding: '0.5rem 0.75rem',
                borderBottom: '1px solid var(--color-border)',
                fontFamily: 'var(--font-mono)',
                alignItems: 'center',
                background: i % 2 === 0 ? 'var(--color-surface)' : 'var(--color-surface-2)',
              }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--color-text-primary)', fontWeight: 600 }}>{n.descripcion}</span>
                <span style={{ fontSize: '0.75rem', color: 'var(--color-alert)', fontVariantNumeric: 'tabular-nums', fontWeight: 700 }}>
                  {n.total_sitios}
                </span>
                <span style={{ fontSize: '0.75rem', color: riskColor, fontVariantNumeric: 'tabular-nums', fontWeight: 700 }}>
                  {n.env_risk_score.toFixed(1)}
                </span>
                <span style={{ fontSize: '0.75rem', color: 'var(--color-text-secondary)', fontVariantNumeric: 'tabular-nums' }}>
                  {(gjVal / 1_000_000).toFixed(2)}M
                </span>
                <AsciiVolumeBar value={n.env_risk_score} max={maxEnvRisk} color={riskColor} />
                
                {hasCoords ? (
                  <button
                    onClick={() => handleFocusNode(nodeId, n.descripcion)}
                    style={{
                      background: 'transparent',
                      border: '1px solid var(--color-ok)',
                      color: 'var(--color-ok)',
                      padding: '2px 6px',
                      fontSize: '0.5625rem',
                      fontFamily: 'var(--font-mono)',
                      fontWeight: 800,
                      cursor: 'pointer',
                      textAlign: 'center',
                    }}
                  >
                    MAP
                  </button>
                ) : (
                  <span style={{ fontSize: '0.5625rem', color: 'var(--color-text-disabled)', fontFamily: 'var(--font-mono)', textAlign: 'center' }}>[N/A]</span>
                )}
              </div>
            )
          })}
          <div style={{
            padding: '0.4rem 0.75rem',
            fontSize: '0.625rem',
            color: 'var(--color-text-muted)',
            fontFamily: 'var(--font-mono)',
            borderTop: '1px solid var(--color-border)',
          }}>
            FUENTE: env_risk_by_nodo.parquet · join gas infra + SEMARNAT sitios contaminados · 24 columnas
          </div>
        </div>
      )}
    </div>
  )
}
