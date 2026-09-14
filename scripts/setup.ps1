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
$installed = (Install-Prerequisite 'git' 'Git.Git' 'Git for Windows') -or $installed
if ($installed) {
    Write-Host 'Required tools were installed. Close this window and run Install Aware Minds.cmd once more so Windows reloads PATH.'
    exit 2
}

if (-not (Test-Path 'apps\web\dist\index.html')) {
    throw 'The prebuilt web application is missing. Download and extract the complete release ZIP again.'
}
if (-not (Test-Path 'apps\web\dist\assets\app.css') -or -not (Test-Path 'apps\web\dist\assets\app.js')) {
    throw 'The prebuilt web assets are incomplete. Download and extract the complete release ZIP again.'
}

py -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Python dependency installation failed.' }

Write-Host ''
Write-Host 'Aware Minds is ready. No Node.js or npm build is required for the downloaded release.'
