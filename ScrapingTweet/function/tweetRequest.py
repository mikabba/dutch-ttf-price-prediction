import re
from pprint import pprint
from datetime import datetime
import requests
import json
import ScrapingTweet.function.log


def fun(start_time,end_time, bearer_token):

    #bearer_token = "AAAAAAAAAAAAAAAAAAAADpWlgEAAAAA1kKQv%2Fp7ntXpWRxGRyYsAb1NgPI%3DhrSQwsvxZurA2aivvpRDL6TjNL3Y228TL1BooW5z7NdRZUm57o"

    environment = "dev1"
    

    # Endpoint di ricerca tweet full archive
    url = f"https://api.twitter.com/1.1/tweets/search/fullarchive/{environment}.json"
    
    # Parametri richiesta
    latitude = 48.135125
    longitude = 11.581981
    radius = 3000
    query = "(#gas OR #gasprice OR #oilgas OR #NaturalGas OR #energy) (place_country:IT OR place_country:DE OR place_country:FR) lang: en"
    
    start_time = start_time
    end_time = end_time
    params = {
        "query": query,
        "maxResults": 100,
        "fromDate": start_time,
        "toDate": end_time
    }
    log.info(query)

    # Intestazione della richiesta
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "TS",
        "Content-Type": "application/json"
    }

    # Richiesta GET
    with_next_token = True
    found_next_token = False
    n_files = []
    i = 1
    while with_next_token:

        response = requests.get(url, headers=headers, params=params)
        log.info(response)
        log.info(response.text)
        results = response.json()
        log.info(results.keys())

        if 'next' in results.keys():
            found_next_token = True
            next_token = results['next']
            params = {
                "query": query,
                "maxResults": 100,
                "fromDate": start_time,
                "toDate": end_time,
                "next": next_token
            }
        else:
            params = {
                "query": query,
                "maxResults": 100,
                "fromDate": start_time,
                "toDate": end_time
            }
            with_next_token = False

        dt = datetime.now()
        dt = f'{dt}'
        encoded_filename = f"{i}-{start_time}-{end_time}"
        with open(f'json_file/{encoded_filename}.json', 'w') as fp:
            fp.writelines(response.text)
        n_files.append(f'{encoded_filename}')
        i = i + 1
    if found_next_token:
        response = requests.get(url, headers=headers, params=params)
        log.info(response)
        log.info(response.text)
        results = response.json()
        log.info(results.keys())
        dt = datetime.now()
        dt = f'{dt}'
        # datetime.timestamp(dt)
        # encoded_filename = f"{i}-{re.sub(' ', '_', dt[:19]).replace(':', '-')}"
        encoded_filename = f"{i}-{start_time}-{end_time}"
        with open(f'json_file/{encoded_filename}.json', 'w') as fp:
            fp.writelines(response.text)
        n_files.append(f'{encoded_filename}')
    return n_files

