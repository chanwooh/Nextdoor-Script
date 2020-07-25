# Python Version 3.8.0

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import sys
import time
import csv

from lxml import html
import requests
import json

from dotenv import load_dotenv
import os

# Load ability to use .env
load_dotenv()

# Set up driver options
capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"

# Set up driver
driver = webdriver.Chrome(desired_capabilities=capa, executable_path='/Users/charliehwang/Desktop/Nextdoor-Script/chromedriver')
driver.get("https://nextdoor.com/login/")

time.sleep(10)

# Log In
username = driver.find_element_by_id("id_email")
password = driver.find_element_by_id("id_password")

username.send_keys(os.getenv("email")) # Retrieved from .env file
password.send_keys(os.getenv("password")) # Retrieved from .env file
driver.find_element_by_xpath('//button[@id="signin_button"]').click()
time.sleep(10) # if not scrolling in time, make this number larger

# Click the pop up, if one appears
try:
	driver.find_element_by_xpath("//button[@class='channels-bulk-join-close-button']").click()
except:
	pass

# Use Selenium to scroll 'range' number of times
# Change the second number in 'range(x, y)' to determine how many times you want it to scroll down.
for i in range(1, 2):
	
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(3)

	# Find all "previous comments and replies"
	numberOfElementsFound = driver.find_elements_by_xpath('//button[contains(@class, "see-previous-comments-button-paged")]')

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
			except Exception:
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
postNodes = tree.xpath('//article[@class="post-container"]')

# Iterate over each post node that has an author to get data in an organized fashion
author_path = './/div[@class="avatar-toggle-node"]/a/text()'
location_path = './/span/*[contains(@class, "post-byline-cursor")]/text()'
title_path = './/*[@class="content-title-container"]/h5/text()'
category_path = './/a[@class="content-scope-line-audience-link"]/text()'
date_path = './/div[@class="content-scope-line"]/a[1]/text()'
post_content_path = './/p[@class="content-body"]//span[@class="Linkify"]/text()'
num_replies_path = './/span[@class="post-comment-count-text"]/text()'
reply_author_path = './/a[@class="comment-detail-author-name"]/text()'
reply_content_path = './/span[@class="Linkify"]/span/text()'

posts = [(post.xpath(author_path),
 		  post.xpath(location_path),
 		  post.xpath(title_path),
 		  post.xpath(category_path),
 		  post.xpath(date_path),
 		  post.xpath(post_content_path),
 		  post.xpath(num_replies_path),
 		  post.xpath(reply_author_path),
 		  post.xpath(reply_content_path),
 		  post) for post in postNodes if post.xpath(author_path) != []]

# Create CSV Writer for first document (Posts)
ofile  = open('posts.csv', "w")
writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

# Create CSV Writer for second document (Replies)
rfile = open('replies.csv', "w")
rWriter = csv.writer(rfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
post_counter = 1

# Output to csv files
for post in posts:
	# Posts
	author = post[0][0].encode('utf8').decode('utf8')

	location = "Unlisted"
	try:
		location = post[1][0].encode('utf8').decode('utf8')
	except:
		pass

	title = "No Title"
	try:
		title = post[2][0].encode('utf8').decode('utf8')
	except:
		pass

	category = "No Category"
	category_list = ""

	try:
		category = post[3][0].encode('utf8').decode('utf8')
	except:
		category_list = post[9].xpath('.//span[@class="content-scope-line-hood-link js-scope-line-hoods"]/text()')
		try:
			category = category_list[0]
		except:
			pass
	
	date = "No Date"
	try:
		date = post[4][0].encode('utf8').decode('utf8')
	except:
		pass

	content = "No Content"
	try:
		content = post[5][0].encode('utf8').decode('utf8')
	except:
		pass
	
	numReplies = 0
	try:
		numReplies = post[6][0].encode('utf8').decode('utf8')
	except:
		pass

	writer.writerow([author, location, title, category, date, content, numReplies])

	# Replies
	# Iterate through all replies with an author (post[7])
	for count in range(0, len(post[7])):
		try:
			name = post[7][count].encode('utf-8').decode('utf8')
		except Exception:
			pass

		try:
			reply = post[8][count].encode('utf-8').decode('utf8')
		except Exception:
			pass

		rWriter.writerow([post_counter, name, reply])

	post_counter += 1

driver.quit()