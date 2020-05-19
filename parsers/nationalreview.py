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
		parts = url.split('nationalreview.com/')[1]
		parts = parts.split('/')
		if len(parts[0]) == 4:
			if len(parts[1]) == 2:
				return True
	except:
		return False

	return False


def scrape():
	results = {}
	url = "https://www.nationalreview.com/"
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')

	for link in soup.find_all('a', href=True):
		if not goodPage(link):
			continue
		myLink = link["href"]

		results[myLink] = {}
		results[myLink]["text"] = link.text.strip()
		results[myLink]["notes"] = ""
	return results


if __name__ == '__main__':
	scrape()
