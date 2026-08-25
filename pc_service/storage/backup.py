import gzip
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class BackupManager:
    def __init__(self, db_path: str, backup_dir: str, retention_days: int = 30):
        self.db_path = db_path
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.retention_days = retention_days

    def backup(self):
        ts = datetime.now().strftime("%Y-%m-%d")
        backup_file = self.backup_dir / f"assistant_{ts}.db.gz"
        with open(self.db_path, 'rb') as f_in:
            with gzip.open(backup_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        logger.info(f"Backup created: {backup_file}")
        self.cleanup_old_backups()

    def cleanup_old_backups(self):
        cutoff = datetime.now() - timedelta(days=self.retention_days)
        for backup_file in self.backup_dir.glob("*.db.gz"):
            try:
                # Fix: backup_file.name = "assistant_2020-01-01.db.gz"
                # Use name (not stem, which would strip ".gz" only leaving "...db")
                # and then split off the suffix to isolate the date
                date_part = backup_file.name.split("_")[1].split(".")[0]
                file_date = datetime.strptime(date_part, "%Y-%m-%d")
                if file_date < cutoff:
                    backup_file.unlink()
                    logger.info(f"Deleted old backup: {backup_file}")
            except (ValueError, IndexError):
                continue