# Utils/chat.py
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from Database.model import ChatSession, ChatLog

# 로그인 이후 채팅 세션 타입 선택
# (1: 새 채팅, 2: 기존 채팅)
def select_chat_type():
    select_type = input("Select Chat (1.New Chat\t 2.Histories\t 3.Delete): ")
    
    if select_type not in ["1", "2", "3"]:
        raise ValueError("Plese Select in [1, 2, 3]")
    select_type = int(select_type)
        
    return select_type


# if select_session_type == 1: create new chatting session
def create_session(db: Session, user_id: int, session_name: Optional[str] = None) -> ChatSession:
    sess = ChatSession(user_id=user_id, session_name=session_name)
    db.add(sess)
    db.flush()
    db.refresh(sess)  # system_default(created_at과 같은)에 들어가는 현재 시각 리프레쉬
    db.commit() 


# delete chat session
def delete_session(db:Session) -> ChatSession:
    session_histories = select_sessions_history()
    for session_history in session_histories:
        print(f"Session ID: {session_history.id}\t \
            Session Name: {session_history.session_name} \
            (Created At: {session_history.created_at})")
    del_chat_session_id  = int(input("Delete Chat Session Nunber: "))
    del_session = db.execute(select(ChatSession).filter(ChatSession.id==del_chat_session_id)).scalars().first()
    
    if del_session:
        db.delete(del_session)
        db.commit()
        return print("Delete!! Chat Session")
    else:        
        return print("Not Exist")    
    

# if select_session_type == 2: show list to user what user's session_id & chat_session_name
def select_sessions_history(db: Session, user_id: int) -> List[ChatSession]:
    stmt = select(ChatSession).where(ChatSession.user_id == user_id).order_by(desc(ChatSession.id))
    session_list = list(db.scalars(stmt).all())
    return session_list


# [user_id, chat_session_id]에 해당하는 채팅 기록(history) 가져오기
def select_chat_log(db: Session, user_id: int, chat_session_id: int) -> List[ChatLog]:
    if not chat_session_id:
        chat_session_id = 0
    stmt = (
        select(ChatLog)
        .where(ChatLog.user_id == user_id, ChatLog.session_id == chat_session_id)
        .order_by(ChatLog.id.desc())
    )
    chat_logs = list(db.scalars(stmt).all())

    return chat_logs

# chat log append
def update_chat_log(db: Session, user_id: int, chat_session_id: int, query:str, response: str) -> ChatLog:
    human = ChatLog(user_id=user_id, session_id=chat_session_id, role='user', chat_log=query)
    ai = ChatLog(user_id=user_id, session_id=chat_session_id, role='assistant', chat_log=response)
    
    for sess in [human, ai]:
        db.add(sess)
        db.flush()
        db.refresh(sess)
    db.commit()


# session title update (criteria(?) is first chatting)
def update_session_title_if_empty(db: Session, chat_session_id: int, title: str) -> None:
    sess = db.get(ChatSession, chat_session_id)
    if sess and (sess.session_name == "New Chat"):
        sess.session_name = title
    db.add(sess)
    db.flush()
    db.refresh(sess)
    db.commit()