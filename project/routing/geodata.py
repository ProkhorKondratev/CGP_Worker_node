from fastapi import APIRouter

router = APIRouter(prefix="/geodata", tags=["geodata"])

@router.get("/")
async def get_geodata():
    return {"data": "geodata"}
