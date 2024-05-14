from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from elasticapm.contrib.starlette import ElasticAPM

from core.config import settings
from core.database import create_tables
from core.logger import apm_client
from routes.users.endpoints import users
from core.security.endpoints import security

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    ElasticAPM,
    client=apm_client
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    # Create database tables
    await create_tables()


app.include_router(users, prefix="/v1")
app.include_router(security, prefix="/v1")


