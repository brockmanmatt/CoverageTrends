from bs4 import BeautifulSoup
import sys, requests

def goodURL(urlObject):
	url = urlObject['href']
	text = urlObject.text.strip()

	if len(text) < 5:
		return False

	if len(url) < 5:
		return False

def scrape():
	results = {}
	url = "https://slate.com/"
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')

	for link in soup.find_all('a', {"class":["story-teaser__cta", "story-card__link"]}):
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
