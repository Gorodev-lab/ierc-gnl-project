#!/usr/bin/env bash
# Script lanzador para IERC GNL Dashboard local
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

# Abrir el navegador tras un breve retraso para permitir que Next.js inicie
(sleep 2 && xdg-open http://localhost:3000) &

# Iniciar servidor de desarrollo de Next.js
npm run dev
