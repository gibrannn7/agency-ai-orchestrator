from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logger import logger
from app.core.exceptions import global_exception_handler, orchestrator_exception_handler, OrchestratorException
from app.core.observability import init_observability
from app.api.v1.webhooks import router as webhooks_router

# Initialize Observability (LangSmith)
init_observability()

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Agency AI Orchestrator API"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handlers
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(OrchestratorException, orchestrator_exception_handler)

# Include Routers
app.include_router(webhooks_router, prefix="/api/v1/webhooks", tags=["Webhooks"])

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Agency AI Orchestrator")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Agency AI Orchestrator")

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "UP",
        "app_name": settings.APP_NAME,
        "environment": "debug" if settings.DEBUG else "production"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
