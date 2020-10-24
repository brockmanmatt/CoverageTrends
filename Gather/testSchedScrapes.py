import git, schedule, time, importlib, os
from git import Repo
import twitter_filter, scraper
import multiprocessing

def updateRepo():
    print("pulled")

def cycle(buildPage = False):
    """ pulls github repo, runs scraper and updates github, then runs the models """
    updateRepo()
    importlib.reload(scraper)
    try:
        print("scraping")
        scraper.run(path="tmp")
    except:
        print("error with scraper")
        pass

    git_push()

def git_push(message='auto-update'):
    print("pushed")

"""
I think I need this to be a class so that I can restart the twitter scraper daily
It can run forever without changing it but I want to be able to push updates via git
So any push will take effect the next day at 00:00 UTC
"""
class twitter_holder:
    print("twitter up")


cycle()
