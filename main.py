import git, schedule, time, importlib, scraper


def updateRepo():
    git.cmd.Git(".").pull()
    print("pulled")

def cycle():
    updateRepo()
    importlib.reload(scraper)
    scraper.run()
    print("test")

def git_push(message='auto-update'):
    try:
        repo = Repo(".")
        repo.git.add(update=True)
        repo.index.commit(message)
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Some error occured while pushing the code')

os.makedir("scrapes", exist_ok=True)

schedule.every(1).hours.do(cycle)

cycle()

git_push()

while False:
    try:
        print("New Cycle!")
        schedule.run_pending()
    except:
        print("error")
        pass
    time.sleep(60)
