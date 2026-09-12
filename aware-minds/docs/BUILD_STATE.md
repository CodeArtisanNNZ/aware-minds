# Build state — 0.3.0 release candidate (local only)

## Verified now

- Existing FastAPI/React/SQLite/Ollama architecture retained. Repeatable additive v2 schema startup; admin bootstrap requires a unique email and 12+ character password.
- Cookie sessions, authorization boundaries, per-email login throttling, explicit Origin/Fetch cross-site rejection, app-key scopes/revocation, user export without auth secrets, database backup and restore dry-run.
- Browser SSE chat, cancellation UI, separate app/project/memory scopes, file extraction and bounded lexical retrieval. Project/user content and document excerpts are untrusted reference messages, not system instructions. App-facing PHP/JS/Python examples remain server-side.
- 11 backend tests passing on clean isolated DBs; 2 frontend Vitest tests; Ruff F checks, ESLint, TypeScript and production Vite build passing. Live API and Vite startup checked over HTTP. JS and Python SDK mock contracts passed. Backup integrity verified. Initial JavaScript bundle reduced from ~603 KB to ~267 KB through Markdown code splitting.
- Playwright tests cover eight target viewports and one mobile navigation flow, but **could not run** because the Chromium download timed out. No screenshots were visually inspected. PHP binary unavailable. Ollama absent; mocked success/error tests passed, live AI response quality unverified.

## Actual behavior and constraints

API version 0.3.0 under `/api/v1`; frontend 0.3.0; SQLite schema v2; only Ollama model provider. `/health` checks process availability only. An absent model produces 503 without saving an unsent chat. Document source metadata indicates retrieved chunks, not validated answer accuracy. No vector store, embedding model, multimodal input, tool executor, provider fallback or MCP server exists. The current app key is a service-account key owned by one Aware Minds user; no external patient/student identity delegation. A formal database migration framework remains pending.

## Blockers before public release

Install/run Playwright Chromium and inspect/repair eight desktop/tablet/mobile screenshots. Test a live Ollama model, multilingual response quality and real RAG grounding. Harden CSRF, registration/IP throttling, upload parser sandbox/virus screening, delegated identity, public TLS/ops, and formal migrations. Review security/UX after actual browser testing. See `docs/RELEASE_CHECKLIST.md`, `docs/SECURITY.md` and `docs/ROADMAP.md`.

**Status: local release candidate; NOT READY for public production.**
