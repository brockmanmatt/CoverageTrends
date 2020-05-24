import os
import pandas as pd

import statsmodels.api as sm
from statsmodels.tsa.api import VAR
import datetime
import matplotlib.pyplot as plt
from pmdarima import auto_arima
import numpy as np

import warnings
warnings.filterwarnings("ignore")


class modelBuilder:
    """ build models for time series
    for now, just fiting to training data; will truncate last day starting next week for testing as well
    (there isn't enough desting data)
    """


    targetPaths : list #list of paths to target time series
    targetDir : str

    def __init__(self, workdir = "docs/timeseries", outdir="docs/models"):
        """ initializing building a list of all the pkls in workdir"""
        self.targetPaths = []
        for filename in os.listdir(workdir):
            if filename.endswith(".pkl"):
                self.targetPaths.append("{}/{}".format(workdir, filename))
        self.targetDir = outdir
        os.makedirs(outdir, exist_ok=True)

    def buildModels(self):
        """ build a model for each target in targetPaths using fnc """
        for target in self.targetPaths:
            df = pd.read_pickle(target)
            self.buildQuickVAR(df, target.split("/")[-1][:-4])
            self.buildQuickSARIMAX(df, target.split("/")[-1][:-4])
            os.remove("{}".format(target))


    def buildQuickVAR(self, df, name):
        """ builds VAR model for series """
        os.makedirs("{}/VAR".format(self.targetDir), exist_ok=True)

        #Fit model
        model = VAR(df)
        results = model.fit(maxlags=24, ic='aic')

        #Get forecast
        lag_order = results.k_ar
        newVals = pd.DataFrame(results.forecast(df.values[-lag_order:], 24))
        newVals.index = [df.index.max()+datetime.timedelta(minutes=30*x) for x in range(1,25)]
        newVals.columns = df.columns
        newVals = results.fittedvalues.append(newVals)

        #plot
        colors = ["orange", "green", "red", "brown", "blue"]
        ax = newVals.plot(style=":", figsize=(8,8), color=colors, title="VAR Quick Fit for {}".format(name))
        df.plot(ax=ax, color=colors, legend=False)

        ax.figure.savefig("{}/VAR/{}.jpg".format(self.targetDir, name))
        plt.close('all') #close all figures

    def buildQuickSARIMAX(self, df, name):
        """ takes dataframe of time series and builds a SARIMAX model for each column """
        """ seasonality is daily for now, which is 48 time step thingies"""
        """ for now, just fiting to training data; will truncate last day starting next week for testing as well"""

        os.makedirs("{}/SARIMAX".format(self.targetDir), exist_ok=True)


        """
        k, doing this at the 30 minute aggregate is WAY too slow, so resampling hour
        """
        corr_df = df.resample("h").mean()
        for i in range(1,13):
            corr_df = pd.concat([corr_df, df.diff(i).add_prefix("L{}_".format(i))], axis=1)

        corr_df = np.abs(corr_df)
        corr_df = corr_df.dropna().corr()[df.columns][len(df.columns):]

        corr_df = df.copy()
        for i in range(1,13):
            corr_df = pd.concat([corr_df, df.diff(i).add_prefix("L{}_".format(i))], axis=1)

        corr_df = np.abs(corr_df)
        corr_df = corr_df.dropna().corr()[df.columns][5:]

        max_lag = -1

        results_df = df.copy()

        #plot SARIMAX using best correlating lag of an exogenous
        for column in df.columns:
            #get max lag - we'll plot them all together so the maxlag is going to be the max_lag
            best_series = corr_df[corr_df.index.map(lambda x: not x.endswith(column))][column].idxmax()
            lag = int(best_series.split("_")[0][1:])
            if lag > max_lag:
                max_lag = lag

            exogenous = best_series.split("_")[1]

            endogenous = df[[column]][lag:].copy()
            exogenous = df[[exogenous]].shift(lag)[lag:]

            model = auto_arima(endogenous, exogenous=exogenous, scoring="mae", out_of_sample_size=12, m=24, stepwise=True)
            endogenous[column]=model.predict_in_sample(exogenous=exogenous)
            results_df[column] = endogenous[column]

        colors = ["orange", "green", "red", "brown", "blue"]
        ax = df.plot(title=name, style="-", label="actual", color=colors)
        results_df.dropna().plot(ax=ax, legend=False, style=":", color=colors)
        ax.figure.savefig("{}/SARIMAX/{}.jpg".format(self.targetDir, name))
        plt.close('all') #close all figures

    def forecastArimaModels(self):
        return False

    """
    So i need to figure out what I want this architecture to look like
     I'll probably build these for use offline, not sure the EC2 instance
     I'm running this on has processing power for them but one way to find out :)
    """
    def buildPCARegressor(self):
        return False

    def buildDecisionTree(self):
        return False

    def tuneNeuralNetwork(self):
        return False
