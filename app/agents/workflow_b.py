from langgraph.graph import StateGraph, END
from app.models.state import ProjectKickoffState, ClickUpTaskDefinition
from app.services.groq_service import groq_service
from app.services.clickup_service import clickup_service
from app.core.logger import logger

# --- Node Functions ---

async def extract_tasks(state: ProjectKickoffState) -> ProjectKickoffState:
    logger.info(f"Extracting tasks from SOW for {state.client_name}")
    system_prompt = (
        "You are a Technical Project Manager. "
        "Parse the provided Statement of Work (SOW) text and break it down into a structured list of actionable tasks. "
        "Return ONLY a JSON object with a key 'tasks' which is a list of objects. "
        "Each object must have 'name' (string) and 'description' (string)."
    )
    user_prompt = f"SOW Text:\n{state.sow_text}"
    
    result = await groq_service.get_json_completion(system_prompt, user_prompt)
    tasks_data = result.get("tasks", [])
    
    tasks = []
    for t in tasks_data:
        tasks.append(ClickUpTaskDefinition(name=t.get("name", "Task"), description=t.get("description", "")))
        
    state.tasks = tasks
    return state

async def create_clickup_project(state: ProjectKickoffState) -> ProjectKickoffState:
    logger.info(f"Creating ClickUp project for {state.client_name}")
    try:
        # Step 1: Find space (We'll just use the first available space for simplicity in this demo)
        spaces = await clickup_service.get_spaces()
        if not spaces:
            logger.error("No ClickUp spaces found.")
            return state
        space_id = spaces[0]["id"]
        
        # Step 2: Create Folder
        folder_res = await clickup_service.create_folder(space_id, f"Project: {state.project_name}")
        state.clickup_folder_id = folder_res.get("id")
        
        # Step 3: Create List
        list_res = await clickup_service.create_list(state.clickup_folder_id, "Sprint 1")
        state.clickup_list_id = list_res.get("id")
        
        # Step 4: Create Tasks
        task_dicts = [{"name": t.name, "description": t.description} for t in state.tasks]
        await clickup_service.create_tasks_batch(state.clickup_list_id, task_dicts)
        
        state.clickup_synced = True
    except Exception as e:
        logger.error(f"Failed to sync with ClickUp: {str(e)}")
        state.clickup_synced = False

    return state

# --- Graph Setup ---
workflow = StateGraph(ProjectKickoffState)

workflow.add_node("extract", extract_tasks)
workflow.add_node("sync_clickup", create_clickup_project)

workflow.set_entry_point("extract")
workflow.add_edge("extract", "sync_clickup")
workflow.add_edge("sync_clickup", END)

app_workflow_b = workflow.compile()
