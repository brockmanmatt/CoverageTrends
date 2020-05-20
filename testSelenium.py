import timem, os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# "$ xvfb-run python test.py", this is how you run this script
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=chrome_options)
options=chrome_options

# Scraping steps
driver.get("cnn.com")
time.sleep(3)
print('Finished!')
driver.quit()
