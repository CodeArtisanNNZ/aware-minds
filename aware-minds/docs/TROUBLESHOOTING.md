# Troubleshooting

- Frontend start error about network interfaces: use the repository's `npm run dev` script, which binds to `127.0.0.1`.
- Model offline: install/start Ollama and pull a model; check `/api/v1/models` after login. Chat returns 503 without saving the request when no model is installed.
- Admin login rejected: set unique `ADMIN_EMAIL` and 12+ character `ADMIN_PASSWORD` **before first startup**. If the email already belongs to a regular user, environment variables do not promote that account. Do not edit the DB by hand.
- 429 login response: wait 15 minutes or correct repeated invalid credentials after the window expires.
- E2E browser missing: `cd apps/web && npx playwright install chromium`; network access may be needed.
- Frontend/API mismatch: API port 8000, Vite port 5173 on localhost; reinstall with setup script and run test script.
