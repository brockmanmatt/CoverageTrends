from bs4 import BeautifulSoup
import sys, requests

def goodPage(urlObject):
	url = urlObject['href']
	text = urlObject.text.strip()

	if len(text) < 5:
		return False

	if len(url) < 5:
		return False

	if url.startswith('j'):
		return False

	if url.count('/') == 2:
		return False

	if url.count('/') == 4:
		if url.count('-') == 1:
			return False

	if url.startswith('h'):
		if not url.startswith('https://www.cnbc.com/'):
			return False

	return True




def scrape():
	results = {}
	url = "https://www.cnbc.com/"
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')
	for frontPage in soup.find_all("div", {"class":"PageBuilder-containerFluidWidths PageBuilder-pageRow"}):
		for link in frontPage.find_all('a', href=True):
			if not goodPage(link):
				continue
			myLink = link['href']
			results[myLink] = {}
			results[myLink]["text"] = link.text.strip()
			results[myLink]["notes"] = ""


	return results

if __name__ == '__main__':
	run()
