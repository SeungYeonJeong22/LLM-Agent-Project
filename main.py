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
            else:
                raise "Select 1, 2"

            print(f"\n----Login Success {user.nickname}!----\n")
            agent = Agent()
            
            chat_type = select_chat_type()
            
            if chat_type == 1: 
                create_session(db=db, user_id=user.id, session_name="New Chat")
                db.commit()
                chat_type = 2
            
            session_histories = list_sessions_history(db, user_id=user.id)
            
            for session_history in session_histories:
                print(f"Session ID: {session_history.id}\t \
                    Session Name: {session_history.session_name} \
                    (Created At: {session_history.created_at})")
            
            # for id, session_name in zip(session_history.id, session_history.session_name):
            #     print(id, session_name)
            session_id = int(input("Select Number in above lists: "))
            
            chat_logs = load_chat_session(db, user.id, session_id)
            print(f"Yours Chatlogs: {chat_logs}")
            
            print("\nStart Chat!\n")
            
            # new_session_title = False
            while True:
                user_input = input("Query : ")
                
                response = chat(user_input, agent)
                print(response)
                
                # append_chat_log(db, user.id, session_id, response)
                # if not session_title_flag: # 나중에 이름 요약 모델 살짝 돌리기
                #     update_session_title_if_empty(db, session_id, )
                # session_title_flag = True
                
                
    
    
    
    
    
    # # chat_type = select_chat_type # [1.new 2.histories]
    
    
    # agent = Agent()
    # user_input = input("Query : ")
    
    # response = chat(user_input, agent)
    # print(response)