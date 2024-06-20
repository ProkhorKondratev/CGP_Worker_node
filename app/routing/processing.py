from fastapi import APIRouter, Form, UploadFile, File, Request
from app.services import Uploader, Processing
import json

router = APIRouter()


@router.post("/run")
async def run_processing(file: UploadFile = File(...), name: str = Form(...), options: str = Form({})):
    try:
        dict_options = json.loads(options)

        async def callback(files_list):
            uuid = await Processing.default_engine.run(name=name, files_list=files_list, options=dict_options)
            return {"status": "success", "uuid": uuid}

        result = await Uploader.upload_task(file, callback)
        return result

    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/tasks")
async def get_tasks():
    try:
        return await Processing.default_engine.tasks_info()
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/tasks/{uuid}")
async def get_task(uuid: str):
    try:
        return await Processing.default_engine.task_info(uuid)
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/tasks/{uuid}/cancel")
async def cancel_task(uuid: str):
    try:
        return await Processing.default_engine.cancel_task(uuid)
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/tasks/{uuid}/restart")
async def restart_task(uuid: str):
    try:
        return await Processing.default_engine.restart_task(uuid)
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/tasks/{uuid}/remove")
async def remove_task(uuid: str):
    try:
        return await Processing.default_engine.remove_task(uuid)
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/tasks/{uuid}/options")
async def get_task_options(uuid: str):
    try:
        return await Processing.default_engine.get_task_options(uuid)
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print(data)
    return data


@router.get("/options")
async def get_options():
    try:
        return await Processing.default_engine.get_options()
    except Exception as e:
        return {"status": "error", "message": str(e)}
