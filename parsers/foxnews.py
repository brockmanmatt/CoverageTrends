from bs4 import BeautifulSoup
import sys, requests

def notBadURL(urlObject):
	url = urlObject['href']
	if url.startswith("https://www.washingtonpost.com/people"):
		return False
	if url.startswith("http://video."):
		return False
	if url.startswith("//www.foxnews.com/on-air/"):
		return False
	if url == "//www.foxnews.com/on-air/americas-news-hq/index.html":
		return False
	if url.startswith("//www.foxnews.com/person"):
		return False
	if url.startswith("//video."):
		return False
	if url == '#':
		return False
	if len(url.split('/')) < 5:
		return False
	if "TopBox__image-link" in str(urlObject):
		return False
	if urlObject.text.strip() == '':
		return False
	if urlObject.text.strip().isspace():
		return False
	if urlObject.text == 'On Now':
		return False
	if urlObject.text == 'View All':
		return False
	return True

def scrape():
	results = {}
	url = "http://www.foxnews.com/"
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')

	currentContainer = soup.find("div", {"class":"page-content"})
	for link in currentContainer.find_all('a', href=True):
		if notBadURL(link):
			myLink = link['href']

			results[myLink] = {}
			results[myLink]["text"] = link.text.strip()
			results[myLink]["notes"] = ""

	currentContainer = soup.find("div", {"class":"post-content"})
	for link in currentContainer.find_all('a', href=True):
		if notBadURL(link):
			results[myLink] = {}
			results[myLink]["text"] = link.text.strip()
			results[myLink]["notes"] = ""

	return results


if __name__ == '__main__':
	scrape()
