import json
from config import schema_config
import sys, threading, time, itertools

CONFIG = schema_config
schema_map = {
    "saramin": CONFIG["saramin"]
}

# api를 호출하기 위한 파라미터들을 유저 쿼리에서 뽑아내는 함수
# llm을 통해서 스스로 생각해서 형식에 맞춰서 파라미터를 추출
def extract_api_params_from_user_query(query, agent, api):
    api_name = api.__class__.__name__
    shcema_name = api_name.replace("API", "").lower()
    schema_path = schema_map[shcema_name]
    function_chain = agent.get_params_mapping_api(api_name, schema_path)

    result = function_chain.invoke({"input": query}) # 1차적으로 여기서 시간이 오래걸림
    user_params = result['function']
    return user_params, schema_path


# 최종 api response 결과 파싱(LLM에 전달하기 위함)
def normalize_response(api_response, schema_path, max_items: int = 5) -> str:
    """
    범용적인 API 응답 파서 함수
    :param api_response: requests.Response 또는 dict
    :param max_items: 리스트 응답 시 최대 몇 개 출력할지
    :return: LLM이 이해할 수 있는 문자열
    """
    if hasattr(api_response, "json"):
        data = api_response.json()
    else:
        data = api_response  # 이미 dict인 경우

    def normalize(obj, depth=0):
        schema_path

    return normalize(data)



# 최종 api response 결과 파싱(LLM에 전달하기 위함)
def parse_api_response(api_response, max_items: int = 5) -> str:
    """
    범용적인 API 응답 파서 함수
    :param api_response: requests.Response 또는 dict
    :param max_items: 리스트 응답 시 최대 몇 개 출력할지
    :return: LLM이 이해할 수 있는 문자열
    """
    if hasattr(api_response, "json"):
        data = api_response.json()
    else:
        data = api_response  # 이미 dict인 경우

    def flatten_and_simplify(obj, depth=0):
        indent = "  " * depth
        if isinstance(obj, dict):
            return "\n".join(f"{indent}- {k}: {flatten_and_simplify(v, depth+1)}" for k, v in obj.items())
        elif isinstance(obj, list):
            sliced = obj[:max_items] if len(obj) > max_items else obj
            return "\n".join(f"{indent}- {flatten_and_simplify(item, depth+1)}" for item in sliced)
        else:
            return str(obj)

    return flatten_and_simplify(data)



class Loader:
    def __init__(self, desc="Loading...", end="Done!", interval=0.1):
        self.desc = desc
        self.end = end
        self.interval = interval
        self._running = False
        self._thread = None

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._animate, daemon=True)
        self._thread.start()

    def _animate(self):
        for c in itertools.cycle(["|", "/", "-", "\\"]):
            if not self._running:
                break
            sys.stdout.write(f"\r{self.desc} {c}")  # \r로 현재 줄 덮어쓰기
            sys.stdout.flush()
            time.sleep(self.interval)

    def stop(self):
        self._running = False
        if self._thread is not None:
            self._thread.join()
        sys.stdout.write(f"\r{self.end}\n")  # 완료 후 줄 바꿈
        sys.stdout.flush()