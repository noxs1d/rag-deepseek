# -------------------------------------- LIBS IMPORT ---------------------------------------------
from fastapi import FastAPI
from enum import Enum
from handle_query import handel_request
from history import chat_history


# # ------------------------------------ VARIABLES ------------------------------------------
class ModelName(str, Enum):
    deepseek_chat="deepseek-chat"
    deepseek_reasoner="deepseek-reasoner"
global session_id
app = FastAPI(
    title="RAG SYSTEM",
    description="A rag system on deepseek chat module",
    version="1.0"
)

# -------------------------------------- FUNCTIONS ---------------------------------------------

@app.post('/user/{session_id}')
async def read_user(session: str):
    """
    Takes a user session id
    :param session: unique session id
    :return: str user session id
    """
    global session_id
    session_id= session
    return session_id

@app.post("/query/{query}/{model_name}")
async def query(query:str, model_name:ModelName):
    """
    Chat with deepseek depending on which model user will choose
    :param query: user's query
    :param model_name: deepseek model name
    :return: respond to the query
    """
    global session_id
    response=await handel_request(session_id,query, model_name)
    return response

@app.get("/history")
async def read_history():
    """
    To get history of the current user
    :return: history
    """
    global session_id
    history = chat_history.get(session_id, [])
    cleaned_chat_history = " ".join(
        [f"{item['role']}: {item.get('query', item.get('response', ''))}" for item in history])
    return cleaned_chat_history