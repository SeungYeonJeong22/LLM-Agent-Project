# Database/model.py
from sqlalchemy import String, Integer, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db_init import Base
from datetime import datetime

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nickname: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)

class ChatSession(Base):
    __tablename__ = "chat_session"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        index=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    session_name: Mapped[str] = mapped_column(String(255), nullable=True)

    user: Mapped["User"] = relationship(
        "User",
        passive_deletes=True
    )

    logs: Mapped[list["ChatLog"]] = relationship(
        "ChatLog",
        back_populates="session",
        cascade="all, delete-orphan",
        single_parent=True
    )

class ChatLog(Base):
    __tablename__ = "chat_log"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        index=True, nullable=False
    )
    session_id: Mapped[int] = mapped_column(
        ForeignKey("chat_session.id", ondelete="CASCADE"),
        index=True, nullable=False
    )
    role: Mapped[str] = mapped_column(String(64), nullable=True)
    chat_log: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    session: Mapped["ChatSession"] = relationship("ChatSession", back_populates="logs")