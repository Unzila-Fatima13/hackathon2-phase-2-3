from sqlmodel import create_engine, Session
from typing import Generator
from core.config import settings

# Import models to ensure they are registered with SQLModel before creating engine
from models.user import User
from models.task import Task

# Create the database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # Set to True to see SQL queries in the logs
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

def get_session() -> Generator[Session, None, None]:
    """
    Dependency to get a database session
    """
    with Session(engine) as session:
        yield session