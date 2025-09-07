# models.py
from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from .db_init import Base

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nickname: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    
    
class ChatSession(Base):
    __tablename__ = "chat_session"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_name: Mapped[str] = mapped_column(String(255)) # 나중에 채팅방 제목 설정 (첫 채팅 기준으로 update할 예정)
    
    
class ChatLog(Base):
    __tablename__ = "chat_log"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int]= mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_log: Mapped[str] = mapped_column(Text)