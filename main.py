from markdowns.save_markdown import write_articles_to_markdown, delete_markdowns_directory
from vectorstore.vectorstore_handler import log_chunks, create_vectorstore, create_list_of_vectorstore_files, list_vectorstore, delete_vectorstore_file
from vectorstore.upload import list_files, upload_list_files, delete_all_files, delete_file, upload_delta_files
from scraper.fetch_articles import get_all_articles
from scraper.scrape_state import load_last_scrape_time, save_current_scrape_time
from scraper.detect_delta import detect_updated, detect_new
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
	# last_scrape_time = load_last_scrape_time()
	# print("Last scrape time:", last_scrape_time)

	# articles = get_all_articles(max_articles=6)
	# s = "2025-05-24 17:48:07.875190+00:00"
	# new_articles = detect_new(articles, datetime.fromisoformat(s.replace("Z", "+00:00")))
	# upadated_articles = detect_updated(articles, last_scrape_time)
	# if not new_articles and not upadated_articles:
	# 	print("No new articles to process.")
	# 	return
	# vectorstores = list_vectorstore()
	# if(len(vectorstores.data) == 0):
	# 	create_vectorstore(NAME)
	# # print("Waiting for vectorstore to be ready...")
	# time.sleep(10)	
	# vectorstores = list_vectorstore()
	# print(vectorstores)

	# # Cần tìm file_id theo slug name để xoá file trên vectorstore và uploader
	# files = list_files()

	# # print("FILES: ", files.data[0].filename)
	# for file in files.data:
	# 	for article in upadated_articles: 
	# 		if(slugify(article["title"])+".md" == file.filename):
	# 			delete_vectorstore_file(client, vectorstores.data[0].id, file.id)
	# 			delete_file(file.id)
	# 			print("Deleted file and vectorstore file: ", file.id, " - ", file.filename, " - ", article["title"])
	# 		else: 
	# 			print()
	# 			print("Not deleted file: ", file.id, " - ", file.filename, " - ", article["title"])
	
	# for file in files.data:
	# 		for article in new_articles: 
	# 			if(slugify(article["title"])+".md" == file.filename):
	# 				delete_vectorstore_file(client, vectorstores.data[0].id, file.id)
	# 				delete_file(file.id)
	# 				print("Deleted file and vectorstore file: ", file.id)
	# 			else: 
	# 				print()
	# 				print("Not deleted file: ", file.id, " - ", file.filename, " - ", article["title"])


	# write_articles_to_markdown(new_articles)
	# write_articles_to_markdown(upadated_articles)
	# upload_delta_files(new_articles)
	# files = list_files()

	# create_list_of_vectorstore_files(client, vectorstores.data[0].id)
	# # log_chunks(client, vectorstores.data[0].id)

	# # # delete_all_files()
	# # # delete_markdowns_directory()
	# now = datetime.now(timezone.utc)
	# save_current_scrape_time(now)
	# print("Saved scrape time:", now)

	articles = get_all_articles(max_articles=7)
	upload_delta_files(articles)
	# upload_list_files()
	# vectorstores = list_vectorstore()
	# create_list_of_vectorstore_files(client, vectorstores.data[0].id)

if __name__ == "__main__":
    main()