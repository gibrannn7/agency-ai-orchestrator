from fastapi import APIRouter, Depends, BackgroundTasks, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.supabase import get_db_session
from app.models.webhooks import IncomingLeadWebhook, DealWonWebhook
from app.api.dependencies import verify_webhook_signature
from app.agents.workflow_a import app_workflow_a
from app.agents.workflow_b import app_workflow_b
from app.models.state import LeadQualificationState, ProjectKickoffState
from app.services.telegram_service import telegram_service
from app.services.brevo_service import brevo_service
from app.models.db_schemas import LeadStatus, ProjectSyncStatus
from app.core.logger import logger
from app.core.cache import cache_manager

router = APIRouter()

async def background_workflow_a(payload_dict: dict, db: AsyncSession):
    try:
        initial_state = LeadQualificationState(
            sender_email=payload_dict["sender_email"],
            subject=payload_dict["subject"],
            body=payload_dict["body"]
        )
        
        # Run LangGraph
        result = await app_workflow_a.ainvoke(initial_state.model_dump())
        final_state = LeadQualificationState(**result)
        
        # Save to DB
        lead = LeadStatus(
            sender_email=final_state.sender_email,
            subject=final_state.subject,
            classification=final_state.classification,
            budget_estimation=final_state.budget_estimation,
            is_processed=True
        )
        db.add(lead)
        await db.commit()
        
        # Action via BackgroundTasks logic
        if final_state.is_valid_lead:
            msg = f"<b>New Lead!</b>\nEmail: {final_state.sender_email}\nBudget: {final_state.budget_estimation}\n\nDraft Proposal:\n{final_state.draft_proposal}"
            await telegram_service.send_message(msg)
            
    except Exception as e:
        logger.error(f"Error in background_workflow_a: {str(e)}")

async def background_workflow_b(payload_dict: dict, db: AsyncSession):
    try:
        initial_state = ProjectKickoffState(
            client_name=payload_dict["client_name"],
            project_name=payload_dict["project_name"],
            client_email=payload_dict["client_email"],
            sow_text=payload_dict["sow_text"]
        )
        
        # Run LangGraph
        result = await app_workflow_b.ainvoke(initial_state.model_dump())
        final_state = ProjectKickoffState(**result)
        
        status = "SUCCESS" if final_state.clickup_synced else "FAILED"
        
        sync_status = ProjectSyncStatus(
            clickup_task_id=final_state.clickup_list_id, # Using list id as reference
            folder_id=final_state.clickup_folder_id,
            client_name=final_state.client_name,
            status=status
        )
        db.add(sync_status)
        await db.commit()
        
        if final_state.clickup_synced:
            html = f"<h1>Welcome, {final_state.client_name}!</h1><p>Your project is kicking off. We have set up your workspace.</p>"
            await brevo_service.send_email(final_state.client_email, final_state.client_name, "Welcome to the Agency!", html)
            
    except Exception as e:
        logger.error(f"Error in background_workflow_b: {str(e)}")


@router.post("/incoming-lead")
async def handle_incoming_lead(
    payload: IncomingLeadWebhook,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_db_session),
    _: bool = Depends(verify_webhook_signature)
):
    idempotency_key = request.headers.get("Idempotency-Key", payload.sender_email + payload.subject)
    
    # Check idempotency cache
    if await cache_manager.get(idempotency_key):
        return {"success": True, "message": "Duplicate request ignored"}
        
    await cache_manager.set(idempotency_key, True, ttl=3600)
    
    background_tasks.add_task(background_workflow_a, payload.model_dump(), db)
    return {"success": True, "message": "Lead received, processing in background"}

@router.post("/deal-won")
async def handle_deal_won(
    payload: DealWonWebhook,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_db_session),
    _: bool = Depends(verify_webhook_signature)
):
    idempotency_key = request.headers.get("Idempotency-Key", payload.client_name + payload.project_name)
    
    if await cache_manager.get(idempotency_key):
        return {"success": True, "message": "Duplicate request ignored"}
        
    await cache_manager.set(idempotency_key, True, ttl=3600)
    
    background_tasks.add_task(background_workflow_b, payload.model_dump(), db)
    return {"success": True, "message": "Deal won, project kickoff started in background"}
