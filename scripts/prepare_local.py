"""Use one durable per-user database across extracted Windows project versions."""
import os
from pathlib import Path


def prepare(project: Path, destination: Path) -> str:
    destination.mkdir(parents=True, exist_ok=True)
    current_db = destination / 'aware-minds.db'
    if current_db.exists():
        return 'Using the existing local workspace.'
    # Never import a database from the extracted application directory. A ZIP
    # may be unpacked over an old copy; importing from it makes a fresh install
    # unexpectedly contain another workspace's projects.
    return 'Starting a new empty local workspace.'


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    data_dir = Path(os.environ['AWARE_MINDS_DATA_DIR'])
    print(prepare(root, data_dir))
    print('Data folder:', data_dir)
