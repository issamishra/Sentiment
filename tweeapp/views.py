from django.shortcuts import redirect, render
from django.http import JsonResponse
from . import analyze
from django.contrib import messages


### importing the django User class
from django.contrib.auth.models import User

### import django authentication and login/logout function
from django.contrib.auth import authenticate,login,logout

### 
from django.contrib.auth.decorators import login_required
# Create your views here.

from .twitterapi import BEARER_TOKEN , search_twitter


@login_required(login_url='index')
def home(request):

    if request.method == 'POST':

        query = request.POST['query']
        return render(request,'home.html',analyze.get_sentiment(query))
    
    else:

        return render(request,'home.html')

@login_required(login_url='index')
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
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method=='POST':
            username = request.POST['username']
            pwd      = request.POST['password']
            user = authenticate(username=username,password=pwd)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,"Invalid Credentials")
        return render(request,'index.html')

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        name     = request.POST['name']
        pwd      = request.POST['password']

        user = User.objects.create(username=username,first_name=name)
        user.set_password(pwd)
        user.save()
        messages.success(request,"User Created successfully")
        return redirect('index')
    else:
        return redirect('index')

def signout(request):
    logout(request)
    return redirect('index')