import os
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# file_path = "markdowns/chunking/chunking_output/chunks.md"


def upload_file(file_path):
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.files.create(
    file=open(file_path, "rb"),
    purpose="assistants"
    )
    print(response)

def upload_list_files():
    print("uploading files")
    md_folder = Path(__file__).resolve().parent.parent/"markdowns" / "md_output"
    print(md_folder)
    for md_file in md_folder.glob("*.md"):
        upload_file(md_file)

def list_files():
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.files.list()
    print(response.data[0].id)
    return response

def delete_file(file_id):
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.files.delete(file_id)
    print(response)

def delete_all_files():
    listfile = list_files()
    for file in listfile.data:
        delete_file(file.id)

