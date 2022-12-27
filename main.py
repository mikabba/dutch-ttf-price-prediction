import requests
from bs4 import BeautifulSoup
import pandas as pd
import traceback
import re


def item_search(topic, page):
    if topic == 'geopolitics':
        source = f"https://oilprice.com/Geopolitics/Europe/Page-{page}.html"
    elif topic == 'gas':
        source = f"https://oilprice.com/Energy/Natural-Gas/Page-{page}.html"

    html = requests.get(source).text
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def visit_link(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    clean_text = re.sub(r'<[^<>]*>|\n\t', "", str(soup.find(id="article-content")))
    clean_text = re.sub(r"[^A-z\d'\$€]", " ", clean_text)
    clean_text = re.sub(r"\s{2,}", " ", clean_text)
    return clean_text


def retrieve_content(start, end, topic):
    links = []
    titles = []
    dates = []

    for page in range(start, end+1):
        print(f"{page}/{end}")
        s = item_search(topic, page)
        for e in s.find_all("div", "categoryArticle__content"):
            links.append(f"{e.a['href']}")
            titles.append(f"{e.h2.string}")
            dates.append(f"{parse_date(e.p.string)}")
    df = pd.DataFrame()
    df['DATE'] = dates
    df['TOPIC'] = topic
    df['TITLE'] = titles
    df['LINK'] = links

    contents = []
    for link in links:
        contents.append(visit_link(link))
    df['CONTENT'] = contents

    return df


def parse_date(string):
    month_dict = {"jan": "01", "feb": "02", "mar": "03", "apr": "04", "may": "05", "jun": "06",
                  "jul": "07", "aug": "08", "sep": "09", "oct": "10", "nov": "11", "dec": "12"}
    parse_date_regex = ".{3}\s\d{2},\s\d{4}"
    date_string = re.match(parse_date_regex, string).group()
    date_string = date_string.replace(",", "").lower().split()
    month, day, year = date_string
    return f"{year}-{month_dict[month]}-{day}"


if __name__ == '__main__':
    news = retrieve_content(1, 80, 'gas')
    news.to_csv("./gas_news.csv", sep=';', index=False)


