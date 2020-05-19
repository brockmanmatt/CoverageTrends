from bs4 import BeautifulSoup
import sys, requests

def goodPage(urlObject):
    url = urlObject['href']
    text = urlObject.text.strip()

    if len(text) < 5:
        return False

    if len(url) < 5:
        return False

    try:
        if urlObject['class'][0] == 'title':
            return True
        if urlObject['data-analytics-module'] == "featured_post":
            return True
        if urlObject['data-analytics-module'] == "title-link":
            return True

        if urlObject['class'][0] == 'tout-title-link':
            return True
    except:
        return False

    return False




def scrape():
	results = {}
	url = "http://www.businessinsider.com/"
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')

	for link in soup.find_all('a', href=True):
		if not goodPage(link):
			continue
		myLink = link['href']
		results[myLink] = {}
		results[myLink]["text"] = link.text.strip()
		results[myLink]["notes"] = ""


	return results

if __name__ == '__main__':
	run()
