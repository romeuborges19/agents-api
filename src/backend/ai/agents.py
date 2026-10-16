import datetime

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIResponses
from agno.run import RunContext
from agno.tools import tool
from lmnr import Laminar

from backend.database import session_factory
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
    db = session_factory()
    cars = CarService(db=db).get_cars()
    cars = [c.model_dump() for c in cars]
    db.close()
    return cars


def get_instructions(run_context: RunContext):
    if not run_context.session_state:
        run_context.session_state = {}

    if car := run_context.session_state.get("car"):
        return (
            f"You may talk only about this car: {car}. "
            "If the user requests other subject, don't do it. "
            "Make sure that you only talk about the refered car (i.e., the object in this instruction)."
        )

    return "Make clear to the user that you are not talking about any car in specific."


class PersonalAgent:
    def __init__(self, session_state: dict):
        self._llm = Agent(
            model=OpenAIResponses(id="gpt-5.2"),
            db=db,
            learning=True,
            add_history_to_context=True,
            num_history_runs=3,
            tools=[retrieve_datetime, retrieve_cars],
            session_state=session_state,
            instructions=get_instructions,
        )

    def query(self, input: str, user_id: int, session_id: int):
        response = self._llm.run(
            input, user_id=str(user_id), session_id=str(session_id)
        )
        return response.content
