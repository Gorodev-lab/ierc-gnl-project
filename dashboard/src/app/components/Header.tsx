import React from 'react'

export default function Header() {
return (
<>
{/* Esoteria Scanlines Overlay */}
<div className="scanlines" />

<header style={{
background: 'var(--color-surface)',
borderBottom: '1px solid var(--color-border-hi)',
position: 'sticky',
top: 0,
zIndex: 100,
backdropFilter: 'blur(10px)',
}}>
{/* Topbar */}
<div style={{
maxWidth: 1400,
margin: '0 auto',
padding: '0.75rem 1.5rem',
display: 'flex',
alignItems: 'center',
justifyContent: 'space-between',
gap: '1rem',
}}>
{/* Brand */}
<div style={{ display: 'flex', alignItems: 'center', gap: '0.875rem' }}>
<div className="hex-pulse" style={{
width: 38, height: 38,
borderRadius: 6,
background: 'var(--color-surface-2)',
border: '1px solid var(--color-amber)',
display: 'flex', alignItems: 'center', justifyContent: 'center',
fontSize: '1.125rem',
color: 'var(--color-amber)',
boxShadow: '0 0 12px var(--color-amber-glow)',
flexShrink: 0,
}}>

</div>

<div>
<h1 style={{
fontSize: '1.0625rem',
fontWeight: 700,
color: 'var(--color-amber)',
lineHeight: 1.2,
letterSpacing: '0.08em',
fontFamily: 'var(--font-mono)',
}}>
IERC-GNL <span style={{ color: 'var(--color-ocean)' }}>[CAUSA NATURA CENTER]</span>
</h1>
<p style={{
fontSize: '0.6875rem',
color: 'var(--color-text-muted)',
marginTop: 2,
letterSpacing: '0.04em',
}}>
Índice Espacial de Riesgo Socioeconómico · Golfo de California
</p>
</div>
</div>

{/* Right Status */}
<div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
<div style={{
display: 'flex', alignItems: 'center', gap: '0.5rem',
padding: '4px 10px',
border: '1px solid var(--color-ok)',
borderRadius: 4,
fontSize: '0.6875rem',
color: 'var(--color-ok)',
letterSpacing: '0.06em',
}}>
<span className="blink" style={{
width: 6, height: 6, borderRadius: '50%',
background: 'var(--color-ok)',
display: 'inline-block',
}} />
GEOPACKAGE API ONLINE
</div>

<div style={{
padding: '4px 10px',
borderRadius: 4,
background: 'var(--color-ocean-glow)',
border: '1px solid var(--color-ocean-dim)',
fontSize: '0.6875rem',
color: 'var(--color-ocean)',
fontWeight: 600,
letterSpacing: '0.06em',
}}>
OGC GeoPackage v1.2
</div>
</div>
</div>

{/* Esoteria System Metrics Strip */}
<div style={{
borderTop: '1px solid var(--color-border)',
background: 'var(--color-surface-2)',
}}>
<div style={{
maxWidth: 1400,
margin: '0 auto',
padding: '0.45rem 1.5rem',
display: 'flex',
gap: '2rem',
overflowX: 'auto',
fontFamily: 'var(--font-mono)',
}}>
{[
{ label: 'PROYECTOS GNL', value: '5', sub: 'capa: proyectos_gnl' },
{ label: 'ALTO RIESGO', value: '3', sub: 'score >= 90.0', color: 'var(--color-alert)' },
{ label: 'GRILLA H3', value: '6,305', sub: 'res 8 (0.73 km²)' },
{ label: 'ZONAS PANGAS', value: '17', sub: 'sitios consolidados', color: 'var(--color-ocean)' },
{ label: 'CRS ESPACIAL', value: 'EPSG:4326', sub: 'WGS84 Geodésico' },
].map(m => (
<div key={m.label} style={{ flexShrink: 0 }}>
<div style={{
fontSize: '0.8125rem',
fontWeight: 700,
color: m.color ?? 'var(--color-amber)',
fontVariantNumeric: 'tabular-nums',
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
