import csv
import time
from html import unescape
import requests
from bs4 import BeautifulSoup
import pandas as pd
import traceback
import re
from function import log


def item_search(topic, page):
    log.info(f'{topic} {page}')
    if topic == 'geopolitics':
        source = f"https://oilprice.com/Geopolitics/Europe/Page-{page}.html"
    elif topic == 'gas':
        source = f"https://oilprice.com/Energy/Natural-Gas/Page-{page}.html"

    html = requests.get(source).text
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def visit_link(url):

    log.info('visit_link')
    html = requests.get(url)
    status_code = html.status_code
    log.info(html.status_code)
    if html.status_code == 200:
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'html.parser')
        article_title_date_soup = soup.find("div", 'singleArticle__content')
        article_title_soup = article_title_date_soup.find_all("h1")
        article_title_text = article_title_soup[0].text
        log.info(article_title_text)
        article_date = article_title_date_soup.span.text.split(" - ")[1]
        date = str(article_date)[:12]
        log.info(date)
        article_content_soup = soup.find(id="article-content")
        if article_content_soup is None:
            article_content_soup = soup.find(id="news-content")
        article_p_soup = article_content_soup.find_all("p")
        related_links = []

        # Preleva tutti i link correlati all'articolo
        for p in article_content_soup.find_all("p"):
            if p.text == 'More Top Reads From Oilprice.com:':
                next_ul = p.find_next_sibling("ul")
                if next_ul:
                    for li in next_ul.find_all("li"):
                        a = li.find("a")
                        if a and not re.match("^https?://", a["href"]):
                            related_links.append(a["href"])

        # Rimuove i paragrafi indesiderati
        for p in article_p_soup:
            if p.text == 'More Top Reads From Oilprice.com:':
                previous_p = p.find_previous_sibling("p")
                previous_p.decompose()
                p.decompose()

            if p.text == 'ADVERTISEMENT':
                p.decompose()

        article_content = str(article_p_soup)
        # Espressione regolare che rimuove i tag HTML
        clean_text = re.sub(r'<[^<>]*>|\n\t', "", article_content)
        # Espressione regolare che rimuove la punteggiatura. Nel caso in cui ci sono numeri relativi (con il punto), non è
        # rimosso il punto. Nel caso in cui ci sono numeri >= 1000 (con la virgola es. 1,000), la virgola è rimossa.
        clean_text = re.sub(r'[\[\]\(\)\{\}]', '', clean_text)
        clean_text = re.sub(r'[,:\";\/\\]', '', clean_text)
        clean_text = re.sub(r"(?!\d)[.](?!\d\b)", "", clean_text)
        # Espressione regolare che rimuove i link.
        clean_text = re.sub(r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)", "",
                            clean_text)

        # Espressione regolare che sostituisce qualsiasi gruppo di spazi consecutivi con un singolo spazio
        clean_text = re.sub(r"\s{2,}", " ", clean_text)

        clean_text = re.sub(r'[^a-zA-Z0-9 €$%.]+', '', clean_text)
        clean_title = re.sub(r'[^a-zA-Z0-9 €$%.]+', '', article_title_text)
        log.info(clean_text)
        log.info(related_links)
        return clean_text, date, clean_title, related_links, status_code
    else:
        return '','','','',status_code


def visit_related_link(url):
    # TODO: NON ESCONO GLI APOSTROFI
    log.info('visit_related_link')
    log.info(url)
    try:
        html = requests.get(url)
        status_code = html.status_code
        log.info(html.status_code)
        if html.status_code == 200:
            html_text = requests.get(url).text
            soup = BeautifulSoup(html_text, 'html.parser')
            article_title_date_soup = soup.find("div", 'singleArticle__content')
            article_title_soup = article_title_date_soup.find_all("h1")
            article_title_text = article_title_soup[0].text
            log.info(article_title_text)
            article_date = article_title_date_soup.span.text.split(" - ")[1]
            date = str(article_date)[:12]
            log.info(date)
            article_content_soup = soup.find(id="article-content")
            if article_content_soup is None:
                article_content_soup = soup.find(id="news-content")
            article_p_soup = article_content_soup.find_all("p")
            # Rimuove i paragrafi indesiderati
            for p in article_p_soup:
                if p.text == 'More Top Reads From Oilprice.com:':
                    previous_p = p.find_previous_sibling("p")
                    previous_p.decompose()
                    p.decompose()

                if p.text == 'ADVERTISEMENT':
                    p.decompose()

            article_content = str(article_p_soup)
            # Espressione regolare che rimuove i tag HTML
            clean_text = re.sub(r'<[^<>]*>|\n\t', "", article_content)
            # Espressione regolare che rimuove la punteggiatura. Nel caso in cui ci sono numeri relativi (con il punto), non è
            # rimosso il punto. Nel caso in cui ci sono numeri >= 1000 (con la virgola es. 1,000), la virgola è rimossa.
            clean_text = re.sub(r'[\[\]\(\)\{\}]', '', clean_text)
            clean_text = re.sub(r'[,:\";\/\\]', '', clean_text)
            clean_text = re.sub(r"(?!\d)[.](?!\d\b)", "", clean_text)
            # Espressione regolare che rimuove i link.
            clean_text = re.sub(r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)", "",
                                clean_text)

            # Espressione regolare che sostituisce qualsiasi gruppo di spazi consecutivi con un singolo spazio
            clean_text = re.sub(r"\s{2,}", " ", clean_text)

            clean_text = re.sub(r'[^a-zA-Z0-9 €$%.]+', '', clean_text)
            clean_title = re.sub(r'[^a-zA-Z0-9 €$%.]+', '', article_title_text)
            log.info(clean_text)

            return clean_text, date, clean_title,status_code
        else:
            return '','','',status_code
    except ValueError as e:
        raise Exception(f"Errore durante lo scaping relativo all'url: {url}. More detail: ") from e


def retrieve_content(start, end, topic):
    link_error = []
    links_work = []
    titles = []
    dates = []

    # for page in range(start, end+1):
    for page in range(start, end+1):
        log.info(f"{page}/{end}")
        s = item_search(topic, page)
        for e in s.find_all("div", "categoryArticle__content"):
            links_work.append(f"{e.a['href']}")

    links = []
    contents = []
    i = 1
    num_links = len(links_work)
    log.info(num_links)

    for link_assignment in links_work:
        links.append(link_assignment)
    with open(f'{topic}_news_work.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['DATE', 'TOPIC', 'TITLE', 'LINK','CONTENT'])
        for link in links_work:
            log.info(f'Links work: {len(links_work)}')
            log.info(f'Links official: {len(links)}')
            log.info(i)
            if i <= num_links:
                try:
                    content, date,title, related_links,status_code = visit_link(link)
                    if status_code == 200:
                        dates.append(parse_date(date))
                        titles.append(title)
                        contents.append(content)
                        writer.writerow([date, topic, title, link, content])
                        for related_link in related_links:
                            if f"https://oilprice.com{related_link}" not in links_work:
                                links_work.append(f"https://oilprice.com{related_link}")
                                links.append(f"https://oilprice.com{related_link}")
                    else:
                        links.remove(link)
                        continue

                except ValueError as e:
                    log.error(e)
                    log.error(f'Link che ha generato errore:{link}')
                    link_error.append(link)
                    links.remove(link)
                    time.sleep(60)
            else:
                try:
                    content, date, title, status_code = visit_related_link(link)
                    if status_code == 200:
                        dates.append(parse_date(date))
                        titles.append(title)
                        contents.append(content)
                        writer.writerow([date, topic, title, link, content])
                    else:
                        log.warning(f'{link} - {status_code}')
                        links.remove(link)
                        continue
                except ValueError as e:
                    log.error(e)
                    log.error(f'Link che ha generato errore:{link}')
                    link_error.append(link)
                    links.remove(link)
                    time.sleep(60)

            i = i + 1

    df = pd.DataFrame()
    df['DATE'] = dates
    df['TOPIC'] = topic
    df['TITLE'] = titles
    df['LINK'] = links
    df['CONTENT'] = contents

    return df,link_error


def parse_date(string):
    month_dict = {"jan": "01", "feb": "02", "mar": "03", "apr": "04", "may": "05", "jun": "06",
                  "jul": "07", "aug": "08", "sep": "09", "oct": "10", "nov": "11", "dec": "12"}
    parse_date_regex = ".{3}\s\d{2},\s\d{4}"
    date_string = re.match(parse_date_regex, string).group()
    date_string = date_string.replace(",", "").lower().split()
    month, day, year = date_string
    return f"{year}-{month_dict[month]}-{day}"