import json
import logging
from server.llm_service import DeepSeekClient
from storage.database import Database

logger = logging.getLogger(__name__)

class ReplayGenerator:
    def __init__(self, db: Database = None):
        self.llm = DeepSeekClient()
        self.db = db

    async def generate(self, call_id: int, transcript: str) -> dict:
        replay = await self.llm.generate_replay(transcript)
        if self.db:
            self.db.execute(
                """INSERT INTO call_replays
                (call_id, summary, customer_concerns, objections, emotion_curve,
                 highlights, improvements, next_actions)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (call_id, replay.get("summary"),
                 json.dumps(replay.get("customer_concerns", []), ensure_ascii=False),
                 json.dumps(replay.get("objections", []), ensure_ascii=False),
                 json.dumps(replay.get("emotion_curve", [])),
                 json.dumps(replay.get("highlights", []), ensure_ascii=False),
                 json.dumps(replay.get("improvements", []), ensure_ascii=False),
                 json.dumps(replay.get("next_actions", []), ensure_ascii=False))
            )
            self.db.conn.commit()
        return replay