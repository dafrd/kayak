#from credentials import access_key, secret_access_key
#from http import client
from gc import callbacks
import scrapy
import json
from scrapy.crawler import CrawlerProcess
import os
import logging
import destinations as dst
#import boto3
#from botocore.client import Config as BotoConfig

class BookingHotelsSpider(scrapy.Spider):
    name = 'bookinghotels'
    search_url = 'https://www.booking.com'
    urls_destinations=[]
    #https://www.booking.com/searchresults.fr.html?ss=Toulon&ssne=Toulon
    start_urls=['https://www.booking.com/']

    def parse(self, response):
        data = {
            'ss': 'Toulon' 
        }
        yield scrapy.FormRequest(url=self.search_url,formdata=data,callback=self.parse_hotels)
        # FormRequest used to make a search in Paris
        #return scrapy.FormRequest.from_response(
        #    response,
        #    formdata={'find_desc': search_keywords, 'dropperText_Mast': search_location},
        #    callback=self.after_search
      
    
    def parse_hotel(self, response):
        for hotel in response.css

# Name of the file where the results will be saved
path="01_scraping/json/"
filename = "espn_scores.json"

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

# Start the crawling using the spider you defined above
process.crawl(ESPNScoresSpider)
process.start()

client = boto3.client('s3',aws_access_key_id=os.environ['AWS_ACCESS_KEY'],aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])

upload_file_bucket = "nflpredictor-scrapy"
upload_file_key = filename

client.upload_file(path+filename,upload_file_bucket,upload_file_key)