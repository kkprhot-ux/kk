import logging
import os
from typing import Dict, List
from server.asr_service import XunfeiASR
from server.llm_service import DeepSeekClient

logger = logging.getLogger(__name__)

class SuggestionPipeline:
    """音频 → ASR → LLM → 话术 的完整 pipeline"""

    def __init__(self):
        self.asr = XunfeiASR(
            app_id=os.getenv("XUNFEI_APP_ID"),
            api_key=os.getenv("XUNFEI_API_KEY"),
            api_secret=os.getenv("XUNFEI_API_SECRET"),
        )
        self.llm = DeepSeekClient()

    async def process_audio(self, audio_chunk: bytes, history: List[Dict] = None, context: Dict = None) -> Dict:
        asr_result = await self.asr.recognize(audio_chunk)
        customer_text = asr_result["text"]
        if not customer_text.strip():
            return {"customer_text": "", "skip": True}
        suggestion = await self.llm.generate_suggestion(
            customer_text=customer_text,
            history=history or [],
            context=context or {},
        )
        return {"customer_text": customer_text, **suggestion}