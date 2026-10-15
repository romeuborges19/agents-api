from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    lmnr_project_api_key: str
    database_url: str

    class Config:
        env_file = ".env"


settings = Settings()
