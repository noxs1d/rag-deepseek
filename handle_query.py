# -------------------------------------- LIBS IMPORT ---------------------------------------------
from deepseek_api import client
from deepseek_api import response
from history import chat_history
from textProcessor import load_tmpl
from cost_calculator import calculate_cost
# -------------------------------------- FUNCTIONS ---------------------------------------------
OPTIMIZE_QUERY =load_tmpl('templates/optimize_query.tmpl')

async def optimize_query(session_id,query, model_name):
    """
    Optimize the query depending on chat history to make query more optimized for embedding
    :param session_id: unique session id
    :param query: users query
    :param model_name: deepseek model name
    :return: optimized query
    """

    history=chat_history.get(session_id, [])
    # getting history as string
    cleaned_chat_history=" ".join([f"{item['role']}: {item.get('query', item.get('response', ''))}" for item in history])
    # giving to the system prompt in which said it should make query more detailed
    messages = [
        {"role": "system", "content": OPTIMIZE_QUERY},
        {"role": "user", "content": "chat history: " + cleaned_chat_history + "\nuser query:" + query}
    ]
    # Request to the deepseek
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        stream=False
    )
    # Getting tokens and calculating cost
    token_usage = {
        'prompt_tokens': response.usage.prompt_tokens,
        'completion_tokens': response.usage.completion_tokens,
        'total_tokens': response.usage.total_tokens
    }
    await calculate_cost(token_usage=token_usage,model_name=model_name)
    return response.choices[0].message.content
async def handel_request(session_id,query, model_name="deepssek-chat"):
    try:
        print("-----------MSG BEFORE OPTIMIZER--------:\n",query)
        opimized_query= await optimize_query(session_id,query,model_name)
        print("\n------------MSG AFTER-----------\n",opimized_query)
        respons=await response(session_id,query,opimized_query,model_name)

    except Exception as e:
        respons = f'An error occurred:\n {e} \n Try again later'
    return respons

