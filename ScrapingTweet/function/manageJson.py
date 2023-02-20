import datetime
from pprint import pprint
from datetime import date
from Service import PostService
import json
from function import StringManipulate as sm
from function import log

def manage(name_file_json):
    posts_string = {}
    i = 0
    with open(f'json_file/{name_file_json}.json', 'r') as file:
        results_json = json.load(file)
        results = results_json['results']

        for result in results:
            created_at = result['created_at']
            created_at = datetime.datetime.strptime(created_at, "%a %b %d %H:%M:%S +0000 %Y")
            created_at = f'{created_at}'
            if 'extended_tweet' in result.keys():
                post = result['extended_tweet']['full_text']
                post = sm.preprocessing_tweet(post)
                # log.info(f'[Tweet] {created_at[:10]} : {post}\n')
            else:
                post = result['text']
            posts_string[i] = [post, created_at[:10]]
            # posts_string[i] = [post, created_at]
            i = i + 1


    # pprint(posts_string)
    with open(f'json_result/{name_file_json}.json','w') as fp:
        json.dump(posts_string,fp)











