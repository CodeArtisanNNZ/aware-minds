# Aware Minds 1.0 — Guided Developer Workspace

Aware Minds is a local-first workspace for people learning to build and publish software. It combines a Canva-like project workspace, a visual Git timeline, safe file editing, contextual learning and a complete idea-to-live roadmap.

## Start on Windows

1. Extract the ZIP completely.
2. Double-click **Start Aware Minds.cmd**.
3. Your browser opens at http://127.0.0.1:8765.
4. Keep the small local process running while editing projects. Closing only the browser tab does not delete data.
5. Optional: double-click **Install Aware Minds.cmd** once to create a Desktop shortcut.

Python 3 and Git are the only prerequisites. There is no npm install, account, Ollama model or external AI API.

## What works

- Clean first launch with no personal projects or demo accounts
- Persistent project library in browser storage
- Beginner, Practising and Professional guidance levels
- Dark and soft-gradient light themes
- Seven-stage Plan → Design → Build → Data → Test → GitHub → Live workflow
- Secure Windows project-folder picker
- Text source file browser/editor with review before writing
- One-edit undo and project progress
- Git status, fetch safety check, commit and push through the installed Git Credential Manager
- Clone GitHub repositories using existing Git authentication
- Open a connected project in VS Code
- Contextual ⓘ explanations on every workspace
- Searchable field guide for languages, databases, Git, interfaces, hosting, domains and GitHub Student benefits
- Keyboard command palette with Ctrl+K
- Responsive desktop, tablet and phone interface
- Reduced-motion support

## Safety boundaries

Aware Minds binds only to 127.0.0.1. It blocks .git, dependencies, build output, secret filenames and path traversal. The editor accepts recognized text files up to 2 MB. Git push is blocked when remote commits are ahead or possible secret files are detected. Force push and arbitrary shell execution are not available.

This is a local developer tool—not a public multi-user server. Do not expose port 8765 to a network.

## GitHub workflow

Connect a project folder → edit and save → open **GitHub** → review changed files → **Review & push** → write a clear commit message → confirm.

Git credentials stay in Git Credential Manager. Aware Minds does not ask for or save a GitHub password.

## Data and removal

Interface data is stored by the browser for http://127.0.0.1:8765. Folder permissions are stored in %LOCALAPPDATA%\AwareMinds\workspace.json.

Use Settings → Reset to remove browser project data. Delete %LOCALAPPDATA%\AwareMinds to remove local folder connections.

## Honest scope

Version 1.0 is a polished local MVP. It does not replace advanced VS Code debugging, extensions, integrated terminals, merge-conflict editors or database administration. The workspace teaches users when to move into VS Code and provides that handoff directly.

Copyright © 2026 Aware Minds. Review and add your chosen commercial license before selling or redistributing.
