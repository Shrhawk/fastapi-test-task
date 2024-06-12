from fastapi import Depends, FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from starlette.responses import JSONResponse

from common.authentication import get_current_user
from common.constants import PAYLOAD_SIZE_EXCEEDED
from common.metadata import tags_metadata
from routes.posts import post_router
from routes.user import user_router

app = FastAPI(
    title="FastAPI Test Task",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs/swagger",
    redoc_url="/docs/redoc",
    openapi_tags=tags_metadata,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def validate_payload_size(request: Request, call_next):
    """
    Validate payload size.

    Args:
        request: Request object.
        call_next: callback function that receives the request and returns the response object.

    Returns:
        The response object.
    """
    if request.method == "POST":
        content_length = request.headers.get('Content-Length')
        if content_length and int(content_length) > (1024 * 1024):
            return JSONResponse(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                content={"detail": PAYLOAD_SIZE_EXCEEDED}
            )
    response = await call_next(request)
    return response


@app.get("/ping", tags=["Health"])
async def health() -> ORJSONResponse:
    """
    Health Check
    """
    return ORJSONResponse(status_code=status.HTTP_200_OK, content={"message": "pong"})


PROTECTED = [Depends(get_current_user)]

app.include_router(user_router, prefix="/api/v1", tags=["User"])
app.include_router(
    post_router, prefix="/api/v1", tags=["Post"], dependencies=PROTECTED
)
