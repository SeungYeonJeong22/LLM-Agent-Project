from typing import Dict, List
import os
from dotenv import load_dotenv
import json
import time

from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    SystemMessage, HumanMessage, AIMessage, ChatMessage, BaseMessage
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.chains.openai_functions import create_structured_output_chain
from langchain.callbacks.base import BaseCallbackHandler


from Utils.chat import select_chat_log
from Utils.utils import Loader

from warnings import filterwarnings
filterwarnings("ignore")

load_dotenv()

OPEN_API_ACCESS_KEY = os.getenv("OPEN_API_ACCESS_KEY")
if not OPEN_API_ACCESS_KEY:
    raise EnvironmentError("OPEN_API_ACCESS_KEY is not exist in .env.")        

os.environ["OPENAI_API_KEY"] = OPEN_API_ACCESS_KEY


class PrintCallback(BaseCallbackHandler):
    def on_llm_new_token(self, token, **kwargs):
        print(token, end="", flush=True)
        

class Agent:
    def __init__(self):        
        # 모델 설정
        self.llm = ChatOpenAI
        self.model = "gpt-5-nano" # 좀 느림
        # self.model = "gpt-4o-mini" # 결과가 매우 이상함
        self.temperature = 0.2
        
        # Chain 설정
        self.chain = None
        self.system_messages: []
        self.ai_messages: List[ChatMessage] = []
        self.human_messages: List[ChatMessage] = []
        
        self.function_chains = {}
        
        self.__set_chain()
        
    def __set_chain(self):
        llm = self.llm(
                model=self.model, 
                temperature=self.temperature, # 얼마나 다양하게 답변을 제공할 것인가
                streaming=True,
                callbacks=[PrintCallback()]
            )

        prompt = ChatPromptTemplate.from_messages([
            ("system", "{system_head}"),
            MessagesPlaceholder("history"),  # List[Human/AI/...]
            ("human", "{input}"),
            ("ai", "다음은 외부 API에서 가져온 검색 결과야:\n\n{api_response}\n\n이걸 참고해서 유저에게 요약된 결과를 알려줘."),
            ("system", "{system_tail}"),
        ])

        self.chain = prompt | llm #LLM 호출 & 체인 연결 (|로 연결)

        # self.system_messages_head = [
        #     ChatMessage(role="system", content="너는 친절한 한국어 에이전트 모델이야. 답변은 반드시 한국어로 해야 해."),
        #     ChatMessage(role="system", content="불확실하면 추측하지 말고 필요한 정보를 물어봐."),
        #     ChatMessage(role="system", content="숫자/단계가 있으면 짧은 목록으로 정리해."),
        #     ChatMessage(role="system", content="코드/명령어는 가능한 한 하나의 블록으로 묶어줘."),
        #     ChatMessage(role="system", content="개인정보/민감정보는 요청해도 제공하지 마.")
        # ]
        
        # 토큰 감소
        self.system_messages_head = [
            SystemMessage(content=(
                "너는 친절한 한국어 에이전트 모델이야. 답변은 반드시 한국어로.\n"
                "불확실하면 추측하지 말고 필요한 정보를 물어봐.\n"
                "숫자/단계는 짧은 목록으로.\n"
                "코드/명령어는 하나의 블록으로.\n"
                "개인정보/민감정보는 제공하지 마."
            ))
        ]
        
        self.system_messages_tail = [
            ChatMessage(role="system", content="스스로 3번 이상 검토해보고 스스로에 대한 유저의 질문과 답하고자 하는 대답간의 유사성 및 재현성을 판단해줘."),
        ]
        
        
    def load_chat_log(self, db, user_id, session_id):
        logs = select_chat_log(db, user_id, session_id)
        histories = []
        
        for log in logs:
            histories += [
                ChatMessage(role=f"{log.role}", content=f"{log.chat_log}")
            ]

        return histories
        
        
    def get_params_mapping_api(self, api_name, schema_path):
        schema = self.get_schema(schema_path)
        loader = Loader(desc="API 파라미터 추출 중...")
        loader.start()
        time.sleep(1)
        
        llm = self.llm(model="gpt-4o-mini", temperature=0.0)
        try:
            function_chain = create_structured_output_chain(
                output_schema=schema['parameters'],
                llm=llm,
                prompt=ChatPromptTemplate.from_messages([
                    ("system", f"유저의 질문으로부터 {api_name} API에 사용할 파라미터를 추출해줘."),
                    ("human", "{input}")
                ]),
                verbose=False
            )
        finally:
            loader.stop()

        self.function_chains[api_name] = function_chain
        return function_chain
        
        
    def get_schema(self, schema_path):
        with open(schema_path, 'r') as f:
            schema = json.load(f)
        return schema