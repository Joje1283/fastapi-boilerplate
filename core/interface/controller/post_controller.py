from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from core.application.service.post_service import PostCommandService, PostQueryService
from core.application.dto.post import PostCommand, PostsQuery
from common.models import CurrentUser
from core.infra.containers import Container
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
    post_service: PostCommandService = Depends(Provide[Container.post_command_service]),
):
    post_command = PostCommand(
        title=body.title,
        contents=body.contents,
        tags=body.tags,
        author_id=current_user.id,
    )
    await post_service.create_post(post_command=post_command)


@router.put("/{post_id}")
@inject
async def update_post(
    post_id: str,
    body: CreatePostBody,
    current_user: CurrentUser = Depends(get_current_user),
    post_service: PostCommandService = Depends(Provide[Container.post_command_service]),
):
    post_command = PostCommand(
        title=body.title,
        contents=body.contents,
        tags=body.tags,
        author_id=current_user.id,
    )
    return await post_service.update_post(post_id=post_id, post_command=post_command)


@router.get("/{post_id}")
@inject
async def get_post(
    post_id: str,
    post_service: PostQueryService = Depends(Provide[Container.post_query_service]),
):
    return await post_service.get_post(post_id=post_id)


@router.get("")
@inject
async def get_posts(
    limit: int = 10,
    offset: int = 0,
    post_service: PostQueryService = Depends(Provide[Container.post_query_service]),
):
    return await post_service.get_posts(
        posts_query=PostsQuery(
            limit=limit,
            offset=offset,
            tags=None,
            author_id=None,
        )
    )
