import git, schedule, time
import pandas as pd
from bs4 import BeautifulSoup as bs


def updateRepo():
    git.cmd.Git(".").pull()
    print("pulled")

def cycle():
    updateRepo()
    print("test")

schedule.every(10).seconds.do(cycle)

while True:
    schedule.run_pending()
    time.sleep(1)
