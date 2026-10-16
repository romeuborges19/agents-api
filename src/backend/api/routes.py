from typing import Annotated

from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

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


@router.post("/cars/{car_id}/sessions")
async def create_session(
    car_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
):
    service = SessionService(db=db)
    return service.create_session(current_user, car_id)


@router.get("/cars/{car_id}/messages")
async def retrieve_messages(
    car_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
):
    service = SessionService(db=db)
    return service.retrieve_messages(car_id)


@router.post("/cars/{car_id}/messages")
async def create_message(
    input: AgentInput,
    car_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
):
    service = AIQueryService(db=db, car_id=car_id)

    return service.query(current_user, input.input)
