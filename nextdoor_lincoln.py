from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import sys
import time
import csv

from lxml import html
import requests
import json

# Set up driver options
capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"

# Set up driver
driver = webdriver.Chrome(desired_capabilities=capa)
driver.get("https://lincolnheightssouthwest.nextdoor.com/news_feed/") # Put url in place of <URL of Neighborhood's Newsfeed>

time.sleep(5)

# Log In
username = driver.find_element_by_id("id_username")
password = driver.find_element_by_id("id_password")

username.send_keys("chi.zhang.7@usc.edu") # Put your username in place of <Username>
password.send_keys("morph6") # Put your password in place of <Password>

driver.find_element_by_id("signin_button").click()
time.sleep(5) # if not scrolling in time, make this number larger

# Use Selenium to scroll 'range' number of times
# Change the second number in 'range(x, y)' to determine how many times you want it to scroll down.
for i in range(1, 100):
	
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(3)

	# Find all "view all replies"
	numberOfElementsFound = driver.find_elements_by_xpath('//a[@class="see-previous-comments-link"]')

	# Scroll to top to avoid "Unable to click element" error
	if (i == 1):
		driver.execute_script("window.scrollTo(0, 0);")
		time.sleep(3)

	# Click all "view all replies" found previously to prepare to scrape the replies
	for pos in range (0, len(numberOfElementsFound)):
		if (numberOfElementsFound[pos].is_displayed()):
			try:
				time.sleep(1.5) 
				driver.execute_script("arguments[0].click();", numberOfElementsFound[pos])
			except Exception, e:
				#print e
				#print numberOfElementsFound[pos]
				pass

	# Click on "see more" to view full reply
	numberOfElementsFound = driver.find_elements_by_xpath('//a[@class="truncate-view-more-link"]')
	for pos in range (0, len(numberOfElementsFound)):
		if (numberOfElementsFound[pos].is_displayed()):
			try:
				time.sleep(1) 
				driver.execute_script("arguments[0].click();", numberOfElementsFound[pos])
			except:
				pass

time.sleep(1)

# Scrape the page source returned from Chrome driver for posts
html_source = driver.page_source
readable_html = html_source.encode('utf-8')
tree = html.fromstring(readable_html)
postNodes = tree.xpath('//div[@data-class="whole-story"]')

# Iterate over each post node to get data (ie authors, neighborhoods, etc) in an organized fashion
posts = [(p.xpath('.//a[@class="author-name"]/text()'),
 		  p.xpath('.//span[@class="post-byline"]/text() | .//span[@class="post-byline"]/*/text()'),
 		  p.xpath('.//*[@class="content-title-container"]/h5/text()'),
 		  p.xpath('.//a[@class="content-scope-line-audience-link"]/text()'),
 		  p.xpath('.//span[@class="content-scope-line-date"]/text()'),
 		  p.xpath('.//p[@class="content-body"]//span[@class="Linkify"]/text()'),
 		  p.xpath('.//a[@class="post-comment-count-link button-text"]/div/text()'),
 		  p.xpath('.//a[@class="comment-detail-author-name"]/text()'),
 		  p.xpath('.//span[@class="comment-detail-body-full"]/span/text()[1]'),
 		  p) for p in postNodes if p.xpath('.//a[@class="author-name"]/text()') != []]

# Create CSV Writer for first document (Posts)
ofile  = open('posts_lincoln.csv', "wb")
writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

# Create CSV Writer for second document (Replies)
rfile = open('replies_lincoln.csv', "wb")
rWriter = csv.writer(rfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
counter = 1

# Output to csv files
for p in posts:
	# Posts
	author = p[0][0]
	author = author.encode('utf8')

	location = "Unlisted"
	try:
		location = p[1][0]
		location = location.encode('utf8')
	except:
		pass

	title = "No Title"
	try:
		title = p[2][0]
		title = title.encode('utf8')
	except:
		pass

	category = "No Category"
	category_list = ""

	try:
		category = p[3][0]
		category = category.encode('utf8')
	except:
		category_list = p[9].xpath('.//span[@class="content-scope-line-hood-link js-scope-line-hoods"]/text()')
		try:
			category = category_list[0]
		except:
			pass
	
	date = "No Date"
	try:
		date = p[4][0]
		date = date.encode('utf8')
	except:
		pass

	content = "No Content"
	try:
		content = p[5][0]
		content = content.encode('utf8')
	except:
		pass
	
	numReplies = 0
	try:
		numReplies = p[6][0]
		numReplies = numReplies.encode('utf8')
	except:
		pass

	writer.writerow([author, location, title, category, date, content, numReplies])

	# Replies
	for c in range(0, len(p[7])):
		try:
			n = p[7][c]
		except Exception, e:
			# print e
			# print n
			# print c
			pass

		try:
			r = p[8][c]
		except Exception, e:
			# print e
			# print r
			# print c
			pass

		rWriter.writerow([counter, n.encode('utf-8'), r.encode('utf-8')])

	counter += 1

#driver.quit()