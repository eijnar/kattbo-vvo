from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from elasticapm.contrib.starlette import ElasticAPM

from core.security import oauth2_scheme
from core.config import settings
from core.database import engine, Base
from core.logger import logger, apm_client
from routes.users.router import users

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
    logger.info('Application is starting')
    async with engine.begin() as conn:
        # Create database tables if they do not exist
        await conn.run_sync(Base.metadata.create_all)
        
app.include_router(users, prefix="/v1")