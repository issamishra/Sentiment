import requests
import json
import os
from django.conf import settings
#its bad practice to place your bearer token directly into the script (this is just done for illustration purposes)
with open(os.path.join(settings.BASE_DIR,'_token.txt'),'rb') as f:
    contents = f.read()

contents = contents.decode()
BEARER_TOKEN = contents
#define search twitter function
def search_twitter(query, tweet_fields, bearer_token = BEARER_TOKEN):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}

    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}".format(
        query, tweet_fields
    )
    response = requests.request("GET", url, headers=headers)

    #print(response.status_code)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()