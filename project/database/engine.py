from .tables import Table
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


engine = create_async_engine("postgresql+asyncpg://cgp-worker:123456@localhost:5434/cgp", echo=True)
new_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Table.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Table.metadata.drop_all)
