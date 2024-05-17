from fastapi import APIRouter, UploadFile, File
from geopandas import GeoDataFrame
from services import Uploader, GeoDataHandler

router = APIRouter()


@router.post("/upload/vector")
async def upload_vectors(files: list[UploadFile] = File(...)):
    try:

        async def callback(geometry_frames: list[GeoDataFrame]):
            result = await GeoDataHandler.upload_vector(geometry_frames)
            return {"status": "success", "result": result}

        return await Uploader.upload_vector_data(files, callback)
    except Exception as e:
        return {"status": "error", "message": str(e)}


# загружаем через переданный geojson c помощью метода POST
@router.post("/upload/vector/geometry")
async def upload_vectors_geometry(geometry: dict):
    try:

        async def callback(geometry_frames: list[GeoDataFrame]):
            result = await GeoDataHandler.upload_vector(geometry_frames)
            return {"status": "success", "result": result}

        return await Uploader.upload_vector_geometry(geometry, callback)
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/vector")
async def get_vectors():
    try:
        return await GeoDataHandler.get_vector()
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/vector/{uuid}")
async def get_vector(uuid: str):
    try:
        return await GeoDataHandler.get_vector(uuid)
    except Exception as e:
        return {"status": "error", "message": str(e)}
