@echo off
cd /d "%~dp0"
where pythonw.exe >nul 2>nul
if errorlevel 1 (echo Python 3 is required. Download it from https://python.org/downloads/ & pause & exit /b 1)
start "" pythonw.exe "%~dp0server.py"
exit /b 0
