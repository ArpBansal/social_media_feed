from .db import Base
from sqlalchemy import Column, String, Boolean, Integer, TIMESTAMP, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    rating = Column(Integer)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    posted_by = relationship("Users")
    # post_rxns = relationship("Vote")

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

class Vote(Base):
  __tablename__ = 'like_dislike'
  user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
  post_id = Column(Integer, ForeignKey('posts.id', ondelete="CASCADE"), primary_key=True)
  choice = Column(Integer, CheckConstraint('vote IN (1, -1)'))
#   __table_args__=(primaryKeyConstraint(user_id, post_id))


class Comments(Base):
    __tablename__ ='comments'
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    post_id = Column(Integer, ForeignKey('posts.id', ondelete="CASCADE"))
    comment = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


# Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
# Set-ExecutionPolicy RemoteSigned
# venv\Scripts\Activate.ps1