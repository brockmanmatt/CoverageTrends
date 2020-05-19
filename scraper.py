import pandas as pd
from bs4 import BeautifulSoup as bs
import time, datetime, os

from datetime import timezone

from parsers import *

def run():
    myTime = datetime.datetime.now(tz=timezone.utc).strftime('%Y%m%d-%H00')
    myDate = datetime.datetime.now(tz=timezone.utc).strftime('%Y%m%d')
    myMonth = myDate = datetime.datetime.now(tz=timezone.utc).strftime('%Y%m')

    sources = pd.read_excel("NewsSites.xlsx")

    for _, row in sources.T.iteritems():
        if "{}.py".format(row["Parser"]) in os.listdir("parsers"):
            try:
                module = "parsers." + row["Parser"]
                module = importlib.import_module(module)
                tmp = pd.DataFrame(module.scrape()).T
                tmp["date"] = myTime

                os.makedirs("archived_links/{}/{}/".format(row["Parser"], myMonth), exist_ok=True)

                if not os.path.isfile("{}/{}/{}/{}_{}.csv".format("archived_links/", row["Parser"], myMonth,row["Parser"], myDate)):
                    tmp.to_csv("{}/{}/{}/{}_{}.csv".format("archived_links/", row["Parser"], myMonth,row["Parser"], myDate))
                else:
                    tmp.to_csv("{}/{}/{}/{}_{}.csv".format("archived_links/", row["Parser"], myMonth,row["Parser"], myDate), mode='a', header=False)
            except:
                pass
if __name__ == '__main__':
    run()
