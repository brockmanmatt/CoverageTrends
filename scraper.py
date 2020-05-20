import pandas as pd
from bs4 import BeautifulSoup as bs
import time, datetime, importlib
import os

from datetime import timezone

def run(verbose=False, path="archived_links", checkSelenium=False):
    myTime = datetime.datetime.now(tz=timezone.utc).strftime('%Y%m%d-%H00')
    myDate = datetime.datetime.now(tz=timezone.utc).strftime('%Y%m%d')
    myMonth = datetime.datetime.now(tz=timezone.utc).strftime('%Y%m')

    sources = pd.read_excel("NewsSites.xlsx")

    os.listdir()

    if verbose:
        print("checking rows")

    if not checkSelenium:
        #try pulling all the ones that requests.get works with
        for _, row in sources.T.iteritems():
            if "{}.py".format(row["Parser"]) in os.listdir("parsers"):
                try:
                    module = "parsers." + row["Parser"]
                    module = importlib.import_module(module)
                    tmp = pd.DataFrame(module.scrape()).T
                    tmp["date"] = myTime

                    os.makedirs("{}/{}/{}/".format(path, row["Parser"], myMonth), exist_ok=True)

                    if not os.path.isfile("{}/{}/{}/{}_{}.csv".format(path, row["Parser"], myMonth,row["Parser"], myDate)):
                        tmp.to_csv("{}/{}/{}/{}_{}.csv".format(path, row["Parser"], myMonth,row["Parser"], myDate))
                    else:
                        tmp.to_csv("{}/{}/{}/{}_{}.csv".format(path, row["Parser"], myMonth,row["Parser"], myDate), mode='a', header=False)
                except Exception as e:
                    if verbose:
                        print(e)
                    pass

    #now try all using selenium instead!
    #This will fail if selenium isn't installed
    try:
        from selenium import webdriver
        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        options.add_argument('--no-sandbox')

        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"

        driver = webdriver.Chrome(desired_capabilities=caps, options=options)


        for _, row in sources.T.iteritems():
            if "{}.py".format(row["Parser"]) in os.listdir("selenium_parsers"):
                try:
                    module = "selenium_parsers." + row["Parser"]
                    module = importlib.import_module(module)
                    tmp = pd.DataFrame(module.scrape(driver)).T #pass my driver so don't need to make new one
                    tmp["date"] = myTime

                    os.makedirs("{}/{}/{}/".format(path, row["Parser"], myMonth), exist_ok=True)

                    if not os.path.isfile("{}/{}/{}/{}_{}.csv".format(path, row["Parser"], myMonth,row["Parser"], myDate)):
                        tmp.to_csv("{}/{}/{}/{}_{}.csv".format(path, row["Parser"], myMonth,row["Parser"], myDate))
                    else:
                        tmp.to_csv("{}/{}/{}/{}_{}.csv".format(path, row["Parser"], myMonth,row["Parser"], myDate), mode='a', header=False)
                except Exception as e:
                    if verbose:
                        print(e)
                    pass

        driver.quit()
    except:
        try:
            driver.quit()
        except:
            pass
        pass



if __name__ == '__main__':
    run(verbose=True)
