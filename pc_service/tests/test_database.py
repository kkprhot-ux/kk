from storage.database import Database

def test_database_creates_schema(tmp_path):
    db_path = tmp_path / "test.db"
    db = Database(str(db_path))
    db.init_schema()
    tables = db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    table_names = [t[0] for t in tables]
    assert "calls" in table_names
    assert "call_replays" in table_names
    assert "realtime_suggestions" in table_names
    assert "contacts" in table_names
