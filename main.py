import git, schedule, time, importlib, scraper

def updateRepo():
    git.cmd.Git(".").pull()
    print("pulled")

def cycle():
    updateRepo()
    importlib.reload(scraper)
    scraper.run()
    print("test")

schedule.every(10).seconds.do(cycle)

while True:
    try:
        schedule.run_pending()
    except:
        print("error")
        pass
    time.sleep(1)
