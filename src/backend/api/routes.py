from typing import Annotated

from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.agents import personal_agent
from backend.api.schemas import AgentInput
from backend.database import get_db

load_dotenv()

router = APIRouter()


@router.post("/")
async def root(input: AgentInput, db: Annotated[Session, Depends(get_db)]):
    response = personal_agent.query(input.input)
    return {"response": response}
