from ScrapingOilPrice.function.function_scraper_oilprice import *
from ScrapingOilPrice.function import log


def scrape_news():
    news, link_error = retrieve_content(1, 34, 'gas')
    log.info(f'FINE GAS TOPIC. LINK PROBLEMATICI: {link_error}')
    news.to_csv("./data/gas_news.csv", sep=';', index=False)
    geo_news, link_error = retrieve_content(1, 6, 'geopolitics')
    log.info(f'FINE GEOPOLITCS TOPIC. LINK PROBLEMATICI: {link_error}')
    geo_news.to_csv("./data/geopolitcs_news.csv", sep=';', index=False)
    all_news = pd.concat([news, geo_news])
    all_news.to_csv("./data/all_news.csv", sep=';', index=False)


