from Settings.apis import *
from Settings.router import APIRouter
from Utils.utils import *
from openai import OpenAI

def chat(query, agent=None, chat_log=None):
    if agent is None or agent.chain is None:
        raise ValueError("Agent is Not Initialization")

    router = APIRouter()
    api = router.route(query)

    if api:
        user_params, schema_path = extract_api_params_from_user_query(query, agent, api)
    
    api_response = api.search(user_params)
    api_response = parse_api_response(api_response)
    # api_response = normalize_response(api_response, schema_path)

    response = agent.chain.invoke({
        "system_head": agent.system_messages_head,
        "history": chat_log,
        "input": query,
        "api_response": api_response,
        "system_tail": agent.system_messages_tail
    })

    return response.content

# 제목 생성
client = OpenAI()
def make_title(text: str) -> str:
    prompt = f"다음 문장을 10자 이하 한국어 요약으로 만들어줘:\n\n{text}"

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",  # 아주 빠른 모델
            messages=[
                {"role": "system", "content": "너는 입력을 간단히 압축해주는 요약기야."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=20,
            temperature=0.3,
        )
        title = resp.choices[0].message.content.strip()
        return title[:10]
    
    except Exception as e:
        print("make_title error:", e)
        return "New Chat"