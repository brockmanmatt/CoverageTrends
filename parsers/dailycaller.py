from bs4 import BeautifulSoup
import sys, requests

def goodURL(urlObject):
	url = urlObject['href']
	text = urlObject.text

	if url.startswith("/20"):
		return True

	return False


def scrape():
	results = {}
	url = "http://dailycaller.com/"
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')

	for link in soup.find_all('a', href=True):
		if not goodURL(link):
			continue
		myLink = link["href"]
		if myLink in results:
			if len(results[myLink]["text"].strip()) > 5:
				continue

		results[myLink] = {}
		results[myLink]["text"] = link.text.strip()
		results[myLink]["notes"] = ""
	return results

if __name__ == '__main__':
	scrape()
