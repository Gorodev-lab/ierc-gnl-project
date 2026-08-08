'use client'

import React, { useEffect, useState } from 'react'

interface Species {
  codigo: string
  nombre_comun: string
  nombre_cientifico: string
  estado_iucn: string
  importancia: string
}

interface ProjectSpecies {
  especies_presentes: string[]
  num_criticas: number
  riesgo_pesquero: number
}

interface SpeciesData {
  metadata: { fecha: string; fuente: string; total_zonas_analizadas: number }
  especies_criticas: Species[]
  por_proyecto: Record<string, ProjectSpecies>
}

const iucnColor: Record<string, { bg: string; color: string; border: string }> = {
  'CR': { bg: 'rgba(192, 57, 43, 0.25)',  color: '#C0392B', border: '#C0392B' },
  'EN': { bg: 'rgba(243, 156, 18, 0.25)', color: '#F39C12', border: '#F39C12' },
  'VU': { bg: 'rgba(255, 176, 0, 0.2)',   color: '#FFB000', border: '#FFB000' },
  'NT': { bg: 'rgba(14, 165, 233, 0.2)',  color: '#0EA5E9', border: '#0EA5E9' },
  'LC': { bg: 'rgba(39, 174, 96, 0.2)',   color: '#27AE60', border: '#27AE60' },
}

const PROJECT_LABELS: Record<string, string> = {
  'MPL_Saguaro_Puerto_Libertad': 'Puerto Libertad (Saguaro GNL)',
  'Bazan_San_Felipe':            'San Felipe',
  'Guaymas_Terminal':            'Guaymas',
}

function SpeciesIcon({ code }: { code: string }) {
  const c = code.toLowerCase()
  let tag = '[PEC]'
  if (c.includes('cam') || c.includes('far')) tag = '[CAM]'
  else if (c.includes('sph') || c.includes('tib')) tag = '[TIB]'
  else if (c.includes('rhi') || c.includes('das') || c.includes('ray')) tag = '[RAY]'
  else if (c.includes('epi') || c.includes('myc') || c.includes('mer') || c.includes('lut') || c.includes('par')) tag = '[PAR]'

  return (
    <span style={{
      fontSize: '0.6875rem',
      fontWeight: 800,
      fontFamily: 'var(--font-mono)',
      color: 'var(--color-accent)',
      letterSpacing: '0.04em',
    }}>
      {tag}
    </span>
  )
}

function IUCNBadge({ status }: { status: string }) {
  const cfg = iucnColor[status] ?? iucnColor['LC']
  return (
    <span style={{
      display: 'inline-block',
      padding: '0.15rem 0.5rem',
      borderRadius: 0,
      fontSize: '0.6875rem',
      fontWeight: 700,
      letterSpacing: '0.05em',
      background: cfg.bg,
      color: cfg.color,
      border: `1px solid ${cfg.border}`,
      fontFamily: 'var(--font-mono)',
    }}>
      {status}
    </span>
  )
}

export default function SpeciesPanel() {
  const [data, setData] = useState<SpeciesData | null>(null)
  const [selected, setSelected] = useState<string | null>(null)

  useEffect(() => {
    fetch('/data/especies_criticas.json')
      .then(r => r.json())
      .then(setData)
      .catch(() => {})
  }, [])

  if (!data) return null

  const { especies_criticas, por_proyecto } = data
  const filteredSpecies = selected
    ? especies_criticas.filter(s =>
        por_proyecto[selected]?.especies_presentes.includes(s.codigo)
      )
    : especies_criticas

  return (
    <div className="section">
      <div className="section-title">ESPECIES CRÍTICAS EN RIESGO PESQUERO (IUCN)</div>

      {/* Filter by project */}
      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.25rem', flexWrap: 'wrap' }}>
        <button
          onClick={() => setSelected(null)}
          style={{
            padding: '0.4rem 0.9rem',
            borderRadius: 0,
            border: `1px solid ${!selected ? 'var(--color-accent)' : 'var(--color-border)'}`,
            background: !selected ? 'var(--color-surface-3)' : 'transparent',
            color: !selected ? 'var(--color-text-primary)' : 'var(--color-text-muted)',
            fontSize: '0.75rem',
            fontWeight: 700,
            cursor: 'pointer',
            fontFamily: 'var(--font-mono)',
          }}
        >
          TODOS LOS PROYECTOS
        </button>
        {Object.entries(PROJECT_LABELS).map(([id, label]) => (
          <button
            key={id}
            onClick={() => setSelected(selected === id ? null : id)}
            style={{
              padding: '0.4rem 0.9rem',
              borderRadius: 0,
              border: `1px solid ${selected === id ? 'var(--color-accent)' : 'var(--color-border)'}`,
              background: selected === id ? 'var(--color-surface-3)' : 'transparent',
              color: selected === id ? 'var(--color-text-primary)' : 'var(--color-text-muted)',
              fontSize: '0.75rem',
              fontWeight: 700,
              cursor: 'pointer',
              fontFamily: 'var(--font-mono)',
            }}
          >
            {label.toUpperCase()}
            {por_proyecto[id] && (
              <span style={{
                marginLeft: '0.5rem',
                padding: '0.1rem 0.4rem',
                borderRadius: 0,
                background: 'rgba(192, 57, 43, 0.2)',
                border: '1px solid var(--color-alert)',
                color: 'var(--color-alert)',
                fontSize: '0.625rem',
                fontWeight: 700,
              }}>
                {por_proyecto[id].riesgo_pesquero}/100
              </span>
            )}
          </button>
        ))}
      </div>

      {/* Species grid */}
      <div className="grid-2">
        {filteredSpecies.map(sp => {
          const projectsWith = Object.entries(por_proyecto)
            .filter(([, pd]) => pd.especies_presentes.includes(sp.codigo))
            .map(([id]) => PROJECT_LABELS[id] ?? id)

          const isCritical = ['CR', 'EN'].includes(sp.estado_iucn)

          return (
            <div
              key={sp.codigo}
              className="card"
              style={{
                display: 'flex',
                gap: '1rem',
                alignItems: 'flex-start',
                borderRadius: 0,
                borderLeft: `3px solid ${isCritical ? 'var(--color-alert)' : 'var(--color-ocean)'}`,
              }}
            >
              {/* Icon */}
              <div style={{
                width: 42, height: 42,
                borderRadius: 0,
                background: 'var(--color-surface-2)',
                border: `1px solid ${isCritical ? 'var(--color-alert)' : 'var(--color-border-hi)'}`,
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                flexShrink: 0,
              }}>
                <SpeciesIcon code={sp.codigo} />
              </div>

              <div style={{ flex: 1, minWidth: 0 }}>
                {/* Name + IUCN */}
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.5rem', marginBottom: '0.25rem' }}>
                  <span style={{ fontWeight: 700, fontSize: '0.875rem', color: 'var(--color-text-primary)', fontFamily: 'var(--font-mono)' }}>
                    {sp.nombre_comun}
                  </span>
                  <IUCNBadge status={sp.estado_iucn} />
                </div>

                {/* Scientific name */}
                <p style={{
                  fontSize: '0.75rem',
                  color: 'var(--color-text-muted)',
                  fontStyle: 'italic',
                  marginBottom: '0.5rem',
                }}>
                  {sp.nombre_cientifico}
                </p>

                {/* Importancia */}
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  fontSize: '0.75rem',
                  marginBottom: '0.5rem',
                }}>
                  <span style={{ color: 'var(--color-text-muted)' }}>IMPORTANCIA:</span>
                  <span style={{ color: 'var(--color-text-secondary)', fontWeight: 600 }}>{sp.importancia.toUpperCase()}</span>
                </div>

                {/* Projects present */}
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.35rem' }}>
                  {projectsWith.map(proj => (
                    <span key={proj} style={{
                      padding: '0.15rem 0.45rem',
                      borderRadius: 0,
                      fontSize: '0.6875rem',
                      fontWeight: 600,
                      background: 'var(--color-surface-3)',
                      border: '1px solid var(--color-border-hi)',
                      color: 'var(--color-text-primary)',
                    }}>
                      {proj}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Source note */}
      <p style={{
        marginTop: '1.25rem',
        fontSize: '0.75rem',
        color: 'var(--color-text-muted)',
        fontFamily: 'var(--font-mono)',
      }}>
        FUENTE: {data.metadata.fuente} · {data.metadata.total_zonas_analizadas.toLocaleString()} ZONAS ANALIZADAS
      </p>
    </div>
  )
}
