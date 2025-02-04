# -------------------------------------- LIBS IMPORT ---------------------------------------------
import asyncio
from history import *
import textProcessor
from handle_query import handel_request
# -------------------------------------- FUNCTIONS ---------------------------------------------
def add_doc(docs):
    """
    Adds documents to the Faiss and before that split it into chunks
    then makes vector and store it
    :param docs: Documents
    :return:
    """
    all_chunks=[]
    all_metadata=[]

    for doc in docs:
        docs_chunks=textProcessor.chunk_text(doc["text"])
        for docs_chunk in docs_chunks:
            all_chunks.append(docs_chunk)
            metadata=doc.copy()
            metadata["text"]=docs_chunk
            all_metadata.append(metadata)

    embeddings_array=textProcessor.vectorize_text(all_chunks)
    store=textProcessor.store(embeddings_array,metadata)
    return store


# -------------------------------------------------------------------------------------------------------
async def main():
    """
    Main function
    """
    documents = [
        {
            "text": "With FAISS, developers can search multimedia documents in ways that are inefficient or impossible with standard database engines (SQL). It includes nearest-neighbor search implementations for million-to-billion-scale datasets that optimize the memory-speed-accuracy tradeoff. FAISS aims to offer state-of-the-art performance for all operating points. FAISS contains algorithms that search in sets of vectors of any size, and also contains supporting code for evaluation and parameter tuning. Some if its most useful algorithms are implemented on the GPU. FAISS is implemented in C++, with an optional Python interface and GPU support via CUDA.",
            "source": "ai.meta.com",
            "date": "2024-01-28"
        }
    ]
    document=add_doc(documents)
    session_id="U221"
    query1="What is the main topic of document?"
    response1=await handel_request(session_id,query1,model_name="deepseek-chat")
    print(f"Query 1: {query1} \nResponse 1: {response1}")
    print(get_history(session_id))

    query2="Tell me more about this please."
    response2=await handel_request(session_id,query2,model_name="deepseek-chat")
    print(f"Query 2: {query2} \nResponse 2: {response2}")

if __name__ == "__main__":
    asyncio.run(main())