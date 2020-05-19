from bs4 import BeautifulSoup
import sys, requests

def goodArticle(myLink):
	url = myLink['href']
	if url.startswith('h'):
		if not url.startswith('http://www.breitbart.com/'):
			return False
	return True

def scrape():
    results = {}
    url = "http://www.breitbart.com/"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    myArticle = soup.find(id= "MainW")

    siteText = ''
    for link in myArticle.find_all('a', href=True):
        if ((not link.text.isspace()) and not (link['href'].strip().startswith("/author/")) and not (link['href'].strip().endswith("disqus_thread")) and not ('img alt' in str(link))):
            if not goodArticle(link):
                continue
            myLink = link['href']
            if (not myLink.startswith("http://www.breitbart.com")):
                myLink = "http://www.breitbart.com" + link['href']
            results[myLink] = {}
            results[myLink]["text"] = link.text.strip()
            results[myLink]["notes"] = ""
    return results


if __name__ == '__main__':
    run()
