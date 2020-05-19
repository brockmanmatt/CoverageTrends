from bs4 import BeautifulSoup
import sys, requests

def goodPage(urlObject):
	url = urlObject['href']
	title = urlObject.text.strip()
	if urlObject.find('h3'):
		title = urlObject.find('h3').text.strip()
	if urlObject.find("picture"):
		return False
	if title == 'Email page link':
		return False
	if title == 'Local':
		return False
	if title == 'Privacy Policy':
		return False
	if title == '':
		return False
	if title == 'Advertise':
		return False
	if title == 'Find Affiliate':
		return False
	if title == 'Extended Forecast':
		return False
	if len(url.split('/')) < 4:
		return False
	if title == 'advertisement':
		return False
	if title == 'NBC Learn':
		return False
	if title == 'Get Breaking news updates':
		return False
	if url.startswith('https://'):
		if len(url.split('/')) < 6:
			return False
	if url.startswith('http://'):
		if len(url.split('/')) < 6:
			return False
	if 'video' in url.split('/'):
		return False
	#if not url.startswith('/'):
	#	return False
	if url.find('/news/us-news/nbc-affiliates') > -1:
		return False
	if url in ["https://www.snapchat.com/add/Stay-Tuned/8367265869"]: return False
	return True


def scrape():
	results = {}
	url = "https://www.nbcnews.com/"
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')

	for link in soup.find_all("a", href=True):
		if not goodPage(link):
			continue
		myLink = link["href"]

		results[myLink] = {}
		results[myLink]["text"] = link.text.strip()
		results[myLink]["notes"] = ""
	return results


if __name__ == '__main__':
	scrape()
