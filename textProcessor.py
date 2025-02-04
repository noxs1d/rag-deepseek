# -------------------------------------- LIBS IMPORT ---------------------------------------------
import numpy as np
import os
from langchain_openai import OpenAIEmbeddings
import faiss
from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
# # ------------------------------------ VARIABLES LOADING ------------------------------------------
load_dotenv()
OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')
embeddings_model = OpenAIEmbeddings(model='text-embedding-3-small', dimensions=1024,api_key=OPENAI_API_KEY)
# -------------------------------------- FUNCTIONS ---------------------------------------------
def chunk_text(text):
    """
    Dividing text to smaller chunks
    :param text: text from docs
    :return: List[docs]
    """
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200, separators=["\n\n", "\n", " ", ""])
    chunks=text_splitter.split_text(text)
    return chunks

def vectorize_text(chunks):
    """
    Making from chunks to vectors
    :param chunks: text which was split into chunks
    :return: array of vectors
    """
    chunk_embeddings = [embeddings_model.embed_documents([chunk])[0] for chunk in chunks]
    return np.array(chunk_embeddings)

def query_embeddings(query):
    """
    Embedding query
    :param query:
    :return:
    """
    embeddings = embeddings_model.embed_query(query)
    return np.array(embeddings)

# ------------------ INITIALIZING FAISS ----------------
index = faiss.IndexFlatL2(1024)
metadata: List[Dict] = []

def store(vector, meta):
    """
    Store vector in Faiss and reshaping vectors
    :param vector: Text which was embedded
    :param meta:
    :return:
    """
    if len(vector.shape)==1:
        vector=vector.reshape(1,-1)

    index.add(vector)
    # faiss.write_index(index, "faiss_stor/index_file.index")
    metadata.append(meta)

def query_vector(vector):
    """
    Finding the most 3 relevant indexes from stored
    :param vector: query which was vectorized
    :return:
    """
    if len(vector.shape)==1:
        vector=vector.reshape(1,-1)
    distances, indices = index.search(vector,3)

    result=[]
    for i in range(len(indices[0])):
        idx=indices[0][i]
        if idx !=-1:
            result.append({
                'score':float(1/(1+distances[0][i])),
                'metadata':metadata[idx]
            })

    return result

def load_tmpl(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content
