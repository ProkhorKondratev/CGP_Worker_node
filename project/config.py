from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    REDIS_HOST: str
    REDIS_PORT: int

    ODM_NODE_HOST: str
    ODM_NODE_PORT: int


settings = Settings()  # type: ignore
