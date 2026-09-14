#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
if [[ -x .venv/bin/python ]]; then aware_python=.venv/bin/python; else aware_python=python; fi
"$aware_python" -m uvicorn services.api.main:app --reload &
api_pid=$!
trap 'kill "$api_pid" 2>/dev/null || true' EXIT
cd apps/web
npm run dev
