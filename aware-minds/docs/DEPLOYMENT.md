# Deployment boundary

This version is a local development release candidate, not a public service. Use `./scripts/setup.sh` + `./scripts/dev.sh` or PowerShell equivalents. Export `ADMIN_EMAIL`/`ADMIN_PASSWORD` before first startup; no `.env` autoload. A public deployment requires complete CSRF and rate-limiting design, HTTPS, hardened upload parsing, delegated external user identity, persistent backup policy, operational logging review, proper database migrations and browser E2E/accessibility QA.
