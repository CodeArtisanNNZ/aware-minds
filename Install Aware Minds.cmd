@echo off
setlocal
cd /d "%~dp0"
where pythonw.exe >nul 2>nul
if errorlevel 1 (echo Install Python 3 from https://python.org/downloads/ and tick "Add Python to PATH". & pause & exit /b 1)
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "$w=New-Object -ComObject WScript.Shell;$s=$w.CreateShortcut([IO.Path]::Combine([Environment]::GetFolderPath('Desktop'),'Aware Minds.lnk'));$s.TargetPath=[IO.Path]::Combine('%~dp0','Start Aware Minds.cmd');$s.WorkingDirectory='%~dp0';$s.IconLocation='$env:SystemRoot\System32\shell32.dll,70';$s.Description='Aware Minds developer workspace';$s.Save()"
if errorlevel 1 (echo Shortcut creation failed. & pause & exit /b 1)
echo Aware Minds shortcut created on your Desktop.
pause
