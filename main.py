from contextlib import asynccontextmanager

from fastapi import FastAPI
from core.infra.logger import logger
from core.infra.containers import Container
from core.infra.redis import redis_client
from core.interface.controller.user_controller import router as user_routers
from core.interface.controller.post_controller import router as post_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        logger.info("Shutting down...")
        await redis_client.close()


app = FastAPI(lifespan=lifespan)
app.container = Container()

app.include_router(user_routers)
app.include_router(post_routers)


@app.get("/")
def hello():
    logger.info("Hello World")
    return {"hello": "FastAPI"}
