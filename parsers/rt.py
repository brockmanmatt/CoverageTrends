from bs4 import BeautifulSoup
import sys, requests

def goodURL(link):
	url = link["href"]

	ignore = ["/newsline/", "/where-to-watch/", "/schedule/"]

	if url in ignore:
		return False

	return True

def scrape():
	results = {}
	url = "http://rt.com/"
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')
	frontPage = soup.find(class_= "layout__content")


	for link in frontPage.find_all('a', href=True):
		if not goodURL(link):
			continue
		myLink = link["href"]
		if myLink in results:
			if len(results[myLink]["text"].strip()) > 10:
				continue
		results[myLink] = {}
		results[myLink]["text"] = link.text.strip()
		results[myLink]["notes"] = ""
	return results


if __name__ == '__main__':
	scrape()
