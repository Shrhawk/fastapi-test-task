from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base_model import BaseModel, BaseQueries


class Post(BaseModel):
    __tablename__ = "posts"

    text = Column(Text, nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"))
    user = relationship("User", back_populates="posts")


class PostMethods(BaseQueries):
    model = Post
