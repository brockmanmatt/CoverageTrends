# CoverageTrends
This archives headlines and links on news websites every 30 minutes. Working on getting it down to less time using less space, but wanted to start archiving sooner than later.

# main.py
Sets timers to run every 30 minutes

# scraper.py
uses each parser in parsers to scrape each news site and add to the daily csv for each news source.

CNN is surprisingly stubborn

# parsers
contains a parser for each news site which visits the home page and scrapes the linked headlines and urls.

# selenium_parsers
parsers that use selenium; see https://selenium-python.readthedocs.io/getting-started.html#simple-usage for installation instructions. It depends on OS. Really, just Google how to install selenium and chrome driver on your OS and go off stack exhcange.

# archived links
contains a folder for each news site, where within each folder there's a .csv for each day with the headlines and urls on the home page at each scrape. Time is normalized to UTC time.

# Major Changes:
20200519 - switched to hourly instead of every 4 hours

20200520 - switched to 30 minutes instead of every hour


# Minor Additions

20200518 - started :-

20200519 - adding more sites

20200519 - adding metadata about location on site


# TODO

_TODO_ Multiple User Agents/IP addresses

_TODO_ Selenium for sites that don't have it

_TODO_ Followup: Can I install selenium easily with reqs.txt

# oh, GDELT apparently already does this hourly on a larger scale. I'll go mess with their data.
https://blog.gdeltproject.org/announcing-gdelt-global-frontpage-graph-gfg/


## Questions?
mattbrockman(at)gmail(dat)com
