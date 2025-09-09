from Settings.agent import Agent
from Functions.chat import *
from Utils.user import *
from Utils.chat import *
from Utils.db import *



if __name__ == "__main__":
    # user login 이후
    print("---------- Start Program ----------")
    
    with get_db() as db:
        while True:
            sign_type = select_sign()
            if sign_type == 1:
                user = sign_in(db) #user.id, user.nickname
            elif sign_type == 2: 
                sign_up(db)
                continue
            elif sign_type == 3:
                delete_users(db)
                continue
            else:
                raise ValueError("Select in [1, 2, 3]")

            print(f"\n----Login Success {user.nickname}!----\n")
            agent = Agent()
            
            while True:
                sessions = {}
                chat_type = select_chat_type()
                
                if chat_type == 1:  #create
                    create_session(db=db, user_id=user.id, session_name="New Chat")
                elif chat_type == 3: #delete
                    delete_session(db)
                    continue
                
                # chat type:2, 기존 채팅창 불러와서 사용(메모라이제이션 기능이 달라짐)
                session_histories = select_sessions_history(db, user_id=user.id)
                chat_log = ""
                
                if not session_histories:
                    print("There is not exist chat histories.\n Create New Chat!")
                    create_session(db=db, user_id=user.id, session_name="New Chat")
                    session_history = select_sessions_history(db, user_id=user.id)
                    sessions[session_history[0].id] = session_history[0].session_name
                else:
                    for session_history in session_histories:
                        sessions[session_history.id] = session_history.session_name
                        print(f"Session ID: {session_history.id}\t \
                            Session Name: {session_history.session_name} \
                            (Created At: {session_history.created_at})")
                    
                    session_id = int(input("Select Number in above lists: "))
                    chat_log = agent.load_chat_log(db, user.id, session_id)
                
                print("\nStart Chat!\n")
                while True:
                    user_input = input("Query : ")
                    
                    response = chat(user_input, agent, chat_log)
                    print(response)
                    
                    # 채팅 로그 기록하기
                    update_chat_log(db, user.id, session_id, user_input, response)
                    if sessions[session_id]=='New Chat': # 나중에 이름 요약 모델 살짝 돌리기
                        title = make_title(response)
                        update_session_title_if_empty(db, session_id, title)