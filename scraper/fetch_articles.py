import requests
import hashlib
from pathlib import Path
import json
from slugify import slugify

HEADERS = {
	"Content-Type": "application/json",
}
def get_all_articles(max_articles, BASE_URL):

    articles = []
    current_batch = []
    page = 1
    per_page = 20
    hash_articles = load_hash_articles()
    delta_articles = []
    articles_count = 0
    added = 0
    updated = 0
    skipped = 0
    while len(articles) < max_articles:
        url = f"{BASE_URL}articles.json?page={page}&per_page={per_page}"
        print("-----------------------------------------")
        print(f"Fetching: {url}")
        print("-----------------------------------------")
        response = requests.get(url, headers=HEADERS)
        data = response.json()
        current_batch = data.get("articles", [])
        if not current_batch: 
            break

        for article in current_batch:
            if len(articles) >= max_articles:
                break

            title = article.get("title", "Untitled")
            body = article.get("body", "")
            slug = slugify(title)
            new_hash = hash_content(title, body)
            
            old_hash = hash_articles.get(slug)            
            if old_hash is None:
                print(f"New article: {title}")
                added += 1
                hash_articles[slug] = new_hash
                delta_articles.append(article)
            elif new_hash != old_hash:
                print(f"Updated: {title}")
                updated += 1
                hash_articles[slug] = new_hash
                delta_articles.append(article)
            else:
                print(f"Unchanged: {title}")
                skipped += 1
            articles.append(article)
        if data.get("next_page") is None:
            break 	 # no next page
        page += 1
    save_hash_articles(hash_articles)
    print("-----------------------------------------")
    print(f"=>Collected: {len(articles)} articles")
    print("-----------------------------------------")
    return delta_articles, added, updated, skipped

def hash_content(title, content):
    combined = title + "\n" + content
    return hashlib.sha256(combined.encode()).hexdigest()

HASH_ARTICLES = Path("json/hash_articles.json")
HASH_ARTICLES.parent.mkdir(parents=True, exist_ok=True)
def load_hash_articles(): 
    if HASH_ARTICLES.exists():
        with open(HASH_ARTICLES, "r") as f:
            return json.load(f)
    return {}

def save_hash_articles(hash_articles):
    with open(HASH_ARTICLES, "w") as f:
        json.dump(hash_articles, f, indent=2)





          
