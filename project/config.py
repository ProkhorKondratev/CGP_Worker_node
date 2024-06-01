from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5434

    REDIS_HOST: str
    REDIS_PORT: int

    ODM_NODE_HOST: str = "localhost"
    ODM_NODE_PORT: int = 3000


settings = Settings()  # type: ignore
