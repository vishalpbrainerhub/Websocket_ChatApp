from sqlalchemy import Column, Integer, String, TIMESTAMP, text, ForeignKey,UUID
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)

# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String,nullable=False,unique=True)
#     password = Column(String,nullable=False)
#     username = Column(String,nullable=False,unique=True)
#     first_name = Column(String,nullable=True)
#     last_name = Column(String,nullable=True)
#     friends = Column(list,nullable=True)
#     comes_request = Column(list,nullable=True)
#     sent_request = Column(list,nullable=True)
#     privacy = Column(bool,server_default=True,nullable=True)
#     profile_pic = Column(String,nullable=True)


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer,ForeignKey("chats.id"))
    sender_id = Column(Integer,ForeignKey("users.id"))
    message = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))


class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True)
    user1_id = Column(Integer,ForeignKey("users.id"))
    user2_id = Column(Integer,ForeignKey("users.id"))


