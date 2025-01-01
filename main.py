from fastapi import FastAPI
from common.logger import logger
from common.containers import Container
from app.user.interface.controllers.user_controller import router as user_routers
from app.post.interface.controllers.post_controller import router as post_routers

app = FastAPI()
app.container = Container()

app.include_router(user_routers)
app.include_router(post_routers)


@app.get("/")
def hello():
    logger.info("Hello World")
    return {"hello": "FastAPI"}
