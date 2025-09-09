# Utils/chat.py
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from Database.model import ChatSession, ChatLog

# 로그인 이후 채팅 세션 타입 선택
# (1: 새 채팅, 2: 기존 채팅)
def select_chat_type():
    select_type = input("Select Chat (1. New\t2.Histories): ")
    
    if select_type not in ["1", "2"]:
        raise ValueError("Plese Check Only Number [1, 2]")
    select_type = int(select_type)
        
    return select_type


# if select_session_type == 1: create new chatting session
def create_session(db: Session, user_id: int, session_name: Optional[str] = None) -> ChatSession:
    sess = ChatSession(user_id=user_id, session_name=session_name)
    db.add(sess)
    db.flush()
    db.refresh(sess)
    # return sess


# if select_session_type == 2: show list to user what user's session_id & chat_session_name
def list_sessions_history(db: Session, user_id: int) -> List[ChatSession]:
    stmt = select(ChatSession).where(ChatSession.user_id == user_id).order_by(desc(ChatSession.id))
    session_list = list(db.scalars(stmt).all())
    return session_list


# [user_id, chat_session_id]에 해당하는 채팅 기록(history) 가져오기
def load_chat_session(db: Session, user_id: int, chat_session_id: int) -> List[ChatLog]:
    stmt = (
        select(ChatLog)
        .where(ChatLog.user_id == user_id, ChatLog.session_id == chat_session_id)
        .order_by(ChatLog.id.asc())
    )
    return list(db.scalars(stmt).all())


# chat log append
def append_chat_log(db: Session, user_id: int, chat_session_id: int, text: str) -> ChatLog:
    log = ChatLog(user_id=user_id, session_id=chat_session_id, chat_log=text)
    db.add(log)
    db.flush()
    return log


# session title update (criteria(?) is first chatting)
def update_session_title_if_empty(db: Session, chat_session_id: int, title: str) -> None:
    sess = db.get(ChatSession, chat_session_id)
    if sess and (not sess.session_name):
        sess.session_name = title
        