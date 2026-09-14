"""Build a clean, data-free ZIP from the checked release workspace."""
from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


EXCLUDED_DIRS = {
    ".git", ".venv", "node_modules", "test-results", "playwright-report",
    "__pycache__", ".pytest_cache", ".ruff_cache", "backups", "uploads",
}
EXCLUDED_SUFFIXES = {".db", ".sqlite", ".sqlite3", ".pyc", ".tsbuildinfo"}


def package(root: Path, output: Path) -> int:
    root = root.resolve()
    output = output.resolve()
    if not (root / "AGENTS.md").is_file() or not (root / "apps/web/dist/index.html").is_file():
        raise SystemExit("Run the production frontend build before packaging.")
    count = 0
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for source in sorted(root.rglob("*")):
            relative = source.relative_to(root)
            if source.is_dir() or any(part in EXCLUDED_DIRS for part in relative.parts):
                continue
            if source.name == ".env":
                continue
            if source.suffix.lower() in EXCLUDED_SUFFIXES:
                continue
            archive.write(source, Path("aware-minds") / relative)
            count += 1
    with zipfile.ZipFile(output) as archive:
        names = archive.namelist()
        forbidden = [name for name in names if Path(name).suffix.lower() in {".db", ".sqlite", ".sqlite3"}]
        if forbidden:
            raise RuntimeError(f"Release contains private workspace data: {forbidden}")
        bad = archive.testzip()
        if bad:
            raise RuntimeError(f"Corrupt ZIP member: {bad}")
    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    project_root = Path(__file__).resolve().parents[1]
    total = package(project_root, args.output)
    print(f"Created {args.output.resolve()} with {total} product files and no workspace database.")
