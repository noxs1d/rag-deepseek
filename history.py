# -------------------------------------- LIBS IMPORT ---------------------------------------------
from typing import List, Dict
chat_history: Dict[str, List[Dict[str, str]]] = {}
# -------------------------------------- FUNCTIONS ---------------------------------------------
def get_history(session_id):
    """Getting history if it is not exists it returns []"""
    return chat_history.get(session_id, [])

def add_history(session_id, query, response):
    """Storing the chat between user and system"""
    if session_id not in chat_history:
        chat_history[session_id] = []

    chat_history[session_id].extend([
        {"role":"user", "query": query},
        {"role":"system", "response": response}]
    )

    while len(chat_history[session_id])/2>5:
        chat_history[session_id].pop(0)
        chat_history[session_id].pop(0)

def delete_history(session_id):
    chat_history[session_id]=[]