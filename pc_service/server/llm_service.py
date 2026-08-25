import os
import json
import httpx
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class DeepSeekClient:
    """DeepSeek API 客户端（OpenAI 兼容）"""

    BASE_URL = "https://api.deepseek.com/v1"

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY not set")

    async def _call_api(self, messages: List[Dict], model: str = "deepseek-chat") -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={"model": model, "messages": messages, "temperature": 0.7},
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()

    async def generate_suggestion(self, customer_text, history=None, context=None):
        from server.sales_prompts import SUGGESTION_SYSTEM_PROMPT
        history = history or []
        context = context or {}
        messages = [
            {"role": "system", "content": SUGGESTION_SYSTEM_PROMPT},
            {"role": "user", "content": self._format_suggestion_input(customer_text, history, context)},
        ]
        response = await self._call_api(messages)
        content = response["choices"][0]["message"]["content"]
        return self._parse_json_response(content)

    async def generate_replay(self, transcript: str) -> dict:
        from server.sales_prompts import REPLAY_SYSTEM_PROMPT
        messages = [
            {"role": "system", "content": REPLAY_SYSTEM_PROMPT},
            {"role": "user", "content": f"以下是一通电话的完整转写：\n\n{transcript}"},
        ]
        response = await self._call_api(messages)
        content = response["choices"][0]["message"]["content"]
        return self._parse_json_response(content)

    def _format_suggestion_input(self, customer_text, history, context):
        parts = []
        if history:
            parts.append("【最近对话】")
            for h in history[-6:]:
                role = "客户" if h["role"] == "customer" else "您"
                parts.append(f"{role}: {h['text']}")
        parts.append(f"\n【客户最新说】\n{customer_text}")
        if context:
            parts.append(f"\n【当前场景】{context.get('scenario', '未知')}")
        return "\n".join(parts)

    def _parse_json_response(self, content: str) -> dict:
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            start = content.find("{")
            end = content.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(content[start:end])
            return {"error": "parse_failed", "raw": content}