@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Setup required: double-click Install Aware Minds.cmd first.
  pause
  exit /b 1
)
if not exist "apps\web\dist\index.html" (
  echo Website build missing: double-click Install Aware Minds.cmd first.
  pause
  exit /b 1
)
start "Aware Minds" ".venv\Scripts\pythonw.exe" "%~dp0scripts\browser_app.py"
exit /b 0
