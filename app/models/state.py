from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class LeadQualificationState(BaseModel):
    # Input
    sender_email: str
    subject: str
    body: str
    
    # Internal state populated by LLM
    classification: Optional[str] = None  # 'LEAD', 'SPAM', 'SUPPORT', 'IGNORE'
    budget_estimation: Optional[float] = None
    project_complexity: Optional[str] = None
    draft_proposal: Optional[str] = None
    
    # Flags
    is_valid_lead: bool = False

class ClickUpTaskDefinition(BaseModel):
    name: str
    description: str

class ProjectKickoffState(BaseModel):
    # Input
    client_name: str
    project_name: str
    client_email: str
    sow_text: str
    
    # Internal state
    tasks: List[ClickUpTaskDefinition] = Field(default_factory=list)
    clickup_folder_id: Optional[str] = None
    clickup_list_id: Optional[str] = None
    
    # Status
    clickup_synced: bool = False
    email_sent: bool = False
