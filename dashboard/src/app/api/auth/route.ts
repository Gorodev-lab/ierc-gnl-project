import { NextRequest, NextResponse } from 'next/server'

export const dynamic = 'force-dynamic'

const COOKIE_NAME = 'ierc_auth'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { password } = body

    const expectedPassword = process.env.DASHBOARD_PASSWORD || 'root'

    if (password === expectedPassword) {
      const response = NextResponse.json({ status: 'success' })
      
      // Establecer la cookie de autenticación de forma segura desde el servidor
      response.cookies.set(COOKIE_NAME, expectedPassword, {
        path: '/',
        maxAge: 2592000, // 30 días
        sameSite: 'lax',
        secure: process.env.NODE_ENV === 'production',
        httpOnly: true, // Protege contra XSS
      })

      return response
    }

    return NextResponse.json(
      { error: 'Contraseña incorrecta' },
      { status: 401 }
    )

  } catch (error: any) {
    return NextResponse.json(
      { error: 'Error interno de autenticación' },
      { status: 500 }
    )
  }
}
