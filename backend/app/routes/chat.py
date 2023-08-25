from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, utils, oauth2
from ..database import get_db

router = APIRouter(
    tags=["Chats"] 
)

@router.get("/chats")
def get_chats(db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    try:
        if not current_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not logged in")
        
        return {"message": "Chats retrieved successfully", "data": []}
    except Exception as e:
        print(e)
        return {"message": "Error", "error": e}


# create chat with a friend
@router.post("/chats/{friend_id}")
def create_chat(friend_id:int, db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    try:
        if not current_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not logged in")
        user1_id = current_user.id
        user2_id = friend_id

        if user1_id == user2_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot create a chat with yourself")
        
        if not db.query(models.User).filter(models.User.id == user2_id).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user2_id} not found")
        
        if db.query(models.Chat).filter(models.Chat.user1_id == user1_id, models.Chat.user2_id == user2_id).first():
            vp_chat_id = db.query(models.Chat).filter(models.Chat.user1_id == user1_id, models.Chat.user2_id == user2_id).first().id
            return {"message": "Chat already exists", "chat_id": vp_chat_id}
        
        new_chat = models.Chat(user1_id=user1_id, user2_id=user2_id)
        db.add(new_chat)
        db.commit()
        db.refresh(new_chat)
        return {"message": "Chat created successfully", "chat_id": new_chat.id}
    except Exception as e:
        print(e)
        return {"message": "Error", "error": e}


@router.post("/messages/{chat_id}")
def send_message(chat_id:int, request:schemas.Message, db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    try:
        if not current_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not logged in")
        
        chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
        if not chat:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Chat with id {chat_id} not found")
        
        if chat.user1_id != current_user.id and chat.user2_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to send messages to this chat")
        
        new_message = models.Message(chat_id=chat_id, sender_id=current_user.id, message=request.message)
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        return {"message": "Message sent successfully", "data": new_message}
    except Exception as e:
        print(e)
        return {"message": "Error", "error": e}


    
@router.get("/messages/{chat_id}")
def get_messages(chat_id:int, db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    try:
        if not current_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not logged in")

        user1 = current_user.id
        user2 = db.query(models.Chat).filter(models.Chat.id == chat_id).first().user2_id

        print(user1)
        print(user2)

        data1 = db.query(models.Message).filter(models.Message.chat_id == chat_id).all()

        #  i have to find out the second users chat from the chat table and then i have to find out the messages of that chat from the message table
        data2 = db.query(models.Chat).filter(models.Chat.user1_id == user2).first()
        if not data2:
            return {"message": "Messages retrieved successfully", "data": data1,"id":user1}
        data2 = data2.id
        data2 = db.query(models.Message).filter(models.Message.chat_id == data2).all()
        if not data1:
            for i in range(len(data2)):
                for j in range(i+1,len(data2)):
                    if data2[i].created_at > data2[j].created_at:
                        data2[i],data2[j] = data2[j],data2[i]
            return {"message": "Messages retrieved successfully", "data": data2,"id":user1}
        if not data2:
            for i in range(len(data1)):
                for j in range(i+1,len(data1)):
                    if data1[i].created_at > data1[j].created_at:
                        data1[i],data1[j] = data1[j],data1[i]
            return {"message": "Messages retrieved successfully", "data": data1,"id":user1}
        
        data = data1 + data2
        
        for i in range(len(data)):
            for j in range(i+1,len(data)):
                if data[i].created_at > data[j].created_at:
                    data[i],data[j] = data[j],data[i]
        
        return {"message": "Messages retrieved successfully", "data": data,"id":user1}
    except Exception as e:
        print(e)
        return {"message": "Error", "error": e}