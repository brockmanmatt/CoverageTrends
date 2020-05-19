from bs4 import BeautifulSoup
import sys, requests

def goodPage(urlObject):
	url = urlObject['href']
	text = urlObject.text.strip()

	if len(text) < 5:
		return False

	if len(url) < 5:
		return False

	if url.find('.html') < 0:
		return False

	if url.startswith('/'):
		if url.startswith('/newsletters'):
			return False
		return True

	if url.find('axios') < 0:
		return False

	if url.startswith('https://www.axios.com/newsletters'):
		return False

	if url.startswith('https://'):
		if not url.startswith('https://www.axios.com'):
			return False

	return True

def scrape():
	results = {}
	url = "https://www.axios.com"
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')

	for link in soup.find_all('a', {"class":"gtm-content-click title-link"}):
		if not goodPage(link):
			continue
		myLink = link['href']
		results[myLink] = {}
		results[myLink]["text"] = link.text.strip()
		results[myLink]["notes"] = ""


	return results

if __name__ == '__main__':
	run()
