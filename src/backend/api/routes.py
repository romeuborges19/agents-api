from typing import Annotated

from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.ai.agents import personal_agent
from backend.api.auth import get_current_active_user
from backend.api.schemas import AgentInput, CarCreate, SessionCreate, UserSchema
from backend.database import get_db
from backend.services.ai import AIQueryService
from backend.services.models import CarService, SessionService

load_dotenv()

router = APIRouter()


@router.get("/cars")
async def get_cars(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
):
    service = CarService(db=db)
    return service.get_cars()


@router.post("/cars")
async def create_car(
    new_car: CarCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
):
    service = CarService(db=db)
    return service.create_car(new_car)


@router.get("/sessions")
async def get_sessions(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
):
    service = SessionService(db=db)
    return service.get_sessions(current_user)


@router.post("/sessions")
async def create_session(
    new_session: SessionCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
):
    service = SessionService(db=db)
    return service.create_session(current_user, new_session)


@router.post("/sessions/{session_id}/messages")
async def root(
    input: AgentInput,
    session_id: str,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
):
    service = AIQueryService(db=db, agent=personal_agent)

    response = service.query(current_user, session_id, input.input)
    return {"response": response}
