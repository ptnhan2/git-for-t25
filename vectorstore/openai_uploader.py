import os
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from slugify import slugify
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def upload_file(file_path):
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.files.create(
    file=open(file_path, "rb"),
    purpose="assistants"
    )

def upload_list_files():
    print("uploading files")
    md_folder = Path(__file__).resolve().parent.parent/"markdowns" / "md_output"
    for md_file in md_folder.glob("*.md"):
        upload_file(md_file)

def upload_delta_files(articles):
    md_folder = Path(__file__).resolve().parent.parent/"markdowns" / "md_output"
    for article in articles:
        upload_file(md_folder/(slugify(article["title"])+".md"))
    print("=> Uploading delta files...")    

def list_files():
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.files.list()
    return response

def delete_file(file_id):
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.files.delete(file_id)
    return response

def delete_all_files():
    listfile = list_files()
    for file in listfile.data:
        delete_file(file.id)

def delete_old_files(files, newest_articles):
    if(len(files.data) > 0):
        for file in files.data:
            for article in newest_articles: 
                if(slugify(article["title"])+".md" == file.filename):
                    delete_file(file.id)
                    print("Deleted file: ", file.id, " - ", file.filename)