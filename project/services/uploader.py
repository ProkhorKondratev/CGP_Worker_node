from fastapi import UploadFile
from typing import Callable
import aiofiles
import aiofiles.os as aos
import os
import asyncio
import zipfile
import geopandas as gpd


def extract_zip(path: str, dest: str):
    with zipfile.ZipFile(path, 'r') as zip_ref:
        for zip_info in zip_ref.infolist():
            if zip_info.is_dir():
                continue

            zip_info.filename = os.path.basename(zip_info.filename)
            zip_ref.extract(zip_info, dest)


class Uploader:
    @staticmethod
    async def upload_task(file: UploadFile, callback: Callable):
        archive_ext = (".zip",)

        if file.filename and file.filename.endswith(archive_ext):
            print(f"Загрузка файла {file.filename}")
            async with aiofiles.tempfile.TemporaryDirectory() as temp_path:
                archive_path = os.path.join(temp_path, file.filename)

                async with aiofiles.open(archive_path, 'wb') as f:
                    content = await file.read()
                    await f.write(content)

                dest_path = os.path.join(temp_path, "extracted")
                await asyncio.to_thread(extract_zip, path=archive_path, dest=dest_path)

                files_list = [os.path.join(dest_path, f) for f in await aos.listdir(dest_path)]
                return await callback(files_list)

    @staticmethod
    async def upload_vector_data(upload_files: list[UploadFile], callback: Callable):
        vector_ext = (".shp", ".geojson", ".gpkg")
        async with aiofiles.tempfile.TemporaryDirectory() as temp_path:
            for upload_file in upload_files:
                if upload_file.filename:
                    file_path = os.path.join(temp_path, upload_file.filename)
                    async with aiofiles.open(file_path, 'wb') as f:
                        content = await upload_file.read()
                        await f.write(content)

            geometry_frames = []
            for file in await aos.listdir(temp_path):
                if file.endswith(vector_ext):
                    geom = gpd.read_file(os.path.join(temp_path, file))  # type: gpd.GeoDataFrame
                    geom = geom.to_crs("EPSG:4326")
                    geometry_frames.append(geom)

            return await callback(geometry_frames)

    @staticmethod
    async def upload_vector_geometry(geometry: dict, callback: Callable):
        frame = gpd.GeoDataFrame.from_features(geometry)
        return await callback([frame])

    @staticmethod
    async def apply_vector_data(files: list[str], callback: Callable):
        geometry_frames = []
        for file in files:
            if await aos.path.exists(file):
                geom = gpd.read_file(file)
                geom = geom.to_crs("EPSG:4326")
                geometry_frames.append(geom)

        return await callback(geometry_frames)
