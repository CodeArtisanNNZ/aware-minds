# Aware Minds 0.3.0 — local release candidate, not production-ready

Aware Minds is one local AI workspace and integration core for Bujhi, Healthcare Central, KAL.RA AI, Kishan Bari and developer-owned applications. The React UI talks to FastAPI; SQLite stores private work; Ollama is the only implemented model provider. Chat requires a locally installed Ollama model. The public landing demo is explicitly a UI preview.

## One setup path

Requires Python 3.12+, Node 20+, npm. For local AI, install Ollama separately and pull a model suited to your RAM. No cloud API key is required.

**Windows PowerShell:**

```powershell
.\scripts\setup.ps1
$env:ADMIN_EMAIL='your-admin@example.com'
$env:ADMIN_PASSWORD='a-unique-password-with-at-least-12-characters'
.\scripts\dev.ps1
```

**Linux/macOS:**

```bash
./scripts/setup.sh
export ADMIN_EMAIL='your-admin@example.com'
export ADMIN_PASSWORD='a-unique-password-with-at-least-12-characters'
./scripts/dev.sh
```

Set admin variables **before the first startup**. The account is created only if the email is absent; setting these variables later does not promote an existing user. Do not commit real credentials to `.env`. You may configure `OLLAMA_MODEL` and `OLLAMA_BASE_URL` as environment variables; see `.env.example`. This application does not automatically load `.env` files. To enable chat, start Ollama and run `ollama pull qwen3:4b` if your hardware can support it (or install a smaller compatible model). Open http://127.0.0.1:5173; API docs are at http://127.0.0.1:8000/docs. Start the API and frontend from the same machine.

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

Document retrieval uses bounded **lexical** chunks and returns retrieved-source metadata, not independently verified answers. There is no semantic vector store or actual tool execution. Local-first mode never calls a cloud model. `/health` checks the API only; `/api/v1/models` reports local model detection after login. See [build state](docs/BUILD_STATE.md), [release checklist](docs/RELEASE_CHECKLIST.md), and [roadmap](docs/ROADMAP.md) for verified coverage and deferred work.
