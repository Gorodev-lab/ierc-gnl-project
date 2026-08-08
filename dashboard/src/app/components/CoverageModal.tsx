'use client'

import React, { useState, useEffect } from 'react'

interface CoverageReport {
  resumen_ejecutivo: {
    fecha: string
    proyecto: string
    area_interes: string
    objetivo_iteracion: string
  }
  cobertura_datos: {
    proyectos_asea: {
      total_portal_consulta_publica: number
      filtrados_sonora_bc_bcs_gnl: number
    }
    proyectos_gnl_consolidados: {
      total: number
      por_tipo: Record<string, number>
      por_estado: Record<string, number>
    }
    batimetria: {
      fuente_principal: string
      resolucion: string
      contornos_generados: number
    }
    gaceta_ecologica: {
      total_publicaciones: number
      años_cubiertos: string
    }
  }
  gaps_identificados: Record<string, string[]>
  acciones_recomendadas_proxima_iteracion: Record<string, string[]>
}

function AsciiBar({ label, value, max = 100, color = 'var(--color-accent)' }: { label: string; value: number; max?: number; color?: string }) {
  const pct = Math.min(100, Math.max(0, Math.round((value / max) * 100)))
  const filled = Math.round((pct / 100) * 10)
  const empty = 10 - filled
  return (
    <div style={{ marginBottom: '0.5rem', fontFamily: 'var(--font-mono)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.15rem' }}>
        <span style={{ fontSize: '0.625rem', color: 'var(--color-text-secondary)', textTransform: 'uppercase' }}>{label}</span>
        <span style={{ fontSize: '0.625rem', fontWeight: 700, color, fontVariantNumeric: 'tabular-nums' }}>
          {pct}%
        </span>
      </div>
      <div style={{
        fontSize: '0.625rem',
        letterSpacing: '0.08em',
        color,
        background: 'var(--color-surface-2)',
        padding: '2px 6px',
        border: '1px solid var(--color-border)',
        borderRadius: 0,
      }}>
        [{'█'.repeat(filled)}{'░'.repeat(empty)}] {value}/{max}
      </div>
    </div>
  )
}

function PriorityBadge({ level, children }: { level: 'alta' | 'media' | 'baja'; children: React.ReactNode }) {
  const colors = {
    alta: { bg: 'rgba(192, 57, 43, 0.15)', border: '#C0392B', text: '#E74C3C' },
    media: { bg: 'rgba(243, 156, 18, 0.15)', border: '#F39C12', text: '#F39C12' },
    baja: { bg: 'rgba(39, 174, 96, 0.15)', border: '#27AE60', text: '#27AE60' },
  }
  const c = colors[level]
  return (
    <span style={{
      display: 'inline-flex',
      alignItems: 'center',
      padding: '0.1rem 0.5rem',
      border: `1px solid ${c.border}`,
      background: c.bg,
      color: c.text,
      fontSize: '0.5625rem',
      fontWeight: 800,
      letterSpacing: '0.05em',
      textTransform: 'uppercase',
      fontFamily: 'var(--font-mono)',
      borderRadius: 0,
    }}>
      {children}
    </span>
  )
}

export default function CoverageModal({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
  const [data, setData] = useState<CoverageReport | null>(null)
  const [activeTab, setActiveTab] = useState<'resumen' | 'gaps' | 'acciones'>('resumen')

  const handleTabChange = (id: string) => {
    setActiveTab(id as 'resumen' | 'gaps' | 'acciones')
  }

  useEffect(() => {
    if (isOpen && !data) {
      fetch('/data/reporte_cobertura.json')
        .then(res => res.json())
        .then(setData)
        .catch(() => {})
    }
  }, [isOpen, data])

  if (!isOpen) return null

  return (
    <div style={{
      position: 'fixed',
      top: 0, left: 0, right: 0, bottom: 0,
      background: 'rgba(0, 0, 0, 0.85)',
      backdropFilter: 'blur(8px)',
      zIndex: 9999,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '1.5rem'
    }}>
      <div style={{
        background: 'var(--color-surface)',
        border: '1px solid var(--color-amber)',
        maxWidth: '950px',
        width: '100%',
        maxHeight: '90vh',
        overflowY: 'auto',
        color: 'var(--color-text-primary)',
        fontFamily: 'var(--font-mono)',
        display: 'flex',
        flexDirection: 'column',
      }}>
        {/* Header */}
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          borderBottom: '1px solid var(--color-border-hi)',
          padding: '1rem 1.5rem',
          background: 'var(--color-surface-2)',
        }}>
          <div>
            <h3 style={{ color: 'var(--color-amber)', fontSize: '1rem', fontWeight: 800, margin: 0, letterSpacing: '0.04em' }}>
              {'>'} REPORTE DE COBERTURA & MATRIZ DE VACÍOS (POA 2026)
            </h3>
            <p style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)', marginTop: '0.25rem' }}>
              Diagnóstico de cobertura institucional (ASEA, CENAGAS, SENER, GEBCO) y Plan de Acción Priorizado
            </p>
          </div>
          <button
            onClick={onClose}
            style={{
              background: 'var(--color-surface-2)',
              border: '1px solid var(--color-border-hi)',
              color: 'var(--color-amber)',
              padding: '0.4rem 0.8rem',
              cursor: 'pointer',
              fontWeight: 700,
              fontSize: '0.75rem',
              fontFamily: 'var(--font-mono)',
            }}
          >
            [X] CERRAR
          </button>
        </div>

        {/* Tab Navigation */}
        <div style={{
          display: 'flex',
          borderBottom: '1px solid var(--color-border)',
          background: 'var(--color-surface-2)',
          padding: '0 1.5rem',
        }}>
          {[
            { id: 'resumen', label: '> RESUMEN EJECUTIVO', icon: '█' },
            { id: 'gaps', label: '> VACÍOS IDENTIFICADOS', icon: '!' },
            { id: 'acciones', label: '> ACCIONES PRIORITARIAS', icon: '>' },
          ].map(t => (
            <button
              key={t.id}
              onClick={() => handleTabChange(t.id)}
              style={{
                background: activeTab === t.id ? 'var(--color-surface)' : 'transparent',
                border: 'none',
                borderBottom: `3px solid ${activeTab === t.id ? 'var(--color-amber)' : 'transparent'}`,
                color: activeTab === t.id ? 'var(--color-amber)' : 'var(--color-text-muted)',
                padding: '0.75rem 1.25rem',
                fontSize: '0.6875rem',
                fontWeight: 800,
                cursor: 'pointer',
                fontFamily: 'var(--font-mono)',
                letterSpacing: '0.04em',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                transition: 'color 0.15s ease',
              }}
            >
              <span style={{ color: activeTab === t.id ? 'var(--color-amber)' : 'var(--color-text-muted)' }}>{t.icon}</span>
              {t.label}
            </button>
          ))}
        </div>

        {data && (
          <div style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            {activeTab === 'resumen' && (
              <>
                {/* Executive Summary Cards */}
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem' }}>
                  <div style={{ background: 'var(--color-surface-2)', padding: '1.25rem', borderLeft: '4px solid var(--color-amber)' }}>
                    <div style={{ fontSize: '0.625rem', color: 'var(--color-text-muted)', textTransform: 'uppercase', marginBottom: '0.5rem' }}>PROYECTOS GNL CONSOLIDADOS</div>
                    <div style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--color-amber)', fontVariantNumeric: 'tabular-nums' }}>
                      {data.cobertura_datos.proyectos_gnl_consolidados.total}
                    </div>
                    <AsciiBar label="Completitud" value={data.cobertura_datos.proyectos_gnl_consolidados.total} max={6} color="var(--color-amber)" />
                  </div>

                  <div style={{ background: 'var(--color-surface-2)', padding: '1.25rem', borderLeft: '4px solid var(--color-ocean)' }}>
                    <div style={{ fontSize: '0.625rem', color: 'var(--color-text-muted)', textTransform: 'uppercase', marginBottom: '0.5rem' }}>BATIMETRÍA PROCESADA</div>
                    <div style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--color-ocean)', fontVariantNumeric: 'tabular-nums' }}>
                      {data.cobertura_datos.batimetria.contornos_generados}
                    </div>
                    <AsciiBar label="Contornos" value={data.cobertura_datos.batimetria.contornos_generados} max={200} color="var(--color-ocean)" />
                  </div>

                  <div style={{ background: 'var(--color-surface-2)', padding: '1.25rem', borderLeft: '4px solid #10B981' }}>
                    <div style={{ fontSize: '0.625rem', color: 'var(--color-text-muted)', textTransform: 'uppercase', marginBottom: '0.5rem' }}>GACETAS ECOLÓGICAS (SINAT)</div>
                    <div style={{ fontSize: '1.75rem', fontWeight: 800, color: '#10B981', fontVariantNumeric: 'tabular-nums' }}>
                      {data.cobertura_datos.gaceta_ecologica.total_publicaciones}
                    </div>
                    <AsciiBar label="PDFs" value={data.cobertura_datos.gaceta_ecologica.total_publicaciones} max={500} color="#10B981" />
                  </div>

                  <div style={{ background: 'var(--color-surface-2)', padding: '1.25rem', borderLeft: '4px solid var(--color-accent)' }}>
                    <div style={{ fontSize: '0.625rem', color: 'var(--color-text-muted)', textTransform: 'uppercase', marginBottom: '0.5rem' }}>ASEA FILTRADOS (SON/BC/BCS)</div>
                    <div style={{ fontSize: '1.75rem', fontWeight: 800, color: 'var(--color-accent)', fontVariantNumeric: 'tabular-nums' }}>
                      {data.cobertura_datos.proyectos_asea.filtrados_sonora_bc_bcs_gnl}
                    </div>
                    <AsciiBar label="Filtrados" value={data.cobertura_datos.proyectos_asea.filtrados_sonora_bc_bcs_gnl} max={data.cobertura_datos.proyectos_asea.total_portal_consulta_publica} color="var(--color-accent)" />
                  </div>
                </div>

                {/* GNL Details Grid */}
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem' }}>
                  <div style={{ background: 'var(--color-surface-2)', padding: '1rem', border: '1px solid var(--color-border)', borderLeft: '4px solid var(--color-alert)' }}>
                    <div style={{ fontSize: '0.625rem', color: 'var(--color-text-muted)', textTransform: 'uppercase', marginBottom: '0.5rem' }}>TIPOLOGÍA GNL</div>
                    {Object.entries(data.cobertura_datos.proyectos_gnl_consolidados.por_tipo).map(([tipo, count]) => (
                      <AsciiBar key={tipo} label={tipo.toUpperCase()} value={count} max={data.cobertura_datos.proyectos_gnl_consolidados.total} color="var(--color-alert)" />
                    ))}
                  </div>

                  <div style={{ background: 'var(--color-surface-2)', padding: '1rem', border: '1px solid var(--color-border)', borderLeft: '4px solid var(--color-ocean)' }}>
                    <div style={{ fontSize: '0.625rem', color: 'var(--color-text-muted)', textTransform: 'uppercase', marginBottom: '0.5rem' }}>DISTRIBUCIÓN ESTATAL</div>
                    {Object.entries(data.cobertura_datos.proyectos_gnl_consolidados.por_estado).map(([estado, count]) => (
                      <AsciiBar key={estado} label={estado.toUpperCase()} value={count} max={data.cobertura_datos.proyectos_gnl_consolidados.total} color="var(--color-ocean)" />
                    ))}
                  </div>
                </div>
              </>
            )}

            {activeTab === 'gaps' && (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>
                {Object.entries(data.gaps_identificados).map(([categoria, gaps]) => (
                  <div key={categoria} style={{ background: 'var(--color-surface-2)', padding: '1.25rem', border: '1px solid var(--color-border)', borderLeft: '4px solid #EF4444' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
                      <span style={{ color: '#EF4444', fontSize: '1rem' }}>!</span>
                      <h4 style={{ color: 'var(--color-text-primary)', fontSize: '0.75rem', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                        {categoria.toUpperCase().replace(/_/g, ' ')}
                      </h4>
                    </div>
                    <ul style={{ listStyle: 'none', padding: 0, display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                      {gaps.map((gap, i) => (
                        <li key={i} style={{
                          color: 'var(--color-text-secondary)',
                          fontSize: '0.75rem',
                          lineHeight: 1.5,
                          paddingLeft: '1.25rem',
                          position: 'relative',
                          borderLeft: '1px dashed var(--color-border)',
                          paddingBottom: '0.5rem',
                        }}>
                          <span style={{ position: 'absolute', left: '0.5rem', color: '#EF4444', fontWeight: 800 }}>▸</span>
                          {gap}
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'acciones' && (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>
                {Object.entries(data.acciones_recomendadas_proxima_iteracion).map(([prioridad, acciones]) => (
                  <div key={prioridad} style={{ background: 'var(--color-surface-2)', padding: '1.25rem', border: '1px solid var(--color-border)', borderLeft: `4px solid ${prioridad === 'prioridad_alta' ? '#EF4444' : prioridad === 'prioridad_media' ? '#F39C12' : '#27AE60'}` }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
                      <PriorityBadge level={prioridad === 'prioridad_alta' ? 'alta' : prioridad === 'prioridad_media' ? 'media' : 'baja'}>
                        {prioridad.toUpperCase().replace('_', ' ')}
                      </PriorityBadge>
                    </div>
                    <ul style={{ listStyle: 'none', padding: 0, display: 'flex', flexDirection: 'column', gap: '0.625rem' }}>
                      {acciones.map((accion, i) => (
                        <li key={i} style={{
                          color: 'var(--color-text-secondary)',
                          fontSize: '0.75rem',
                          lineHeight: 1.5,
                          paddingLeft: '1.5rem',
                          position: 'relative',
                          borderLeft: '1px dashed var(--color-border)',
                          paddingBottom: '0.5rem',
                        }}>
                          <span style={{ position: 'absolute', left: '0.5rem', color: 'var(--color-accent)', fontWeight: 800 }}>▸</span>
                          {accion}
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {!data && (
          <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--color-text-muted)' }}>
            [ CARGANDO REPORTE DE COBERTURA... ]
          </div>
        )}
      </div>
    </div>
  )
}