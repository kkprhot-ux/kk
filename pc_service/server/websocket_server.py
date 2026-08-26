import json
import logging
import os
from datetime import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from storage.database import Database
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Real-time Sales Assistant")
logger = logging.getLogger(__name__)

db_instance = None
active_calls = {}


def init_app():
    """Initialize (idempotent: safe to call multiple times)."""
    global db_instance
    db_path = os.getenv("DB_PATH", "D:\\PersonalAssistant\\data\\assistant.db")
    if db_instance is not None:
        try:
            db_instance.close()
        except Exception:
            pass
        db_instance = None
    db_instance = Database(db_path)
    db_instance.init_schema()
    logger.info(f"Database initialized at {db_path}")


@app.on_event("startup")
async def startup():
    init_app()


@app.get("/")
def root():
    return {"status": "ok", "service": "Real-time Sales Assistant"}


@app.get("/health")
def health():
    return {"status": "ok", "db_connected": db_instance is not None}


@app.websocket("/ws/audio")
async def audio_websocket(websocket: WebSocket):
    await websocket.accept()
    call_id = None
    try:
        while True:
            data = await websocket.receive()
            if "text" in data:
                msg = json.loads(data["text"])
                if msg["type"] == "call_start":
                    call_id = create_call_record(msg.get("phone_number"))
                    active_calls[call_id] = {"phone": msg.get("phone_number"), "transcript": []}
                    await websocket.send_json({"type": "ack", "call_id": call_id})
                elif msg["type"] == "call_end":
                    if call_id:
                        finalize_call(call_id)
                        del active_calls[call_id]
                    await websocket.send_json({"type": "ack"})
    except WebSocketDisconnect:
        logger.info("Client disconnected")


def create_call_record(phone_number: str = None) -> int:
    cursor = db_instance.execute(
        "INSERT INTO calls (start_time, phone_number) VALUES (datetime('now', 'localtime'), ?)",
        (phone_number,),
    )
    db_instance.conn.commit()
    return cursor.lastrowid


def finalize_call(call_id: int):
    db_instance.execute(
        "UPDATE calls SET end_time = datetime('now', 'localtime'), duration_sec = CAST((julianday(end_time) - julianday(start_time)) * 86400 AS INTEGER) WHERE id = ?",
        (call_id,),
    )
    db_instance.conn.commit()


@app.get("/calls")
def list_calls(limit: int = 50):
    """List recent calls (newest first)."""
    rows = db_instance.execute(
        "SELECT id, start_time, end_time, phone_number, duration_sec, scenario "
        "FROM calls ORDER BY start_time DESC LIMIT ?",
        (limit,),
    ).fetchall()
    return [dict(row) for row in rows]