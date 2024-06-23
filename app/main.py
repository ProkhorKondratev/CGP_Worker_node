# FastAPI приложение
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import create_tables, delete_tables
from routing import geodata_router, processing_router, info_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("База готова")
    yield
    # await delete_tables()
    # print("База очищена")


app = FastAPI(lifespan=lifespan, title="CGP-worker", version="0.1.0", docs_url=None, redoc_url=None)
app.include_router(geodata_router, prefix="/geodata", tags=["geodata"])
app.include_router(processing_router, prefix="/processing", tags=["processing"])
app.include_router(info_router, prefix="/info", tags=["info"])


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui.css",
    )


@app.get("/ping")
async def ping():
    return {"ping": "pong"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)
