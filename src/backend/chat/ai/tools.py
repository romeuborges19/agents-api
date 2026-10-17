import datetime

from agno.tools import tool

from backend.chat import service
from backend.core.database import session_factory


@tool
def retrieve_datetime():
    """Retorna a data e hora atual"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


@tool
def retrieve_cars():
    """Retorna os carros existentes na base de dados e se já existe uma sessão vinculada a eles."""
    db = session_factory()
    cars = service.get_cars(db)
    cars = [c.model_dump() for c in cars]
    db.close()
    return cars
