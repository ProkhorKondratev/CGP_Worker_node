from .geodata import router as geodata_router
from .processing import router as processing_router
from .info import router as info_router

__all__ = [
    "geodata_router",
    "processing_router",
    "info_router",
]
