import httpx
from app.core.config import settings
from app.core.logger import logger

class BrevoService:
    def __init__(self):
        self.base_url = "https://api.brevo.com/v3/smtp/email"
        self.headers = {
            "api-key": settings.BREVO_API_KEY,
            "Content-Type": "application/json"
        }
        self.sender = {"email": settings.SENDER_EMAIL, "name": "Agency Orchestrator"}

    async def send_email(self, to_email: str, to_name: str, subject: str, html_content: str) -> bool:
        """
        Send an email via Brevo API.
        """
        payload = {
            "sender": self.sender,
            "to": [{"email": to_email, "name": to_name}],
            "subject": subject,
            "htmlContent": html_content
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.base_url,
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()
                logger.info(f"Email sent successfully to {to_email}")
                return True
            except Exception as e:
                logger.error(f"Brevo API Error sending email to {to_email}: {str(e)}")
                return False

brevo_service = BrevoService()
