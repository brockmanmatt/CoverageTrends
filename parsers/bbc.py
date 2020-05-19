from bs4 import BeautifulSoup
import sys, requests

def goodPage(urlObject):
	url = urlObject['href']
	text = urlObject.text
	if text.count(" ") < 2:
		return False
	if url.count('/') == 1:
		return False
	if url[-1] == '/':
		return False

	if url == "/news/world/us_and_canada":
		return False

	if url == "/news/world/latin_america":
		return False

	if url == "/news/entertainment_and_arts":
		return False

	if url == "/news/science_and_environment":
		return False

	if url == "/news/in_pictures":
		return False

	if url.startswith('/'):
		if url.startswith('/news'):
			return True
		elif url.startswith('/sport'):
			return True
		else:
			return False
	if url.startswith('/'):
		if url.startswith('http://www.bbc.com/news'):
			return True
		elif url.startswith('http://www.bbc.com/sport'):
			return True
		else:
			return False

	return False


def scrape():
	results = {}
	url = "http://www.bbc.com/"
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')
	frontPage = soup.find("div", class_="content")

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
