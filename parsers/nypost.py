from bs4 import BeautifulSoup
import sys, requests

def goodPage(urlObject):
	url = urlObject['href']
	text = urlObject.text.strip()

	if url.startswith('h'):
		if not url.startswith('https://nypost'):
			return False

	if url.startswith('https://nypost.com/video'):
		return False

	if url.startswith('/'):
		if url.count('/') < 3:
			return False

	if len(text) < 5:
		return False

	if len(url) < 5:
		return False
	return True



def scrape():
	results = {}
	url = "https://nypost.com/"
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')
	frontPage = soup.find("div", {"id":"content"})

	for link in frontPage.find_all('a', href=True):
		if not goodPage(link):
			continue
		myLink = link["href"]

		results[myLink] = {}
		results[myLink]["text"] = link.text.strip()
		results[myLink]["notes"] = ""
	return results


if __name__ == '__main__':
	scrape()
