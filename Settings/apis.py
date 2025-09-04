# 사람인 API 요청
import requests
import os
from dotenv import load_dotenv

load_dotenv()
SARAMIN_ACCESS_KEY = os.getenv("SARAMIN_API_ACCESS_KEY")

class SaraminAPI:
    def __init__(self):
        self.url = "https://oapi.saramin.co.kr/job-search"
        self.access_key = SARAMIN_ACCESS_KEY

        self.headers = {
            "Accept":"application/json"
        }

        self.keywords = ["기업명", "공고명", "업직종 키워드", "직무내용"]

        self.params = {
            "access-key": self.access_key,
        }

    def search(self, user_params=None):
        if user_params:
            for k,v in user_params.items(): self.params[k] = v
        response = requests.get(url=self.url, params=self.params, headers=self.headers)
        return response