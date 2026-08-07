'use client'

import React, { useState, useEffect } from 'react'
import { useFetch } from '@/lib/useFetch'
import RiskBadge from './RiskBadge'
import { getRiskColor } from '@/lib/risk'

interface Project {
  proyecto_id: string
  proyecto_nombre: string
  latitud: number
  longitud: number
  estado: string
  estatus: string
  capacidad_mtpa: number | null
  riesgo_pesquero: number
  nivel_riesgo: string
  num_zonas_encontradas: number
  zona_mas_cercana_km: number | null
  densidad_esfuerzo_pesquero: number
  proximidad_normalizada: number
  especies_criticas_score: number
  artes_de_pesca: string[]
  nota: string
}

const ZONE_META: Record<string, { zone: string; code: string; desc: string }> = {
  'MPL_Saguaro_Puerto_Libertad': {
    zone: 'Puerto Libertad (Saguaro GNL)',
    code: 'PL-SAG-01',
    desc: 'Terminal Saguaro Energía (30 MTPA total). Conexión con Gasoducto Sierra Madre (800 km). Pesca artesanal de camarón, chano y almeja.',
  },
  'Amigo_LNG_Guaymas': {
    zone: 'Guaymas (Amigo LNG)',
    code: 'GYM-AMG-02',
    desc: 'Terminal Amigo LNG (7.8 MTPA). Coordenadas exactas GEM Wiki. Puerto pesquero industrial de alta diversidad de artes.',
  },
  'Vista_Pacifico_Topolobampo': {
    zone: 'Topolobampo (Vista Pacífico LNG)',
    code: 'TOP-VPA-03',
    desc: 'PROYECTO CANCELADO Feb 2026. Afectaba Sitio Ramsar Topolobampo (21.9 ha) y ANP Islas del Golfo de California (2.15 km W).',
  },
  'GNL_Cosala_Sinaloa': {
    zone: 'Mazatlán & Zapopan (GNL Cosalá)',
    code: 'MZT-COS-04',
    desc: 'Estaciones de compresión propano y almacenamiento. En evaluación ASEA (trámites 25SI2023G0009 y 14JA2025G0073).',
  },
}

function AsciiBar({ label, value }: { label: string; value: number }) {
  const percent = Math.min(100, Math.max(0, Math.round(value * 100)))
  const filledBlocks = Math.round((percent / 100) * 10)
  const emptyBlocks = 10 - filledBlocks
  const barString = '█'.repeat(filledBlocks) + '░'.repeat(emptyBlocks)

  return (
    <div style={{ marginBottom: '0.625rem', fontFamily: 'var(--font-mono)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 2 }}>
        <span style={{ fontSize: '0.6875rem', color: 'var(--color-text-secondary)', textTransform: 'uppercase' }}>{label}</span>
        <span style={{ fontSize: '0.6875rem', fontWeight: 700, color: 'var(--color-accent)', fontVariantNumeric: 'tabular-nums' }}>
          {percent}%
        </span>
      </div>
      <div style={{
        fontSize: '0.72rem',
        letterSpacing: '0.08em',
        color: value > 0.6 ? 'var(--color-alert)' : value > 0.3 ? 'var(--color-warn)' : 'var(--color-ok)',
        background: 'var(--color-surface-2)',
        padding: '2px 6px',
        border: '1px solid var(--color-border)',
        borderRadius: 0,
      }}>
        [{barString}]
      </div>
    </div>
  )
}

function ProjectCard({ project }: { project: Project }) {
  const meta = ZONE_META[project.proyecto_id]
  const hasRisk = project.riesgo_pesquero > 0
  const isCancel = project.estatus.includes('CANCELADO')

  return (
    <div className={`card ${isCancel ? '' : 'card--amber'}`} style={{
      display: 'flex',
      flexDirection: 'column',
      gap: '0.875rem',
      opacity: isCancel ? 0.85 : 1,
      borderColor: isCancel ? 'var(--color-border-hi)' : undefined,
      borderRadius: 0,
    }}>
      {/* Card Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '0.5rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
            <span className="terminal-tag">{meta?.code ?? 'GNL-00'}</span>
            <span style={{
              fontSize: '0.9375rem',
              fontWeight: 800,
              color: isCancel ? 'var(--color-text-secondary)' : 'var(--color-accent)',
              fontFamily: 'var(--font-mono)',
            }}>
              {meta?.zone ?? project.estado}
            </span>
          </div>
          <p style={{ fontSize: '0.6875rem', color: 'var(--color-text-muted)', lineHeight: 1.4, fontFamily: 'var(--font-mono)' }}>
            {project.proyecto_nombre}
          </p>
        </div>
        <RiskBadge level={isCancel ? 'CANCELADO' : project.nivel_riesgo} />
      </div>

      {/* Score gauge */}
      <div style={{
        background: 'var(--color-surface-2)',
        padding: '0.75rem',
        border: '1px solid var(--color-border)',
        borderRadius: 0,
        textAlign: 'center'
      }}>
        <div style={{
          fontSize: '1.75rem',
          fontWeight: 800,
          fontFamily: 'var(--font-mono)',
          color: isCancel ? 'var(--color-text-muted)' : project.riesgo_pesquero >= 70 ? 'var(--color-alert)' : 'var(--color-accent)',
          fontVariantNumeric: 'tabular-nums',
          lineHeight: 1.1,
        }}>
          {hasRisk ? project.riesgo_pesquero.toFixed(1) : '0.0'}
        </div>
        <div style={{ fontSize: '0.625rem', color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginTop: 4 }}>
          ÍNDICE IERC DE RIESGO PESQUERO / 100
        </div>
      </div>

      {/* Zone description */}
      {meta?.desc && (
        <p style={{
          fontSize: '0.75rem',
          color: 'var(--color-text-secondary)',
          lineHeight: 1.5,
          padding: '0.625rem',
          background: 'var(--color-surface-2)',
          borderRadius: 0,
          border: '1px solid var(--color-border)',
          fontFamily: 'var(--font-mono)',
        }}>
          {meta.desc}
        </p>
      )}

      {/* Component Breakdown Bars */}
      {hasRisk && (
        <div style={{ padding: '0.5rem 0' }}>
          <AsciiBar label="Densidad Esfuerzo Pesquero" value={project.densidad_esfuerzo_pesquero} />
          <AsciiBar label="Proximidad Infraestructura GNL" value={project.proximidad_normalizada} />
          <AsciiBar label="Especies & Hábitats Críticos" value={project.especies_criticas_score} />
        </div>
      )}

      {/* Quick stats grid */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
        <div style={{
          background: 'var(--color-surface-2)',
          border: '1px solid var(--color-border)',
          borderRadius: 0,
          padding: '0.5rem',
        }}>
          <div style={{ fontSize: '1rem', fontWeight: 800, color: 'var(--color-ocean)', fontVariantNumeric: 'tabular-nums', fontFamily: 'var(--font-mono)' }}>
            {project.num_zonas_encontradas.toLocaleString()}
          </div>
          <div style={{ fontSize: '0.625rem', color: 'var(--color-text-muted)', textTransform: 'uppercase' }}>
            Polígonos PANGAS
          </div>
        </div>
        <div style={{
          background: 'var(--color-surface-2)',
          border: '1px solid var(--color-border)',
          borderRadius: 0,
          padding: '0.5rem',
        }}>
          <div style={{ fontSize: '1rem', fontWeight: 800, color: isCancel ? 'var(--color-text-muted)' : 'var(--color-accent)', fontVariantNumeric: 'tabular-nums', fontFamily: 'var(--font-mono)' }}>
            {project.zona_mas_cercana_km !== null ? `${project.zona_mas_cercana_km} km` : 'N/A'}
          </div>
          <div style={{ fontSize: '0.625rem', color: 'var(--color-text-muted)', textTransform: 'uppercase' }}>
            Buffer pesquero min
          </div>
        </div>
      </div>

      {/* Artes de pesca */}
      {project.artes_de_pesca?.length > 0 && (
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.35rem', marginTop: '0.25rem' }}>
          {project.artes_de_pesca.map(art => (
            <span key={art} className="terminal-tag">
              {art}
            </span>
          ))}
        </div>
      )}

      {/* Location Footer */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        fontSize: '0.6875rem',
        color: 'var(--color-text-muted)',
        marginTop: 'auto',
        paddingTop: '0.5rem',
        borderTop: '1px solid var(--color-border)',
        fontVariantNumeric: 'tabular-nums',
        fontFamily: 'var(--font-mono)',
      }}>
        <span>{project.estado}</span>
        <span>{project.latitud.toFixed(4)}°N · {Math.abs(project.longitud).toFixed(4)}°W</span>
      </div>
    </div>
  )
}

export default function ZoneCards() {
  const { data, loading, error, refetch } = useFetch<{ proyectos: Project[] }>('/data/riesgo_proyectos.json')

  return (
    <div className="section">
      <div className="section-title">Terminales GNL & Evaluación de Riesgo Pesquero PANGAS</div>

      {loading && (
        <div style={{ padding: '2rem', textAlign: 'center', fontFamily: 'var(--font-mono)', color: 'var(--color-text-muted)' }}>
          [ CARGANDO TERMINALES GNL... ]
        </div>
      )}

      {error && (
        <div style={{ padding: '1rem', background: 'rgba(192,57,43,0.15)', border: '1px solid #C0392B', color: '#E74C3C', fontFamily: 'var(--font-mono)', fontSize: '0.75rem' }}>
          Error cargando datos: {error.message}
          <button onClick={refetch} style={{ marginLeft: '1rem', background: 'transparent', border: '1px solid #C0392B', color: '#E74C3C', padding: '0.2rem 0.5rem', cursor: 'pointer', fontFamily: 'var(--font-mono)', fontSize: '0.6875rem' }}>
            REINTENTAR
          </button>
        </div>
      )}

      {!loading && !error && (
        <div className="grid-2" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.25rem' }}>
          {data?.proyectos?.map(p => <ProjectCard key={p.proyecto_id} project={p} />) || []}
        </div>
      )}
    </div>
  )
}
