import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from elasticapm.contrib.starlette import ElasticAPM

from core.config import settings
from core.database.base import create_tables
from core.logger.setup import setup_logging, apm_client
from core.security.endpoints import security
from routes.users.endpoints import users

def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(title=settings.APP_NAME)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(
        ElasticAPM,
        client=apm_client
    )

    app.include_router(users, prefix="/v1")
    app.include_router(security, prefix="/v1")

    @app.on_event("startup")
    async def startup_event():
        # Create database tables
        await create_tables()
        
    return app

def main():
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
if __name__ == "__main__":
    main()