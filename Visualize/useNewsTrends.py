from newstrends import visualize
import buildWebPage

import git
from git import Repo
import time

import sys
sys.path.append(".")

startTime = time.time()


git.cmd.Git(".").pull()

viz = visualize.visualizer(coverageTrendsPath=".", workdir="docs")
viz.runDefault()
viz.buildModels()

print("updating webpage")
wp = buildWebPage.webpageBuilder()
wp.buildWebpage()

timeTaken="({} seconds taken)".format(time.time()-startTime)

try:
    message = ("manual run add-models {}".format(timeTaken))
    repo = Repo("./.git")
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
