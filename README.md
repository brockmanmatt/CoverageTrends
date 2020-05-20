# CoverageTrends
This archives headlines and links on news websites every hour. Working on getting it down to less time using less space, but wanted to start archiving sooner than later.

# main.py
Sets timers to run every 1 hours

# scraper.py
uses each parser in parsers to scrape each news site and add to the daily csv for each news source.

# parsers
contains a parser for each news site which visits the home page and scrapes the linked headlines and urls.

# archived links
contains a folder for each news site, where within each folder there's a .csv for each day with the headlines and urls on the home page at each scrape. Time is normalized to UTC time.

# Major Changes:
20200519 - switched to hourly instead of every 4 hours

# Minor Additions

20200518 - started :-

20200519 - adding more sites

# TODO

_TODO_ Multiple User Agents/IP addresses

_TODO_ Selenium for sites that don't have it

_TODO_ Followup: Can I install selenium easily with reqs.txt


## Questions?
mattbrockman(at)gmail(dat)com
