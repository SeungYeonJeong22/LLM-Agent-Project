from Settings.agent import Agent
from Functions.chat import *

if __name__ == "__main__":
    agent = Agent()
    user_input = input("Query : ")
    
    response = chat(user_input, agent)
    print(response)