from fastapi import FastAPI, Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.database import get_db
from app.models import User, Room, Message
from app.routers.websocket_manager import ConnectionManager
from app.schemas import RoomCreate, RoomOutput
from app.services.oauth2 import get_current_user, verify_access_token
import logging

logger = logging.getLogger("uvicorn")
router = APIRouter(prefix="/chat", tags=["chat"])

manager = ConnectionManager()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=RoomOutput)
def create_room(room: RoomCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_room = Room(name=room.name)
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room


@router.post("/room-create-private/{user_id}", response_model=RoomOutput)
def create_room_private(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    room = db.query(Room).filter(
        or_(Room.name == f"{user_id}_{current_user.id}", Room.name == f"{current_user.id}_{user_id}")).first()
    if room:
        return room
    new_room = Room(name=f"{user_id}_{current_user.id}")
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room


@router.get("/room-list", response_model=list[RoomOutput])
def get_rooms(db: Session = Depends(get_db)):
    return db.query(Room).all()


@router.websocket('/room/{room_id}/message')
async def create_message(room_id: int, websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        token = websocket.headers.get('Authorization', '').split(' ')[1]
        logger.info(f"Received token: {token}")
        user_id = verify_access_token(token)
        if not user_id:
            logger.error("Token validation failed")
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        # Websocket ulanishini boshqaruvchi qo'shilish
        await manager.connect(websocket)

        # Xabarlar qabul qilish va yuborish
        try:
            while True:
                data = await websocket.receive_text()
                message = Message(room_id=room_id, user_id=user_id, content=data)
                db.add(message)
                db.commit()
                await manager.send_message(f'{user_id}: {data}')  # Barcha ulanganlarga xabar yuborish
        except WebSocketDisconnect:
            manager.disconnect(websocket)  # WebSocketDisconnect xatoligida uzilish

    except Exception as e:
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        print(f"WebSocket error: {e}")
