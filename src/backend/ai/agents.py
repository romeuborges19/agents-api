import datetime

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIResponses
from agno.run import RunContext
from agno.tools import tool
from lmnr import Laminar
from pydantic import BaseModel, Field

from backend.api.schemas import CarSchema, CarWithSession
from backend.database import session_factory
from backend.services.models import CarService

db = SqliteDb(db_file="tmp/agents.db")

Laminar.initialize()


class CarAgentResponse(BaseModel):
    response: str = Field(description="The response")
    next_car: CarWithSession | None = Field(
        description="The car for the next subject. None if there's no subject change."
    )


@tool
def retrieve_datetime():
    """Retorna a data e hora atual"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


@tool
def retrieve_cars():
    """Retorna os carros existentes na base de dados e se já existe uma sessão vinculada a eles."""
    db = session_factory()
    cars = CarService(db=db).get_cars()
    cars = [c.model_dump() for c in cars]
    db.close()
    return cars


def get_instructions(run_context: RunContext):
    if not run_context.session_state:
        run_context.session_state = {}

    car_instruction = (
        "Make clear to the user that you are not talking about any car in specific."
    )
    if car := run_context.session_state.get("car"):
        car_instruction = (
            f"You may talk only about this car: {car}. "
            "Make sure that you only talk about the refered car (i.e., the object in this instruction). "
            "If you notice that the user wants to change subject, "
            "check if this car exists (`retrieve_cars` tool). If so, "
            "suggest the user to change to it through the field `next_car`. "
            "The user can create a new session about the car, if there ain't any. "
            "If one exists, suggest the user to go to it."
        )

    return car_instruction


class PersonalAgent:
    def __init__(self, session_state: dict):
        self._llm = Agent(
            model=OpenAIResponses(id="gpt-5.2"),
            db=db,
            learning=True,
            num_history_runs=3,
            tools=[retrieve_datetime, retrieve_cars],
            session_state=session_state,
            instructions=get_instructions,
            output_schema=CarAgentResponse,
        )

    def query(self, input: str, user_id: int, session_id: int) -> CarAgentResponse:
        response = self._llm.run(
            input, user_id=str(user_id), session_id=str(session_id)
        )
        return response.content
