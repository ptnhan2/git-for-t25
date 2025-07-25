from markdowns.save_markdown import write_articles_to_markdown, delete_markdowns_directory
from vectorstore.vectorstore_handler import log_chunks, create_vectorstore, create_list_of_vectorstore_files, list_vectorstore, delete_vectorstore_file, delete_old_vectorstore_files
from vectorstore.openai_uploader import list_files, delete_all_files, delete_file, upload_delta_files, delete_old_files
from scraper.fetch_articles import get_all_articles
from dotenv import load_dotenv
from openai import OpenAI
import os
from datetime import datetime, timezone
import time
from slugify import slugify
import logging
from pathlib import Path


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MAX_ARTICLES = os.getenv("MAX_ARTICLES")
SCRAPER_BASE_URL = os.getenv("SCRAPER_BASE_URL")
VECTORSTORE_NAME = os.getenv("VECTORSTORE_NAME")
LOG_FILE = Path("logs/job.log")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def main():
	client = OpenAI(api_key=OPENAI_API_KEY)
	logging.basicConfig(
		filename = LOG_FILE,
		level = logging.INFO,
		format="%(asctime)s - %(levelname)s - %(message)s"
	)
	logging.getLogger("httpcore").setLevel(logging.WARNING)
	logging.getLogger("httpx").setLevel(logging.WARNING)
	logging.getLogger("openai").setLevel(logging.WARNING)

	added = 0
	updated = 0
	skipped = 0

	delta_articles, added, updated, skipped  = get_all_articles(max_articles=int(MAX_ARTICLES), BASE_URL=SCRAPER_BASE_URL)
	write_articles_to_markdown(delta_articles)

	vectorstores = list_vectorstore()
	if(len(vectorstores.data) == 0):
		create_vectorstore(VECTORSTORE_NAME)
		print("-----------------------------------------")
		print("Waiting for vectorstore to be ready...")
		time.sleep(10)	
	vectorstores = list_vectorstore()
	vectorstores_id = vectorstores.data[0].id
	files = list_files()

	delete_old_files(files, delta_articles)
	delete_old_vectorstore_files(slugify, files, delta_articles, client, vectorstores_id)
	
	upload_delta_files(delta_articles)
	
	create_list_of_vectorstore_files(client, vectorstores_id)
	log_chunks(client, vectorstores_id)

	logging.info(f"Job finished. Added: {added}, Updated: {updated}, Skipped: {skipped}")
	print(f"Added: {added}, Updated: {updated}, Skipped: {skipped}")
	print("-----------------------------------------")

if __name__ == "__main__":
    main()