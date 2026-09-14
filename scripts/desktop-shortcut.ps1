$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$desktop = [Environment]::GetFolderPath('DesktopDirectory')
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut((Join-Path $desktop 'Aware Minds.lnk'))
$shortcut.TargetPath = Join-Path $root 'Start Aware Minds.cmd'
$shortcut.WorkingDirectory = $root
$shortcut.Description = 'Open the Aware Minds developer project workspace'
$shortcut.IconLocation = (Join-Path $root 'apps\web\public\aware-minds.ico') + ',0'
$shortcut.Save()
Write-Host "Desktop shortcut created: $desktop\Aware Minds.lnk"
