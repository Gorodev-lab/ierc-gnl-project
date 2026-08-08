'use client'

import React from 'react'
import RiskBadge from './RiskBadge'

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

interface ZoneMeta {
  zone: string
  code: string
  desc: string
}

interface ProjectCardProps {
  project: Project
  zoneMeta: ZoneMeta | null
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

export default function ProjectCard({ project, zoneMeta }: ProjectCardProps) {
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
            <span className="terminal-tag">{zoneMeta?.code ?? 'GNL-00'}</span>
            <span style={{
              fontSize: '0.9375rem',
              fontWeight: 800,
              color: isCancel ? 'var(--color-text-secondary)' : 'var(--color-accent)',
              fontFamily: 'var(--font-mono)',
            }}>
              {zoneMeta?.zone ?? project.estado}
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
      {zoneMeta?.desc && (
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
          {zoneMeta.desc}
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