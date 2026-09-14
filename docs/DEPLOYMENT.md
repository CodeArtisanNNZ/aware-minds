# Deployment boundary

This version is a local development release candidate, not a public service. Use `./scripts/setup.sh` + `./scripts/dev.sh` or PowerShell equivalents. Export `ADMIN_EMAIL`/`ADMIN_PASSWORD` before first startup; no `.env` autoload. A public deployment requires complete CSRF and rate-limiting design, HTTPS, hardened upload parsing, delegated external user identity, persistent backup policy, operational logging review, proper database migrations and browser E2E/accessibility QA.

## Hosted-model staging configuration (not a public release)

The Dockerfile builds the React frontend and serves it from FastAPI at the same origin. In a **private staging environment**, set `AI_PROVIDER=hosted`, `HOSTED_AI_BASE_URL` to your provider's HTTPS OpenAI-compatible `/v1` URL, `HOSTED_AI_MODEL` to a model available on that provider, and `HOSTED_AI_API_KEY` as a secret in the host settings. `SERVE_WEB=1` is baked into the image. Do not commit the key. With this configuration Ollama is not needed. `/api/v1/models` reports the configured model; it does not probe the remote provider, so a successful chat is the actual availability check. External inference providers receive chat text, retrieved document snippets and selected memories; do not upload patient or student data without a privacy review and consent.

Use persistent storage for `/app/data` and back it up: SQLite and uploads vanish if hosted on an ephemeral container. Run one backend instance against SQLite; multi-instance deployments require a database migration. Set `PRODUCTION=1` for Secure cookies and configure the exact `CORS_ORIGIN` if hosting a separate web origin. Prefer the included same-origin frontend to avoid cross-origin cookies. `/health` only reports process liveness.

Do not expose this image publicly until the security blockers above are fixed and reviewed. A model-provider key and an online container alone do not make the application production-safe.
