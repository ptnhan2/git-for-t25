from scraper import fetch_articles
from markdowns.save_markdown import write_articles_to_markdown
from scraper.scrape_state import parse_z_isoformat 
def detect_updated(articles, last_scrape_time):
    result = []
    for article in articles:
        if "updated_at" not in article:
            continue 
        updated_time = parse_z_isoformat(article["updated_at"])

        if updated_time > last_scrape_time:
            print("updated_time > last_scrape_time")
            result.append(article)
    return result
    
def detect_new(articles, last_scrape_time):
    result = []
    for article in articles:
        if "created_at" not in article:
            continue 
        updated_time = parse_z_isoformat(article["created_at"])

        if updated_time > last_scrape_time:
            print("updated_time > last_scrape_time")
            result.append(article)
    return result

