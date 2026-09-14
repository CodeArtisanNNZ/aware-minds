@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Install Aware Minds first.
  pause
  exit /b 1
)
set "AWARE_MINDS_DATA_DIR=%LOCALAPPDATA%\AwareMinds"
".venv\Scripts\python.exe" scripts\backup.py
if errorlevel 1 (pause & exit /b 1)
echo The backup is in %AWARE_MINDS_DATA_DIR%\backups
echo Store a copy on a drive you control. It contains private account and memory data.
pause
