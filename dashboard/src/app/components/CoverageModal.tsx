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

export default function CoverageModal({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
  const [data, setData] = useState<CoverageReport | null>(null)

  useEffect(() => {
    if (isOpen && !data) {
      fetch('/data/reporte_cobertura.json')
        .then(res => res.json())
        .then(setData)
        .catch(console.error)
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
        maxWidth: '900px',
        width: '100%',
        maxHeight: '90vh',
        overflowY: 'auto',
        padding: '1.5rem',
        color: 'var(--color-text-primary)',
        fontFamily: 'var(--font-mono)'
      }}>
        {/* Header */}
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          borderBottom: '1px solid var(--color-border-hi)',
          paddingBottom: '1rem',
          marginBottom: '1rem'
        }}>
          <div>
            <h3 style={{ color: 'var(--color-amber)', fontSize: '1.125rem', fontWeight: 700 }}>
              &gt; REPORTES & MATRIZ DE VACÍOS DE INFORMACIÓN (POA 2026)
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
              fontSize: '0.875rem'
            }}
          >
            [X] CERRAR
          </button>
        </div>

        {data ? (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem', fontSize: '0.8125rem' }}>
            {/* Executive Summary Cards */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '0.75rem' }}>
              <div style={{ background: 'var(--color-surface-2)', padding: '0.875rem', borderLeft: '3px solid var(--color-amber)' }}>
                <div style={{ fontSize: '0.6875rem', color: 'var(--color-text-muted)' }}>PROYECTOS GNL CONSOLIDADOS</div>
                <div style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--color-amber)' }}>
                  {data.cobertura_datos.proyectos_gnl_consolidados.total}
                </div>
                <div style={{ fontSize: '0.6875rem', color: 'var(--color-text-primary)' }}>ASEA, CENAGAS, SENER</div>
              </div>

              <div style={{ background: 'var(--color-surface-2)', padding: '0.875rem', borderLeft: '3px solid var(--color-ocean)' }}>
                <div style={{ fontSize: '0.6875rem', color: 'var(--color-text-muted)' }}>BATIMETRÍA PROCESADA</div>
                <div style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--color-ocean)' }}>
                  {data.cobertura_datos.batimetria.contornos_generados} contornos
                </div>
                <div style={{ fontSize: '0.6875rem', color: 'var(--color-text-primary)' }}>GEBCO 2024 / ETOPO1</div>
              </div>

              <div style={{ background: 'var(--color-surface-2)', padding: '0.875rem', borderLeft: '3px solid #10B981' }}>
                <div style={{ fontSize: '0.6875rem', color: 'var(--color-text-muted)' }}>GACETAS ECOLÓGICAS (SINAT)</div>
                <div style={{ fontSize: '1.25rem', fontWeight: 700, color: '#10B981' }}>
                  {data.cobertura_datos.gaceta_ecologica.total_publicaciones} PDFs
                </div>
                <div style={{ fontSize: '0.6875rem', color: 'var(--color-text-primary)' }}>Periodo 2023 - 2026</div>
              </div>
            </div>

            {/* High Priority Actions */}
            <div>
              <h4 style={{ color: 'var(--color-amber)', borderBottom: '1px dashed var(--color-border)', paddingBottom: '0.35rem', marginBottom: '0.6rem' }}>
                &gt; ACCIONES PRIORITARIAS DE IMPLEMENTACIÓN (ITERACIÓN ALTA)
              </h4>
              <ul style={{ listStyleType: 'square', paddingLeft: '1.25rem', display: 'flex', flexDirection: 'column', gap: '0.35rem' }}>
                {data.acciones_recomendadas_proxima_iteracion.prioridad_alta?.map((act, i) => (
                  <li key={i} style={{ color: '#FBBF24' }}>{act}</li>
                ))}
              </ul>
            </div>

            {/* Identified Gaps */}
            <div>
              <h4 style={{ color: '#EF4444', borderBottom: '1px dashed var(--color-border)', paddingBottom: '0.35rem', marginBottom: '0.6rem' }}>
                [!] VACÍOS DE INFORMACIÓN CLAVE (GAPS DETECTADOS)
              </h4>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                <div>
                  <strong style={{ color: 'var(--color-text-muted)', fontSize: '0.75rem' }}>PROYECTOS GNL & INFRAESTRUCTURA:</strong>
                  <ul style={{ listStyleType: 'circle', paddingLeft: '1rem', marginTop: '0.35rem', display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
                    {data.gaps_identificados.proyectos_gnl?.map((gap, i) => (
                      <li key={i} style={{ color: 'var(--color-text-secondary)' }}>{gap}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <strong style={{ color: 'var(--color-text-muted)', fontSize: '0.75rem' }}>BATIMETRÍA & OCEANOGRAFÍA:</strong>
                  <ul style={{ listStyleType: 'circle', paddingLeft: '1rem', marginTop: '0.35rem', display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
                    {data.gaps_identificados.batimetria?.map((gap, i) => (
                      <li key={i} style={{ color: 'var(--color-text-secondary)' }}>{gap}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>

          </div>
        ) : (
          <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--color-text-muted)' }}>
            Cargando datos de cobertura y vacíos...
          </div>
        )}
      </div>
    </div>
  )
}
