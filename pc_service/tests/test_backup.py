from storage.backup import BackupManager

def test_backup_creates_archive(tmp_path):
    db_path = tmp_path / "test.db"
    db_path.write_text("test data")
    backup_dir = tmp_path / "backups"
    mgr = BackupManager(str(db_path), str(backup_dir))
    mgr.backup()
    archives = list(backup_dir.glob("*.db.gz"))
    assert len(archives) == 1

def test_backup_cleans_old_files(tmp_path):
    db_path = tmp_path / "test.db"
    db_path.write_text("test data")
    backup_dir = tmp_path / "backups"
    backup_dir.mkdir()
    # 创建 31 天前的备份
    old_backup = backup_dir / "assistant_2020-01-01.db.gz"
    old_backup.write_text("old")
    mgr = BackupManager(str(db_path), str(backup_dir), retention_days=30)
    mgr.backup()
    assert not old_backup.exists()