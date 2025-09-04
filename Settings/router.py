from Settings.apis import *

class APIRouter:
    def __init__(self):
        self.api_map = {
            "취업": SaraminAPI(),
        }

    def route(self, query: str):
        for keyword, api in self.api_map.items():
            if keyword in query:
                return api
        return None  # fallback
        
