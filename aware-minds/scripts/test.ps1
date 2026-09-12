$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
& .\.venv\Scripts\python.exe -m pytest tests -q
if ($LASTEXITCODE -ne 0) { throw 'Backend tests failed.' }
Push-Location apps/web
try {
  npm test; if ($LASTEXITCODE -ne 0) { throw 'Frontend tests failed.' }
  npm run typecheck; if ($LASTEXITCODE -ne 0) { throw 'TypeScript failed.' }
  npm run build; if ($LASTEXITCODE -ne 0) { throw 'Frontend build failed.' }
} finally { Pop-Location }
