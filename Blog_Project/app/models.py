from .database import Base
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))

    posts = relationship("Post", back_populates="owner", cascade="all, delete")
    # python link : User.posts -> list of Post

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index = True)
    title = Column(String, nullable=False, index = True)
    content = Column(Text, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default = lambda : datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default = lambda : datetime.datetime.now(datetime.timezone.utc), onupdate=lambda : datetime.datetime.now(datetime.timezone.utc))

    owner = relationship("User", back_populates="posts")
    # python link : post.owner -> User

