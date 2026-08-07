import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

const PASSWORD = process.env.DASHBOARD_PASSWORD || 'root'
const COOKIE_NAME = 'ierc_auth'

export function middleware(request: NextRequest) {
  const cookie = request.cookies.get(COOKIE_NAME)?.value
  const isLoginPage = request.nextUrl.pathname === '/login'

  if (cookie === PASSWORD) {
    return NextResponse.next()
  }

  if (isLoginPage) {
    return NextResponse.next()
  }

  const loginUrl = new URL('/login', request.url)
  loginUrl.searchParams.set('redirect', request.nextUrl.pathname)
  return NextResponse.redirect(loginUrl)
}

export const config = {
  matcher: ['/((?!_next|api|data|favicon.ico).*)'],
}