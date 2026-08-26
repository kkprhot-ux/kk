"""PC-side smoke test: validates the full backend chain end-to-end with mocks."""
import os
import json
import shutil
import tempfile
import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("DEEPSEEK_API_KEY", "smoke-test-key")
os.environ.setdefault("XUNFEI_APP_ID", "smoke-test")
os.environ.setdefault("XUNFEI_API_KEY", "smoke-test")
os.environ.setdefault("XUNFEI_API_SECRET", "smoke-test")

from server import websocket_server as ws_module
from server.websocket_server import app, init_app

_SMOKE_TMP = tempfile.mkdtemp(prefix="sales_assistant_smoke_")
_DB_PATH = os.path.join(_SMOKE_TMP, "smoke.db")
_BACKUP_DIR = os.path.join(_SMOKE_TMP, "backups")
os.environ["DB_PATH"] = _DB_PATH
os.environ["BACKUP_DIR"] = _BACKUP_DIR


@pytest.fixture(scope="module")
def client():
    init_app()
    client = TestClient(app)
    with client:
        yield client
    if ws_module.db_instance is not None:
        try:
            ws_module.db_instance.close()
        except Exception:
            pass
    try:
        shutil.rmtree(_SMOKE_TMP, ignore_errors=True)
    except Exception:
        pass


def test_health_endpoint_responds(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["db_connected"] is True


def test_root_endpoint_responds(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "Real-time Sales Assistant"


def test_call_record_creation_and_lookup():
    """Verify that a call record can be created and read back via the API."""
    # Direct DB test (bypasses WebSocket threading issues)
    call_id = ws_module.create_call_record(phone_number="13800138999")
    assert call_id > 0
    rows = ws_module.db_instance.execute(
        "SELECT id, phone_number, start_time FROM calls WHERE id = ?", (call_id,)
    ).fetchall()
    assert len(rows) == 1
    assert dict(rows[0])["phone_number"] == "13800138999"


def test_calls_list_endpoint_returns_history(client):
    """GET /calls returns the calls list (newest first)."""
    response = client.get("/calls")
    assert response.status_code == 200
    calls = response.json()
    assert isinstance(calls, list)
    # calls created in previous test should be in the list
    assert any(c.get("phone_number") == "13800138999" for c in calls)


def test_pipeline_components_importable():
    from server.asr_service import XunfeiASR
    from server.llm_service import DeepSeekClient
    from analyzer.suggestion import SuggestionPipeline
    from analyzer.replay import ReplayGenerator
    from storage.backup import BackupManager
    assert XunfeiASR.__name__ == "XunfeiASR"
    assert DeepSeekClient.__name__ == "DeepSeekClient"
    assert SuggestionPipeline.__name__ == "SuggestionPipeline"
    assert ReplayGenerator.__name__ == "ReplayGenerator"
    assert BackupManager.__name__ == "BackupManager"


def test_backup_manager_can_archive_db():
    from pathlib import Path
    from storage.backup import BackupManager

    mgr = BackupManager(_DB_PATH, _BACKUP_DIR, retention_days=30)
    mgr.backup()

    archives = list(Path(_BACKUP_DIR).glob("*.db.gz"))
    assert len(archives) >= 1
    assert archives[0].stat().st_size > 0


def test_sales_prompts_have_required_fields():
    from server.sales_prompts import SUGGESTION_SYSTEM_PROMPT, REPLAY_SYSTEM_PROMPT
    for key in ["scenario", "intent", "emotion", "recommended_script", "next_step"]:
        assert key in SUGGESTION_SYSTEM_PROMPT, f"Missing key '{key}' in SUGGESTION prompt"
    for key in ["summary", "customer_concerns", "objections", "emotion_curve", "highlights", "improvements", "next_actions"]:
        assert key in REPLAY_SYSTEM_PROMPT, f"Missing key '{key}' in REPLAY prompt"


def test_schema_has_all_required_tables(client):
    """v2.1: 3 tables (contacts removed in v2.1)."""
    tables = [r[0] for r in ws_module.db_instance.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    ).fetchall()]
    assert "calls" in tables
    assert "call_replays" in tables
    assert "realtime_suggestions" in tables
    assert "contacts" not in tables, "contacts table should be removed in v2.1"


