from markdowns.save_markdown import write_articles_to_markdown, delete_markdowns_directory
from vectorstore.vectorstore_handler import log_chunks, create_vectorstore, create_list_of_vectorstore_files, list_vectorstore, delete_vectorstore_file, delete_old_vectorstore_files
from vectorstore.upload import list_files, delete_all_files, delete_file, upload_delta_files, delete_old_files
from scraper.fetch_articles import get_all_articles
from dotenv import load_dotenv
from openai import OpenAI
import os
from datetime import datetime, timezone
import time
from slugify import slugify




load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NAME = "Chatbot Vector Store"

def main():
	client = OpenAI(api_key=OPENAI_API_KEY)

	newest_articles = get_all_articles(max_articles=5)
	write_articles_to_markdown(newest_articles)
	vectorstores = list_vectorstore()
	if(len(vectorstores.data) == 0):
		create_vectorstore(NAME)
		print("Waiting for vectorstore to be ready...")
		time.sleep(10)	
	vectorstores = list_vectorstore()
	vectorstores_id = vectorstores.data[0].id
	files = list_files()
	# delete old files
	delete_old_files(files, newest_articles)

	# delete old vectorstore files
	delete_old_vectorstore_files(slugify, files, newest_articles, client, vectorstores_id)
	
	upload_delta_files(newest_articles)
	create_list_of_vectorstore_files(client, vectorstores_id)
	log_chunks(client, vectorstores_id)

	# delete_all_files()
	# delete_markdowns_directory()

	# upload_list_files()
	# vectorstores = list_vectorstore()
	# create_list_of_vectorstore_files(client, vectorstores.data[0].id)

if __name__ == "__main__":
    main()