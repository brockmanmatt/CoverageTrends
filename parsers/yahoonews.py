from bs4 import BeautifulSoup
import sys, requests



def scrape():
	results = {}
	url = "https://news.yahoo.com/"
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')
	frontpage=soup.find("div", {"id":"Main"})

	for link in frontpage.find_all('a', href=True):
		myLink = link["href"]
		if myLink in results:
			if len(results[myLink]["text"].strip()) > 10:
				continue
		results[myLink] = {}
		results[myLink]["text"] = link.text.strip()
		results[myLink]["notes"] = ""
	return results


if __name__ == '__main__':
	scrape()
