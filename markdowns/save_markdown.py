import os
from slugify import slugify
import shutil 
from scraper.fetch_articles import get_all_articles, get_article_detail
from markdowns.html_to_md import clean_and_convert_html

OUTPUT_DIR = os.path.join("markdowns", "md_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def write_articles_to_markdown(articles):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")
    else: 
        print(f"Directory already exists: {OUTPUT_DIR}")
    for i, article in enumerate(articles):
        article_id = article["id"]
        title, html_body = get_article_detail(article_id)

        markdown = clean_and_convert_html(html_body)
        slug = slugify(title)

        file_path = os.path.join(OUTPUT_DIR, f"{slug}.md")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")
            f.write(markdown)

        print(f"[{i+1}] Saved: {file_path}")


def delete_markdowns_directory():
	if os.path.exists(OUTPUT_DIR):
		shutil.rmtree(OUTPUT_DIR)
		print(f"Deleted directory: {OUTPUT_DIR}")
	else:
		print(f"Directory does not exist: {OUTPUT_DIR}")
          