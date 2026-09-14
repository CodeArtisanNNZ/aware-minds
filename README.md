# Aware Minds Developer Hub

Aware Minds is a local developer workspace designed to make project and Git management easier without requiring command-line experience.

Connect an existing Git folder or clone a GitHub repository, browse and edit project files, review changes, and commit and push through a guided visual workflow.

## Features

- Account-free local workspace
- Connect local Git repositories
- Clone projects from GitHub
- Browse and edit supported text files
- Preview changes before applying them
- Visual Connect → Edit → Review → Push workflow
- Guided Git commit and push
- Protection for common secret files
- Project-specific themes
- Light and dark appearance
- Local SQLite workspace storage
- No Ollama or external AI API required

## Windows installation

1. Download the latest ZIP from GitHub Releases.
2. Extract the complete ZIP into a permanent folder.
3. Double-click `Install Aware Minds.cmd`.
4. Allow the installation to finish.
5. Open Aware Minds using the desktop shortcut.

A first-time installation starts with an empty project library.

## Requirements

The installer can install missing prerequisites through Windows Package Manager:

- Python 3.12 or newer
- Node.js LTS
- Git for Windows

## Privacy

Aware Minds runs locally on the user’s computer. Project information is stored under `%LOCALAPPDATA%\AwareMinds`.

Passwords, API keys and GitHub credentials are not stored by Aware Minds. GitHub authentication is handled through Git Credential Manager.

## Safety

Repository modifications require a preview and confirmation. Common secret files, credentials, private keys and environment files are blocked from the Quick Push workflow.

Always review changes before committing or pushing.
