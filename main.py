import git, schedule, time, importlib, scraper, os
from git import Repo


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
        repo.index.commit(message)
        origin = repo.remote(name='origin')
        origin.push()
        print("pushed")
    except:
        print('Some error occured while pushing the code')

os.makedirs("archived_links", exist_ok=True)

schedule.every().day.at("03:00").do(cycle)
schedule.every().day.at("07:00").do(cycle)
schedule.every().day.at("11:00").do(cycle)
schedule.every().day.at("15:00").do(cycle)
schedule.every().day.at("19:00").do(cycle)
schedule.every().day.at("23:00").do(cycle)

while True:
    try:
        print("New Cycle!")
        schedule.run_pending()
    except:
        print("error")
        pass
    time.sleep(60)
