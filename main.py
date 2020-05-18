import git
import pandas as pd
from bs4 import BeautifulSoup as bs

g = git.cmd.Git(".")
g.pull()
print("pulled")
