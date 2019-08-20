from selenium import webdriver
from lxml import html

# Global Variable
priceMax = ".10"
url = "http://www.ebay.com/sch/i.html?_from=R40&_sacat=0&_nkw=%28or%2Cand%2Cof%2Cis%2CI%2Cif%2Cat%2Cwhere%2Cwhen%29&rt=nc&_mPrRngCbx=1&_udlo=0&_udhi=" + priceMax

# Use selenium to get page source of url
driver = webdriver.Chrome()
driver.get(url)

# Form DOM tree using the page source
domTree = html.fromstring(driver.page_source.encode('utf-8'))

# Find all items and prices using xpaths
items = domTree.xpath('//a[@class="vip"]/text()')
prices = domTree.xpath('//li[@class="lvprice prc"]/span/text()')

# Loop and print the items with their corresponding prices
for i in range(0, 25):
   print "The item " + items[i].encode('utf-8') + " costs " + prices[i].encode('utf-8') + "." + "\n"

# Quit the driver
driver.quit()