# Python Version 3.8.0

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains

import sys
import time
import csv

from lxml import html
import requests
import json

from dotenv import load_dotenv
import os
import pyautogui

# Seed random number generator
# Using random wait times to "simulate" a real user
random.seed()

# Load ability to use .env
load_dotenv()

# Set up driver options
capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"

# Set up driver
driver = webdriver.Chrome(desired_capabilities=capa, executable_path=os.getenv("chromedriver_path"))
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
for i in range(1, 11):
	
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(random.randint(3, 6))

	# Find all "previous comments and replies"
	numberOfElementsFound = driver.find_elements_by_xpath('//button[contains(@class, "see-previous-comments-button-paged")]')

	# Scroll to top to avoid "Unable to click element" error
	if (i == 1):
		driver.execute_script("window.scrollTo(0, 0);")
		time.sleep(random.randint(3, 6))

	# Click all "view all replies" found previously to prepare to scrape the replies
	for pos in range (0, len(numberOfElementsFound)):
		if (numberOfElementsFound[pos].is_displayed()):
			try:
				time.sleep(random.randint(1, 3)) 
				driver.execute_script("arguments[0].click();", numberOfElementsFound[pos])
			except Exception:
				pass

	# Click on "see more" to view full reply
	numberOfElementsFound = driver.find_elements_by_xpath('//a[@class="truncate-view-more-link"]')
	for pos in range (0, len(numberOfElementsFound)):
		if (numberOfElementsFound[pos].is_displayed()):
			try:
				time.sleep(random.randint(1, 3)) 
				driver.execute_script("arguments[0].click();", numberOfElementsFound[pos])
			except:
				pass

	print("Scroll {} finished!".format(i))

	# Save every 25 scrolls
	if (i % 5 == 0):

		time.sleep(30) # give browser time to catch up

		# Try saving with pyautogui
		pyautogui.hotkey("ctrl", "s")
		time.sleep(10) # give browser time to open 'save as' dialog

		pyautogui.typewrite("scroll{}.html".format(i))
		pyautogui.hotkey("enter")

		# Try saving with selenium
		path = os.getenv("selenium_html") + "scroll{}.html".format(i)
		with open(path, "w") as f:
    		f.write(driver.page_source)

