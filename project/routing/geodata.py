from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
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


@router.post("/upload/raster")
async def upload_raster(file_path: str):
    try:
        return await GeoDataHandler.upload_raster(file_path)
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post("/upload/3dtiles")
async def upload_3dtiles(file_path: str):
    try:
        return await GeoDataHandler.upload_3d_tiles(file_path)
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


@router.get("/tiles/{uuid}/{z}/{x}/{y}")
async def get_tiles(uuid: str, z: int, x: int, y: int):
    try:
        return FileResponse(await GeoDataHandler.get_tiles(uuid, z, x, y))
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/3dtiles/{uuid}/{file:path}")
async def get_3d_tiles(uuid: str, file: str):
    try:
        return FileResponse(await GeoDataHandler.get_3d_tiles(uuid, file))
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
