from dotenv import load_dotenv

from backend.agents import personal_agent
from backend.api.schemas import AgentInput
from backend.setup import app

load_dotenv()


@app.post("/")
async def root(input: AgentInput):
    response = personal_agent.query(input.input)
    return {"response": response}
