from bs4 import BeautifulSoup
import sys, requests

def goodPage(urlObject):
	url = urlObject['href']
	text = urlObject.text.strip()

	if len(text) < 5:
		return False

	if len(url) < 5:
		return False


	if len(url.split('/')) < 7:
		return False

	if url.startswith('https://www.npr.org/20'):
		return True

	if url.startswith('https://www.npr.org/sections'):
		return True

	return False


def scrape():
	results = {}
	url = "https://www.npr.org/"
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')

	for link in soup.find_all('a', href=True):
		if not goodPage(link):
			continue
		myLink = link["href"]

		results[myLink] = {}
		try:
			results[myLink]["text"] = link.title.strip()

		except:
			results[myLink]["text"] = link.text.strip()

		results[myLink]["notes"] = ""
	return results


if __name__ == '__main__':
	scrape()
