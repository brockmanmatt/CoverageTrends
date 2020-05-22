# CoverageTrends
This archives headlines and links on news websites every 30 minutes. Working on getting it down to less time using less space, but wanted to start archiving sooner than later. Should be updating graphs at https://brockmanmatt.github.io/CoverageTrends/ in the next couple days, also should move it off of this repo now that I think about it.

# main.py
Sets timers to run every 30 minutes

# scraper.py
uses each parser in parsers to scrape each news site and add to the daily csv for each news source.

CNN is surprisingly stubborn

# parsers
contains a parser for each news site which visits the home page and scrapes the linked headlines and urls.

# selenium_parsers
parsers that use selenium; see https://selenium-python.readthedocs.io/getting-started.html#simple-usage for installation instructions. It depends on OS. Really, just Google how to install selenium and chrome driver on your OS and go off stack exhcange.

# twitter_filter.py
scrapes twitter, requires a twitter API with the keys in "twitter_keys.json" as a dict with the following properties:
```
{
  "CONSUMER_KEY":"[KEY]",
  "CONSUMER_SECRET":"[KEY]",
  "ACCESS_TOKEN":"[KEY]",
  "ACCESS_TOKEN_SECRET":"[KEY]"
}

```

# archived links
contains a folder for each news site, where within each folder there's a .csv for each day with the headlines and urls on the home page at each scrape. Time is normalized to UTC time.

# archived tweets
contains a folder by month for each publisher, where each month has a .csv for each day with all tweets for the publisher. Original tweets can be found at twitter.com/[name]/status/[tweetid]


# Major Changes:
20200519 - switched to hourly instead of every 4 hours

20200520 - switched to 30 minutes instead of every hour

20200520 - Added twitter feeds


# Minor Additions

20200518 - started :-

20200519 - adding more sites

20200519 - adding metadata about location on site


# TODO

_TODO_ Multiple User Agents/IP addresses

_TODO_ Selenium for sites that don't have it

_TODO_ Followup: Can I install selenium easily with reqs.txt (I think the answer is no)

_TODO_ Figure out how to hook this into a github website with JS


## oh, GDELT apparently already does this hourly on a larger scale.

So they have everything and list where on page link appears (well, where in HTML)

https://blog.gdeltproject.org/announcing-gdelt-global-frontpage-graph-gfg/

They pull quite a bit of data, might be able to just use that if I figure out what the relative position on page means, but for now playing with this to see if it's easier to manually label the sections on these publications.

## Questions?
mattbrockman(at)gmail(dat)com
