from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App Config
    APP_NAME: str = "agency-ai-orchestrator"
    DEBUG: bool = False
    
    # API Keys
    GROQ_API_KEY: str
    CLICKUP_API_TOKEN: str
    CLICKUP_TEAM_ID: str
    BREVO_API_KEY: str
    SENDER_EMAIL: str
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_CHAT_ID: str
    
    # LangSmith
    LANGCHAIN_TRACING_V2: str = "true"
    LANGCHAIN_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGCHAIN_API_KEY: str
    LANGCHAIN_PROJECT: str
    
    # Database
    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE_KEY: str
    SUPABASE_DB_URL: str
    PASSWORD_SUPABASE: str
    PROJECT_ID: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
