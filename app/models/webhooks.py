from pydantic import BaseModel, EmailStr, Field

class IncomingLeadWebhook(BaseModel):
    sender_email: EmailStr
    subject: str
    body: str

class DealWonWebhook(BaseModel):
    client_name: str
    project_name: str
    client_email: EmailStr
    sow_text: str
