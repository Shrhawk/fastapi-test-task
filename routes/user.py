import uuid

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.orm import Session

from common.authentication import (
    authenticate_user,
    create_access_token,
    get_password_hash,
)
from common.constants import (
    EMAIL_EXISTS,
    USER_CREATED,
    WRONG_CREDENTIALS,
)
from database.db import get_db
from models.user import UserMethods
from schemas.users_schema import (
    UserRequestLoginSchema,
    UserRequestSchema,
)

user_router = APIRouter(
    prefix="/users",
    responses={404: {"description": "Not found"}},
)


@user_router.post("/create")
async def create_user(
    user: UserRequestSchema, db: Session = Depends(get_db)
) -> ORJSONResponse:
    """
    Sign up as new User.

    Args:
        user: UserRequestSchema
        db: Session

    Returns:
        User
    """
    user_check = UserMethods.get_record_with_(db, email=user.email)
    if user_check:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=EMAIL_EXISTS
        )
    user_data = user.model_dump()
    user_data["id"] = str(uuid.uuid4())
    user_data["password"] = get_password_hash(user.password.get_secret_value())
    UserMethods.create_record(user_data, db)
    db.commit()

    return ORJSONResponse(
        content={"message": USER_CREATED, "user_id": user_data["id"]},
        status_code=status.HTTP_201_CREATED
    )


@user_router.post("/login")
async def login_user(
    user: UserRequestLoginSchema, db: Session = Depends(get_db)
) -> ORJSONResponse:
    """
    Login user if the provided creds are correct.

    Args:
        user: UserRequestLoginSchema
        db: Session

    Returns:
        Dict
    """
    user_data = await authenticate_user(
        email=user.email, password=user.password.get_secret_value(), db=db
    )
    if not user_data:
        raise HTTPException(detail=WRONG_CREDENTIALS, status_code=400)
    access_token = create_access_token(
        data={
            "id": user_data.id,
            "email": user_data.email,
        }
    )
    token_data = {
        "status": "success",
        "access_token": access_token,
        "token_type": "bearer",
    }
    return ORJSONResponse(
        content={"data": token_data},
        status_code=status.HTTP_200_OK
    )
