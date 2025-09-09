# Utils/user.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from Database.model import User

class UserAlreadyExists(Exception):
    pass

class UserNotFound(Exception):
    pass

def select_sign():
    selected_sign_type = int(input("1.SignIN \t\t 2.SignUP: ", ))
    return selected_sign_type

def sign_in(db: Session) -> User:
    nickname = input("Input Nickname: ")
    user = db.scalar(select(User).where(User.nickname == nickname))
    if not user:
        raise UserNotFound(f"nickname '{nickname}' not found")
    return user

def sign_up(db: Session) -> User:
    nickname = input("Register nickname: ")
    exists = db.scalar(select(User.id).where(User.nickname == nickname))
    if exists:
        raise UserAlreadyExists(f"nickname '{nickname}' already exists")

    user = User(nickname=nickname)
    db.add(user)
    db.commit()   # 반영
    db.refresh(user)  # user.id 같은 자동생성 컬럼 채워줌
    return user