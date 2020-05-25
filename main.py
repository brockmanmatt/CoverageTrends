import git, schedule, time, importlib, scraper, os
from git import Repo
import twitter_filter, multiprocessing
import buildWebPage
import timeSeriesConvert
import quickModel

def updateRepo():
    git.cmd.Git(".").pull()
    print("pulled")

def cycle(buildPage = False):
    """ pulls github repo, runs scraper and updates github, then runs the models """
    updateRepo()
    importlib.reload(scraper)
    try:
        scraper.run()
    except:
        print("error with scraper")
        pass

    if buildPage:
        buildmodels()

    git_push()


def cycle2():
    cycle(buildPage=True)

def buildmodels():

    importlib.reload(buildWebPage)
    importlib.reload(timeSeriesConvert)
    importlib.reload(quickModel)

    try:
        print("building words")
        tsc = timeSeriesConvert.wordCruncher()
        tsc.runCurrentDefault()
    except:
        print("error making images")
        pass

    try:
        print("building models")
        qm = quickModel.modelBuilder()
        qm.buildModels()
    except:
        print("error building models")
        pass

    try:
        print("building webpage")
        wp = buildWebPage.webpageBuilder()
        wp.buildWebpage()
    except:
        print("error building webpage")
        pass

def git_push(message='auto-update'):
    try:
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

"""
I think I need this to be a class so that I can restart the twitter scraper daily
It can run forever without changing it but I want to be able to push updates via git
So any push will take effect the next day at 00:00 UTC
"""
class twitter_holder:

    processes = []
    def __init__(self):
        print("starting twitter scraper")
        self.processes.append(multiprocessing.Process(target=twitter_filter.run))
        for process in self.processes:
            process.start()
        print("started")

    def reset_twitter_filter(self):
        try:
            for process in self.processes:
                process.terminate()
            self.processes = []
        except:
            print("messed up the twitter process; check for zombies")
            pass

        importlib.reload(twitter_filter)
        self.processes.append(multiprocessing.Process(target=twitter_filter.run))
        for process in self.processes:
            process.start()


os.makedirs("archived_links", exist_ok=True)
os.makedirs("docs", exist_ok=True)


myTwitterScraper = twitter_holder()

schedule.every().day.at("00:00").do(myTwitterScraper.reset_twitter_filter)

schedule.every().day.at("00:00").do(cycle2)
schedule.every().day.at("01:00").do(cycle2)
schedule.every().day.at("02:00").do(cycle2)
schedule.every().day.at("03:00").do(cycle2)
schedule.every().day.at("04:00").do(cycle2)
schedule.every().day.at("05:00").do(cycle2)
schedule.every().day.at("06:00").do(cycle2)
schedule.every().day.at("07:00").do(cycle2)
schedule.every().day.at("08:00").do(cycle2)
schedule.every().day.at("09:00").do(cycle2)
schedule.every().day.at("10:00").do(cycle2)
schedule.every().day.at("11:00").do(cycle2)
schedule.every().day.at("12:00").do(cycle2)
schedule.every().day.at("13:00").do(cycle2)
schedule.every().day.at("14:00").do(cycle2)
schedule.every().day.at("15:00").do(cycle2)
schedule.every().day.at("16:00").do(cycle2)
schedule.every().day.at("17:00").do(cycle2)
schedule.every().day.at("18:00").do(cycle2)
schedule.every().day.at("19:00").do(cycle2)
schedule.every().day.at("20:00").do(cycle2)
schedule.every().day.at("21:00").do(cycle2)
schedule.every().day.at("22:00").do(cycle2)
schedule.every().day.at("23:00").do(cycle2)

schedule.every().day.at("00:30").do(cycle2)
schedule.every().day.at("01:30").do(cycle2)
schedule.every().day.at("02:30").do(cycle2)
schedule.every().day.at("03:30").do(cycle2)
schedule.every().day.at("04:30").do(cycle2)
schedule.every().day.at("05:30").do(cycle2)
schedule.every().day.at("06:30").do(cycle2)
schedule.every().day.at("07:30").do(cycle2)
schedule.every().day.at("08:30").do(cycle2)
schedule.every().day.at("09:30").do(cycle2)
schedule.every().day.at("10:30").do(cycle2)
schedule.every().day.at("11:30").do(cycle2)
schedule.every().day.at("12:30").do(cycle2)
schedule.every().day.at("13:30").do(cycle2)
schedule.every().day.at("14:30").do(cycle2)
schedule.every().day.at("15:30").do(cycle2)
schedule.every().day.at("16:30").do(cycle2)
schedule.every().day.at("17:30").do(cycle2)
schedule.every().day.at("18:30").do(cycle2)
schedule.every().day.at("19:30").do(cycle2)
schedule.every().day.at("20:30").do(cycle2)
schedule.every().day.at("21:30").do(cycle2)
schedule.every().day.at("22:30").do(cycle2)
schedule.every().day.at("23:30").do(cycle2)


while True:
    try:
        print("New Cycle!")
        schedule.run_pending()
    except:
        print("error")
        pass
    time.sleep(60)
