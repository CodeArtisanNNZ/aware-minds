$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
if (-not (Get-Command py -ErrorAction SilentlyContinue)) { throw 'Install Python 3.12 or newer first.' }
if (-not (Get-Command npm -ErrorAction SilentlyContinue)) { throw 'Install Node.js 20 or newer first.' }
py -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Python dependency install failed.' }
Push-Location apps/web
try { npm ci; if ($LASTEXITCODE -ne 0) { throw 'npm ci failed.' } } finally { Pop-Location }
Write-Host 'Ready. Set ADMIN_EMAIL and ADMIN_PASSWORD (12+ characters) before the first launch, then run .\scripts\dev.ps1.'
