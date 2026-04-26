from groq import AsyncGroq
from app.core.config import settings
from app.core.logger import logger
import json
from typing import Any, Dict

class GroqService:
    def __init__(self):
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"
        
    async def get_json_completion(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """
        Calls Groq LLM forcing a JSON output.
        """
        try:
            chat_completion = await self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model=self.model,
                response_format={"type": "json_object"},
            )
            response_text = chat_completion.choices[0].message.content
            return json.loads(response_text)
        except Exception as e:
            logger.error(f"Groq API Error: {str(e)}")
            raise

groq_service = GroqService()
