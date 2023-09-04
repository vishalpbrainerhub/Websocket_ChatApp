from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect,Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import json
from .routes import user,authentication,chat
from .database import engine,get_db
from . import models, schemas, oauth2
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(chat.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def Home():
    return "Welcome home of chatting app"


class ConnectionManager:

    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        print(message)
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        print(message)
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int,db: Session = Depends(get_db)):
    print(client_id)

    chat = db.query(models.Chat).filter(models.Chat.id == client_id).first()
    print(chat.user1_id,"-------------------")
    print(chat.user2_id,"-------------------")
    
    await manager.connect(websocket)
    now = datetime.now()
    current_time = now.strftime("%H:%M")

    try:
        while True:
            data = await websocket.receive_text()
            message = {"time":current_time,"clientId":client_id,"message":data,"senderId":chat.user1_id}
            # storing the data of messages in the database
            if data == "Connect":
                continue
            else:
                new_message = models.Message(chat_id=client_id, sender_id=chat.user1_id, message=data)
                db.add(new_message)
                db.commit()
                db.refresh(new_message)
            await manager.broadcast(json.dumps(message))
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        message = {"time":current_time,"clientId":client_id,"message":"Offline"}
        await manager.broadcast(json.dumps(message))
