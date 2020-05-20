from bs4 import BeautifulSoup
import sys, requests, json

def goodPage(urlObject):
	url = urlObject['href']
	text = urlObject.text.strip()


	if url.startswith('https://techcrunch.com/20'):
		return True
	if url.startswith('/20'):
		return True

	return False


def scrape():
	results = {}
	url = "https://techcrunch.com/"
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')

	#asdf have to mess with the JSON, i hate my life.
	#I wonder if I could have done this with CNN...
	#but parsing CNN was way harder for some reason
	scripts = [x for x in soup.find_all("script") if x.text.find("var tc_app_data") > -1][0].text
	scripts = json.loads(scripts[19:-2])
	articles = scripts["feature_islands"]["homepage"]

	for article in articles:
		myLink = article["link"]
		results[myLink] = {}
		results[myLink]["text"] = article["title"]["rendered"]
		results[myLink]["notes"] = ""


	for link in soup.find_all('a', href=True):
		if not goodPage(link):
			continue
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
