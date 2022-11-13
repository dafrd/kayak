from __future__ import absolute_import
from unicodedata import name
import scrapy
#from booking.items import BookingItem
from scrapy.utils.response import open_in_browser
from scrapy.shell import inspect_response
from statistics import mean
import datetime
#from dateutil.parser import parse 
import pandas as pd
import os
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from http import client
import json
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
import logging
import datetime
#from botocore.client import Config as BotoConf
import boto3
#from bookingscraper.items import BookingscraperItem
from scrapy.utils.log import configure_logging
from multiprocessing import Process, Queue
from twisted.internet import reactor
import scrapy.crawler as crawler

class BookingSpider(scrapy.Spider):

    name = 'booking'
    allowed_domains = ['booking.com']
    site_url = "https://www.booking.com/index.fr-fr.html"

    warmer_cities=[]

    weather_df = pd.read_csv ('weather.csv')

    checkin = str(datetime.date.today())
    checkout = str(datetime.date.today() + datetime.timedelta(days=2))

    for index, row in weather_df.iterrows():
        warmer_cities.append('https://www.booking.com/searchresults.fr.html?group_adults=2&checkin='+checkin+'&ss='+row['city']+'&no_rooms=1&checkout='+checkout+'&lang=fr&order=review_score_and_price')

    warmer_cities = warmer_cities[:5]
    start_urls=warmer_cities

    #https://www.booking.com/searchresults.fr.html?group_adults=2&checkin=2022-10-09&ss=Marseille&no_rooms=1&checkout=2022-10-11&lang=fr&order=review_score_and_price

    def parse(self, response):
        for hotel in response.css('div[data-testid="property-card"]'):
            hotel_url = hotel.css('a[data-testid="title-link"]::attr(href)').get()
            hotel_city = response.xpath('//*[@id="bodyconstraint-inner"]/div[1]/div/div/div/nav/ol/li[4]/span/a/span/text()').get()
            yield response.follow(hotel_url, callback=self.hotel_detail, cb_kwargs = {"hotel_city" : hotel_city})

    def hotel_detail(self, response, hotel_city):
            #hotel_item = BookingscraperItem()
            # hotel_item['hotel_city'] = hotel_city
            # hotel_item['hotel_url'] = response.url
            # hotel_item['hotel_name'] = response.xpath('//*[@id="hp_hotel_name"]/div/div/h2/text()').get()
            # hotel_item['hotel_description'] = response.xpath('//*[@id="property_description_content"]/p/text()').getall()
            # hotel_item['hotel_score'] = response.xpath('//*[@id="js--hp-gallery-scorecard"]/a/div/div/div/div/div[1]/text()').get()
            # hotel_item['hotel_coord'] = response.xpath('//*[@id="showMap2"]/a/@data-atlas-latlng').get()
            # yield hotel_item
             yield {
                 'hotel_city' : hotel_city,
                 'hotel_url' : response.url,             
                 'hotel_name' : response.xpath('//*[@id="hp_hotel_name"]/div/div/h2/text()').get(),
                 "hotel_description" : response.xpath('//*[@id="property_description_content"]/p/text()').getall(),
                 'hotel_score' :  response.xpath('//*[@id="js--hp-gallery-scorecard"]/a/div/div/div/div/div[1]/text()').get(),
                 'hotel_coord': response.xpath('//*[@id="showMap2"]/a/@data-atlas-latlng').get()   
             }        


# # the wrapper to make it run more times
# def run_spider(spider):
#     def f(q):
#         try:
#             runner = crawler.CrawlerRunner()
#             deferred = runner.crawl(spider)
#             deferred.addBoth(lambda _: reactor.stop())
#             reactor.run()
#             q.put(None)
#         except Exception as e:
#             q.put(e)

#     q = Queue()
#     p = Process(target=f, args=(q,))
#     p.start()
#     result = q.get()
#     p.join()

#     if result is not None:
#         raise result



# Name of the file where the results will be saved
path="json/"
filename = "booking_hotels.json"

# if the file exist, remove this
if filename in os.listdir(path):
    os.remove(path+filename)

    # Declare a new CrawlerProcess with some settings
## USER_AGENT => Simulates a browser on an OS
## LOG_LEVEL => Minimal Level of Log 
## FEEDS => Where the file will be stored 
## More info on built-in settings => https://docs.scrapy.org/en/latest/topics/settings.html?highlight=settings#settings

process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.DEBUG,
    #'FEED FORMAT' : ,
    'FEED URI' : path,
    "FEEDS": {
        path+filename : {"format": "json"},
    },
    "AUTOTHROTTLE_ENABLED" : False
})

#settings = get_project_settings()
#runner = CrawlerRunner(settings)
#runner.crawl(BookingscraperItem)
#runner.crawl(MySpider2)
#d = runner.join()
#d.addBoth(lambda _: reactor.stop())

#reactor.run() # the script will block here until all crawling jobs are finished

# configure_logging()
# print('first run:')
# run_spider(BookingSpider)

# print('\nsecond run:')
# run_spider(BookingSpider)

# Start the crawling using the spider you defined above
process.crawl(BookingSpider)
process.start()

client = boto3.client('s3',aws_access_key_id=os.environ['AWS_ACCESS_KEY'],aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
upload_file_bucket = "kayak-project-bucket"
upload_file_key = filename

client.upload_file(path+filename,upload_file_bucket,upload_file_key)
client.close()