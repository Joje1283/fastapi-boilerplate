from fastapi import FastAPI
from core.logger import logger
from core.containers import Container
from app.user.interface.controllers.user_controller import router as user_routers

app = FastAPI()
app.container = Container()
app.include_router(user_routers)


@app.get("/")
def hello():
    logger.info("Hello World")
    return {"hello": "FastAPI"}
