from openai import BaseModel


class AgentInput(BaseModel):
    input: str
