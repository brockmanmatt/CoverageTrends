from bs4 import BeautifulSoup
import sys, requests

def goodPage(urlObject):
	url = urlObject['href']
	text = urlObject.text.strip()

	if len(text) < 5:
		return False

	if len(url) < 5:
		return False

	if url in ["https://www.livescience.com/62824-about-us.html",
	"https://www.livescience.com/download-your-favorite-magazines.html",
	"https://www.livescience.com/lifes-little-mysteries-podcast.html",
	"https://www.livescience.com/how-to-advertise-with-us.html",
	"https://www.livescience.com/how-to-turn-off-web-notifications-for-chrome-macos.html"
	]: return False

	if not url.endswith('html'):
		return False

	return True


def scrape():
	results = {}
	url = "https://www.livescience.com/"
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')

	for link in soup.find_all('a', href=True):
		if not goodPage(link):
			continue
		myLink = link["href"]

		results[myLink] = {}
		results[myLink]["text"] = link.text.strip()
		results[myLink]["notes"] = ""
	return results


if __name__ == '__main__':
	scrape()
