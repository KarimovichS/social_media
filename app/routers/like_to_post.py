from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Post, Like
from app.schemas import LikeScheme, UserOutput
from app.services.oauth2 import get_current_user

router = APIRouter(prefix='/posts', tags=['posts'])


@router.post('/like', status_code=status.HTTP_201_CREATED)
def like_post(data: LikeScheme, db: Session = Depends(get_db), user: UserOutput = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == data.post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'Post does not exist')
    query = db.query(Like).filter(Like.post_id == data.post_id, Like.owner_id == user.id).first()
    if query is None:
        new_like = Like(post_id=post.id, owner_id=user.id)
        db.add(new_like)
        db.commit()
        db.refresh(new_like)
        return {"message": "success like"}
    else:
        db.delete(query)
        db.commit()
        return {"message": "success delete"}
