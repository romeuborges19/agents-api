from sqlalchemy.orm import Session as DBSession

from backend.ai.agents import PersonalAgent
from backend.api.schemas import (
    UserSchema,
)
from backend.models import Message, Session


class AIQueryService:
    def __init__(self, db: DBSession, agent: PersonalAgent):
        self.db = db
        self.agent = agent

    def _create_message(
        self, content: str, session: Session, user_id: int | None = None
    ):
        message = Message(user_id=user_id, session_id=session.id, content=content)
        self.db.add(message)
        self.db.flush()

    def query(self, user: UserSchema, session_id: int, input: str):
        session = Session.get_by_id(self.db, session_id)

        self._create_message(user_id=user.id, session=session, content=input)
        response = self.agent.query(input)

        self._create_message(content=response, session=session)
        self.db.commit()
        return response
