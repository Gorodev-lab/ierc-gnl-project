import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'IERC-GNL Dashboard — Riesgo Pesquero Golfo de California',
  description:
    'Índice Espacial de Riesgo Socioeconómico para Comunidades pesqueras ante proyectos de Gas Natural Licuado en el Golfo de California. Basado en Moreno-Báez et al. (2011, 2012).',
  keywords: [
    'IERC', 'GNL', 'Golfo de California', 'riesgo pesquero', 'Moreno-Báez',
    'comunidades pesqueras', 'Puerto Libertad', 'San Felipe', 'Guaymas',
    'PANGAS', 'pesca artesanal', 'zonas pesqueras'
  ],
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="es">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="app-shell">
        {children}
      </body>
    </html>
  )
}
