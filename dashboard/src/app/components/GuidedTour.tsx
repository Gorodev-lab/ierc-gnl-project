'use client'

import React, { useState, useEffect } from 'react'
import { createPortal } from 'react-dom'

interface TourStep {
  id: string
  target: string // CSS selector
  title: string
  content: string
  position?: 'top' | 'bottom' | 'left' | 'right' | 'center'
}

interface GuidedTourProps {
  steps: TourStep[]
  onComplete?: () => void
  storageKey?: string
}

export default function GuidedTour({ steps, onComplete, storageKey = 'ierc-tour-completed' }: GuidedTourProps) {
  const [currentStep, setCurrentStep] = useState(0)
  const [isOpen, setIsOpen] = useState(false)
  const [targetRect, setTargetRect] = useState<DOMRect | null>(null)
  const [targetsReady, setTargetsReady] = useState(false)

  // Wait for all target elements to exist in DOM
  useEffect(() => {
    const checkTargets = () => {
      const allExist = steps.every(step => document.querySelector(step.target))
      if (allExist) {
        setTargetsReady(true)
      } else {
        requestAnimationFrame(checkTargets)
      }
    }
    checkTargets()
  }, [steps])

  // Auto-start on first visit (after targets ready)
  useEffect(() => {
    if (typeof window !== 'undefined' && targetsReady) {
      const completed = localStorage.getItem(storageKey)
      if (!completed) {
        setTimeout(() => setIsOpen(true), 500)
      }
    }
  }, [storageKey, targetsReady])

  // Update target position on step change
  useEffect(() => {
    if (!isOpen || currentStep >= steps.length) return
    const el = document.querySelector(steps[currentStep].target)
    if (el) setTargetRect(el.getBoundingClientRect())
    else setTargetRect(null)
  }, [currentStep, isOpen, steps])

  const next = () => {
    if (currentStep < steps.length - 1) setCurrentStep(s => s + 1)
    else complete()
  }

  const complete = () => {
    setIsOpen(false)
    localStorage.setItem(storageKey, 'true')
    onComplete?.()
  }

  const skip = () => complete()

  if (!isOpen || currentStep >= steps.length || !targetsReady) return null

  const step = steps[currentStep]
  const position = step.position || 'bottom'

  // Re-query element on each render to handle dynamic DOM (conditional rendering)
  let pos = targetRect
  if (!pos) {
    const el = document.querySelector(steps[currentStep].target)
    if (el) {
      pos = el.getBoundingClientRect()
      setTargetRect(pos)
    }
  }

  // Calculate portal position
  let portalStyle: React.CSSProperties = { position: 'fixed', zIndex: 9999, left: 0, top: 0 }
  if (pos) {
    const scrollX = window.scrollX
    const scrollY = window.scrollY
    switch (position) {
      case 'top':
        portalStyle = { ...portalStyle, left: pos.left + scrollX + pos.width / 2, top: pos.top + scrollY - 10, transform: 'translateX(-50%) translateY(-100%)' }
        break
      case 'bottom':
        portalStyle = { ...portalStyle, left: pos.left + scrollX + pos.width / 2, top: pos.bottom + scrollY + 10, transform: 'translateX(-50%)' }
        break
      case 'left':
        portalStyle = { ...portalStyle, left: pos.left + scrollX - 10, top: pos.top + scrollY + pos.height / 2, transform: 'translateY(-50%) translateX(-100%)' }
        break
      case 'right':
        portalStyle = { ...portalStyle, left: pos.right + scrollX + 10, top: pos.top + scrollY + pos.height / 2, transform: 'translateY(-50%)' }
        break
      default:
        portalStyle = { ...portalStyle, left: '50%', top: '50%', transform: 'translate(-50%, -50%)' }
    }
  } else {
    portalStyle = { ...portalStyle, left: '50%', top: '50%', transform: 'translate(-50%, -50%)' }
  }

  const overlay = (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        background: 'rgba(0,0,0,0.6)',
        zIndex: 9998,
      }}
      onClick={skip}
    />
  )

  const tooltip = (
    <div
      style={{
        ...portalStyle,
        pointerEvents: 'auto',
        background: 'var(--color-surface)',
        border: '1px solid var(--color-accent)',
        borderLeft: '4px solid var(--color-accent)',
        padding: '1rem 1.25rem',
        maxWidth: '360px',
        fontFamily: 'var(--font-mono)',
        boxShadow: '0 8px 32px rgba(0,0,0,0.5)',
        borderRadius: 0,
      }}
      role="dialog"
      aria-labelledby="tour-title"
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem' }}>
        <h4 id="tour-title" style={{ fontSize: '0.8125rem', fontWeight: 800, color: 'var(--color-accent)', margin: 0, letterSpacing: '0.04em' }}>
          {step.title}
        </h4>
        <span style={{ fontSize: '0.625rem', color: 'var(--color-text-muted)', fontVariantNumeric: 'tabular-nums' }}>
          {currentStep + 1} / {steps.length}
        </span>
      </div>
      <p style={{ fontSize: '0.75rem', color: 'var(--color-text-secondary)', lineHeight: 1.6, margin: 0 }}>
        {step.content}
      </p>
      <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1rem', justifyContent: 'flex-end' }}>
        <button
          onClick={skip}
          style={{
            background: 'transparent',
            border: '1px solid var(--color-border)',
            color: 'var(--color-text-secondary)',
            padding: '0.375rem 0.75rem',
            fontSize: '0.6875rem',
            fontWeight: 700,
            fontFamily: 'var(--font-mono)',
            cursor: 'pointer',
            borderRadius: 0,
            letterSpacing: '0.04em',
            textTransform: 'uppercase',
          }}
        >
          Saltar
        </button>
        <button
          onClick={next}
          style={{
            background: 'var(--color-surface-2)',
            border: '1px solid var(--color-accent)',
            color: 'var(--color-accent)',
            padding: '0.375rem 0.75rem',
            fontSize: '0.6875rem',
            fontWeight: 700,
            fontFamily: 'var(--font-mono)',
            cursor: 'pointer',
            borderRadius: 0,
            letterSpacing: '0.04em',
            textTransform: 'uppercase',
          }}
        >
          {currentStep === steps.length - 1 ? 'Entendido' : 'Siguiente'}
        </button>
      </div>
    </div>
  )

  // Highlight target element
  const highlight = pos ? (
    <div
      style={{
        position: 'fixed',
        left: pos.left + window.scrollX,
        top: pos.top + window.scrollY,
        width: pos.width,
        height: pos.height,
        border: '2px solid var(--color-accent)',
        boxShadow: '0 0 0 9999px rgba(0,0,0,0.5), 0 0 0 2px var(--color-accent)',
        borderRadius: 4,
        zIndex: 9998,
        pointerEvents: 'none',
        animation: 'pulse 1.5s ease-in-out infinite',
      }}
    />
  ) : null

  return createPortal(
    <>
      <style>{`
        @keyframes pulse {
          0%, 100% { box-shadow: 0 0 0 9999px rgba(0,0,0,0.5), 0 0 0 2px var(--color-accent); }
          50% { box-shadow: 0 0 0 9999px rgba(0,0,0,0.5), 0 0 0 6px var(--color-accent); }
        }
      `}</style>
      {overlay}
      {highlight}
      {tooltip}
    </>,
    document.body
  )
}