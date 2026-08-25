import pytest
from unittest.mock import patch
from server.llm_service import DeepSeekClient

@pytest.mark.asyncio
async def test_generate_suggestion():
    client = DeepSeekClient(api_key="test")
    mock_response = {
        "choices": [{"message": {"content": '{"scenario": "异议处理", "recommended_script": "理解您"}'}}]
    }
    with patch.object(client, '_call_api', return_value=mock_response):
        result = await client.generate_suggestion(
            customer_text="你们太贵了", history=[], context={"scenario": "cold_call"}
        )
        assert result["scenario"] == "异议处理"

@pytest.mark.asyncio
async def test_generate_replay():
    client = DeepSeekClient(api_key="test")
    mock_response = {
        "choices": [{"message": {"content": '{"summary": "客户对比价格", "highlights": []}'}}]
    }
    with patch.object(client, '_call_api', return_value=mock_response):
        result = await client.generate_replay(transcript="...")
        assert "summary" in result