import requests
from scraper.config import BASE_URL, HEADERS, AUTH

def get_all_articles(max_articles):
    articles = []
    page = 1
    per_page = 20
    # url = f"{BASE_URL}articles"
    while len(articles) < max_articles:
        url = f"{BASE_URL}articles.json?page={page}&per_page={per_page}"
        print(f"Fetching: {url}")
        response = requests.get(url, headers=HEADERS, auth=AUTH)
        data = response.json()
        current_article = data.get("articles", [])
        if not current_article: 
            break
        articles.extend(current_article)
        print(f"=>Collected: {len(articles)} articles")
        if data.get("next_page") is None:
            break 	 # no next page
        page += 1
    return articles  
def get_article_detail(article_id):
    url = f"{BASE_URL}articles/{article_id}"
    response = requests.get(url, headers=HEADERS, auth=AUTH)
    article = response.json().get("article", {})
    return article.get("title", "Untitled"), article.get("body", "")





          
