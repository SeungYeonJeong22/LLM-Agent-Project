from Settings.apis import *
from Settings.router import APIRouter
from Utils.utils import *

def chat(query, agent=None):
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
        "input": query,
        "api_response": api_response,
        # "api_response": parsed_api_response,
        "system_tail": agent.system_messages_tail
    })

    return response.content