from typing import Annotated

from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.ai.agents import personal_agent
from backend.api.auth import get_current_active_user
from backend.api.schemas import AgentInput, UserSchema
from backend.database import get_db
from backend.services import AIQueryService

load_dotenv()

router = APIRouter()


@router.post("/")
async def root(
    input: AgentInput,
    user: Annotated[UserSchema, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
):
    service = AIQueryService(db=db, agent=personal_agent)

    response = service.query(user, input.input)
    return {"response": response}
