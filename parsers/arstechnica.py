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
		tmp = urlObject['class']
		return False
	except:
		d=1

	if url.startswith('/'):
		return False
	if url.startswith('https://arstechnica.com/author'):
		return False
	if not url.startswith('https://a'):
		return False

	return True

def scrape():
	results = {}
	url = "https://arstechnica.com/"
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')
	frontPage = soup.find("section", {"id":"section_home"})

	for link in soup.find_all('a', href=True):
		if not goodPage(link):
			continue
		myLink = link['href']
		results[myLink] = {}
		results[myLink]["text"] = link.text.strip()
		results[myLink]["notes"] = ""


	return results

if __name__ == '__main__':
	run()
