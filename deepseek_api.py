# -------------------------------------- LIBS IMPORT ---------------------------------------------
from dotenv import load_dotenv
import os
from openai import OpenAI
from textProcessor import *
from history import *
from cost_calculator import calculate_cost
import textProcessor
# # ------------------------------------ VARIABLES LOADING ------------------------------------------
load_dotenv()
DEEPSEEK_API_KEY=os.getenv('DEEPSEEK_API_KEY')
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
PROMPT=load_tmpl("templates/rag_structure.tmpl")
# -------------------------------------- FUNCTIONS ---------------------------------------------
async def deepseek_get_response(session_id,query,content,model_name="deepseek-chat"):
    """
    DeepSeek gets the query and answer to it depending on chat history and content from RAG
    :param session_id: unique id of user
    :param query: User's query
    :param content:
    :param model_name: deepseek-chat / deepseek-reasoner
    :return: respond from DeepSeek API
    """
    history = chat_history.get(session_id, [])
    cleaned_chat_history = " ".join([f"{item['role']}: {item.get('query', item.get('response', ''))}" for item in history])

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": f'chat history: {cleaned_chat_history}\nuser query: {query}\nrelevant data: {content}'},
        ],
        stream=False
    )
    deepseek_response = f"{model_name}'s response:\n\n"
    deepseek_response += response.choices[0].message.content
    token_usage = {
        'prompt_tokens': response.usage.prompt_tokens,
        'completion_tokens': response.usage.completion_tokens,
        'total_tokens': response.usage.total_tokens
    }
    await calculate_cost(token_usage,model_name)
    print(deepseek_response)

    return deepseek_response

async def response(session_id, query, optimized_query, model_name="deepseek-chat"):
    """
    This function is responsible for embedding query and for finding the most relevant
    vectors for a given optimized query and send it to deepseek_get_response function
    :param session_id: unique session id
    :param query: user's query
    :param optimized_query: Query which was optimized to find the most relevant vectors
    :param model_name: deepseek-chat/ deepseek-reasoner
    :return: response from DeepSeek API
    """
    query_embedding=textProcessor.query_embeddings(optimized_query)
    results=textProcessor.query_vector(query_embedding)
    context="\n\n".join([f"Doc {i+1}:\n{result['metadata']['text']}" for i, result in enumerate(results)])
    response = await deepseek_get_response(session_id,query,context,model_name)
    add_history(session_id,query,response)
    return response