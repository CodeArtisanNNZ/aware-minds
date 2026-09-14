# Project feature synchronization

Place `aware-hub.json` in a connected project's root folder. The hub reads this file when **Sync manifest** is selected; it never executes the project code.

```json
{
  "features": [
    {"title": "Emergency ambulance search", "status": "complete", "description": "Public emergency lookup without login."},
    {"title": "Medicine price comparison", "status": "building", "description": "Links to verified external medicine sellers."},
    {"title": "Bangla interface", "status": "planned"}
  ]
}
```

Allowed status values are `planned`, `building`, and `complete`. Synchronization adds new feature titles and updates matching titles. It does not delete manually created features.

Git operations use credentials already configured by Git or GitHub Desktop. The hub does not store GitHub passwords or tokens. **Push to Git** pushes existing commits; it does not automatically stage or commit files.

Database browsing supports SQLite databases located inside the configured project folder. Raw SQL and arbitrary database paths remain disabled. The first 100 rows are shown and individual cells can be edited through validated table and column names.

## Repository command examples

```text
replace 999 with 16297 everywhere
replace Old heading with New heading in src/page.tsx
delete public/old-logo.png
commit changes as Update project files
push current branch
```

Commands and uploaded files create previews and require approval. This is a deterministic command system, not a generative AI agent, so unsupported or vague instructions are rejected instead of guessed.
