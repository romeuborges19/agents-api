import datetime

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIResponses
from agno.tools import tool
from lmnr import Laminar

from backend.database import get_db
from backend.services.models import CarService

db = SqliteDb(db_file="tmp/agents.db")

Laminar.initialize()


@tool
def retrieve_datetime():
    """Retorna a data e hora atual"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


@tool
def retrieve_cars():
    """Retorna os carros existentes na base de dados"""
    db = get_db()
    return CarService(db=db).get_cars()


class PersonalAgent:
    def __init__(self):
        self._llm = Agent(
            model=OpenAIResponses(id="gpt-5.2"),
            db=db,
            learning=True,
            add_history_to_context=True,
            num_history_runs=3,
            tools=[retrieve_datetime],
        )

    def query(self, input: str):
        response = self._llm.run(input, user_id="romeu", session_id="123")
        return response.content


personal_agent = PersonalAgent()
