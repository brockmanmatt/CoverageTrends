from bs4 import BeautifulSoup
import sys, requests
import os, pickle

def goodurl(linkobject):
	linktext = linkobject.text.strip()
	linkurl = linkobject['href'].strip()
	#print ("trying %s" % linkurl)
	if linktext == '':
		return False
	if linktext == 'Comments':
		return False
	if 'img alt' in str(linkobject):
		return False
	if linkurl.startswith("https://www.nytimes.com/20"):
		return True
	if linkurl.endswith(".html"):
		return True

	return False

def scrape():
	results = {}
	url = "http://nytimes.com/"
	page = requests.get(url)

	soup = BeautifulSoup(page.text, 'html.parser')

	for link in soup.find_all('a', href=True):
		myLink = link["href"]
		if goodurl(link):
			results[myLink] = {}
			results[myLink]["text"] = link.text.strip()
			results[myLink]["notes"] = ""

	return results
