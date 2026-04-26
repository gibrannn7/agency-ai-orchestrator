from fastapi import Header, HTTPException
import hmac
import hashlib
from app.core.config import settings

async def verify_webhook_signature(x_webhook_signature: str = Header(..., alias="X-Webhook-Signature"), body: bytes = None):
    """
    Dependency to verify webhook signature.
    Since we don't have a specific secret defined for this in .env yet, 
    we use the TELEGRAM_BOT_TOKEN as a generic webhook secret for demonstration.
    """
    secret = settings.TELEGRAM_BOT_TOKEN.encode()
    
    # Normally you'd hash the raw body
    # computed_sig = hmac.new(secret, body, hashlib.sha256).hexdigest()
    # if not hmac.compare_digest(computed_sig, x_webhook_signature):
    #     raise HTTPException(status_code=401, detail="Invalid signature")
    
    # Simulating token-based verification for now if raw body isn't available
    if x_webhook_signature != settings.TELEGRAM_BOT_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid signature token")
        
    return True
