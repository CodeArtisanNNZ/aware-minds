$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$dataPath = Join-Path $env:LOCALAPPDATA 'AwareMinds'
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$backupPath = Join-Path $env:LOCALAPPDATA "AwareMinds-backup-$stamp"

$answer = [System.Windows.Forms.MessageBox]::Show(
  "Start with an empty Aware Minds workspace?`n`nYour current projects will be moved to:`n$backupPath",
  'Aware Minds — Start Fresh',
  [System.Windows.Forms.MessageBoxButtons]::YesNo,
  [System.Windows.Forms.MessageBoxIcon]::Warning
)
if ($answer -ne [System.Windows.Forms.DialogResult]::Yes) { exit 0 }

Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue | ForEach-Object {
  $process = Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue
  $details = Get-CimInstance Win32_Process -Filter "ProcessId = $($_.OwningProcess)" -ErrorAction SilentlyContinue
  $isCurrentInstall = $process -and $process.Path -and $process.Path.StartsWith($root, [System.StringComparison]::OrdinalIgnoreCase)
  $isAwareLauncher = $details -and $details.Name -match '^pythonw?(\.exe)?$' -and $details.CommandLine -match 'scripts[\\/]browser_app\.py'
  if ($isCurrentInstall -or $isAwareLauncher) {
    Stop-Process -Id $process.Id -Force
  }
}
Start-Sleep -Milliseconds 500
if (Test-Path $dataPath) { Move-Item -LiteralPath $dataPath -Destination $backupPath }
Start-Process -FilePath (Join-Path $root 'Start Aware Minds.cmd') -WorkingDirectory $root
