import json
import time
import tweepy
from function import log
from function import StringManipulate
from datetime import datetime
from Class import Auth


def initialize_api():
    """
    Crea un'istanza dell'API di Twitter utilizzando il pacchetto tweepy.

    return:
        tweepy.API: Un'istanza dell'API di Twitter.

    Authors:
        Michele Abbaticchio <m.abbaticchio@studenti.poliba.it>
    """
    user = Auth.Auth()
    auth = tweepy.OAuthHandler(user.get_consumer_key(), user.get_consumer_secret())
    auth.set_access_token(user.get_access_token(), user.get_access_token_secret())
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api


def get_post_from_europe(api, query, min_date, max_date, max_post):
    """
    Recupera i post dell'area europea e in un intervallo di date specifico.
    Salva i post recuperati in un file JSON.

    :param api: oggetto di Tweepy utilizzato per accedere all'API di Twitter
    :param query: stringa contenente la query per la ricerca dei post
    :param min_date: stringa che rappresenta la data minima in formato "YYYY-MM-DD"
    :param max_date: stringa che rappresenta la data massima in formato "YYYY-MM-DD"
    :param max_post: numero massimo di post da recuperare

    Authors:
        Michele Abbaticchio <m.abbaticchio@studenti.poliba.it>
    """
    date_min_obj = datetime.strptime(min_date, "%Y-%m-%d")
    date_min_obj = date_min_obj.replace(day=date_min_obj.day + 1)
    date_max_obj = datetime.strptime(max_date, "%Y-%m-%d")
    if not api.verify_credentials():
        log.error("Le credenziali non sono valide")
    elif date_min_obj == date_max_obj:
        log.error('L\'intervallo di tempo selezionato è troppo piccolo, selezionare un max_date più grande')
    elif date_min_obj > date_max_obj:
        log.error('min_date è più grande di max_date')
    else:
        log.info("Autenticazione avvenuta")
        # latitude = 54.525961
        # longitude = 15.255119
        latitude = 48.135125
        longitude = 11.581981
        radius = 3000
        posts_string = {}
        i = 0
        try:
            rate_limit = api.rate_limit_status()
            remaining = rate_limit['resources']['search']['/search/tweets']['remaining']
            if remaining <= 1:
                sleep_time = rate_limit['resources']['search']['/search/tweets']['reset'] - int(time.time()) + 5
                log.warning(f"sleeping for {sleep_time} seconds")
                time.sleep(sleep_time)
            for tweet in tweepy.Cursor(api.search_tweets,
                                       q=query,
                                       since=min_date,
                                       until=max_date,
                                       geocode=f"{latitude},{longitude},{radius}km",
                                       lang='en',
                                       tweet_mode="extended").items(max_post):
                i = i + 1
                created_at = tweet.created_at
                name_user = {StringManipulate.preprocessing_tweet(tweet.user.name)}
                post = StringManipulate.preprocessing_tweet(tweet.full_text)
                log.info(f'[TWEET]: {created_at} {name_user} {post}')
                posts_string[i] = post.split()

            with open("file/json_posts_string.json", "w") as outfile:
                json.dump(posts_string, outfile)
                log.info(f'Creazione del file file/json_posts_string.json: {posts_string}')
        except tweepy.errors.TweepyException as e:
            log.error(e)
        except tweepy.errors.TooManyRequests as e:
            log.warning(e)
            rate_limit = api.rate_limit_status()
            sleep_time = rate_limit['resources']['search']['/search/tweets']['reset'] - int(time.time()) + 5
            log.warning(f"Esecuzione in pausa per {sleep_time} secondi")
            time.sleep(sleep_time)
