from sqlalchemy.orm import Session

from backend.ai.agents import PersonalAgent
from backend.api.schemas import UserSchema


class AIQueryService:
    def __init__(self, db: Session, agent: PersonalAgent):
        self.db = db
        self.agent = agent

    def query(self, user: UserSchema, input: str):
        return self.agent.query(input)
