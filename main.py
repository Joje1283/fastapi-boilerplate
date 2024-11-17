from fastapi import FastAPI
from core.logger import logger
from core.containers import Container

app = FastAPI()
app.container = Container()


@app.get("/")
def hello():
    logger.info("Hello World")
    return {"hello": "FastAPI"}
