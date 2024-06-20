from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

postgres_host = settings.POSTGRES_HOST
postgres_port = settings.POSTGRES_PORT


if settings.DEBUG:
    postgres_host = "localhost"
    postgres_port = settings.POSTGRES_PORT

conn_string = (
    f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{postgres_host}:{postgres_port}/{settings.POSTGRES_DB}"
)

print("=" * 25)
print("УСТАНОВКА ПОДКЛЮЧЕНИЯ К БАЗЕ ДАННЫХ")
print(conn_string)
print("=" * 25)

async_engine = create_async_engine(conn_string, echo=settings.DEBUG)
new_session = async_sessionmaker(async_engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
