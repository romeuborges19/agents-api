from sqlalchemy.orm import Session as DBSession

from backend.ai.agents import PersonalAgent
from backend.api.schemas import (
    CarDescription,
    UserSchema,
)
from backend.models import Car, Message, Session


class AIQueryService:
    def __init__(self, db: DBSession, car_id: int):
        self.db = db

        car = Car.get_by_id(self.db, car_id)

        session = car.sessions[0]
        refered_car = CarDescription.model_validate(car)
        self.agent = PersonalAgent(session_state={"car": refered_car.model_dump()})
        self.session = session

    def _create_message(
        self, content: str, session: Session, user_id: int | None = None
    ):
        message = Message(user_id=user_id, session_id=session.id, content=content)
        self.db.add(message)
        self.db.flush()

    def query(self, user: UserSchema, input: str):
        self._create_message(user_id=user.id, session=self.session, content=input)
        response = self.agent.query(input, user.id, self.session.id)

        self._create_message(content=response.response, session=self.session)
        self.db.commit()
        return response
