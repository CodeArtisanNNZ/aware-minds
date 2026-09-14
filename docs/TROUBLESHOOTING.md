# Troubleshooting

- **The desktop shortcut does not open a browser:** browse to `http://127.0.0.1:8000/hub`. If it is unavailable, inspect `%LOCALAPPDATA%\AwareMinds\aware-minds.log`, then run `Install Aware Minds.cmd` again.
- **Port 8000 is already in use:** close the other local server or restart Windows, then double-click the Aware Minds shortcut. Clicking the shortcut while Aware Minds itself is already running simply opens another browser tab.
- **A prerequisite was installed:** close the installer and run it once more so Windows can refresh `PATH`. The guided installer uses `winget` when available; otherwise install Python 3.12+, Node.js 20+ and Git manually.
- **PowerShell says a script is not digitally signed:** use the `.cmd` installer instead. For development only, run `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\setup.ps1` from the extracted folder.
- **A project will not connect:** choose a local folder containing a `.git` directory, or use an HTTPS GitHub URL under **Connections → Clone and connect**. A web URL is not a local folder path.
- **Git push asks for authentication:** complete the Git Credential Manager browser prompt. Aware Minds does not store GitHub passwords or tokens.
- **Push is blocked as behind the remote:** pull and resolve the remote changes first. Force push is intentionally unavailable.
- **Open in VS Code is unavailable:** install Visual Studio Code and enable its `code` command, then restart Aware Minds. The built-in Files workspace remains available for quick edits.
- **An old project is absent:** inspect `%LOCALAPPDATA%\AwareMinds\aware-minds.db`. If data exists only in an older extracted copy's `data` folder, stop Aware Minds and keep backups before moving anything. Do not overwrite a populated database.
- **E2E Chromium is missing:** from `apps\web`, run `npx playwright install chromium`; network access may be required.
- **Development frontend/API mismatch:** Vite uses port 5173 and FastAPI uses 8000. The desktop shortcut does not use Vite; it serves both UI and API on port 8000.

The normal local release has no registration, sign-in, Ollama or external AI API requirement.
