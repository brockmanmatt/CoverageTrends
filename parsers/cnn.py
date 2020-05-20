from bs4 import BeautifulSoup
import sys, requests, time

def notBadURL(url):
	if url.startswith("/vi"):
		return False

	if url.startswith("/videos"):
		return False

	if not url.startswith("/"):
		return False

	return True

"""
k, cnn's officially wierd
"""
def scrape():

	for i in range (4):
		try:
			results = {}
			url = "http://www.cnn.com/"
			page = requests.get(url)
			soup = BeautifulSoup(page.text, 'html.parser')

			currentContainer = soup.find_all("script")
			for script in currentContainer:
				if (script.text.find("articleList") > -1):
					urls = script.text.split("\"uri\":")
					urls = urls[1:]

					try:
						urls[len(urls)-1] = urls[len(urls)-1][:urls[len(urls)-1].find("\",\"layout")]
					except:
						continue
					for url in urls:
						myURL = url[1:url.find(".html")+5]

						if not notBadURL(myURL):
							continue

						headline = url[url.find("headline")+11:url.find("\",\"thumbnail")]
						if headline[0] == "\\":
							headline = headline[13:len(headline)-14]
						results[myURL] = {}
						results[myURL]["text"] = headline
						results[myURL]["notes"] = ""


			return results
		except:
			time.sleep(5)

if __name__ == '__main__':
	scrape()
