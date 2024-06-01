from datetime import datetime
from datetime import timezone
from sqlalchemy import Column, JSON, select, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
from uuid import uuid4
from .engine import Base, new_session


class Table(Base):
    __abstract__ = True

    uuid: Mapped[str] = mapped_column(
        UUID,
        primary_key=True,
        index=True,
        unique=True,
        nullable=False,
        default=uuid4,
    )
    name: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    async def save(self):
        async with new_session() as session:
            session.add(self)
            await session.commit()

    async def delete(self):
        async with new_session() as session:
            session.delete(self)
            await session.commit()

    @classmethod
    async def get(cls, uuid: str):
        async with new_session() as session:
            return await session.get(cls, uuid)

    @classmethod
    async def all(cls):
        async with new_session() as session:
            result = await session.execute(select(cls))
            return result.scalars().all()


class VectorData(Table):
    __tablename__ = 'vector_data'

    style: Mapped[dict] = mapped_column(JSON, nullable=True)
    geom = Column(Geometry(geometry_type="GEOMETRYZ", srid=4326))
    attributes: Mapped[dict] = mapped_column(JSON, nullable=True)


class RasterData(Table):
    __tablename__ = 'raster_data'

    path: Mapped[str] = mapped_column(nullable=True)
    properties: Mapped[dict] = mapped_column(JSON, nullable=True)
    coverage = Column(Geometry(geometry_type="POLYGON", srid=4326))


class ThreeDimData(Table):
    __tablename__ = 'three_dim_data'

    path: Mapped[str] = mapped_column(nullable=True)
    coverage = Column(Geometry(geometry_type="POLYGON", srid=4326))


class ProcessingTask(Table):
    __tablename__ = 'processing_tasks'
