@echo off
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\setup.ps1"
if errorlevel 2 (pause & exit /b 2)
if errorlevel 1 (pause & exit /b 1)
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\desktop-shortcut.ps1"
if errorlevel 1 (pause & exit /b 1)
echo Installed. Double-click the Aware Minds desktop shortcut to open it in your browser.
pause
