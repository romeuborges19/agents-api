from agno.models.message import Message
from dotenv import load_dotenv
from lmnr import evaluate
from lmnr.sdk.types import Datapoint

from backend.ai.agents import personal_agent

load_dotenv()


def accuracy(output: str, target: str):
    return 1 if target.lower() in output.lower() else 0


evaluate(
    data=[
        Datapoint(
            data=Message(content="Qual a capital da França?", role="user"),
            target="Paris",
        ),
        Datapoint(
            data=Message(content="Qual a capital da Tailândia?", role="user"),
            target="Bangkok",
        ),
        Datapoint(
            data=Message(content="Qual a capital da Rússia?", role="user"),
            target="Moscou",
        ),
        Datapoint(
            data=Message(content="Qual a capital do Brasil?", role="user"),
            target="Brasília",
        ),
    ],
    executor=personal_agent.query,
    evaluators={"accuracy": accuracy},
    name="Teste capitais v1 (gpt-5.2)",
    group_name="capitais",
)
