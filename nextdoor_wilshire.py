from selenium import webdriver

import sys
import time
import csv

from lxml import html
import requests
import json

# Set up driver
driver = webdriver.Chrome()
driver.get("https://wilshirenormandie.nextdoor.com/news_feed/") # Put url in place of <URL of Neighborhood's Newsfeed>

# Log In
username = driver.find_element_by_id("id_username")
password = driver.find_element_by_id("id_password")

username.send_keys("chizzymoi@gmail.com") # Put your username in place of <Username>
password.send_keys("metamorph6") # Put your password in place of <Password>

driver.find_element_by_id("signin_button").click()

# Use Selenium to scroll 'range' number of times
# Change the second number in 'range(x, y)' to determine how many times you want it to scroll down.
for i in range(1, 100):
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(1.5) # if not scrolling in time, make this number larger

# Click on "view all replies" when necessary to scrape all replies
numberOfElementsFound = driver.find_elements_by_xpath('//a[@data-action="view-all-comments-link"]')
for pos in range (0, len(numberOfElementsFound)):
	if (numberOfElementsFound[pos].is_displayed()):
		try:
			time.sleep(1.5)
			numberOfElementsFound[pos].click()
		except:
			print pos

time.sleep(5)

# Scrape the page source returned from Chrome driver for posts
html_source = driver.page_source
readable_html = html_source.encode('utf-8')
tree = html.fromstring(readable_html)
postNodes = tree.xpath('//div[@id="nf_stories"]/div[@data-class="whole-story"]')

# Iterate over each post node to get data (ie authors, neighborhoods, etc) in an organized fashion
posts = [(p.xpath('.//h5[@class="media-author"]//a[@data-class="linked-name"]/*/text()'),
 		  p.xpath('.//h5[@class="media-author"]//a[@data-type="neighborhood"]/text() | .//h5[@class="media-author"]//a[@class="notranslate"]/text() | .//p[@class="notranslate"]/text()'),
 		  p.xpath('.//h4[@class="media-heading"]//a[@class="notranslate"]/text()'),
 		  p.xpath('.//a[@href="/events/"]/text() | .//span[@data-class="topics-label"]/span[@class="notranslate"]/text() | .//span[@data-class="topics-label"]/a/text()'),
 		  p.xpath('.//span[@class="timestamp"]/span/@data-utc'),
 		  p.xpath('.//p[@data-class="post-content"]/@data-story | .//a[@class="title"]/span[@class="notranslate"]/text() | .//p[@data-class="post-content"]//span[@class="notranslate"]/text() | .//p/text()'),
 		  p.xpath('.//div[@data-class="comment-like-container"]/@data-num-comments'),
 		  p.xpath('.//h6[@class="media-author"]/span[@class="user-name js-profile-menu-init"]/a/span/text() | .//h6[@class="media-author"]/span[@class="user-name js-profile-menu-init"]/span/text()'),
 		  p.xpath('.//span[@class="notranslate"]/@data-story')) for p in postNodes if p.xpath('.//h5[@class="media-author"]//a[@data-class="linked-name"]/*/text()') != []]

# Create CSV Writer for first document (Posts)
ofile  = open('posts1.csv', "wb")
writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

# Create CSV Writer for second document (Replies)
rfile = open('replies1.csv', "wb")
rWriter = csv.writer(rfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
counter = 1

# Output to csv files
for p in posts:
	# Posts
	author = p[0][0]
	author = author.encode('utf8')
	location = p[1][0]
	location = location.encode('utf8')

	try:
		title = p[2][0]
		title = title.encode('utf8')
		category = p[3][0]
		category = category.encode('utf8')
	except:
		pass
		
	date = p[4][0]
	date = date.encode('utf8')
	content = p[5][0]
	if content != []: 
		content = content.encode('utf8')
	else:
		content = "Poll"
	numReplies = p[6][0]
	numReplies = numReplies.encode('utf8')
	writer.writerow([author, location, title, category, date, content, numReplies])

	# Replies
	for c in range(0, len(p[7])):
		try:
			n = p[7][c]
			r = p[8][c]
			rWriter.writerow([counter, n.encode('utf-8'), r.encode('utf-8')])
		except Exception, e:
			print n
			print r

	counter += 1

#driver.quit()