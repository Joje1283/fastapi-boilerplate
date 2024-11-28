from fastapi import FastAPI
from core.logger import logger
from core.containers import Container
from app.user.interface.controllers.user_controller import router as user_routers
from app.post.interface.controllers.post_controller import router as post_routers
from core.middlewares.session import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware)
app.container = Container()

app.include_router(user_routers)
app.include_router(post_routers)


@app.get("/")
def hello():
    logger.info("Hello World")
    return {"hello": "FastAPI"}
