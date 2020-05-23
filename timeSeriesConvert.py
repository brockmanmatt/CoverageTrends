import os, re
import pandas as pd
import numpy as np
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
import datetime
from datetime import timezone
"""

still building this, not entirely sure where I'm going with it;
the coal is:
(1) extract interesting terms (dunno what those are yet)
(2) see difference in interesting terms between publications
(3) convert into time series for each publication by coverage

"""

class wordCruncher:
    """ this'll hold a corpus of all my words and other stuff """
    workdir : str #where the scraper's been sticking the scrapes
    allPubs : list #what publications to look at
    vocab : set #thought I needed this but uh
    articles : dict #holds articles before mathing them
    bigdf : pd.DataFrame #holds all articles
    ready : bool #ready is true once bigdf is built
    vectorizer : CountVectorizer #this'll be assigned later
    sources : dict #holds dict of tfidf vals I think
    extra_stopwords : list #extra stopwords

    def __init__(self, workdir = "archived_links"):
        """ load possible publications from workdir, assumes set up workdir/pub/month """
        self.allPubs = [x for x in os.listdir(workdir) if x.find(".") == -1]
        self.workdir = workdir
        self.ready = False
        self.vectorizer = None
        self.sources = {}
        self.extra_stopwords = ["news", "say", "said", "told", "tell", "day", "video", "week", "state", "new"]


    def loadArticles(self, pubList=[], dateStart = -1, dateEnd = -1):
        """ load text of articles into a dictionary """
        getPubs = pubList
        if pubList == []:
            getPubs = self.allPubs

        self.articles = {}
        for pub in getPubs:
            if pub not in self.allPubs:
                print("No folder found for {}".format(pub))
            else:
                self.articles[pub] = self.loadPubArticles(pub, dateStart, dateEnd)

    def loadPubArticles(self, publisher, dateStart=-1, dateEnd=-1):
        """ Loads articles from dateStart to dateEnd into articles as a dataframe in a dict"""

        pubPath = "{}/{}".format(self.workdir, publisher)

        myData = []

        for month in os.listdir(pubPath):
            if month.find(".") > -1:
                continue
            monthPath = "{}/{}".format(pubPath, month)
            for day in os.listdir(monthPath):
                myData.append("{}/{}".format(monthPath, day))

        myData = pd.concat([pd.read_csv(x) for x in myData], ignore_index=True)
        myData["source"] = publisher

        return myData


    def buildBigDF(self):
        """ also sets up bigdf by concating all articles into a big df"""
        """ Also, stems everything into quickReplace column """

        """ since later I use lastN scrapes, I should include a size here so I'm not loading everything """

        self.ready= True

        try:
            if len(self.articles) == 0:
                print ("No articles loaded")
                return None
        except:
            print ("No articles loaded")
            return None
        stemmer = SnowballStemmer("english", ignore_stopwords=True)

        self.bigdf= pd.concat([self.loadPubArticles(x) for x in self.articles]).fillna("")

        stemmer = SnowballStemmer("english", ignore_stopwords=True)
        self.bigdf["quickReplace"] = self.bigdf["text"].apply(lambda x: re.sub('[^a-z]+', " ", x.lower()))
        self.bigdf["quickReplace"] = self.bigdf["quickReplace"].apply(lambda x: " ".join([stemmer.stem(y) for y in x.split() if len (y) > 2]))


        #testing["quickReplace"] = testing["text"].apply(lambda x: re.sub('[^a-z]+', " ", x.lower()))
        #testing["quickReplace"] = testing["quickReplace"].apply(lambda x: " ".join([stemmer.stem(y) for y in x.split() if len (y) > 2]))


    def getSimilarities(self, lastN = -1, vectorizestyle=TfidfVectorizer, ngramRange=(1,2)):
        """ checks cosine similarity between publications, can check just last n scrapes """

        if not self.ready:
            print("run buildBigDf first")
            return -1

        stopwords = text.ENGLISH_STOP_WORDS.union(self.extra_stopwords)

        self.vectorizer = vectorizestyle(analyzer='word', ngram_range=ngramRange, stop_words = stopwords)
        self.vectorizer.fit(self.bigdf["quickReplace"])


        sources = {}
        earliestDate = ""
        for source in self.bigdf.source.unique():

            if int(lastN) != lastN:
                print("use lastN of int > 0 plz")
                return

            if earliestDate == "":
                if lastN > 0:
                    print(lastN)
                    earliestDate = sorted(self.bigdf.date.unique())[-lastN-1]
                    print(earliestDate)

            if lastN < 1:
                X = self.vectorizer.transform(self.bigdf[self.bigdf.source==source]["quickReplace"]).sum(axis=0)
            else:
                X = self.vectorizer.transform(self.bigdf[(self.bigdf.source==source) & (self.bigdf.date > earliestDate)]["quickReplace"]).sum(axis=0)

            sources[source] = X

        self.sources = sources.copy()

        cosims = pd.DataFrame()
        for source in sources:
            for otherSource in sources:
                cosims.at[source,otherSource] = cosine_similarity(sources[source], sources[otherSource])

        cosims2 = pd.DataFrame()
        for source in cosims.columns:
            cosims2[source] = cosims.T.sort_values(by=source, ascending=False).index

        return cosims2

    def getTopNWords(self, topN = 10):
        """ get topN important words for each publication """

        if self.vectorizer == None:
            print("run something that makes the vectorizer first")
            return -1

        result = pd.DataFrame()
        for source in self.sources:
            score = [(word, self.sources[source][0, idx]) for word, idx in self.vectorizer.vocabulary_.items()]
            score =sorted(score, key = lambda x: x[1], reverse=True)
            result[source] = [x[0] for x in score[:topN]]

        return result

    def runCurrentDefault(self, verbose=False):
        if verbose:
            print("loading articles")
        self.loadArticles(pubList = ["newyorktimes", "foxnews", "washingtonpost", "cnn", "breitbart"])

        if verbose:
            print("building bigdf")
        self.buildBigDF()

        if verbose:
            print("getting sims")
        self.getSimilarities(lastN = 5, vectorizestyle=TfidfVectorizer, ngramRange=(1,1))

        if verbose:
            print("getting topN")
        topN = self.getTopNWords()

        os.makedirs("img", exist_ok=True)

        vcs = topN.melt(var_name='publisher', value_name='words')["words"].value_counts()

        myTime = datetime.datetime.now(tz=timezone.utc).strftime('%Y%m%d-%H%M')
        myTime = myTime[:-1]
        myTime +="0"

        os.makedirs("docs/img", exist_ok=True)
        for middleWord in vcs.where((vcs==2)|(vcs==3)).dropna().index: #k, this is going to be wayyy too many images, but just testing
            tmp = self.bigdf[self.bigdf["quickReplace"].apply(lambda x: x.find(middleWord) > -1)].copy()
            tmp.date = pd.to_datetime(tmp.date)
            tmp = tmp.groupby(["source", "date"]).count()["quickReplace"]
            ax = tmp.unstack(level=0).fillna(0).plot(title="Frontpage mentions of {}".format(middleWord), figsize=(8,8))
            ax.set_ylabel("frontpage mentions at time")
            ax.figure.savefig("docs/img/{}_{}.jpg".format(myTime, middleWord))
