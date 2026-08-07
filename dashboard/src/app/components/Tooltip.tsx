'use client'

import React from 'react'

interface TooltipProps {
  content: string
  children: React.ReactElement<any>
  position?: 'top' | 'bottom' | 'left' | 'right'
}

const POSITIONS = {
  top: { bottom: '120%', left: '50%', transform: 'translateX(-50%)' },
  bottom: { top: '120%', left: '50%', transform: 'translateX(-50%)' },
  left: { right: '120%', top: '50%', transform: 'translateY(-50%)' },
  right: { left: '120%', top: '50%', transform: 'translateY(-50%)' },
} as const

export default function Tooltip({ content, children, position = 'top' }: TooltipProps) {
  const [visible, setVisible] = React.useState(false)
  const pos = POSITIONS[position]

  return (
    <span
      style={{ position: 'relative', display: 'inline-flex' }}
      onMouseEnter={() => setVisible(true)}
      onMouseLeave={() => setVisible(false)}
      onFocus={() => setVisible(true)}
      onBlur={() => setVisible(false)}
    >
      {React.cloneElement(children as React.ReactElement<any>, {
        style: { ...(children.props.style || {}), cursor: 'help' } as React.CSSProperties,
      })}
      {visible && (
        <div
          style={{
            position: 'absolute',
            zIndex: 1000,
            ...pos,
            background: 'var(--color-surface)',
            border: '1px solid var(--color-border-hi)',
            padding: '0.5rem 0.75rem',
            fontSize: '0.6875rem',
            fontFamily: 'var(--font-mono)',
            color: 'var(--color-text-primary)',
            whiteSpace: 'nowrap',
            maxWidth: '280px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.4)',
            borderRadius: 0,
            pointerEvents: 'none',
          } as React.CSSProperties}
          role="tooltip"
        >
          {content}
        </div>
      )}
    </span>
  )
}