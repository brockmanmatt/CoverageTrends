import buildWebPage
import timeSeriesConvert
import quickModel

import git
from git import Repo
import time

startTime = time.time()


git.cmd.Git(".").pull()

print("selecting words")
tsc = timeSeriesConvert.wordCruncher()
tsc.runCurrentDefault()

print("making models")
qm = quickModel.modelBuilder()
qm.buildModels()


print("updating webpage")
wp = buildWebPage.webpageBuilder()
wp.buildWebpage()

timeTaken="({} seconds taken)".format(time.time()-startTime)


try:
    message = ("manual run add-models {}".format(timeTaken))
    repo = Repo("./.git")
    repo.git.add("archived_links")
    try:
        repo.git.add("archived_tweets")
    except:
        pass

    try:
        repo.git.add("docs")
    except:
        pass

    repo.index.commit(message)
    origin = repo.remote(name='origin')
    origin.push()
    print("pushed")
except:
    print('Some error occured while pushing the code')
