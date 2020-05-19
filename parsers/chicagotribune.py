from bs4 import BeautifulSoup
import sys, requests

def goodPage(urlObject):
	url = urlObject['href']
	text = urlObject.text.strip()

	if len(text) < 5:
		return False

	if len(url) < 5:
		return False

	if len(text.split()) < 4:
		return False

	if text == 'Auto reviews and news':
		return False

	if url.startswith('h'):
		if not url.startswith('http://www.chicagotribune.com'):
			return False

	if url.startswith('http://www.chicagotribune.com/huy'):
		return False

	if url.endswith('outfit'):
		return False

	if text == 'Ask Amy by Amy Dickinson':
		return False

	if 'hoy' in url.split('/'):
		return False

	return True




def scrape():
	results = {}
	url = "http://www.chicagotribune.com/"
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')

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
