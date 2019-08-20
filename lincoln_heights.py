import unicodecsv
import scrapy
import re
from scrapy.http.request import Request
from scrapy.selector import Selector
from urllib2 import unquote

externalCounter = 0

class LincolnHeightsSpider(scrapy.Spider):
    name = "LincolnHeights"

    def start_requests(self):

        # Create CSV Writer for csv document

        # Comment out lines 18 and 19 if you want to append to file
        ffile = open('./csv/lincoln_heights.csv', "w+")
        ffile.close()

        # Get listings for Lincoln Heights as JSON through Trulia
        url = 'https://www.zillow.com/homes/for_sale/Lincoln-Heights-Los-Angeles-CA/116206_rid/34.121682,-118.149462,34.024138,-118.273058_rect/12_zm/1_p/1_rs/1_fr/'
        request = Request(url=url, callback=self.parse_json)
        yield request

    def parse_json(self, response):
        data = json.loads(response.text)
        listings = data['dots']
        size = len(listings)

        for i in range (0, size):
            url = listings[i]['url']
            request = Request("https://www.trulia.com/" + url, callback=self.parse_link)
            request.meta['address'] = listings['address']
            request.meta['price'] = listings['price']
            yield request

    def parse_link(self, response):
        sel = Selector(response)

        # Date
        date = sel.xpath('//div[@class="mbm"]/span[@class="typeLowlight h6"]/text()')
        date = date.extract()
        date = date[0].encode('utf-8')

        # Address
        address = response.meta['address']

        # Square Feet
        sqft = sel.xpath('//ul[@class="listInlineBulleted man pts ptXxsHidden pbsXxsVisible"]/li[1]/text()')
        sqft = sqft.extract()
        sqft = sqft[0].encode('utf-8')

        # Get Info Column 2
        infoCols = sel.xpath('//ul[@class="man"]')
        colTwo = infoCols[1]

        # Listing Type
        lType = colTwo.xpath('/li[3]/text()')

        with open('./csv/lincoln_heights.csv', "ab") as ffile:
            writer = unicodecsv.writer(ffile, delimiter=',', quotechar='"', quoting=unicodecsv.QUOTE_ALL)
            writer.writerow(['LH'+str(externalCounter), date, address, sqft, lType])

        externalCounter += 1
