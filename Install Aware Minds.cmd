@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "$s=(New-Object -COM WScript.Shell).CreateShortcut([IO.Path]::Combine([Environment]::GetFolderPath('Desktop'),'Aware Minds.lnk'));$s.TargetPath=[IO.Path]::Combine('%~dp0','index.html');$s.WorkingDirectory='%~dp0';$s.Description='Aware Minds guided developer workspace';$s.Save()"
if errorlevel 1 (echo Shortcut creation failed. & pause & exit /b 1)
echo Installed. Open Aware Minds from your desktop.
pause
