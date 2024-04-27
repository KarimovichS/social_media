from http.client import HTTPException
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from typing import List
from app.database import get_db
from app.models import User, Post, Comment
from app.schemas import PostCreate, PostOutput, UserOutput, UpdatePost, DeletePost, CommentOutput, PostOutputAll
from app.services.oauth2 import get_current_user
from app.utils import verify

router = APIRouter(prefix='/posts', tags=['posts'])


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=PostOutput)
def post_create(data: PostCreate, db: Session = Depends(get_db), user: UserOutput = Depends(get_current_user)):
    print(data, '-----', user)
    new_post = Post(**data.dict(), owner_id=user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/get', status_code=status.HTTP_200_OK, response_model=List[PostOutput])
def post_get(db: Session = Depends(get_db), user: UserOutput = Depends(get_current_user)):
    posts = db.query(Post).filter(Post.owner_id == user.id).all()
    return posts


@router.put('/update', status_code=status.HTTP_200_OK, response_model=PostOutput)
def post_update(data: UpdatePost, db: Session = Depends(get_db), user: UserOutput = Depends(get_current_user)):
    post = db.query(Post).filter(Post.owner_id == user.id).filter(Post.title == data.title).first()
    if post:
        post.title = data.update_title
        post.content = data.update_content
        db.add(post)
        db.commit()
        db.refresh(post)
        return post
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@router.delete('/delete', status_code=status.HTTP_200_OK)
def delete_post(data: DeletePost, db: Session = Depends(get_db), user: UserOutput = Depends(get_current_user)):
    post = db.query(Post).filter(Post.owner_id == user.id).filter(Post.title == data.title).first()
    if post:
        db.delete(post)
        db.commit()
        return {"detail": "Post deleted successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@router.get('/all', status_code=200, response_model=list[PostOutputAll])
def post_get_all(db: Depends = Depends(get_db)):
    post = db.query(Post).all()
    return post
