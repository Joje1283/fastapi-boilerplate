from fastapi import FastAPI
from core.infra.logger import logger
from core.infra.containers import Container
from core.interface.controller.user_controller import router as user_routers
from core.interface.controller.post_controller import router as post_routers

app = FastAPI()
app.container = Container()

app.include_router(user_routers)
app.include_router(post_routers)


@app.get("/")
def hello():
    logger.info("Hello World")
    return {"hello": "FastAPI"}
