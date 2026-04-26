from langgraph.graph import StateGraph, END
from app.models.state import LeadQualificationState
from app.services.groq_service import groq_service
from app.core.logger import logger

# --- Node Functions ---

async def classify_and_extract_budget(state: LeadQualificationState) -> LeadQualificationState:
    logger.info(f"Classifying email from {state.sender_email}")
    system_prompt = (
        "You are an AI assistant for a digital agency. "
        "Classify the following email into one of these categories: 'LEAD', 'SPAM', 'SUPPORT', 'IGNORE'. "
        "If it is a LEAD, also estimate the budget as a number (e.g., 5000) and describe the project_complexity. "
        "Return ONLY a JSON object with keys: classification (string), budget_estimation (number or null), "
        "project_complexity (string or null). No other text."
    )
    user_prompt = f"Subject: {state.subject}\nBody:\n{state.body}"
    
    result = await groq_service.get_json_completion(system_prompt, user_prompt)
    
    state.classification = result.get("classification", "IGNORE")
    state.budget_estimation = result.get("budget_estimation")
    state.project_complexity = result.get("project_complexity")
    
    if state.classification == "LEAD":
        state.is_valid_lead = True
    else:
        state.is_valid_lead = False
        
    return state

async def generate_draft_proposal(state: LeadQualificationState) -> LeadQualificationState:
    if not state.is_valid_lead:
        return state
        
    logger.info(f"Generating draft proposal for {state.sender_email}")
    system_prompt = (
        "You are an expert sales representative for a digital agency. "
        "Based on the email, generate a draft proposal including a greeting, an understanding of the project, "
        "an Estimated Timeline based on the project complexity, and next steps. "
        "Return ONLY a JSON object with key: draft_proposal (string). No other text."
    )
    user_prompt = (
        f"Email:\n{state.body}\n\n"
        f"Complexity: {state.project_complexity}\n"
        f"Budget: {state.budget_estimation}"
    )
    
    result = await groq_service.get_json_completion(system_prompt, user_prompt)
    state.draft_proposal = result.get("draft_proposal")
    
    return state

def route_classification(state: LeadQualificationState) -> str:
    if state.is_valid_lead:
        return "generate_proposal"
    return END

# --- Graph Setup ---
workflow = StateGraph(LeadQualificationState)

workflow.add_node("classify", classify_and_extract_budget)
workflow.add_node("generate_proposal", generate_draft_proposal)

workflow.set_entry_point("classify")
workflow.add_conditional_edges(
    "classify",
    route_classification,
    {
        "generate_proposal": "generate_proposal",
        END: END
    }
)
workflow.add_edge("generate_proposal", END)

app_workflow_a = workflow.compile()
