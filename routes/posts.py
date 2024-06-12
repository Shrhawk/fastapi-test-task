from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Response
from fastapi.responses import ORJSONResponse
from sqlalchemy.orm import Session
from cachetools import TTLCache, cached

from common.authentication import get_current_user
from common.constants import NO_DATA_FOUND
from database.db import get_db
from models.post import PostMethods
from models.user import User
from schemas.post_schema import PostRequestSchema, PostResponseSchema

post_router = APIRouter(
    prefix="/post",
    responses={404: {"description": "Not found"}},
)
cache = TTLCache(maxsize=100, ttl=300)


@post_router.post("/")
async def create_post(
    post: PostRequestSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ORJSONResponse:
    """
    Create Post.

    Args:
        post: PostRequestSchema
        current_user: User
        db: Session

    Returns:
        ORJSONResponse
    """
    post_data = {
        "user_id": current_user.id,
        "text": post.text,
    }
    new_post = PostMethods.create_record(post_data, db)
    db.commit()

    return ORJSONResponse(
        status_code=status.HTTP_200_OK, content={"post_id": new_post.id}
    )


@post_router.get("/get-posts/", response_model=List[PostResponseSchema])
async def get_user_posts(
    response: Response,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[PostResponseSchema]:
    """
    Get all posts by user_id.

    Args:
        response: Response
        current_user: User
        db: Session

    Returns:
        ORJSONResponse
    """
    cache_key = f"user_posts_{current_user.id}"

    if cache_key in cache:
        return cache[cache_key]
    posts = PostMethods.get_all_record_with_(db, user_id=current_user.id)

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NO_DATA_FOUND)

    cache[cache_key] = posts

    return posts
