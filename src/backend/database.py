from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.settings import settings

engine = create_engine(settings.database_url)

session_factory = sessionmaker(engine)


async def get_db():
    db = session_factory()
    try:
        yield db
    finally:
        db.close()
