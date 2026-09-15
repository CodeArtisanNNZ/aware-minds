# Build state

## Guided Developer Workspace v1 — 2026-09-14

Status: frontend milestone ready for review on `build/guided-developer-workspace-v1`.

Implemented:

- Replaced the invalid one-byte `apps` placeholder with a real `apps/web` frontend tree.
- Added a prebuilt browser UI under `apps/web/dist` for the existing desktop launcher.
- Added first-launch animation using the approved muted purple and teal direction.
- Added an empty universal project library; no personal project seeds are included.
- Added goal-based entry points: build, local import, GitHub continuation, repair and sample project.
- Added Beginner, Practising and Professional interface levels.
- Added the six-stage roadmap: Plan, Build, Data, Test, GitHub and Publish.
- Added a contextual “I’m lost” rescue flow, project-system map and learning library.
- Added light/dark appearance while retaining the purple brand.
- Connected project listing and creation to the existing local `/api/v1/hub` endpoints, with a browser-storage fallback for standalone UI review.
- Added a minimal frontend test preventing reintroduction of legacy Ollama, account and sign-in controls.

Current limitations:

- This milestone establishes the universal guided shell; visual page generation, database-provider OAuth, GitHub clone/push dialogs and hosting-provider deployment remain implementation work.
- The backend still contains legacy disabled AI endpoints for compatibility. They are not exposed by this frontend and should be removed through a deliberate API/database migration rather than by deleting unrelated working routes.
- Automated Python/npm execution was not available in the connector environment; tests must run in CI or a local checkout before merge.

# Build state — 0.7.0 universal developer workspace

## Universal workflow release (2026-09-14)

- Replaced the decorative bottom breadcrumb with a clickable, repository-driven Connect → Edit → Review → Push workflow.
- Connected repositories are verified automatically; saved changes advance the review stage, a Quick Push confirmation advances the push stage, and successful pushes remain visible after a restart.
- New releases are created by `scripts/package_release.py`, which rejects database files and excludes uploads, backups, dependencies, caches and build/test residue.
- Fresh installations contain zero projects. Existing `%LOCALAPPDATA%\AwareMinds` workspaces remain intact during upgrades; **Start Fresh** creates a recoverable timestamped backup before resetting.
- The first project experience is generic and accepts any local Git repository or valid GitHub repository URL. No model or external AI provider is required.
- Verification: 18 backend tests and 2 frontend tests pass; TypeScript, ESLint, Python compilation, the production build, a disposable empty-workspace production smoke test and data-free ZIP validation pass. Ruff is unavailable in this environment. The nine Playwright scenarios remain blocked because the Chromium executable is not installed.

## Visual workbench release (2026-09-14)

- Replaced the active-project dashboard arrangement with a predictable three-zone workbench: vertical tools, central editor/work area and contextual inspector.
- Added a collapsible repository command bar with `Ctrl+K`, plus a permanent Git change timeline and human-readable review-and-push flow.
- Added Beginner, Practicing and Professional workspace depths. Learning material stays behind one **Learn** control rather than competing with project work.
- Added concise project-type workflows, keyboard shortcuts, coding safeguards, language guidance and clearly qualified free hosting/database choices.
- Removed product-specific theme names from new-project creation. Fresh installations start empty; upgrades preserve existing local projects instead of deleting user data.
- Improved Windows startup failures so the popup shows the real exception and exact log path.
- Fixed silent Windows startup under `pythonw.exe` by disabling Uvicorn's console-dependent default formatter and access logger.
- Stopped importing legacy databases from reused extraction folders. Added a confirmed, recoverable **Start Fresh** launcher that moves the current local workspace to a timestamped backup before creating an empty one.

## Browser workspace release (2026-09-14)

- The desktop shortcut starts the local service without a console and opens `/hub` in the default browser. Reopening it detects the running service and does not create a duplicate server.
- Home is a responsive project gallery. Selecting a project opens a full-width editor workspace instead of permanently squeezing a project list beside project details.
- Added compact workspace navigation, responsive project cards and a bottom change path inspired by editing timelines. Desktop, tablet and mobile rules remove the previous fixed-width horizontal clipping.
- Added safe **Open in VS Code** integration using a fixed subprocess argument list. Quick edits stay in Aware Minds; complex work can move to a full IDE.
- Quick Push remains preview-first: it shows changed files and remote divergence, blocks common secrets, and requires final confirmation. Force push remains unavailable.
- The installer offers to install missing Python, Node.js and Git packages through Windows Package Manager. This is not yet a signed standalone Windows installer; systems without `winget` need manual prerequisites.
- Verification: 17 backend tests, 2 frontend tests, Python bytecode compilation, ESLint, TypeScript and the production build pass. Playwright flows are prepared for eight target viewports but remain environment-blocked because Chromium could not be installed.

## Account-free local mode (2026-09-14)

- Removed registration, sign-in and sign-out from the user interface. `/`, `/login`, `/register`, and legacy AI bookmarks now open `/hub` directly.
- The backend creates and uses one stable local workspace owner automatically. When upgrading an account-based database, it opens the existing workspace with the most projects so saved work is not hidden. Projects and settings persist in `%LOCALAPPDATA%\AwareMinds` without cookies or account creation.
- Account endpoints return HTTP 410 for compatibility instead of creating users. Admin pages are unavailable in this single-user build. Application API keys and preview/approval checks remain independent safeguards.
- This mode is deliberately for a trusted local Windows account. It must not be exposed to a LAN or public internet because anyone who can reach the service can control connected repositories and project databases.

## Current Windows local workflow

- `Install Aware Minds.cmd` builds frontend and creates a desktop shortcut; `Start Aware Minds.cmd` starts one FastAPI process serving React and API together at `127.0.0.1:8000`, with Ollama on the local machine. Older two-process dev scripts remain for developers; running both simultaneously conflicts on port 8000.
- On first launch `scripts/prepare_local.py` creates the stable `%LOCALAPPDATA%\AwareMinds` directory but never imports a database from the extracted application. Moving between application versions retains the stable local workspace. **Start Fresh** is the explicit, recoverable reset path.
- User-supplied PNG is reused as the full logo in hero/auth and cropped visually for compact brand markers; PWA cache v2 includes the logo. Windows desktop shortcut points at the packaged icon. UI provides explicit corrections saved as scoped editable memories, **not model-weight self-training**. Local backups use `Backup Aware Minds.cmd` and JSON export remains in Settings.
- Verification: 14 backend tests, 2 frontend tests, TypeScript/production build, ESLint, Ruff F checks, same-origin HTTP and session continuity after restart. Windows desktop shortcut itself and actual Ollama output were not executable in this Linux environment; E2E browser viewport checks remain pending.

## Hosted-model work in progress

The user-supplied teal/purple brain and AWARE MINDS wordmark is now the canonical frontend brand asset at `apps/web/public/aware-minds-logo.png`, including header, workspace, authentication, demo, orb and PWA metadata. The original supplied pixels are retained.

Optional `AI_PROVIDER=hosted` sends non-streaming and streaming chat through a configured HTTPS OpenAI-compatible model endpoint, including app integration requests. `AI_PROVIDER=ollama` remains the default. Dockerfile builds the React frontend and serves it from the same FastAPI origin when `SERVE_WEB=1`; this is **private staging preparation, not a public deployment**. Hosted inference sends selected conversation history, memory and retrieved document snippets to the configured provider. Remote provider is mocked in automated tests; live hosted inference and deployment are not verified. Security blockers listed below remain open.

## Verified now

- Existing FastAPI/React/SQLite/Ollama architecture retained. Repeatable additive v2 schema startup; admin bootstrap requires a unique email and 12+ character password.
- Cookie sessions, authorization boundaries, per-email login throttling, explicit Origin/Fetch cross-site rejection, app-key scopes/revocation, user export without auth secrets, database backup and restore dry-run.
- Browser SSE chat, cancellation UI, separate app/project/memory scopes, file extraction and bounded lexical retrieval. Project/user content and document excerpts are untrusted reference messages, not system instructions. App-facing PHP/JS/Python examples remain server-side.
- 14 backend tests passing on isolated DBs; 2 frontend Vitest tests; Ruff F checks, ESLint, TypeScript and production Vite build passing. Live same-origin API/UI routes and session continuity checked in-process. JS and Python SDK mock contracts passed in the prior release pass. Backup integrity verified. Initial JavaScript bundle reduced from ~603 KB to ~270 KB through Markdown code splitting.
- Playwright tests cover eight target viewports and one mobile navigation flow, but **could not run** because the Chromium download timed out. No screenshots were visually inspected. PHP binary unavailable. Ollama absent; mocked success/error tests passed, live AI response quality unverified.

## Actual behavior and constraints

API version 0.3.0 under `/api/v1`; frontend 0.3.0; SQLite schema v2; Ollama is the local default and a separately configured hosted model adapter exists for private staging. `/health` checks process availability only. An absent model produces 503 without saving an unsent chat. Document source metadata indicates retrieved chunks, not validated answer accuracy. No vector store, embedding model, multimodal input, tool executor, provider fallback or MCP server exists. The current app key is a service-account key owned by one Aware Minds user; no external patient/student identity delegation. A formal database migration framework remains pending.

## Blockers before public release

Install/run Playwright Chromium and inspect/repair eight desktop/tablet/mobile screenshots. Test a live Ollama model, multilingual response quality and real RAG grounding. Harden CSRF, registration/IP throttling, upload parser sandbox/virus screening, delegated identity, public TLS/ops, and formal migrations. Review security/UX after actual browser testing. See `docs/RELEASE_CHECKLIST.md`, `docs/SECURITY.md` and `docs/ROADMAP.md`.

**Status: local release candidate; NOT READY for public production.**
# Project Hub pivot (2026-09-13)

- The primary product is now a private project command center, not a personal AI assistant. `/hub` is the default signed-in route and the Windows shortcut opens it directly.
- Added user-isolated, SQLite-backed projects, progress, status, priority, next action, tasks, notes and decisions. Bujhi, Healthcare Central, KAL.RA and Kishan Bari are seeded once per account; users can add and delete their own projects.
- Replaced the public landing experience and primary navigation with the hub. Legacy AI routes remain isolated for architectural compatibility but are hidden from the normal product flow. The hub requires no Ollama or external AI API.
- Account/session persistence continues in `%LOCALAPPDATA%\AwareMinds`; ZIP replacement does not reset existing accounts or project data. Desktop install/start/backup launchers remain the supported Windows flow.
- Backend tests now include project seeding, mutation, persistence behavior and cross-user authorization.

## Unified control workspace (2026-09-13)

- Each project now carries a validated visual theme; selecting it changes the workspace accent while retaining the Aware Minds shell.
- Added expandable project feature catalogs with planned/building/complete states. Known projects receive starter capability lists. `aware-hub.json` safely synchronizes declared features without importing or executing source code.
- Added project-scoped teammate records. No notifications, reports, health score, or universal task manager were introduced.
- Added local Git repository connection, status, and push of existing commits. GitHub credentials are delegated to the user's existing Git configuration and never stored by Aware Minds.
- Added protected SQLite inspection and cell editing for a database inside the configured project directory. Arbitrary paths and raw SQL are rejected.
- Future-project onboarding accepts name, purpose, theme, local folder, repository URL, and website in one form.

## Repository Control (2026-09-13)

- Added a deterministic, preview-first repository command console for text replacement, protected deletion, uploaded-file placement, Git commit and Git push without an AI provider.
- Every write becomes a pending action with a file summary. Apply and Reject are authenticated; previews expire after 30 minutes and fail if a source file changed after preview.
- Paths cannot escape the project root. `.git`, dependency/build folders, `.env`, credentials and secret files are protected. Global replacement is restricted to recognized text files, 2 MB per file and 500 affected files.
- Uploads are limited to 2 MB and require approval. Controls and dashboard typography were normalized for a denser interface.
- External projects have not had their own authentication physically removed because their repositories are not part of this workspace. The hub is the central control login; replacing child-app authentication requires a separately reviewed SSO connector in each child repository, not shared cookies or copied passwords.
- Verification: 15 backend tests and 2 frontend tests pass; TypeScript production build and ESLint pass. Playwright remains environment-blocked because Chromium is not installed.

## Legacy route repair (2026-09-13)

- Removed the obsolete AI document-library entry from hub navigation. Legacy `/library`, `/chat`, `/memory`, `/apps`, `/projects`, `/conversations`, and `/developers` bookmarks now resolve to `/hub` instead of opening disconnected AI screens.
- Advanced the PWA shell cache so installed/local Chrome sessions replace the older cached interface on restart.

## Superseded 0.4 native-window experiment (historical)

- The earlier pywebview shell has been replaced by the 0.5 default-browser launcher because browser sizing, popovers and responsive behavior are more reliable.
- Added a Windows native folder picker and GitHub clone-and-connect workflow. GitHub credentials remain delegated to Git Credential Manager and are never stored by Aware Minds.
- Removed personal project seeding for newly created accounts. Existing saved projects remain in the persistent database; new developers receive a clean first-project onboarding state.
- Added a protected repository file browser and UTF-8 editor for text files up to 2 MB. Saves are hash-checked and require a review confirmation; `.env`, credentials, keys, dependencies, build output and `.git` remain inaccessible.
- Added Quick Push: visible changed files, branch/ahead/behind information, blocked-secret warnings, commit message, final summary, remote fetch/conflict check, commit and push. Force push is not implemented.
- Added persistent light and dark appearance modes. Both retain the purple Aware Minds identity while selected projects retain their configured accent.
- Verification: 16 backend tests, including a real local Git commit/push to a disposable bare remote; 2 frontend component tests; Python bytecode compilation; ESLint; TypeScript; and the production build pass. Playwright's 9 responsive tests remain blocked because its Chromium download timed out. Ruff is not installed in this environment. Native Windows shell and folder dialog cannot be executed in Linux and must be smoke-tested on Windows after installation.
