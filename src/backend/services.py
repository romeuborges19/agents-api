from sqlalchemy.orm import Session as DBSession

from backend.ai.agents import PersonalAgent
from backend.api.schemas import (
    CarCreate,
    CarSchema,
    SessionCreate,
    SessionSchema,
    UserSchema,
)
from backend.models import Car, Message, Session


class CarService:
    def __init__(self, db: DBSession):
        self.db = db

    def get_cars(self) -> list[CarSchema]:
        cars = Car.get_cars(self.db)
        return [CarSchema.model_validate(c) for c in cars]

    def create_car(self, new_car: CarCreate) -> CarSchema:
        car_obj = Car(name=new_car.name, description=new_car.description)
        self.db.add(car_obj)
        self.db.commit()
        return CarSchema.model_validate(car_obj)


class SessionService:
    def __init__(self, db: DBSession):
        self.db = db

    def get_sessions(self, user: UserSchema) -> list[SessionSchema]:
        sessions = Session.get_sessions(self.db, user)
        return [SessionSchema.model_validate(s) for s in sessions]

    def create_session(
        self, user: UserSchema, new_session: SessionCreate
    ) -> SessionSchema:
        session_obj = Session(subject=new_session.subject, user_id=user.id)
        self.db.add(session_obj)
        self.db.commit()
        return SessionSchema.model_validate(session_obj)


class AIQueryService:
    def __init__(self, db: DBSession, agent: PersonalAgent):
        self.db = db
        self.agent = agent

    def _create_message(
        self, content: str, session: Session, user_id: int | None = None
    ):
        message = Message(user_id=user_id, content=content)
        self.db.add(message)
        self.db.flush()

    def query(self, user: UserSchema, session_id: int, input: str):
        session = Session.get_by_id(session_id)

        self._create_message(user_id=user.id, session=session, content=input)
        response = self.agent.query(input)

        self._create_message(content=response, session=session)
        self.db.commit()
        return response
