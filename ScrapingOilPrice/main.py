from function.function_scraper_oilprice import *
from function import log


news,link_error = retrieve_content(1, 34, 'gas')
log.info(f'FINE GAS TOPIC. LINK PROBLEMATICI: {link_error}')
news.to_csv("gas_news.csv", sep=';', index=False)
news,link_error = retrieve_content(1, 6, 'geopolitics')
log.info(f'FINE GEOPOLITCS TOPIC. LINK PROBLEMATICI: {link_error}')
news.to_csv("geopolitcs_news.csv", sep=';', index=False)
