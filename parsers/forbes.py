from bs4 import BeautifulSoup
import sys, requests

def goodPage(url):


	if 'sites' in url.split('/'):
		return True


	return False



#k, this is a giant blob of JSON

def scrape():
	results = {}
	url = "https://www.forbes.com/"
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')

	for link in soup.find_all("a", {"class":"happening__title"}):
		myLink = link['href']
		results[myLink] = {}
		results[myLink]["text"] = link.text.strip()
		results[myLink]["notes"] = ""


	return results

if __name__ == '__main__':
	run()
