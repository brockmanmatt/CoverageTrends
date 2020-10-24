"""
K, so I'm not sure exactly where I'm going here but I guess I want to have a dataframe that's loaded
And then I can do stuff with it! Now really, I should be doing that all along =/

I think maybe I've been trading off functionality for being able to update every 30 minutes vs.
holding longer term structures that I can do things with.

This is going to replicate the functionality of timeSeriesConvert but I want it to be cleaner
"""

class Wranger:

    def __init__(self, workdir = "archived_links"):
        self.workdir = workdir


    def loadArticles(self, pubList=[], dateStart = -1, dateEnd = -1, lastN=-1):
        return False
