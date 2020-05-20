from bs4 import BeautifulSoup
import sys, requests, json, time

def goodPage(urlObject):
	url = urlObject['href']
	text = urlObject.text.strip()


	if url.startswith('https://techcrunch.com/20'):
		return True
	if url.startswith('/20'):
		return True

	return False


def scrape(driver):
	results = {}
	url = "https://techcrunch.com/"
	driver.get(url)
	print("driver getting url")
	time.sleep(5)
	page = driver.page_source
	soup = BeautifulSoup(page, 'html.parser')

	#asdf have to mess with the JSON, i hate my life.
	#I wonder if I could have done this with CNN...
	#but parsing CNN was way harder for some reason
	#i think the datacenter this is hosted in is blocked though

	for header in soup.find_all("h2"):
		for link in header.find_all('a', href=True):
			if not goodPage(link):
				continue
			myLink = link["href"]
			if myLink in results:
				if len(results[myLink]["text"].strip()) > 10:
					continue

			results[myLink] = {}
			results[myLink]["text"] = link.text.strip()
			results[myLink]["notes"] = "h2"

	for header in soup.find_all("h3"):
		for link in header.find_all('a', href=True):
			if not goodPage(link):
				continue
			myLink = link["href"]
			if myLink in results:
				if len(results[myLink]["text"].strip()) > 10:
					continue

			results[myLink] = {}
			results[myLink]["text"] = link.text.strip()
			results[myLink]["notes"] = "h3"


	return results


if __name__ == '__main__':
	scrape()
