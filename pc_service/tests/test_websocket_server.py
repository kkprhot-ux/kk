import os
import tempfile
from fastapi.testclient import TestClient
from server import websocket_server
from server.websocket_server import app, init_app

def test_root_returns_ok():
    with tempfile.TemporaryDirectory() as tmp:
        os.environ["DB_PATH"] = os.path.join(tmp, "test.db")
        init_app()
        try:
            client = TestClient(app)
            response = client.get("/")
            assert response.status_code == 200
            assert response.json()["status"] == "ok"
        finally:
            if websocket_server.db_instance is not None:
                websocket_server.db_instance.close()

def test_health_endpoint():
    with tempfile.TemporaryDirectory() as tmp:
        os.environ["DB_PATH"] = os.path.join(tmp, "test.db")
        init_app()
        try:
            client = TestClient(app)
            response = client.get("/health")
            assert response.status_code == 200
            data = response.json()
            assert "db_connected" in data
        finally:
            if websocket_server.db_instance is not None:
                websocket_server.db_instance.close()
