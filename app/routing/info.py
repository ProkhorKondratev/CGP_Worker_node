from fastapi import APIRouter
from services import AppHandler
router = APIRouter()


@router.get("")
async def get_info():
    return await AppHandler.get_node_info()
