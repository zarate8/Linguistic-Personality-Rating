# For tutorial go to https://www.youtube.com/watch?v=pUUxmvvl2FE

from __future__ import absolute_import, print_function
import sys

#tweepy
import tweepy
import json

from credentials.credentials import getConsumerKey
from credentials.credentials import getConsumerSecret
from credentials.credentials import getAccessToken
from credentials.credentials import getAccessSecret
from RatingSystemFiles.xml_parser import get_categories
from RatingSystemFiles.personality_calc import rate_tweet
from RatingSystemFiles.trait_definitions import getDefinitions

consumer_key = getConsumerKey()
consumer_secret = getConsumerSecret()
access_token = getAccessToken()
access_secret = getAccessSecret()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


# Get the location and map it to the word count of the tweet                                                                                                  
def map_to_count(s):
        word_list = s.split(' ')
        result_d = dict([])
        for word in word_list:
                word = word.lower()
                if(word in result_d):
                        result_d[word] += 1
                else:
                        result_d[word] = 1
        return (result_d)

def save_handler(user_handler):
    with open('RatingSystemFiles/rated_history.txt', 'r+') as f:
        #import pdb; pdb.set_trace()
        for l in f:
            if(user_handler in l):
                return    
        f.write(user_handler+"\n")


# Gets the tweets from the specified userhandler
# throws an exception if the user_handler is not valid.
def getTweets(user_handler):
    
    stuff = api.user_timeline(screen_name = user_handler, count = 500, include_rts = True)

    tweets = ''
    for s in stuff:
        status = s
        
        jsonStr = json.dumps(status._json)
        j = json.loads(jsonStr)
        t = j['text']
        print (t)
        tweets += t

    clean_tweets = tweets.encode('ascii', 'ignore').decode('ascii')
    
    save_handler(user_handler)
            
    #with open('rated_history.txt', 'a') as f:
    #    f.write(user_handler+"\n")

    return clean_tweets


def findMax(rating):
    max = ('ps', rating['ps'])
    #import pdb; pdb.set_trace()
    #for r in rating:
    for key, value in rating.items():
        if max[1] < value:
            max = (key, value)      
    return max[0]


def rateTweets(user_handler):
    cats = get_categories()
    #tweets = getTweets('villordoos')

    try:
	    tweets = getTweets(user_handler)
	    
	    map_tweets = map_to_count(tweets)
	    print ("\n\n\t")
    #print (getDefinitions())

	    rating = rate_tweet(map_tweets, cats)
    
	    print ('\n\n')
    #print (findMax(rating))
	    max_rtng = findMax(rating)
	    definition = getDefinitions()[max_rtng]
	    print (definition)
	    print ('\n\n')

	    print (rating)
	    print ("\n\n")
    except tweepy.TweepError:
	    print ('Error: You possibly provided the wrong username or are not allowed to view this person\'s profile!')


if len(sys.argv) > 1:
    rateTweets(sys.argv[1])
else:
    print ('\n\n\tMust provide a user hanlder as a parameter to rate\n\n')
    print ('\ti.e. EvaluateTweets.py @myUserName\n\n')
