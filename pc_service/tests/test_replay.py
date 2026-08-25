import os
os.environ.setdefault("DEEPSEEK_API_KEY", "test")
import pytest
from unittest.mock import patch, MagicMock
from analyzer.replay import ReplayGenerator

@pytest.mark.asyncio
async def test_generate_replay_saves_to_db():
    db = MagicMock()
    gen = ReplayGenerator(db=db)
    with patch.object(gen.llm, 'generate_replay', return_value={
        "summary": "客户对比价格",
        "customer_concerns": ["价格"],
        "objections": ["贵"],
        "emotion_curve": ["😐", "😕"],
        "highlights": ["成功共情"],
        "improvements": ["让步时机偏晚"],
        "next_actions": ["发送对比表"]
    }):
        result = await gen.generate(call_id=1, transcript="...")
        assert result["summary"] == "客户对比价格"
        db.execute.assert_called_once()
        db.conn.commit.assert_called_once()