import os, datetime, sys
import tweepy
import json, requests
import pandas as pd
import datetime
import time
from datetime import timezone


"""
quick line to unshorten url from
https://stackoverflow.com/questions/7153096/how-can-i-un-shorten-a-url-using-python/7153185#7153185
"""
def unshorten_url(url):
    try:
        return requests.head(url, allow_redirects=True).url
    except:
        return "-1"
"""
Loads names to scrape from xlsx file
"""
def loadNames():
    tmp = pd.read_excel("NewsSites.xlsx")
    nameDict.update(tmp[["TwitterAccount", "TwitterID"]].set_index("TwitterAccount", drop=True).to_dict()["TwitterID"])
    return nameDict

"""
extracts text content from a tweet as well as urls
"""
def getText(status, verbose=False):
    myText = ""

    isRetweet = False
    isShort = False

    myURL = ""

    try:
        retweeted = status["retweeted_status"]
        myText += "RT @"
        myText += retweeted["user"]["screen_name"] + ": "
        try:
            myText += retweeted["extended_tweet"]["full_text"]
            myURL = retweeted["extended_tweet"]["entities"]["urls"][0]["url"]
        except:
            myText += retweeted["text"]
            if len(retweeted["entities"]["urls"]) > 0:
                myURL = retweeted["entities"]["urls"][0]["url"]
    except:
        try:
            myText = status["extended_tweet"]["full_text"]
            myURL = status["extended_tweet"]["entities"]["urls"][0]["url"]

        except:
            #print ("no extended tweet")
            #print(status)
            myText = status["text"]
            if len(status["entities"]["urls"]) > 0:
                myURL = status["entities"]["urls"][0]["url"]

    if myURL != "":
        myURL = unshorten_url(myURL)
    if verbose:
        print (myText)
    return (myText, myURL)

def saveToCSV(status, name):

    savePath = "archived_tweets"

    myDate = datetime.datetime.now(tz=timezone.utc).strftime('%Y%m%d')
    myMonth = datetime.datetime.now(tz=timezone.utc).strftime('%Y%m')

    os.makedirs("{}/{}/{}/".format(savePath, name, myMonth), exist_ok=True)

    text, url = getText(status)
    print("text: {}".format(text))
    print("url: {}".format(url))

    myID = status["id"]

    tmp = pd.DataFrame([{"name":name, "text":text, "id": myID, "url":url}])

    if not os.path.isfile("{}/{}/{}/{}_{}.csv".format(savePath, name, myMonth,name, myDate)):
        tmp.to_csv("{}/{}/{}/{}_{}.csv".format(savePath, name, myMonth,name, myDate))
    else:
        tmp.to_csv("{}/{}/{}/{}_{}.csv".format(savePath, name, myMonth,name, myDate), mode='a', header=False)


#this is the actual thing that does the tweet listening
class CustomStreamListener(tweepy.StreamListener):

    #when a tweet is found, print the info for the tweet
    def on_status(self, status):
        try:
            #there doesn't seem to be a better way to filter out replies; I'm checking if the tweeter is the account tweeted at
            if status.author.screen_name in nameDict.keys():
                saveToCSV(status._json, status.author.screen_name)

        except Exception as e:
            print("error")
            pass

    def on_error(self, status_code):
        #401 means your API keys are bad
        #406 means your twitter IDs are bad
        print ('Encountered error with status code:', status_code)
        return True # Don't kill the stream
    def on_timeout(self):
        print ('Timeout...')
        return True # Don't kill the stream

"""
import keys from json file (make it yourself)
"""
def import_credentials(credPath):
    try:
        with open(credPath, 'r') as infile:
            keys = json.load(infile)

        CONSUMER_KEY = keys["CONSUMER_KEY"]
        CONSUMER_SECRET = keys["CONSUMER_SECRET"]
        ACCESS_TOKEN = keys["ACCESS_TOKEN"]
        ACCESS_TOKEN_SECRET = keys["ACCESS_TOKEN_SECRET"]

    except:
        print ("The Twitter API requires the following four keys:")
        print("Consumer Key, Consumer Secret Key, Access Token, Access Token Secret")
        print ("Please enter Twitter Consumer Key")
        CONSUMER_KEY = input()
        print ("Please enter Twitter Consumer Secret Key")
        CONSUMER_SECRET = input()
        print ("Please enter Twitter Access Token")
        ACCESS_TOKEN = input()
        print ("Please enter Twitter Access Token Secret")
        ACCESS_TOKEN_SECRET = input()
    #connects to tweepy which handles the tweeting
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return auth

def initiate_api(credentials, verbose=False):
    api = tweepy.streaming.Stream(credentials, CustomStreamListener(), timeout=60)
    target = []
    for i in nameDict:
        target.append(str(nameDict[i]))
    if verbose:
        print(target)
    api.filter(follow=target)

verbose = False
nameDict = {}
def run(verbose=False):
    verbose=verbose
    time.sleep(5)
    attempts = 100
    while True:
        try:
            if verbose:
                print("importing creds")
            step = "importing Twitter credentials"
            credentials = import_credentials("twitter_keys.json")
            step = "importing names"
            nameDict = loadNames()
            if verbose:
                print("initiating api")

            step = "initiating Twitter API"
            initiate_api(credentials, verbose=verbose)
            step = "running"
        except Exception as e:
            print("broke on {} relooping".format(step))
            time.sleep(10)

if __name__ == "__main__":
    run(verbose=True)
