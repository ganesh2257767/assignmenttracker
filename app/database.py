from sqlmodel import Session, create_engine
from app.config import settings

DB_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_host}/{settings.database_name}"
engine = create_engine(DB_URL)

def get_session():
    with Session(engine) as session:
        yield session
