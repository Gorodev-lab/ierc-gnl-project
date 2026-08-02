'use client'

import React, { useEffect, useState } from 'react'
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

const ZONE_META: Record<string, { zone: string; icon: string; desc: string }> = {
  'MPL_Saguaro_Puerto_Libertad': {
    zone: 'Puerto Libertad (Saguaro GNL)',
    icon: '⚡',
    desc: 'Terminal Saguaro Energía (30 MTPA total). Conexión con Gasoducto Sierra Madre (800 km). Pesca artesanal de camarón, chano y almeja.',
  },
  'Amigo_LNG_Guaymas': {
    zone: 'Guaymas (Amigo LNG)',
    icon: '🚢',
    desc: 'Terminal Amigo LNG (7.8 MTPA). Coordenadas exactas GEM Wiki. Puerto pesquero industrial de alta diversidad de artes.',
  },
  'Vista_Pacifico_Topolobampo': {
    zone: 'Topolobampo (Vista Pacífico LNG)',
    icon: '❌',
    desc: 'PROYECTO CANCELADO Feb 2026. Afectaba Sitio Ramsar Topolobampo (21.9 ha) y ANP Islas del Golfo de California (2.15 km W).',
  },
  'GNL_Cosala_Sinaloa': {
    zone: 'Mazatlán & Zapopan (GNL Cosalá)',
    icon: '🏭',
    desc: 'Estaciones de compresión propano y almacenamiento. En evaluación ASEA (trámites 25SI2023G0009 y 14JA2025G0073).',
  },
}

function getRiskLevelClass(nivel: string) {
  if (nivel === 'CANCELADO') return 'progress-fill--ocean'
  if (nivel === 'Alto')      return 'progress-fill--high'
  if (nivel === 'Moderado')  return 'progress-fill--medium'
  return 'progress-fill--low'
}

function ComponentBar({ label, value }: { label: string; value: number }) {
  return (
    <div style={{ marginBottom: '0.625rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 3 }}>
        <span style={{ fontSize: '0.6875rem', color: 'var(--color-text-muted)' }}>{label}</span>
        <span style={{ fontSize: '0.6875rem', fontWeight: 600, color: 'var(--color-amber)', fontVariantNumeric: 'tabular-nums' }}>
          {(value * 100).toFixed(0)}%
        </span>
      </div>
      <div className="progress-bar">
        <div
          className="progress-fill progress-fill--high"
          style={{ width: `${value * 100}%` }}
        />
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
      display: 'flex', flexDirection: 'column', gap: '0.875rem',
      opacity: isCancel ? 0.85 : 1,
      borderColor: isCancel ? '#546E7A' : undefined
    }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '0.5rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
            <span style={{ fontSize: '1.125rem' }}>{meta?.icon ?? ''}</span>
            <span style={{
              fontSize: '0.9375rem',
              fontWeight: 700,
              color: isCancel ? '#90A4AE' : 'var(--color-amber)',
              fontFamily: 'var(--font-mono)',
            }}>
              {meta?.zone ?? project.estado}
            </span>
          </div>
          <p style={{ fontSize: '0.6875rem', color: 'var(--color-text-muted)', lineHeight: 1.4 }}>
            {project.proyecto_nombre}
          </p>
        </div>
        <RiskBadge level={isCancel ? 'CANCELADO' : project.nivel_riesgo} />
      </div>

      {/* Score gauge */}
      <div style={{ textAlign: 'center', padding: '0.25rem 0' }}>
        <div className="score-number" style={{ color: isCancel ? '#90A4AE' : undefined }}>
          {hasRisk ? project.riesgo_pesquero.toFixed(1) : '—'}
        </div>
        <div className="score-label">Riesgo pesquero / 100</div>
        <div className="progress-bar" style={{ marginTop: '0.5rem' }}>
          <div
            className={`progress-fill ${getRiskLevelClass(project.nivel_riesgo)}`}
            style={{ width: `${project.riesgo_pesquero}%`, background: isCancel ? '#78909C' : undefined }}
          />
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
          borderRadius: 'var(--radius-sm)',
          border: '1px solid var(--color-border)',
        }}>
          {meta.desc}
        </p>
      )}

      {/* Stats */}
      {hasRisk && (
        <div>
          <ComponentBar label="Densidad de esfuerzo" value={project.densidad_esfuerzo_pesquero} />
          <ComponentBar label="Proximidad normalizada" value={project.proximidad_normalizada} />
          <ComponentBar label="Especies críticas" value={project.especies_criticas_score} />
        </div>
      )}

      {/* Quick stats */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
        <div style={{
          background: 'var(--color-surface-2)',
          border: '1px solid var(--color-border)',
          borderRadius: 'var(--radius-sm)',
          padding: '0.5rem',
        }}>
          <div style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--color-ocean)', fontVariantNumeric: 'tabular-nums' }}>
            {project.num_zonas_encontradas.toLocaleString()}
          </div>
          <div style={{ fontSize: '0.625rem', color: 'var(--color-text-muted)' }}>
            zonas pesqueras
          </div>
        </div>
        <div style={{
          background: 'var(--color-surface-2)',
          border: '1px solid var(--color-border)',
          borderRadius: 'var(--radius-sm)',
          padding: '0.5rem',
        }}>
          <div style={{ fontSize: '1rem', fontWeight: 700, color: isCancel ? '#90A4AE' : 'var(--color-amber)', fontVariantNumeric: 'tabular-nums' }}>
            {project.zona_mas_cercana_km !== null ? `${project.zona_mas_cercana_km} km` : 'N/A'}
          </div>
          <div style={{ fontSize: '0.625rem', color: 'var(--color-text-muted)' }}>
            zona más cercana
          </div>
        </div>
      </div>

      {/* Artes */}
      {project.artes_de_pesca?.length > 0 && (
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.35rem', marginTop: '0.25rem' }}>
          {project.artes_de_pesca.map(art => (
            <span key={art} style={{
              padding: '0.15rem 0.5rem',
              borderRadius: 3,
              fontSize: '0.625rem',
              background: 'var(--color-surface-3)',
              border: '1px solid var(--color-border-hi)',
              color: 'var(--color-text-secondary)',
            }}>
              {art}
            </span>
          ))}
        </div>
      )}

      {/* Location */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        fontSize: '0.6875rem',
        color: 'var(--color-text-muted)',
        marginTop: 'auto',
        paddingTop: '0.5rem',
        borderTop: '1px solid var(--color-border)',
        fontVariantNumeric: 'tabular-nums',
      }}>
        <span>{project.estado}</span>
        <span>{project.latitud.toFixed(4)}°N · {Math.abs(project.longitud).toFixed(4)}°W</span>
      </div>
    </div>
  )
}

export default function ZoneCards() {
  const [projects, setProjects] = useState<Project[]>([])

  useEffect(() => {
    fetch('/data/riesgo_proyectos.json')
      .then(r => r.json())
      .then(data => {
        setProjects(data.proyectos || [])
      })
      .catch(console.error)
  }, [])

  return (
    <div className="section">
      <div className="section-title">Terminales GNL en Evaluación & Riesgo Pesquero PANGAS</div>
      <div className="grid-2" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.25rem' }}>
        {projects.map(p => <ProjectCard key={p.proyecto_id} project={p} />)}
      </div>
    </div>
  )
}
