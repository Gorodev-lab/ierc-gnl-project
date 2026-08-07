'use client'

import React, { useState, Suspense } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'

function LoginForm() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const redirect = searchParams.get('redirect') || '/'
  const [password, setPassword] = useState('')
  const [error, setError] = useState(false)
  const [showPassword, setShowPassword] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const res = await fetch('/api/auth', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password })
      })

      if (res.ok) {
        router.push(redirect)
        router.refresh()
      } else {
        setError(true)
        setPassword('')
      }
    } catch {
      setError(true)
      setPassword('')
    }
  }

  return (
    <div style={{
      minHeight: '100vh',
      background: 'var(--color-bg)',
      color: 'var(--color-text-primary)',
      fontFamily: 'var(--font-mono)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '2rem'
    }}>
      <form onSubmit={handleSubmit} style={{
        background: 'var(--color-surface)',
        border: '1px solid var(--color-border-hi)',
        borderRadius: '0px',
        padding: '2.5rem',
        width: '100%',
        maxWidth: '400px',
        boxShadow: 'none'
      }}>
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <div style={{
            width: 56,
            height: 56,
            borderRadius: 0,
            background: 'var(--color-surface-2)',
            border: '1px solid var(--color-accent)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '1.5rem',
            fontWeight: 800,
            color: 'var(--color-accent)',
            margin: '0 auto 1rem',
            fontFamily: 'var(--font-mono)',
          }}>{'>'}</div>
          <h1 style={{
            fontSize: '1.25rem',
            fontWeight: 800,
            color: 'var(--color-text-primary)',
            letterSpacing: '0.04em',
            marginBottom: '0.5rem',
            fontFamily: 'var(--font-mono)',
          }}>
            IERC-GNL
          </h1>
          <p style={{
            fontSize: '0.75rem',
            color: 'var(--color-text-secondary)',
            fontFamily: 'var(--font-mono)',
          }}>
            Índice Espacial de Riesgo Socioeconómico
          </p>
        </div>

        <div style={{ marginBottom: '1.5rem' }}>
          <label style={{
            display: 'block',
            fontSize: '0.75rem',
            fontWeight: 700,
            color: 'var(--color-text-secondary)',
            textTransform: 'uppercase',
            letterSpacing: '0.05em',
            marginBottom: '0.5rem',
            fontFamily: 'var(--font-mono)',
          }}>
            CONTRASEÑA
          </label>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <input
              type={showPassword ? 'text' : 'password'}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              onKeyDown={(e: React.KeyboardEvent) => e.key === 'Enter' && handleSubmit(e)}
              autoFocus
              style={{
                flex: 1,
                background: 'var(--color-surface-2)',
                border: `1px solid ${error ? 'var(--color-alert)' : 'var(--color-border-hi)'}`,
                borderRadius: '0px',
                color: 'var(--color-text-primary)',
                padding: '0.75rem 1rem',
                fontSize: '1rem',
                fontFamily: 'var(--font-mono)',
                fontVariantNumeric: 'tabular-nums',
                letterSpacing: '0.1em',
                outline: 'none',
                boxSizing: 'border-box',
              }}
              placeholder=""
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              style={{
                background: 'var(--color-surface-2)',
                border: '1px solid var(--color-border-hi)',
                borderRadius: '0px',
                color: 'var(--color-text-secondary)',
                padding: '0.75rem 1rem',
                fontSize: '0.6875rem',
                fontWeight: 700,
                fontFamily: 'var(--font-mono)',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                minWidth: '56px',
                transition: 'background 0.15s ease, color 0.15s ease',
                letterSpacing: '0.05em',
                textTransform: 'uppercase',
              }}
              onMouseOver={(e) => { e.currentTarget.style.background = 'var(--color-surface-3)'; e.currentTarget.style.color = 'var(--color-accent)'; }}
              onMouseOut={(e) => { e.currentTarget.style.background = 'var(--color-surface-2)'; e.currentTarget.style.color = 'var(--color-text-secondary)'; }}
              aria-label={showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'}
            >
              {showPassword ? '[OCU]' : '[VIS]'}
            </button>
          </div>
        </div>

        {error && (
          <div style={{
            background: 'rgba(192, 57, 43, 0.15)',
            border: '1px solid var(--color-alert)',
            borderRadius: '0px',
            padding: '0.75rem',
            marginBottom: '1.5rem',
            fontSize: '0.75rem',
            color: 'var(--color-alert)',
            fontFamily: 'var(--font-mono)',
            textAlign: 'center',
          }}>
            [!] CONTRASEÑA INCORRECTA
          </div>
        )}

        <button
          type="submit"
          style={{
            width: '100%',
            background: 'var(--color-surface-2)',
            border: '1px solid var(--color-accent)',
            color: 'var(--color-accent)',
            borderRadius: '0px',
            padding: '0.75rem',
            fontSize: '0.8125rem',
            fontWeight: 800,
            cursor: 'pointer',
            fontFamily: 'var(--font-mono)',
            letterSpacing: '0.05em',
            textTransform: 'uppercase',
            transition: 'background 0.15s ease',
          }}
          onMouseOver={(e) => e.currentTarget.style.background = 'var(--color-surface-3)'}
          onMouseOut={(e) => e.currentTarget.style.background = 'var(--color-surface-2)'}
        >
          {'>'} ACCEDER AL SISTEMA
        </button>

        <p style={{
          marginTop: '1.5rem',
          fontSize: '0.6875rem',
          color: 'var(--color-text-muted)',
          textAlign: 'center',
          fontFamily: 'var(--font-mono)',
        }}>
          [ OGC GeoPackage v1.1 · EPSG:4326 · Golfo de California ]
        </p>
      </form>
    </div>
  )
}

export default function Login() {
  return (
    <Suspense fallback={
      <div style={{
        minHeight: '100vh',
        background: 'var(--color-bg)',
        color: 'var(--color-text-primary)',
        fontFamily: 'var(--font-mono)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}>
        <div style={{ fontSize: '1rem', color: 'var(--color-text-secondary)' }}>Cargando...</div>
      </div>
    }>
      <LoginForm />
    </Suspense>
  )
}