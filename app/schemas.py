from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOutput(BaseModel):
    id: int
    email: EmailStr
    created: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class PostCreate(BaseModel):
    title: str
    content: str


class PostOutput(PostCreate):
    id: int
    created: datetime
    owner: UserOutput


class UpdatePost(BaseModel):
    title: str
    content: str
    update_title: str
    update_content: str

    class Config:
        orm_mode = True


class DeletePost(BaseModel):
    title: str


class LikeScheme(BaseModel):
    post_id: int


class CommitPost(BaseModel):
    post_id: int
    content: str


class LikeOutput(BaseModel):
    id: int
    post_id: int
    created: datetime


class CommentOutput(BaseModel):
    id: int
    content: str
    created: datetime


class PostOutputAll(BaseModel):
    id: int
    title: str
    content: str
    created: datetime
    comments: list[CommentOutput]
    like: list[LikeOutput]


class FollowerOutput(BaseModel):
    id: int
    user: UserOutput


class RequestOutput(BaseModel):
    id: int
    user: UserOutput


class DoFollow(BaseModel):
    user_id: int


class AccRejReq(BaseModel):
    request_id: int
    is_accept: bool


class AllFriendSchemeFollower(BaseModel):
    id: int
    follower: UserOutput
    is_following: bool


class AllFriendSchemeFollowing(BaseModel):
    id: int
    following: UserOutput
    is_following: bool


class RoomCreate(BaseModel):
    name: str


class RoomOutput(RoomCreate):
    id: int
    created: datetime
