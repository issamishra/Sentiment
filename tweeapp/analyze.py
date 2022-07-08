import nltk
from textblob import TextBlob


def get_sentiment(query):

    data = TextBlob(query)

    s = data.sentiment

    if s[1]<=0.5:
        sub = "Fact"
    elif s[1]>0.5:
        sub = "Opinion"

    return {"polarity":(s[0]+1)/2,"subjectivity":sub}

def get_absolute_sentiment(query):

    sent_val = get_sentiment(query)

    sentiment = ''
    if 0<sent_val['polarity']<0.5:

        sentiment = "Bad"
    elif sent_val['polarity']==0.5:
        sentiment = "Neutral"
    else:
        sentiment = "Good"
    return {"polarity":sentiment}