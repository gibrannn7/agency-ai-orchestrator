from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings

# Since we use Alembic with SQLAlchemy, we connect to the database via SQLAlchemy
# We use pgbouncer pooler for the application with prepared_statement_cache_size=0
engine = create_async_engine(
    f"{settings.SUPABASE_DB_URL}?prepared_statement_cache_size=0",
    echo=settings.DEBUG,
)

async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def get_db_session():
    async with async_session_maker() as session:
        yield session
