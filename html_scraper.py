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

# Open local html file
with open(os.getenv("pyautogui_html"), "r", encoding="utf-8") as f:
    page = f.read()
tree = html.fromstring(page)
postNodes = tree.xpath('//div[contains(@class, "css-aqcial")]')

# Iterate over each post node that has an author to get data in an organized fashion
author_path = './/a[@class="_19bqJaQo dBEpfhFh"]/text()'
location_path = './/span/*[contains(@class, "post-byline-cursor")]/text()'
title_path = './/*[@class="content-title-container"]/a/text()'
category_path = './/div[@class="content-scope-line"]/span/a/text()'
date_path = './/a[@class="post-byline-redesign"]/text()'
post_content_path = './/p[contains(@class, "content-body")]//span[@class="Linkify"]/span/text()'
num_replies_path = './/span[contains(@class, "post-comment-count-text")]/text()'
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
ofile  = open('posts.csv', "w", encoding='utf-8')
writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
writer.writerow(["Post Number", "Author", "Location", "Title", "Category", "Date", "Content", "Number of Replies"])

# Create CSV Writer for second document (Replies)
rfile = open('replies.csv', "w", encoding='utf-8')
rWriter = csv.writer(rfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
rWriter.writerow(["From Post", "Author", "Reply Content"])
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
	
	numReplies = "0 Comments"
	try:
		numReplies = post[6][0].encode('utf8').decode('utf8')
	except:
		pass

	if numReplies == "Comment":
		numReplies = "0 Comments"

	writer.writerow([post_counter, author, location, title, category, date, content, numReplies])

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