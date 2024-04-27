from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Post, Comment
from app.schemas import UserOutput
from app.services.oauth2 import get_current_user
from app.schemas import CommitPost

router = APIRouter(prefix='/posts', tags=['posts'])


@router.post('/commit', status_code=status.HTTP_201_CREATED)
def post_commit(data: CommitPost, db: Session = Depends(get_db), user: UserOutput = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == data.post_id).first()
    if post:
        new_commit = Comment(post_id=data.post_id, owner_id=user.id, content=data.content)
        db.add(new_commit)
        db.commit()
        db.refresh(new_commit)
        return {"message": "success commit"}
    else:
        return {status.HTTP_204_NO_CONTENT}
