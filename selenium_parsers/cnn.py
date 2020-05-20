from bs4 import BeautifulSoup
import sys, requests, time

def notBadURL(url):

	if not url.startswith("/"):
		return False

	return True

"""
k, cnn's officially wierd
"""
def scrape(driver):
	results = {}
	url = "http://www.cnn.com/"
	driver.get(url)
	print("driver getting url")
	time.sleep(5)
	page = driver.page_source
	soup = BeautifulSoup(page, 'html.parser')

	for link in soup.find_all("article"):
		for url in link.find_all("a"):
			myURL = url["href"]
			results[myURL] = {}
			results[myURL]["text"] = url.text
			results[myURL]["notes"] = ""
			if link.find("h2"):
				results[myURL]["notes"] = "h2"

	return results

if __name__ == '__main__':
	scrape()
