from bs4 import BeautifulSoup
import sys, requests

def notBadURL(urlObject):
	url = urlObject['href']
	if url.startswith("/author"):
		return False
	if url.startswith("https://www.thedailybeast.com/category"):
		return False
	if url.startswith("/keyword"):
		return False
	if url.startswith("/cheat-sheet"):
		return False
	if url.startswith("/category"):
		return False
	if "Story__image-link" in str(urlObject):
		return False
	if "AuthorCard__image" in str(urlObject):
		return False
	if "TopBox__image-link" in str(urlObject):
		return False
	#if "img class" in str(urlObject):
	#	return False
	return True


def scrape():
	results = {}
	url = "https://www.thedailybeast.com"
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')

	sectionOne = soup.find("section", {"class":"GridTopBox"})
	for link in sectionOne.find_all('a', href=True):
		if notBadURL(link):
			#siteText += "\nLINK: "+ (str(link))

			myLink = link['href']
			results[myLink] = {}
			results[myLink]["text"] = link.text.strip()
			results[myLink]["notes"] = ""

	sectionTwo = soup.find("div", {"class":"HomePage__layout-wrapper"})
	for link in sectionTwo.find_all('a', href=True):
		if notBadURL(link):
			#siteText += "\nLINK: "+ (str(link))

			myLink = link['href']
			results[myLink] = {}
			results[myLink]["text"] = link.text.strip()
			results[myLink]["notes"] = ""

	return results

if __name__ == '__main__':
	run()
