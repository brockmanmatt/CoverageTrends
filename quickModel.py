import os
import pandas as pd

import statsmodels.api as sm
from statsmodels.tsa.api import VAR
import datetime
import matplotlib.pyplot as plt
from pmdarima import auto_arima
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

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
        self.colors = ["orange", "green", "red", "brown", "blue", "yellow", "pink"]


    def buildModels(self):
        """ build a model for each target in targetPaths using fnc """
        for target in self.targetPaths:
            df = pd.read_pickle(target)
            self.buildQuickVAR(df, target.split("/")[-1][:-4])

            myFreq = "3h"
            self.buildQuickSARIMAX(df.resample(myFreq).mean().fillna(0), target.split("/")[-1][:-4], freq=8)
            os.remove("{}".format(target))


    def buildQuickVAR(self, df, name, test_size=-1, validation_size=-1):
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
        ax = newVals.plot(style=":", figsize=(8,8), color=self.colors, title="VAR Quick Fit for {}".format(name))
        df.plot(ax=ax, color=self.colors, legend=False)

        ax.figure.savefig("{}/VAR/{}.jpg".format(self.targetDir, name))
        plt.close('all') #close all figures

    def buildQuickSARIMAX(self, df, name, freq=24, test_size=-1, validation_size=-1):
        """ takes dataframe of time series and builds a SARIMAX model for each column """
        """ seasonality is daily for now, which is 48 time step thingies"""
        """ for now, just fiting to training data; will truncate last day starting next week for testing as well"""

        os.makedirs("{}/SARIMAX".format(self.targetDir), exist_ok=True)

        """
        k, doing this at the 30 minute aggregate is WAY too slow, so resampling hour
        """
        corr_df = df.copy()
        for i in range(1,13):
            corr_df = pd.concat([corr_df, df.diff(i).add_prefix("L{}_".format(i))], axis=1)

        corr_df = np.abs(corr_df)
        corr_df = corr_df.dropna().corr()[df.columns][len(df.columns):]

        corr_df = df.copy()
        for i in range(1,13):
            corr_df = pd.concat([corr_df, df.diff(i).add_prefix("L{}_".format(i))], axis=1)

        corr_df = np.abs(corr_df)
        corr_df = corr_df.dropna().corr()[df.columns][len(df.columns):]

        max_lag = -1
        results_df = df.copy()

        #plot SARIMAX using best correlating lag of an exogenous
        #does some magic to do a bunch of forecasts
        #I probably should be measuring errors =/
        for column in df.columns:
            #get max lag - we'll plot them all together so the maxlag is going to be the max_lag
            best_series = corr_df[corr_df.index.map(lambda x: not x.endswith(column))][column].idxmax()
            lag = int(best_series.split("_")[0][1:])
            if lag > max_lag:
                max_lag = lag

            exog = best_series.split("_")[1]

            endogenous = df[[column]][lag:].copy()
            exogenous = df[[exog]].shift(lag)[lag:]
            model = auto_arima(endogenous, exogenous=exogenous, scoring="mae", out_of_sample_size=freq, m=freq, stepwise=True)
            endogenous[column]=model.predict_in_sample(exogenous=exogenous)
            forecasts = pd.DataFrame()
            forecasts[column] = model.predict(n_periods=lag, exogenous=df[[exog]][-lag:])
            forecasts.index = [endogenous.index[-1] + x*endogenous.index[-1].freq for x in range(1,lag+1)]
            endogenous = endogenous.append(forecasts)
            while results_df.index.max() < endogenous.index.max():
                results_df = results_df.append(pd.Series(name=results_df.index[-1] + results_df.index[-1].freq))
            results_df[column] = endogenous[column]

        ax = results_df[max_lag:].plot(legend=False, style=":", color=self.colors, title=name, figsize=(8,8))
        df.plot(ax=ax, style="-", color=self.colors, legend=True)

        ax.figure.savefig("{}/SARIMAX/{}.jpg".format(self.targetDir, name))
        plt.close('all') #close all figures

    def funCorrelationalMatrix(self):
        """ shows lagged correlation for series """
        return False

    def forecastArimaModels(self):
        return False

    """
    So i need to figure out what I want this architecture to look like
     I'll probably build these for use offline, not sure the EC2 instance
     I'm running this on has processing power for them but one way to find out :)
    """
    def buildPCARegressor(self, name, test_size=-1, validation_size=-1):
        return False

    def buildDecisionTree(self):
        return False

    def tuneNeuralNetwork(self):
        return False
