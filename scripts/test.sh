#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
.venv/bin/python -m pytest tests -q
(cd apps/web && npm test && npm run typecheck && npm run build)
