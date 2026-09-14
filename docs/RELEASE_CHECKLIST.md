# Release checklist — 0.7.0

- [x] Default-browser launch with duplicate-server detection
- [x] Project gallery and full-width workspace navigation
- [x] Protected file editing, reviewed save and reviewed Quick Push
- [x] Open connected repository in VS Code without shell interpolation
- [x] Guided Windows prerequisite installation when `winget` is available
- [ ] Smoke-test browser launch, folder picker, Git Credential Manager and VS Code opening on Windows
- [ ] Produce a signed standalone Windows installer for non-developer distribution

| Check | Status | Evidence / blocker |
| --- | --- | --- |
| Empty DB startup and repeatable additive upgrade | Pass | `tests/test_release.py` |
| Universal empty first-project onboarding | Pass | `tests/test_release.py` |
| Protected repository file browser/save | Pass | Hash-checked API integration test |
| Quick Push commit and remote push | Pass | Disposable bare Git remote integration test |
| Secret filename/content blocking | Pass | API integration test |
| Windows native desktop shell and folder picker | Pending Windows smoke test | Cannot execute Windows GUI in Linux release environment |
| Admin bootstrap and role access | Pass | tests; requires 12+ character env password on first startup |
| Backend, frontend unit tests | Pass | 11 pytest, 2 Vitest |
| Frontend TypeScript, ESLint, production build | Pass | `npm run typecheck`, `npm run lint`, `npm run build` |
| Python lint | Pass | Ruff F rules |
| API/chat/stream/memory/isolation/upload | Pass under deterministic mocked model | Tests cover real routes; no live Ollama |
| SDK contracts | Pass | JS transpilation + mock fetch; Python mock urllib |
| PHP integration runtime | Not tested | PHP binary unavailable |
| 8 viewport screenshots / visual QA | Blocked | No local browser; Playwright Chromium download timed out. No screenshots inspected |
| Security: auth/CSRF/rate limits/files | Partial | Auth/isolation/Origin/throttle tests pass; no extractor sandbox or full production review |
| Secrets check | Partial | No real secrets committed; manual code review only |
| AI provider | Blocked | Ollama absent; unavailable and malformed paths pass |
| Backup | Pass | SQLite backup integrity and restore dry-run; live restore not attempted |
| App keys | Pass | Scope/wrong-app/revocation tests |
| MCP | Not applicable | No MCP server implemented; not claimed |
| Documentation | Pass | README and `docs/` updated |
| Version tagging | Pending | No external git repository or release tag requested |

**Decision: NOT READY for public production.** Remain on localhost until security hardening, delegated end-user identity and browser/visual QA are complete.
