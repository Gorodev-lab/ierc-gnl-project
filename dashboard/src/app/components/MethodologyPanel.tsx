import React from 'react'

export default function MethodologyPanel() {
const weights = [
{ label: 'Amenaza (infraestructura GNL)', weight: '20%', color: 'var(--color-alert)' },
{ label: 'Exposición pesquera', weight: '20%', color: 'var(--color-warn)' },
{ label: 'Sensibilidad de especies', weight: '15%', color: 'var(--color-amber)' },
{ label: 'Dependencia económica', weight: '15%', color: 'var(--color-amber-dim)' },
{ label: 'Valor biocultural', weight: '15%', color: 'var(--color-ok)' },
{ label: '(1 − Capacidad adaptativa)', weight: '15%', color: 'var(--color-ocean)' },
]

return (
<div className="section" style={{ borderTop: '1px solid var(--color-border)', paddingTop: '2rem' }}>
<div className="section-title">Metodología IERC & Motor de Cálculo Monte Carlo</div>

<div className="grid-2">
{/* Formula card */}
<div className="card card--amber">
<h3 style={{
fontSize: '0.875rem',
fontWeight: 700,
color: 'var(--color-amber)',
marginBottom: '1rem',
fontFamily: 'var(--font-mono)',
}}>
Fórmula IERC Total (6 Sub-índices)
</h3>
<div className="formula-box">
<div style={{ color: 'var(--color-text-muted)', marginBottom: '0.5rem', fontSize: '0.6875rem' }}>
// ÍNDICE ESPACIAL DE RIESGO SOCIOECONÓMICO DE COMUNIDADES
</div>
IERC = (Amenaza × 0.20)<br />
&nbsp;&nbsp;&nbsp;&nbsp;+ (Exposición × 0.20)<br />
&nbsp;&nbsp;&nbsp;&nbsp;+ (Sensibilidad × 0.15)<br />
&nbsp;&nbsp;&nbsp;&nbsp;+ (Dependencia × 0.15)<br />
&nbsp;&nbsp;&nbsp;&nbsp;+ (Biocultural × 0.15)<br />
&nbsp;&nbsp;&nbsp;&nbsp;+ ((1 − Cap.Adaptativa) × 0.15)
<br /><br />
<span style={{ color: 'var(--color-text-muted)', fontSize: '0.6875rem' }}>
// RIESGO PESQUERO (MORENO-BÁEZ ET AL. 2011, 2012):<br />
R = (0.50 × esfuerzo) + (0.30 × proximidad) + (0.20 × especies_críticas)
</span>
</div>

{/* Pesos */}
<div style={{ marginTop: '1.25rem' }}>
{weights.map(w => (
<div key={w.label} style={{
display: 'flex',
justifyContent: 'space-between',
alignItems: 'center',
padding: '0.45rem 0',
borderBottom: '1px solid var(--color-border)',
fontSize: '0.75rem',
}}>
<div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
<span style={{
display: 'inline-block',
width: 6, height: 6, borderRadius: '50%',
background: w.color,
}} />
<span style={{ color: 'var(--color-text-secondary)' }}>{w.label}</span>
</div>
<span style={{ fontWeight: 700, color: w.color, fontVariantNumeric: 'tabular-nums' }}>{w.weight}</span>
</div>
))}
</div>
</div>

{/* References + GeoPackage Engine */}
<div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
{/* References */}
<div className="card">
<h3 style={{
fontSize: '0.875rem',
fontWeight: 700,
color: 'var(--color-amber)',
marginBottom: '0.875rem',
fontFamily: 'var(--font-mono)',
}}>
Referencias Bibliográficas
</h3>
{[
{
authors: 'Moreno-Báez et al.',
year: '2011',
title: 'Integrating the spatial and temporal dimensions of fishing for management in the Northern Gulf of California, Mexico',
journal: 'Marine Policy, 35(3), 297–309',
},
{
authors: 'Moreno-Báez et al.',
year: '2012',
title: 'Integrating the spatial and temporal dimensions of fishing activities for management in the Northern Gulf of California, Mexico',
journal: 'Marine Policy, 38, 483–489',
},
].map(ref => (
<div key={ref.year} style={{
padding: '0.75rem',
background: 'var(--color-surface-2)',
borderRadius: 'var(--radius-sm)',
marginBottom: '0.625rem',
border: '1px solid var(--color-border)',
}}>
<div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--color-amber)', marginBottom: '0.25rem' }}>
{ref.authors} ({ref.year})
</div>
<div style={{ fontSize: '0.6875rem', color: 'var(--color-text-secondary)', lineHeight: 1.4, marginBottom: '0.25rem' }}>
{ref.title}
</div>
<div style={{ fontSize: '0.625rem', color: 'var(--color-ocean)', fontStyle: 'italic' }}>
{ref.journal}
</div>
</div>
))}
</div>

{/* Monte Carlo + Data Sources */}
<div className="card">
<h3 style={{
fontSize: '0.875rem',
fontWeight: 700,
color: 'var(--color-amber)',
marginBottom: '0.875rem',
fontFamily: 'var(--font-mono)',
}}>
Motor de Cálculo & Repositorio
</h3>
<div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
{[
{ label: 'Simulación Monte Carlo', value: '1,000 iteraciones/celda' },
{ label: 'Resolución espacial H3', value: 'Uber H3 Res 8 (0.73 km²)' },
{ label: 'Formato Entregable v1', value: 'OGC GeoPackage (EPSG:4326)' },
{ label: 'Ruta del Repositorio', value: 'deliverables/v1_geopackage/' },
{ label: 'Celdas H3 procesadas', value: '6,305 polígonos' },
{ label: 'Fuentes de datos', value: 'PANGAS GDB · dataMares · GFW' },
].map(row => (
<div key={row.label} className="stat-row">
<span className="stat-row-label">{row.label}</span>
<span className="stat-row-value">{row.value}</span>
</div>
))}
</div>
</div>
</div>
</div>

{/* Footer */}
<div style={{
marginTop: '2rem',
padding: '1rem 1.25rem',
background: 'var(--color-surface)',
borderRadius: 'var(--radius-md)',
border: '1px solid var(--color-border)',
display: 'flex',
justifyContent: 'space-between',
alignItems: 'center',
flexWrap: 'wrap',
gap: '0.75rem',
fontFamily: 'var(--font-mono)',
}}>
<div style={{ fontSize: '0.75rem', color: 'var(--color-amber)' }}>
IERC-GNL Project · Esoteria Design System v2
</div>
<div style={{ fontSize: '0.6875rem', color: 'var(--color-text-muted)' }}>
Datos: ierc_golfo_california.gpkg · PANGAS GDB · dataMares UCSD · GFW · CONANP
</div>
</div>
</div>
)
}
