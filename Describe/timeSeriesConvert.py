import os, re
import pandas as pd
import numpy as np
import nltk
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
import datetime
from datetime import timezone
import matplotlib.pyplot as plt
import math

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
        nltk.download('stopwords')
        self.allPubs = [x for x in os.listdir(workdir) if x.find(".") == -1]
        self.workdir = workdir
        self.ready = False
        self.vectorizer = None
        self.sources = {}
        self.extra_stopwords = ["news", "say", "said", "told", "tell", "day", "video", "week", "state", "new", "york", "times"]
        self.colors = ["orange", "green", "red", "brown", "blue", "yellow", "pink"]
        self.bigdf = ""

    def loadArticles(self, pubList=[], dateStart = -1, dateEnd = -1, lastN=-1):
        """ load text of articles into a dictionary """
        getPubs = pubList
        if pubList == []:
            getPubs = self.allPubs

        myDate_start = dateStart
        if lastN != -1:
            myDate_start = (datetime.datetime.today()-datetime.timedelta(days=math.ceil(lastN/24))).strftime("%Y%m%d")
            print(myDate_start)

        self.articles = {}
        for pub in getPubs:
            if pub not in self.allPubs:
                print("No folder found for {}".format(pub))
                continue

            self.articles[pub] = self.loadPubArticles(pub, myDate_start, dateEnd)

    def loadPubArticles(self, publisher, dateStart=-1, dateEnd=-1):
        """ Loads articles from dateStart to dateEnd into articles as a dataframe in a dict"""

        pubPath = "{}/{}".format(self.workdir, publisher)

        myData = []

        for month in os.listdir(pubPath):
            if month.find(".") > -1:
                continue
            monthPath = "{}/{}".format(pubPath, month)

            #load each day if not outside start/end
            for day in os.listdir(monthPath):
                if int(dateStart) > -1:
                    if int(day.split("_")[1][:-4]) < int(dateStart):
                        continue
                if int(dateEnd) > -1:
                    if int(day.split("_")[1][:-4]) > int(dateEnd):
                        continue

                myData.append("{}/{}".format(monthPath, day))

        myData = pd.concat([pd.read_csv(x) for x in myData], ignore_index=True)
        myData["source"] = publisher

        return self.stemArticle(myData)


    def stemArticle(self, some_df):
        #from stemmer, get list of stemmed words
        try:
            stemmer = SnowballStemmer("english", ignore_stopwords=True)
            some_df["quickReplace"] = some_df["text"].fillna("").apply(lambda x: re.sub('[^a-z]+', " ", x.lower()))
            some_df["tokens"] = some_df["quickReplace"].apply(lambda x: [stemmer.stem(y) for y in x.split() if len (y) > 2])
            some_df["quickReplace"] = some_df["tokens"].apply(lambda x: " ".join(x))
            return some_df
        except:
            return None


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

        self.bigdf= pd.concat([self.articles[x] for x in self.articles]).fillna("")


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



    def generateCoOccurances(self, pubList = ["newyorktimes", "foxnews", "washingtonpost", "cnn", "breitbart", "abcnews", "dailycaller"], verbose=False, outdir="tmp", vectorizestyle=CountVectorizer, dateStart = -1, topK = 20):
        """ So topics are nice, but how does the 2nd level agenda setting (framing) work?
            (that might not be the right terminology; I'm not a worder)
        """

        if verbose:
            print("loading articles")
        self.loadArticles(pubList = pubList, dateStart = dateStart)

        if verbose:
            print("building bigdf")
        self.buildBigDF()

        stopwords = text.ENGLISH_STOP_WORDS.union(self.extra_stopwords)

        self.vectorizer = vectorizestyle(stop_words = stopwords)

        # get the transformed DF
        X = self.vectorizer.fit_transform(self.bigdf.quickReplace)
        X[X > 0] = 1

        coOccurance = (X.T * X)
        coOccurance.setdiag(0)
        d = coOccurance.todense()

        top_prs = np.dstack(np.unravel_index(np.argpartition(d.ravel(),-20)[:,-20:],d.shape))[0]

        vals = []
        keys = self.vectorizer.get_feature_names()
        for pair in top_prs:
            vals.append([keys[pair[0]], keys[pair[1]]])

        #So now for each day for each time period I want to math out the co-occurances!
        return vals

    def getRecentInterestingGroups(self, pubList = ["newyorktimes", "foxnews", "washingtonpost", "cnn", "breitbart", "abcnews", "dailycaller"], outdir = "docs"):
        vals =self.generateCoOccurances(dateStart=(datetime.datetime.today()-datetime.timedelta(days=1)).strftime("%Y%m%d"), )

        grps = {}
        idx = 0
        for val in vals:
            found = False
            for grp in grps:
                if val[0] in grps[grp]:
                    grps[grp].add(val[1])
                    found=True
                    continue
                elif val[1] in grps[grp]:
                    grps[grp].add(val[0])
                    found=True
                    continue

            if not found:
                grps[idx] = set()
                grps[idx].add(val[0])
                grps[idx].add(val[1])
                idx +=1

        myTargets = [x[1] for x in grps.items() if len(x[1]) < 4]
        print("targets: {}".format(myTargets))

        self.loadArticles(pubList=pubList)
        print("building bigdf2")
        self.buildBigDF()

        myTime = datetime.datetime.now(tz=timezone.utc).strftime('%Y%m%d-%H%M')
        myTime = myTime[:-1]
        myTime +="0"

        plt.close('all') #in case of zombies or something
        os.makedirs("{}/img".format(outdir), exist_ok=True)
        os.makedirs("{}/timeseries".format(outdir), exist_ok=True)

        for target_words in myTargets:
            print("making df for {}".format(target_words))
            tmp = self.bigdf[self.bigdf.tokens.apply(lambda x: len(set(x))==len(target_words|set(x)))]

            print(len(tmp))

            tmp.date = pd.to_datetime(tmp.date)
            tmp = tmp.groupby(["source", "date"]).count()["quickReplace"]

            print("making source series for {}".format(target_words))
            tmp.unstack(level=0).fillna(0).to_pickle("{}/timeseries/{}.pkl".format(outdir, "+".join(target_words)))

            print("making plot for {}".format(target_words))
            ax = tmp.unstack(level=0).fillna(0).plot(title="Frontpage mentions of {}".format("+".join(target_words)), figsize=(8,8))
            ax.set_ylabel("frontpage mentions at time")

            deleteMe = [oldFile for oldFile in os.listdir("{}/img".format(outdir)) if oldFile.endswith("+".join(target_words)+".jpg")]
            for oldFile in deleteMe:
                os.remove("docs/img/{}".format(oldFile))

            ax.figure.savefig("{}/img/{}_{}.jpg".format(outdir, myTime, "+".join(target_words)))
            plt.close('all') #close all figures



    def runCurrentDefault(self, verbose=False, outdir="docs"):
        if verbose:
            print("loading articles")
        self.loadArticles(pubList = ["newyorktimes", "foxnews", "washingtonpost", "cnn", "breitbart", "abcnews", "dailycaller"])

        if verbose:
            print("building bigdf")
        self.buildBigDF()

        if verbose:
            print("getting sims")
        self.getSimilarities(lastN = 2, vectorizestyle=TfidfVectorizer, ngramRange=(1,1))

        if verbose:
            print("getting topN")
        topN = self.getTopNWords()

        vcs = topN.melt(var_name='publisher', value_name='words')["words"].value_counts()

        myTime = datetime.datetime.now(tz=timezone.utc).strftime('%Y%m%d-%H%M')
        myTime = myTime[:-1]
        myTime +="0"
        plt.close('all') #in case of zombies or something
        os.makedirs("{}/img".format(outdir), exist_ok=True)
        os.makedirs("{}/timeseries".format(outdir), exist_ok=True)
        #for middleWord in vcs.where((vcs==2)|(vcs==3)).dropna().index: #k, this is going to be wayyy too many images, but just testing
        for middleWord in vcs.where(vcs>1).dropna().index: #k, this is going to be wayyy too many images, but just testing

            tmp = self.bigdf[self.bigdf["tokens"].apply(lambda x: (middleWord in x))].copy()
            tmp.date = pd.to_datetime(tmp.date)
            tmp = tmp.groupby(["source", "date"]).count()["quickReplace"]
            try:  #for some reason, sometimes the formatting's getting messed up
                tmp.unstack(level=0).fillna(0).to_pickle("{}/timeseries/{}.pkl".format(outdir, middleWord))
            except:
                pass
            ax = tmp.unstack(level=0).fillna(0).plot(title="Frontpage mentions of {}".format(middleWord), figsize=(8,8))
            ax.set_ylabel("frontpage mentions at time")
            try:
                deleteMe = [oldFile for oldFile in os.listdir("{}/img".format(outdir)) if oldFile.endswith(middleWord+".jpg")]
                for oldFile in deleteMe:
                    os.remove("docs/img/{}".format(oldFile))
            except:
                pass

            ax.figure.savefig("{}/img/{}_{}.jpg".format(outdir, myTime, middleWord))
            plt.close('all') #close all figures
