from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    lmnr_project_api_key: str
    database_url: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
