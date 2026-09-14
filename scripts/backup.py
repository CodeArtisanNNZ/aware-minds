"""Create a consistent development database backup. Protect this file like the original DB."""
import argparse
import os
import sqlite3
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description='Back up the local development SQLite database')
DATA_DIR=Path(os.getenv('AWARE_MINDS_DATA_DIR',str(ROOT/'data')))
parser.add_argument('--database',type=Path,default=ROOT/os.getenv('DATABASE_PATH',str(DATA_DIR/'aware-minds.db')))
parser.add_argument('--output',type=Path,default=None)
args=parser.parse_args()
if not args.database.is_file():parser.error('Database not found; start the API first')
out=args.output or DATA_DIR/'backups'/f'aware-minds-{datetime.now(timezone.utc):%Y%m%d-%H%M%S}.db'
out.parent.mkdir(parents=True,exist_ok=True)
if out.exists():parser.error('Output already exists; choose a different path')
with sqlite3.connect(f'file:{args.database}?mode=ro',uri=True) as source,sqlite3.connect(out) as destination:
    source.backup(destination)
    if destination.execute('PRAGMA integrity_check').fetchone()[0]!='ok':raise RuntimeError('Backup integrity check failed')
out.chmod(0o600)
print(f'Backup created: {out}. Contains private data; protect it and do not share it.')
