from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship
from .base_model import BaseModel, BaseQueries


class User(BaseModel):
    __tablename__ = "users"

    email = Column(String(128), unique=True, index=True)
    password = Column(String(80))
    posts = relationship("Post", back_populates="user")


class UserMethods(BaseQueries):
    model = User
