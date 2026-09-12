"""Explicit local-only restore with an automatic pre-restore backup."""
import argparse
import os
import shutil
import sqlite3
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description='Restore a LOCAL development database while the API is stopped')
parser.add_argument('backup',type=Path)
parser.add_argument('--database',type=Path,default=ROOT/os.getenv('DATABASE_PATH','data/aware-minds.db'))
parser.add_argument('--confirm-local-restore',action='store_true')
args=parser.parse_args()
if not args.backup.is_file():parser.error('Backup file not found')
with sqlite3.connect(f'file:{args.backup}?mode=ro',uri=True) as candidate:
    if candidate.execute('PRAGMA integrity_check').fetchone()[0]!='ok':parser.error('Backup is not a valid SQLite database')
if not args.confirm_local_restore:
    print(f'Dry run only. Would restore {args.backup} to {args.database}. Stop the API and rerun with --confirm-local-restore.')
else:
    if os.getenv('APP_ENV')=='production':parser.error('Production restore is not supported by this utility')
    args.database.parent.mkdir(parents=True,exist_ok=True)
    if args.database.exists():
        safety=args.database.with_name(args.database.stem+f'-before-restore-{datetime.now(timezone.utc):%Y%m%d-%H%M%S}.db')
        with sqlite3.connect(args.database) as source,sqlite3.connect(safety) as destination:source.backup(destination)
        safety.chmod(0o600)
        print(f'Pre-restore backup: {safety}')
    shutil.copy2(args.backup,args.database)
    args.database.chmod(0o600)
    print(f'Restored {args.database}; start the API and verify login.')
