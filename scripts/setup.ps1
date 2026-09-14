$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
function Install-Prerequisite($Command, $Package, $Label) {
    if (Get-Command $Command -ErrorAction SilentlyContinue) { return $false }
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        throw "$Label is required. Install it, then run this installer again."
    }
    Write-Host "Installing $Label..."
    winget install --id $Package --exact --silent --accept-package-agreements --accept-source-agreements
    if ($LASTEXITCODE -ne 0) { throw "$Label installation failed." }
    return $true
}
$installed = $false
$installed = (Install-Prerequisite 'py' 'Python.Python.3.12' 'Python 3.12') -or $installed
$installed = (Install-Prerequisite 'npm' 'OpenJS.NodeJS.LTS' 'Node.js LTS') -or $installed
$installed = (Install-Prerequisite 'git' 'Git.Git' 'Git for Windows') -or $installed
if ($installed) {
    Write-Host 'Required tools were installed. Close this window and run Install Aware Minds.cmd once more so Windows reloads PATH.'
    exit 2
}
py -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Python dependency install failed.' }
Push-Location apps/web
try {
    npm ci
    if ($LASTEXITCODE -ne 0) { throw 'npm ci failed.' }
    npm run build
    if ($LASTEXITCODE -ne 0) { throw 'Frontend build failed.' }
} finally { Pop-Location }
Write-Host 'Ready. The Aware Minds shortcut will open the workspace in your default browser.'
