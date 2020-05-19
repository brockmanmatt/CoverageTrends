from bs4 import BeautifulSoup
import sys, requests

def goodPage(urlObject):
	url = urlObject['href']
	text = urlObject.text
	if text == '':
		return False
	if text.isspace():
		return False
	if url.startswith("/profile"):
		return False
	if url.startswith("/topics/"):
		return False
	if url.startswith("#"):
		return False
	if url.startswith("https://www.instagram.com"):
		return False
	if url[-1] == '/':
		return False
	return True

def scrape():
	results = {}
	url = "https://www.aljazeera.com/"
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')
	frontPage = soup.find("div", {"type":"content"})

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
