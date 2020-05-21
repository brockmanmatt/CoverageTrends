import git, schedule, time, importlib, scraper, os
from git import Repo
import twitter_filter, multiprocessing

def updateRepo():
    git.cmd.Git(".").pull()
    print("pulled")

def cycle():
    updateRepo()
    importlib.reload(scraper)
    scraper.run()
    git_push()

def git_push(message='auto-update'):
    try:
        repo = Repo("./.git")
        repo.git.add("archived_links")
        try:
            repo.git.add("archived_tweets")
        except:
            pass
        repo.index.commit(message)
        origin = repo.remote(name='origin')
        origin.push()
        print("pushed")
    except:
        print('Some error occured while pushing the code')

twitter_process = ""
def reset_twitter_filter():

    try:
        twitter_process.terminate()
    except:
        pass

    importlib.reload(twitter_filter)
    twitter_process = multiprocessing.Process(target=twitter_filter.run)
    twitter_process.start()

os.makedirs("archived_links", exist_ok=True)

reset_twitter_filter()
schedule.every().day.at("00:00").do(reset_twitter_filter)

schedule.every().day.at("00:00").do(cycle)
schedule.every().day.at("01:00").do(cycle)
schedule.every().day.at("02:00").do(cycle)
schedule.every().day.at("03:00").do(cycle)
schedule.every().day.at("04:00").do(cycle)
schedule.every().day.at("05:00").do(cycle)
schedule.every().day.at("06:00").do(cycle)
schedule.every().day.at("07:00").do(cycle)
schedule.every().day.at("08:00").do(cycle)
schedule.every().day.at("09:00").do(cycle)
schedule.every().day.at("10:00").do(cycle)
schedule.every().day.at("11:00").do(cycle)
schedule.every().day.at("12:00").do(cycle)
schedule.every().day.at("13:00").do(cycle)
schedule.every().day.at("14:00").do(cycle)
schedule.every().day.at("15:00").do(cycle)
schedule.every().day.at("16:00").do(cycle)
schedule.every().day.at("17:00").do(cycle)
schedule.every().day.at("18:00").do(cycle)
schedule.every().day.at("19:00").do(cycle)
schedule.every().day.at("20:00").do(cycle)
schedule.every().day.at("21:00").do(cycle)
schedule.every().day.at("22:00").do(cycle)
schedule.every().day.at("23:00").do(cycle)

schedule.every().day.at("00:30").do(cycle)
schedule.every().day.at("01:30").do(cycle)
schedule.every().day.at("02:30").do(cycle)
schedule.every().day.at("03:30").do(cycle)
schedule.every().day.at("04:30").do(cycle)
schedule.every().day.at("05:30").do(cycle)
schedule.every().day.at("06:30").do(cycle)
schedule.every().day.at("07:30").do(cycle)
schedule.every().day.at("08:30").do(cycle)
schedule.every().day.at("09:30").do(cycle)
schedule.every().day.at("10:30").do(cycle)
schedule.every().day.at("11:30").do(cycle)
schedule.every().day.at("12:30").do(cycle)
schedule.every().day.at("13:30").do(cycle)
schedule.every().day.at("14:30").do(cycle)
schedule.every().day.at("15:30").do(cycle)
schedule.every().day.at("16:30").do(cycle)
schedule.every().day.at("17:30").do(cycle)
schedule.every().day.at("18:30").do(cycle)
schedule.every().day.at("19:30").do(cycle)
schedule.every().day.at("20:30").do(cycle)
schedule.every().day.at("21:30").do(cycle)
schedule.every().day.at("22:30").do(cycle)
schedule.every().day.at("23:30").do(cycle)


while True:
    try:
        print("New Cycle!")
        schedule.run_pending()
    except:
        print("error")
        pass
    time.sleep(60)
