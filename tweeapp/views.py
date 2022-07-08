from django.shortcuts import redirect, render
from django.http import JsonResponse
from . import analyze
# Create your views here.

from .twitterapi import BEARER_TOKEN , search_twitter

def home(request):

    if request.method == 'POST':

        query = request.POST['query']
        return render(request,'home.html',analyze.get_sentiment(query))
    
    else:

        return render(request,'home.html')


def get_tweets(request):

    if request.method=='POST':
        tweet_fields = "tweet.fields=text"
        query = request.POST['query']
        #twitter api call
        content = dict()
        if not len(query)==0:
            json_response = search_twitter(query=query, tweet_fields=tweet_fields, bearer_token=BEARER_TOKEN)

            

            if json_response['meta']['result_count']>0:
                for i,t in enumerate(json_response['data']):
                    content.update({i:{'tweet':t['text'],'sent':analyze.get_absolute_sentiment(t['text'])}})
            else:
                content.update({1:"No Tweet Found"})
        else:
            content.update({1:"No Query Entered"})
        return render(request,'tweet.html',{'content':content})
    else:
        return redirect('home')

def index(request):
    return render(request,'index.html')
