#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
test -f apps/web/dist/index.html || { echo "Prebuilt web application is missing."; exit 1; }
test -f apps/web/dist/assets/app.css || { echo "Prebuilt CSS is missing."; exit 1; }
test -f apps/web/dist/assets/app.js || { echo "Prebuilt JavaScript is missing."; exit 1; }
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
echo "Aware Minds is ready. No npm build is required for the downloaded release."
