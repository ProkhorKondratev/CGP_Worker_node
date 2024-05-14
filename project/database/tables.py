from datetime import datetime
from datetime import timezone
from sqlalchemy import Column, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
from uuid import uuid4


class Table(DeclarativeBase):
    id: Mapped[str] = mapped_column(UUID, primary_key=True, index=True, unique=True, nullable=False, default=uuid4)
    name: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(onupdate=datetime.now(timezone.utc))


class VectorData(Table):
    __tablename__ = 'vector_data'

    name: Mapped[str] = mapped_column(nullable=True)
    style: Mapped[dict] = mapped_column(JSON, nullable=True)
    geom = Column(Geometry(geometry_type="GEOMETRY", srid=4326))


class RasterData(Table):
    __tablename__ = 'raster_data'

    coverage = Column(Geometry(geometry_type="POLYGON", srid=4326))


class ThreeDimData(Table):
    __tablename__ = 'three_dim_data'

    coverage = Column(Geometry(geometry_type="POLYGON", srid=4326))
