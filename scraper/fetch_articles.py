import requests
from scraper.config import BASE_URL, HEADERS, AUTH
import hashlib
from pathlib import Path
import json
from slugify import slugify

def get_all_articles(max_articles):
    articles = []
    current_batch = []
    page = 1
    per_page = 20
    hash_articles = load_hash_articles()
    updated_articles = []

    # url = f"{BASE_URL}articles"
    articles_count = 0
    while len(articles) < max_articles:
        url = f"{BASE_URL}articles.json?page={page}&per_page={per_page}"
        print(f"Fetching: {url}")
        response = requests.get(url, headers=HEADERS, auth=AUTH)
        data = response.json()
        current_batch = data.get("articles", [])
        if not current_batch: 
            break
        i = 0
        for article in current_batch:
            if len(articles) >= max_articles:
                break

            title = article.get("title", "Untitled")
            body = article.get("body", "")
            slug = slugify(title)
            new_hash = hash_content(title, body)
            old_hash = hash_articles.get(slug)
            if new_hash != old_hash:
                print(f"Updated: {title}")
                hash_articles[slug] = new_hash
                updated_articles.append(article)
            elif new_hash == old_hash:
                print(f"Unchanged: {title}")
            else: 
                print(f"New article: {title}")
            articles.append(article)
        print(f"=>Collected: {len(articles)} articles")
        if data.get("next_page") is None:
            break 	 # no next page
        page += 1
    # print("ARTICLES", articles[:max_articles])
    save_hash_articles(hash_articles)

    return updated_articles 

def hash_content(title, content):
    combined = title + "\n" + content
    return hashlib.sha256(combined.encode()).hexdigest()

HASH_ARTICLES = Path("scraper/hash_articles.json")
def load_hash_articles(): 
    if HASH_ARTICLES.exists():
        with open(HASH_ARTICLES, "r") as f:
            return json.load(f)
    return {}

def save_hash_articles(hash_articles):
    with open(HASH_ARTICLES, "w") as f:
        json.dump(hash_articles, f, indent=2)


# def get_article_detail(article_id):
#     url = f"{BASE_URL}articles/{article_id}"
#     response = requests.get(url, headers=HEADERS, auth=AUTH)
#     article = response.json().get("article", {})
#     return article.get("title", "Untitled"), article.get("body", "")





          
