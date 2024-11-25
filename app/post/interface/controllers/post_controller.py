from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.post.application.post_service import PostService
from app.post.application.schema.post import PostCommand
from common.models import CurrentUser
from core.containers import Container
from core.dependencies.auth import get_current_user

router = APIRouter(prefix="/posts", tags=["posts"])


class CreatePostBody(BaseModel):
    title: str
    contents: str
    tags: list[str]


@router.post("", status_code=201)
@inject
async def create_post(
    body: CreatePostBody,
    current_user: CurrentUser = Depends(get_current_user),
    post_service: PostService = Depends(Provide[Container.post_service]),
):
    post_command = PostCommand(
        title=body.title,
        contents=body.contents,
        tags=body.tags,
        author_id=current_user.id,
    )
    await post_service.create_post(post_command=post_command)
