import requests
from bs4 import BeautifulSoup
import pandas as pd
import traceback
import re

links = []
titles = []
for page in range(1, 26):
    print(page)
    site = "https://www.worldoil.com/"
    stocknews = f"{site}/topics/europe/?page={page}"
    html = requests.get(stocknews).text
    soup = BeautifulSoup(html, 'html.parser')
    for e in soup.find_all("div", "topic-title"):
        links.append(f"{site}{e.a['href']}")

texts = []
tkns = []
for link in links:
    html = requests.get(link).text
    soup = BeautifulSoup(html, 'html.parser')
    article = soup.find("div", "news-detail-content content-body")
    text = " ".join(re.findall(r"(?<=<p>).*(?=<\/p>)", str(article)))
    clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
    texts.append(clean_text)
    tokens = clean_text.split()
    tkns.append(tokens)

df = pd.DataFrame()
df['links'] = links
df['text'] = texts
df['tokens'] = tkns

df.to_csv("./text_news.csv")


