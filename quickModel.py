import os
import pandas as pd

import statsmodels.api as sm
from statsmodels.tsa.api import VAR
import datetime
import matplotlib.pyplot as plt

class modelBuilder:
    """ build models for time series """

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
            os.remove("{}/{}".format(self.targetPaths, target))


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

    def buildArimaModels(self, df, name):
        """ takes dataframe of time series and builds a SARIMAX model for each column """
        """ for now actually, it'll just be SARIMA """
        """ seasonality is daily for now, which is 48 time step thingies"""

        print(df.columns)

        return False

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
