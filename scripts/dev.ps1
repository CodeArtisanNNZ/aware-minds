$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
if (-not (Test-Path .venv\Scripts\python.exe)) { throw 'Run .\scripts\setup.ps1 first.' }
$api = Start-Process -FilePath '.\.venv\Scripts\python.exe' -ArgumentList '-m','uvicorn','services.api.main:app','--host','127.0.0.1','--port','8000' -PassThru -NoNewWindow
try { Push-Location apps/web; try { npm run dev } finally { Pop-Location } } finally { Stop-Process -Id $api.Id -ErrorAction SilentlyContinue }
