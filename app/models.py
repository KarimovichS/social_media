from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    owner = relationship(User, backref='posts')


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(String, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    post = relationship(Post, backref='comments')
    owner = relationship(User, backref='comments')


class Like(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    post = relationship(Post, backref='likes')
    owner = relationship(User, backref='likes')
