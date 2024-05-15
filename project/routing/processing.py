from fastapi import APIRouter, Form, UploadFile, File
from pyodm import Node
import asyncio
import os
import zipfile
import aiofiles
import aiofiles.os as aos

router = APIRouter(prefix="/processing", tags=["geodata"])


@router.get("/status")
async def get_geodata():
    return {"status": "processing"}


def extract_zip(path: str, dest: str):
    with zipfile.ZipFile(path, 'r') as zip_ref:
        for zip_info in zip_ref.infolist():
            if zip_info.is_dir():
                continue

            zip_info.filename = os.path.basename(zip_info.filename)
            zip_ref.extract(zip_info, dest)


@router.post("/run")
async def run_processing(name: str = Form(...), file: UploadFile = File(...)):
    archive_ext = (".zip", ".tar", "rar")

    if file.filename and file.filename.endswith(archive_ext):
        async with aiofiles.tempfile.TemporaryDirectory() as temp_path:
            async with aiofiles.open(os.path.join(temp_path, file.filename), 'wb') as f:
                content = await file.read()
                await f.write(content)

            await asyncio.to_thread(
                extract_zip, path=os.path.join(temp_path, file.filename), dest=os.path.join(temp_path, "extracted")
            )

            files_list = [
                os.path.join(temp_path, "extracted", f) for f in await aos.listdir(os.path.join(temp_path, "extracted"))
            ]

            print(files_list)

            node = Node("localhost", 3000)
            task = node.create_task(files_list)
            info = task.info()
            return {"status": info.status, "uuid": info.uuid, "progress": info.progress, "node": node.info()}

    return {"error": "Ошибка загрузки файла"}


@router.get("/task/{uuid}")
async def get_task(uuid: str):

    def get_task_info(uuid):
        node = Node("localhost", 3000)
        task = node.get_task(uuid)
        return task.info()

    info = await asyncio.to_thread(get_task_info, uuid)
    return {"status": info.status, "progress": info.progress}
