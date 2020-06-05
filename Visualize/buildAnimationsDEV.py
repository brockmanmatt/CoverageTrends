from wordcloud import WordCloud
import os, math
import pandas as pd
import matplotlib.pyplot as plt
import imageio

from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.animation as animation

from sklearn.feature_extraction import text


import sys
sys.path.append(".")

import Describe.timeSeriesConvert as timeSeriesConvert
from pygifsicle import optimize

def cf(*args, **kwargs):
    return "black"

class animator:

    def __init__(self):
        """ not sure where I'm going with this """
        self.df = ""
        self.extra_stopwords = ["news", "say", "said", "told", "tell", "day", "video", "week", "state", "new", "york", "times"]

    def generateWordClouds(self, inDF="", lastN=-1, windowSize=5, publications=[], out_dir="wordCloudImages", individual=False, verbose=False):
        """ takes a DF of date deliniated articles and generates a bunch of images in target folder """

        if verbose:
            print("started!")

        os.makedirs(out_dir, exist_ok=True)

        df = inDF

        if df == "":
            if verbose:
                print("Generating DF")
            tsc = timeSeriesConvert.wordCruncher()
            tsc.loadArticles(pubList=publications)
            tsc.buildBigDF()
            df = tsc.bigdf

        self.df = df

        if verbose:
            print("DF loaded")

        if len(publications) > 0:
            df = df[df.source.isin(publications)]

        if individual:
            if verbose:
                print("individual")

            targetDates = sorted(df.date.unique())

            if lastN > 0:
                targetDates = targetDates[-lastN-windowSize:]


            for dateIdx in range(len(targetDates)-windowSize):
                fig, axs = plt.subplots(nrows=math.ceil((1+len(publications))/4), ncols=min(4, 1+len(publications)), figsize=(20,2*len(publications)))

                print(dateIdx)

                tmp = df[df.date.isin(targetDates[dateIdx:dateIdx+windowSize])]

                for idx in range(len(publications)+1):
                    try:
                        #set for the overall
                        ax = axs[math.floor(idx/4), idx%4]
                        if idx ==0:
                            wordcloud = WordCloud(background_color='white', color_func=cf).generate(" ".join(tmp.text))
                            ax.imshow(wordcloud, interpolation="bilinear")
                            ax.set_title(targetDates[dateIdx+windowSize])
                            ax.axis('off')
                        else:
                            wordcloud = WordCloud(background_color='white', color_func=cf).generate(" ".join(tmp[tmp.source==publications[idx-1]].text))
                            ax.imshow(wordcloud, interpolation="bilinear")
                            ax.set_title(publications[idx-1])
                            ax.axis('off')

                    except:
                        pass

                plt.savefig("{}/{}.jpg".format(out_dir, dateIdx), bbox_inches = 'tight', pad_inches = 0)
                plt.close()


        else:
            print("Together")
            targetDates = sorted(df.date.unique())

            if lastN > 0:
                targetDates = targetDates[-lastN-windowSize:]


            for dateIdx in range(len(targetDates)-windowSize):
                fig, ax = plt.subplots(figsize=(12,12))

                print(dateIdx)
                try:
                    if verose:
                        print("DATES: {}".format(targetDates[dateIdx:dateIdx+windowSize]))
                    tmp = df[df.date.isin(targetDates[dateIdx:dateIdx+windowSize])]
                    #set for the overall
                    wordcloud = WordCloud(background_color='white', color_func=cf).generate(" ".join(tmp.text))
                    ax.imshow(wordcloud, interpolation="bilinear")
                    ax.set_title(targetDates[dateIdx+windowSize])
                    ax.axis('off')

                except Exception as e:
                    if verbose:
                        print(e)
                    pass

                plt.savefig("{}/{}.jpg".format(out_dir, dateIdx), bbox_inches = 'tight', pad_inches = 0)
                plt.close()

    def generateBarCharts(self, inDF="", lastN=-1, windowSize=5, publications=["cnn", "foxnews"], out_dir="testBuildAnimation", verbose=False, keyword="", fsize=(12,12), extra_stopwords=[]):

        stopwords = text.ENGLISH_STOP_WORDS.union(self.extra_stopwords)
        if len(extra_stopwords) > 0:
            stopwords = stopwords.union(set(extra_stopwords))

        if verbose:
            print("started!")

        os.makedirs(out_dir, exist_ok=True)

        df = inDF

        if df == "":
            if verbose:
                print("Generating DF")
            tsc = timeSeriesConvert.wordCruncher()
            tsc.loadArticles(pubList=publications)
            tsc.buildBigDF()
            df = tsc.bigdf

        if keyword != "":
            df = df[df["text"].apply(lambda x: x.lower().find(keyword.lower()) > -1)]

        self.df = df
        self.df = self.df[self.df.source.isin(publications)]

        #doing counts so using count instead of TFIDF
        vectorizer = CountVectorizer(stop_words = stopwords, ngram_range=(1,3))
        vectorizer.fit(self.df.quickReplace)

        targetDates = sorted(self.df.date.unique())

        os.makedirs(out_dir, exist_ok=True)

        prior_dfs = {} #going to save previous timesteps to see if ranking goes up

        mySources = publications

        print("Saving plots in {}".format(out_dir))

        for dateIdx in range(len(targetDates)-windowSize):
            print("{}: {}/{}".format(targetDates[dateIdx+windowSize], dateIdx, len(targetDates)-windowSize))
            tmp = self.df[self.df.date.isin(targetDates[dateIdx:dateIdx+windowSize])].copy()
            tmp["count"] = vectorizer.transform(tmp.quickReplace)

            fig, axs = plt.subplots(nrows =1, ncols=2, figsize=fsize)

            for srcIdx in range(2): # go through each of the publications, just doing 2 for now
                mySource = mySources[srcIdx]
                if verbose:
                    print(mySource)
                myWords = tmp[tmp.source==mySource]

                if len(myWords) < 1: #skip if there aren't any words to plot
                    continue

                myWords = vectorizer.transform(myWords.quickReplace)

                wordCounts = myWords.sum(axis=0)
                labels = [(word, wordCounts[0, idx]) for word, idx in vectorizer.vocabulary_.items()]

                test = pd.DataFrame(labels)
                test = test[test[1] > 0].set_index(0).sort_values(by=1)
                test["rank"] = range(len(test))[::-1]

                myTopics = test[-10:].index.to_list()

                colors = []

                """
                This calcultes if the rank went up or down
                """
                for word in myTopics:
                    new_color="black"
                    try: #might not be in old so just try
                        old_rank=prior_dfs[mySource][prior_dfs[mySource].index == word]["rank"].to_list()[0]
                        new_rank = test[test.index == word]["rank"].to_list()[0]

                        if old_rank > new_rank:
                            new_color="green"
                        if new_rank > old_rank:
                            new_color="red"
                    except: #wasn't in old list
                        pass
                    colors.append(new_color)

                if len(colors) == 0:
                    colors = ["black"]

                test[-10:][[1]]\
                    .plot.barh(legend=False, ax=axs[srcIdx], \
                               color=[colors], title="{}".format(mySource))

                prior_dfs[mySource] = test

                if srcIdx%2 ==1:
                    axs[srcIdx].invert_xaxis()
                    axs[srcIdx].yaxis.set_label_position("right")
                    axs[srcIdx].yaxis.tick_right()
                    axs[srcIdx].set(adjustable='box')



            fig.suptitle(targetDates[dateIdx+windowSize], y=.92)
            fig.savefig("{}/{}.jpg".format(out_dir, dateIdx), bbox_inches = 'tight', pad_inches = 0)
            plt.close()

    def visualizeTimePeriod(self, img_dr="wordCloudImages", outdir="animatedGIFs", vid_name="test.gif", remove=False, frameSpeed=1, subrectangles=False, palettesize=256):
        """ Create animation from frames """
        """ I want to be able to do the chart that flips from top to """
        imagePaths = sorted([int(x[:-4]) for x in os.listdir(img_dr) if x.endswith("jpg")])

        images = [img_dr + "/" + str(x) + ".jpg" for x in imagePaths]
        image_list = []

        os.makedirs(outdir, exist_ok=True)

        for file_name in images:
            try:
                print(file_name)
                image_list.append(imageio.imread(file_name))
                if remove:
                    os.remove(file_name)

            except:
                continue

        imageio.mimwrite("{}/{}".format(outdir, vid_name), image_list, duration = frameSpeed, subrectangles=subrectangles, palettesize=palettesize)
        gif_path = "{}/{}".format(outdir, vid_name)
        optimize(gif_path)


    def animate(self, dateIdx):


        targetDates = self.targetDates
        mySources = self.mySources
        prior_dfs = self.prior_dfs
        windowSize = self.windowSize
        fsize = self.fsize
        verbose = self.verbose

        print("{}: {}/{}".format(targetDates[dateIdx+windowSize], dateIdx, len(targetDates)-windowSize))
        tmp = self.df[self.df.date.isin(targetDates[dateIdx:dateIdx+windowSize])].copy()
        tmp["count"] = self.vectorizer.transform(tmp.quickReplace)

        axs = self.axs
        fig = self.fig

        for srcIdx in range(2): # go through each of the publications, just doing 2 for now
            mySource = mySources[srcIdx]
            axs[srcIdx].clear()

            if verbose:
                print(mySource)
            myWords = tmp[tmp.source==mySource]

            if len(myWords) < 1: #skip if there aren't any words to plot
                continue

            myWords = self.vectorizer.transform(myWords.quickReplace)

            wordCounts = myWords.sum(axis=0)
            labels = [(word, wordCounts[0, idx]) for word, idx in self.vectorizer.vocabulary_.items()]

            test = pd.DataFrame(labels)
            test = test[test[1] > 0].set_index(0).sort_values(by=1)
            test["rank"] = range(len(test))[::-1]

            myTopics = test[-10:].index.to_list()

            colors = []

            """
            This calcultes if the rank went up or down
            """
            for word in myTopics:
                new_color="black"
                try: #might not be in old so just try
                    old_rank=prior_dfs[mySource][prior_dfs[mySource].index == word]["rank"].to_list()[0]
                    new_rank = test[test.index == word]["rank"].to_list()[0]

                    if old_rank > new_rank:
                        new_color="green"
                    if new_rank > old_rank:
                        new_color="red"
                except: #wasn't in old list
                    pass
                colors.append(new_color)

            if len(colors) == 0:
                colors = ["black"]

            test[-10:][[1]]\
                .plot.barh(legend=False, ax=axs[srcIdx], \
                           color=[colors], title="{}".format(mySource))

            self.prior_dfs[mySource] = test

            if srcIdx%2 ==1:
                axs[srcIdx].invert_xaxis()
                axs[srcIdx].yaxis.set_label_position("right")
                axs[srcIdx].yaxis.tick_right()
                axs[srcIdx].set(adjustable='box')

        fig.suptitle(targetDates[dateIdx+windowSize], y=.92)

    def generateBarAnimations(self, inDF="", lastN=-1, windowSize=5, publications=["cnn", "foxnews"], out_dir="testBuildAnimation", fname="testing", verbose=False, keyword="", fsize=(12,12), extra_stopwords=[]):
        self.fsize = fsize
        stopwords = text.ENGLISH_STOP_WORDS.union(self.extra_stopwords)
        if len(extra_stopwords) > 0:
            stopwords = stopwords.union(set(extra_stopwords))
        self.verbose = verbose
        if verbose:
            print("started!")

        os.makedirs(out_dir, exist_ok=True)

        df = inDF

        if df == "":
            if verbose:
                print("Generating DF")
            tsc = timeSeriesConvert.wordCruncher()
            tsc.loadArticles(pubList=publications)
            tsc.buildBigDF()
            df = tsc.bigdf

        if keyword != "":
            df = df[df["text"].apply(lambda x: x.lower().find(keyword.lower()) > -1)]

        self.df = df
        self.df = self.df[self.df.source.isin(publications)]

        #doing counts so using count instead of TFIDF
        self.vectorizer = CountVectorizer(stop_words = stopwords, ngram_range=(1,3))
        self.vectorizer.fit(self.df.quickReplace)

        targetDates = sorted(self.df.date.unique())

        os.makedirs(out_dir, exist_ok=True)

        prior_dfs = {} #going to save previous timesteps to see if ranking goes up

        mySources = publications

        print("Saving plots in {}".format(out_dir))

        self.targetDates = targetDates
        self.mySources = mySources
        self.prior_dfs = prior_dfs
        self.windowSize = windowSize
        fig = plt.figure(figsize=(10,10))

        #for dateIdx in range(len(targetDates)-windowSize):

        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=6, metadata=dict(artist='Me'), bitrate=1800)

        fig, axs = plt.subplots(nrows =1, ncols=2, figsize=fsize)
        self.axs = axs
        self.fig = fig

        ani = animation.FuncAnimation(fig, self.animate, frames=(len(targetDates)-windowSize), repeat=False)

        ani.save('{}/{}.mp4'.format(out_dir, fname), writer=writer)
