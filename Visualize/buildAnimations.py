from wordcloud import WordCloud
import os, math
import pandas as pd
import matplotlib.pyplot as plt
import imageio

import sys
sys.path.append(".")

import Describe.timeSeriesConvert as timeSeriesConvert
from pygifsicle import optimize

def cf(*args, **kwargs):
    return "black"

class wordCloudMaker:

    def __init__(self):
        """ not sure where I'm going with this """
        self.df = ""

    def test(self):
        return 1

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

    def generateBarCharts(self, inDF="", lastN=-1, windowSize=5, publications=[], out_dir="wordCloudImages", individual=False, verbose=False):
        return -1

    def visualizeTimePeriod(self, img_dr="wordCloudImages", outdir="animatedGIFs", vid_name="test.gif", remove=False):
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

        imageio.mimwrite("{}/{}".format(outdir, vid_name), image_list, duration = 1)
        gif_path = "{}/{}".format(outdir, vid_name)
        optimize(gif_path)
