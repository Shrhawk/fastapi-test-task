from pydantic import BaseModel


class PostRequestSchema(BaseModel):
    text: str

    class Config:
        from_attributes = True


class PostResponseSchema(BaseModel):
    text: str

    class Config:
        from_attributes = True
