from fastai.text import *
from sklearn.model_selection import train_test_split
import os
import numpy as np

class ulmfitter:
    """ only run me with a GPU """

    def __init__(self, workdir = "archived_links", outdir = "tmp"):
        """ initialize with location of my articles and outdir """
        self.workdir = workdir
        self.outdir = outdir
        self.bigdf = ""
        self.ArticlesLoaded = False
        self.clf = ""


    def loadArticles(self, pubList=[], outdir = ""):
        """ generates the dataframe and label """

        allArticles = {}
        publishers = [x for x in os.listdir(self.workdir) if x.find(".") == -1]
        for publisher in publishers:
            if len(pubList) > 0:
                if publisher not in pubList:
                    continue
            articles = []
            publisherDir = "{}/{}".format(self.workdir, publisher)
            for month in [x for x in os.listdir(publisherDir) if x.find(".") == -1]:
                monthDir = "{}/{}".format(publisherDir, month)
                for day in os.listdir(monthDir):
                    if day.endswith(".csv"):
                        articles.append("{}/{}".format(monthDir, day))

            articles = pd.concat([pd.read_csv(x) for x in articles], ignore_index=True)
            articles["source"] = publisher
            allArticles[publisher] = articles.drop_duplicates(subset="text", keep='first', inplace=False)
            allArticles[publisher].date = allArticles[publisher].date.apply(lambda x: x.split("-")[0])
            allArticles[publisher]["label"] = allArticles[publisher]["source"] + "_" + allArticles[publisher]["date"]
            allArticles[publisher] = allArticles[publisher][["text", "label"]]


        if len(articles) > 1:
            self.bigdf= pd.concat([allArticles[x] for x in allArticles]).fillna("")
        else:
            self.bigdf = articles[list(allArticles.keys())[0]]
        self.ArticlesLoaded = True

        if outdir == "":
            return

        os.makedirs(outdir, exist_ok=True)
        self.bigdf.to_pickle("{}/bigdf.pkl".format(outdir))



    def setUpSets(self, outdir=""):
        """ creates the train:validation:test dataframe """

        if not self.ArticlesLoaded:
            print("load articles first")
            return

        self.train, self.test = train_test_split(self.bigdf, test_size=0.30, random_state=42)
        self.train, self.valid = train_test_split(self.train, test_size=0.50, random_state=42)

        if outdir == "":
            return
        os.makedirs(outdir, exist_ok=True)
        self.train.to_pickle("{}/train.pkl".format(outdir))
        self.valid.to_pickle("{}/valid.pkl".format(outdir))
        self.test.to_pickle("{}/test.pkl".format(outdir))

        print("sets saved")


    def loadSets(self, indir=""):
        """ load train, test, and validation sets """

        if indir=="":
            print("specify folder")
            return -1

        self.train = pd.read_pickle("{}/train.pkl".format(indir))
        self.valid = pd.read_pickle("{}/valid.pkl".format(indir))
        self.test = pd.read_pickle("{}/test.pkl".format(indir))

        print("sets loaded")


    def setupEmbeddings(self, path = "awd_lm"):
        """ fine tune features for awd_listm a few times"""
        try:
            data_lm = TextLMDataBunch.from_df(path, train_df=self.train, valid_df=self.valid,\
            text_cols = "text", label_cols = "label")
        except:
            print("error creating LM")
            return

        learn = language_model_learner(data_lm, arch=AWD_LSTM, drop_mult=.25)
        learn.fit_one_cycle(1, 1e-2)
        learn.save_encoder('ft_enc_1')

        learn.unfreeze()
        learn.fit_one_cycle(3, 1e-3)
        learn.save_encoder('ft_enc_1')

        learn.unfreeze()
        learn.fit_one_cycle(5, 5e-4)
        learn.save_encoder('ft_enc_1')

        print("feature encoding saved")


    def train_classifier(self, path = "awd_lm"):
        """ train classifier """

        data_lm = TextLMDataBunch.from_df(path, train_df=self.train, valid_df=self.valid,\
    text_cols = "text", label_cols = "label")

        data_clas = TextClasDataBunch.from_df(path, train_df=self.train, valid_df=self.valid, test_df=self.test, \
    vocab=data_lm.train_ds.vocab, label_cols = "label", text_cols="text", bs=32)

        learn = text_classifier_learner(data_clas, arch=AWD_LSTM, drop_mult=.25)
        learn.load_encoder('ft_enc_1')

        learn.fit_one_cycle(1, 1e-2)
        learn.freeze_to(-2)
        learn.fit_one_cycle(6, slice(5e-3/2., 5e-3))
        learn.save("awd_lstm_trained")

        self.clf = learn

    def predict_test_set(self, outdir = ""):
        if self.clf == "":
            print("no classifier loaded")
            return
        classes = self.clf.data.classes
        preds, _ = self.clf.get_preds(ds_type=DatasetType.Test)
        self.test["predicted"] = preds
        self.test["predicted"] = self.test["predicted"].apply(lambda x: classes[np.argmax(x)])
        os.makedirs(outdir, exist_ok=True)
        self.test.to_pickle("{}/predictions.pkl".format(outdir))
        return self.test

    def runMeDefault(self, pubList = []):
        if pubList == "default"
            pubList = ["newyorktimes", "foxnews", "washingtonpost", "cnn", "breitbart", "abcnews", "dailycaller"]
        self.loadArticles(pubList = pubList, outdir="test")
        self.setUpSets(outdir="test")
        self.setupEmbeddings(path="test")
        self.train_classifier(path="test")
        self.predict_test_set(outdir="test")
