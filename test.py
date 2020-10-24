import git, schedule, time, importlib, scraper, os
from git import Repo
import twitter_filter, multiprocessing

"""
I think I need this to be a class so that I can restart the twitter scraper daily
It can run forever without changing it but I want to be able to push updates via git
So any push will take effect the next day at 00:00 UTC
"""
class twitter_holder:

    processes = []
    def __init__(self):
        print("starting twitter scraper")
        self.processes.append(multiprocessing.Process(target=twitter_filter.run))
        for process in self.processes:
            process.start()

        print("started")

    def reset_twitter_filter(self):
        try:
            for process in self.processes:
                process.terminate()
            self.processes = []
        except:
            print("messed up the twitter process; check for zombies")
            pass

        importlib.reload(twitter_filter)
        self.processes.append(multiprocessing.Process(target=twitter_filter.run))
        for process in self.processes:
            process.start()
