from bs4 import BeautifulSoup
import sys, requests

def goodURL(urlObject):
	url = urlObject['href']
	title = urlObject.text
	if title.strip() == '':
		return False
	if url.startswith("https://www.theatlantic.com/author/"):
		return False
	if len(url.split('/')) < 6:
		return False
	if url.split('/')[4] == "toc":
		return False
	if url:
		return True
	return False

def scrape():
	results = {}
	url = "https://www.theatlantic.com/"
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')

	for link in soup.find("main").find_all('a', href=True):
		if not goodURL(link):
			continue
		myLink = link["href"]

		results[myLink] = {}
		results[myLink]["text"] = link.text.strip()
		results[myLink]["notes"] = ""
	return results

if __name__ == '__main__':
	scrape()
