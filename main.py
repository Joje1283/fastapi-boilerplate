from fastapi import FastAPI, Request

from common.models import CurrentUser
from core.logger import logger
from core.containers import Container
from app.user.interface.controllers.user_controller import router as user_routers
from app.post.interface.controllers.post_controller import router as post_routers
from common.context_vars import user_context
from core.middlewares.session import SessionMiddleware
from utils.jwt_utils import decode_access_token

app = FastAPI()
app.add_middleware(SessionMiddleware)
app.container = Container()


@app.middleware("http")
async def get_current_user_middleware(request: Request, call_next):
    authorization = request.headers.get("Authorization")
    if authorization:
        splits = authorization.split(" ")
        if splits[0] == "Bearer":
            token = splits[1]
            payload = decode_access_token(token)
            user_id = payload.get("user_id")
            user_role = payload.get("role")
            # 컨텍스트에 사용자 정보 설정
            user_context.set(CurrentUser(id=user_id, role=user_role))
    logger.info(f"Request URL: {request.url}")
    response = await call_next(request)
    return response


app.include_router(user_routers)
app.include_router(post_routers)


@app.get("/")
def hello():
    logger.info("Hello World")
    return {"hello": "FastAPI"}
