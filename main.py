import logging
import sys
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from warehouse.routers import router
from warehouse.core.config import settings
from warehouse.core.db import sessionmanager


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if settings.log_level == "DEBUG" else logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    """
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()


app = FastAPI(version=settings.version,title=settings.project_name,lifespan=lifespan,title=settings.project_name)


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Routers
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)