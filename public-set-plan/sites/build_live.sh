#!/usr/bin/env bash
# Build the live (Vercel) pages with the instant-quote endpoint wired in, then rebuild the preview copies.
set -euo pipefail
cd "$(dirname "$0")"
QUOTE_URL="https://drmwqgcqrvxkcibrptep.supabase.co/functions/v1/quote" python3 build_sites.py
mkdir -p live
for f in crew getaway celebrate; do
  { printf '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>body{margin:0}[hidden]{display:none!important}img{max-width:100%%}</style></head><body>'; cat "$f.html"; printf '</body></html>'; } > "live/$f.html"
done
python3 build_sites.py   # preview copies (form not connected) for claude.ai artifacts
