import os
from openai import OpenAI
from dotenv import load_dotenv
from .openai_uploader import list_files, upload_list_files
import requests
import tiktoken
import math

encoding = tiktoken.encoding_for_model("text-embedding-3-small")

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def create_vectorstore(NAME):
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.vector_stores.create(
        name=NAME
    )
    return response

def list_vectorstore():
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.vector_stores.list()
    return response

def delete_vectorstore(vector_store_id):
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.vector_stores.delete(vector_store_id)
    return response

def delete_all_vectorstore():
    vectorstores = list_vectorstore()
    for vectorstore in vectorstores.data:
        delete_vectorstore(vectorstore.id)

def create_vectorstore_file(client, vector_store_id, file_id):
    vector_store_file = client.vector_stores.files.create(
    vector_store_id=vector_store_id, 
    file_id= file_id,
    chunking_strategy={
        "type": "auto",
    }
    )
    return vector_store_file

def create_list_of_vectorstore_files(client, vectorstore_id):
    try:
        files = list_files()
        for file in files.data:
            create_vectorstore_file(client, vectorstore_id , file.id)
            
        return "Success"
    except:
        return "Error"

def list_of_vectorstore_files(client, vector_store_id):
    vector_store_files = client.vector_stores.files.list(
    vector_store_id=vector_store_id,
    limit=100
    )
    return vector_store_files

def log_chunks(client, vector_store_id):
    vector_store_files = list_of_vectorstore_files(client, vector_store_id)
    total_files = len(vector_store_files.data)
    total_chunks = 0
    print("=> Logging chunks...")
    for file in vector_store_files.data:
        file_content = retrieve_vectorstore_file_content(vector_store_id, file.id)
        file_tokens = encoding.encode(file_content["data"][0]["text"])
        file_size_tokens = len(file_tokens)
        chunk_size_tokens = file.chunking_strategy.static.max_chunk_size_tokens
        chunks = math.ceil(file_size_tokens / chunk_size_tokens)
        total_chunks += chunks
        print(f"File with id: {file.id} had {file_size_tokens} tokens and was chunked into {chunks} chunks",)
    print("-----------------------------------------")
    print(f"Total number of files embedded:  {total_files}")
    print(f"Total number of chunks embedded: {total_chunks}")
    print("-----------------------------------------")

def retrieve_vectorstore_file_content(vector_store_id, file_id):
    url = f"https://api.openai.com/v1/vector_stores/{vector_store_id}/files/{file_id}/content"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}"   
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None
    

def delete_vectorstore_file(client, vector_store_id, file_id):
    vector_store_file = client.vector_stores.files.delete(
    vector_store_id=vector_store_id, 
    file_id= file_id,
    )
    return vector_store_file

def delete_old_vectorstore_files(slugify, files, newest_articles, client, vector_store_id):
    if(len(files.data) > 0):
            for file in files.data:
                for article in newest_articles: 
                    if(slugify(article["title"])+".md" == file.filename):
                        delete_vectorstore_file(client, vector_store_id, file.id)
                        print("Deleted vectorstore file: ", file.id, " - ", file.filename)