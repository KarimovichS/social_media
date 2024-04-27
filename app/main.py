from fastapi import FastAPI
from app.routers.user import router as user_router
from app.routers.auth import router as auth_router
from app.routers.post import router as post_router
from app.routers.like_to_post import router as like_router
from app.routers.post_commit import router as post_comment_router
from app.routers.follower import router as follower_router
from app.routers.chat import router as chat_router
from app.routers.Files import router as upload_router
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello world"}


app.include_router(user_router)
app.include_router(auth_router)
app.include_router(post_router)
app.include_router(like_router)
app.include_router(post_comment_router)
app.include_router(follower_router)
app.include_router(chat_router)
app.include_router(upload_router)
