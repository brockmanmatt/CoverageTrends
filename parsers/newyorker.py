from bs4 import BeautifulSoup
import sys, requests

def goodPage(urlObject):
	url = urlObject['href']
	text = urlObject.text.strip()

	if len(text) < 5:
		return False

	if len(url) < 5:
		return False

	if url.startswith('h'):
		if not url.startswith('https://www.newyorker.com'):
			return False
		if url.startswith('https://www.newyorker.com/newsletters'):
			return False

	else:
		if url.count('/') < 3:
			return False
		if url.startswith('/about'):
			return False

	if len(url) < 25:
		return False

	if text == 'The New Yorker Recommends':
		return False

	return True



def scrape():
	results = {}
	url = "https://www.newyorker.com/"
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
