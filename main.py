from markdowns.save_markdown import write_articles_to_markdown, delete_markdowns_directory
from vectorstore.vectorstore_handler import log_chunks, create_vectorstore, create_list_of_vectorstore_files, list_vectorstore
from vectorstore.upload import list_files, upload_list_files, delete_all_files
from scraper.fetch_articles import get_all_articles
from dotenv import load_dotenv
from openai import OpenAI
import os



load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NAME = "Chatbot Vector Store"

def main():
	client = OpenAI(api_key=OPENAI_API_KEY)
	articles = get_all_articles(max_articles=40)
	write_articles_to_markdown(articles)
	# create_vectorstore(NAME)
	vectorstores = list_vectorstore()
	# upload_list_files()
	files = list_files()
	create_list_of_vectorstore_files(client, vectorstores.data[0].id)
	log_chunks(client, vectorstores.data[0].id)
	# delete_all_files()
	# delete_markdowns_directory()

if __name__ == "__main__":
    main()