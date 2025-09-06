from Settings.apis import *
from Settings.router import APIRouter
from Utils.utils import parse_api_response, extract_api_params_from_user_query

def chat(query, agent=None):
    if agent is None or agent.chain is None:
        raise ValueError("Agent is Not Initialization")

    router = APIRouter()
    api = router.route(query)

    if api:
        user_params = extract_api_params_from_user_query(query, agent, api)
    
    api_response = api.search(user_params)
    parsed_api_response = parse_api_response(api_response)

    response = agent.chain.invoke({
        "system": agent.get_system_message()[0],
        "input": query,
        "response_api": parsed_api_response,
        "ai": agent.get_ai_message(),
        "system": agent.get_system_message()[-1]
    })


    return response.content