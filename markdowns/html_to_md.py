from bs4 import BeautifulSoup
from markdownify import markdownify as md

def clean_and_convert_html(html_body):
    soup = BeautifulSoup(html_body, "html.parser")
    for tag in soup(["nav", "footer", "script", "style", "aside", "form", "button"]):
        tag.decompose()

    clean_html = str(soup)
    markdown = md(clean_html, heading_style="ATX")
    return markdown
