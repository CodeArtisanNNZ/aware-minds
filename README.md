# Aware Minds Developer Hub 0.7.0

Aware Minds is a local developer workspace for any Git or GitHub project. Track project details, inspect and edit files, preview repository changes, and publish through a guarded Git workflow. React provides the interface, FastAPI the backend, and SQLite stores workspace configuration locally. The Project Hub does not require Ollama or an external AI API.

Project workspaces also support themed views, expandable feature catalogs, teammates, local Git status/push, and guarded SQLite browsing/editing. See [project manifest synchronization](docs/PROJECT_MANIFEST.md). Git pushes use credentials already configured on the computer and only push existing commits. External applications do not share passwords or browser cookies with this hub.

## Windows: install once, then double-click

Extract the ZIP and double-click **`Install Aware Minds.cmd`**. The guided installer uses Windows Package Manager to install missing Python, Node.js or Git prerequisites when available, then builds the website and creates an **Aware Minds** desktop shortcut. Double-clicking the shortcut starts the local service silently and opens `http://127.0.0.1:8000/hub` in the default browser. Clicking it again opens the workspace without starting a duplicate server. The Project Hub does not require Ollama or an AI API.

The release ZIP never contains or imports a workspace database. A first-time installation creates an empty workspace in `%LOCALAPPDATA%\AwareMinds`. Later application updates use that stable folder so projects and settings survive upgrades. Aware Minds opens directly as a single-user local workspace—there is no registration or sign-in screen. To deliberately reset an existing installation, run **`Start Fresh.cmd`**; it moves the current workspace to a timestamped backup before opening an empty one.

Settings → Export my data downloads conversations, documents and memories as JSON. Double-click **`Backup Aware Minds.cmd`** for a consistent SQLite backup in `%LOCALAPPDATA%\AwareMinds\backups`. Store a copy on another drive you control. Keep backups private. See [memory](docs/MEMORY.md).

## One setup path

Runtime development requires Python 3.12+, Node 20+ and Git. The Windows installer attempts to install missing prerequisites through `winget`; if it does, run the installer once more after Windows refreshes PATH. No model, Ollama installation or cloud API key is required.

**Windows PowerShell (development only):**

```powershell
.\scripts\setup.ps1
.\scripts\dev.ps1
```

**Linux/macOS:**

```bash
./scripts/setup.sh
./scripts/dev.sh
```

The normal desktop release has no account, admin password, Ollama model, or cloud API requirement. Development mode opens the Vite interface at http://127.0.0.1:5173; API docs are at http://127.0.0.1:8000/docs.

## Verify

```bash
./scripts/test.sh                       # Linux/macOS: backend, frontend, types, build
# Windows: .\scripts\test.ps1
cd apps/web && npm run lint && cd ../..  # frontend lint
.venv/bin/python -m ruff check services tests packages/python-sdk scripts --select F  # optional Python lint if Ruff installed
```

`cd apps/web && npm run e2e` runs the viewport flow when Playwright Chromium is installed (`npx playwright install chromium`), which may require network access. The E2E tests are currently **unverified** in this environment because the browser download timed out and the managed browser could not open localhost. Unit/integration checks run without a browser.

## Operations and scope

Create apps/keys at `/developers`; the app key must stay on your server. The key acts as the app owner's **service account**, not as an individual patient or student. Connect child apps only after delegated identity is implemented. See [integration instructions](docs/APP_INTEGRATION.md) and [security limits](docs/SECURITY.md). Users can export their own data from Settings; exports exclude passwords, sessions and keys but contain private content. For a consistent local database backup run `python scripts/backup.py`; `python scripts/restore.py PATH` dry-runs and requires `--confirm-local-restore` while the API is stopped. Treat backups as sensitive.

Document retrieval uses bounded **lexical** chunks and returns retrieved-source metadata, not independently verified answers. There is no semantic vector store or actual tool execution. Local-first mode never calls a cloud model. `/health` checks the API only. See [build state](docs/BUILD_STATE.md), [release checklist](docs/RELEASE_CHECKLIST.md), and [roadmap](docs/ROADMAP.md) for verified coverage and deferred work.
