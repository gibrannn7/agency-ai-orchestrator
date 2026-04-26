import httpx
from app.core.config import settings
from app.core.logger import logger

class TelegramService:
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.chat_id = settings.TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    async def send_message(self, text: str) -> bool:
        """
        Send a text message to the configured Telegram chat.
        """
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "HTML"
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/sendMessage",
                    json=payload
                )
                response.raise_for_status()
                logger.info(f"Telegram message sent to chat {self.chat_id}")
                return True
            except Exception as e:
                logger.error(f"Telegram API Error: {str(e)}")
                return False

telegram_service = TelegramService()
