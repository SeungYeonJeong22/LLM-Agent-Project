# Utils/user.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from Database.model import User

class UserAlreadyExists(Exception):
    pass

class UserNotFound(Exception):
    pass

# 로그인, 회원가입, 삭제 선택
def select_sign():
    selected_sign_type = int(input("1.SignIN\t 2.SignUP\t 3.Delete\n Select Type:", ))
    return selected_sign_type


# 로그인
def sign_in(db: Session) -> User:
    nickname = input("Input Nickname: ")
    user = db.scalar(select(User).where(User.nickname == nickname))
    if not user:
        raise UserNotFound(f"nickname '{nickname}' not found")
    return user

# 회원가입
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

# 삭제 (일단 그냥 닉네임으로 삭제)
def delete_users(db:Session) -> User:
    nickname = input("Delete User Nickname: ")
    db_user = db.execute(select(User).filter(User.nickname==nickname)).scalars().first()

    if db_user:
        db.delete(db_user)
        db.commit()
        return print("Delete!!")
    else:        
        return print("Not Exist")