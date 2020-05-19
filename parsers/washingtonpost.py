from bs4 import BeautifulSoup
import sys, requests

def notBadURL(urlObject):
	url = urlObject['href']
	if url.startswith("https://www.washingtonpost.com/people"):
		return False
	if url.startswith("https://subscribe.washingtonpost.com"):
		return False
	if url.startswith("https://www.washingtonpost.com/graphics"):
		return False
	if url.startswith("#"):
		return False
	if url.startswith("/people"):
		return False
	if url.endswith("gallery.html"):
		return False
	if len(url.split('/')) < 6:
		return False
	if url == "https://www.washingtonpost.com/opinions/the-posts-view/":
		return False
	if url == "https://www.washingtonpost.com/local/obituaries/":
		return False
	if urlObject.text.strip() == '':
		return False
	if urlObject.text == 'Graphic':
		return False
	if urlObject.text == 'Photos':
		return False
	if "TopBox__image-link" in str(urlObject):
		return False
	return True


def scrape():
	results = {}
	url = "https://www.washingtonpost.com/"
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')
	currentContainer = soup.find("section", {"id":"main-content"})

	for link in currentContainer.find_all('a', href=True):
		if notBadURL(link):
			myLink = link['href']
			results[myLink] = {}
			results[myLink]["text"] = link.text.strip()
			results[myLink]["notes"] = ""

	currentContainer = soup.find("section", {"id":"bottom-content"})
	for link in currentContainer.find_all('a', href=True):
		if notBadURL(link):
			myLink = link['href']
			results[myLink] = {}
			results[myLink]["text"] = link.text.strip()
			results[myLink]["notes"] = ""

	return results

if __name__ == '__main__':
	run()
