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

from http import client
import json
from scrapy.crawler import CrawlerProcess
import logging
import datetime
#from botocore.client import Config as BotoConf

class BookingSpider(scrapy.Spider):

    name = 'booking'
    allowed_domains = ['booking.com']
    site_url = "https://www.booking.com/index.fr-fr.html"

    warmer_cities=[]
    #os.path.abspath(os.getcwd())

    #today = 

    weather_df = pd.read_csv ('weather.csv')

    checkin = str(datetime.date.today())
    checkout = str(datetime.date.today() + datetime.timedelta(days=2))

    for index, row in weather_df.iterrows():
        warmer_cities.append('https://www.booking.com/searchresults.fr.html?group_adults=2&checkin='+checkin+'&ss='+row['city']+'&no_rooms=1&checkout='+checkout+'&lang=fr&order=review_score_and_price')
        #print(row['city'])
        #weather_df = weather_df.head()
        #for city in weather_df.iterrows():
        #print(city)

    #warmer_cities = pd.DataFrame(warmer_cities)
    #warmer_cities = warmer_cities.head(6)
    #warmer_cities
    warmer_cities = warmer_cities[:5]
    start_urls=warmer_cities

    #https://www.booking.com/searchresults.fr.html?group_adults=2&checkin=2022-10-09&ss=Marseille&no_rooms=1&checkout=2022-10-11&lang=fr&order=review_score_and_price

    #def __init__(self, *args):

    def parse(self, response):

        for hotel in response.css('div[data-testid="property-card"]'):
            #try:
                #idgame = scores.css('section.Scoreboard.bg-clr-white.flex.flex-auto.justify-between::attr(id)').get()
                yield{
                    'city' : response.xpath('//*[@id="bodyconstraint-inner"]/div[1]/div/div/div/nav/ol/li[4]/span/a/span/text()').get(),
                    'hotel_name' : hotel.css('div[data-testid="title"]::text').get(),
                    'hotel_url': hotel.css('a[data-testid="title-link"]::attr(href)').get(),
                    'hotel_grade': hotel.css('div[data-testid="review-score"] > div::text').get(),
                    'price' : hotel.css('span[data-testid="price-and-discounted-price"]::text').get()
                    #'hotel_rating': ,
                    #'hotel_price': ,hote
                    #'week': response.css('div.custom--week.is-active > span.week.week-range::text').get(),
                    #'season' : split[9],
                    #'week' : split[7],
                    #'awayteam': scores.css('div.ScoreCell__TeamName.ScoreCell__TeamName--shortDisplayName.truncate.db::text').get(),
                    #'hometeam': scores.css('div.ScoreCell__TeamName.ScoreCell__TeamName--shortDisplayName.truncate.db::text').extract()[1],
                    #'awayscore' : scores.css('div.ScoreCell__Score.h4.clr-gray-01.fw-heavy.tar.ScoreCell_Score--scoreboard.pl2::text').get(),
                    #'homescore': scores.css('div.ScoreCell__Score.h4.clr-gray-01.fw-heavy.tar.ScoreCell_Score--scoreboard.pl2::text').extract()[1],
                    #'gamecast' : str('https://espn.com')+scores.css('a.AnchorLink.Button.Button--sm.Button--anchorLink.Button--alt.mb4.w-100.mr2::attr(href)').extract()[0],
                    #'boxscore' : str('https://espn.com')+scores.css('a.AnchorLink.Button.Button--sm.Button--anchorLink.Button--alt.mb4.w-100.mr2::attr(href)').extract()[1],
                    #'idgame' : scores.css('section.Scoreboard.bg-clr-white.flex.flex-auto.justify-between::attr(id)').get(),
                    #'awayteam global record' : scores.css('span.ScoreboardScoreCell__Record::text').get(),
                    #'awayteam away record' : scores.css('span.ScoreboardScoreCell__Record::text').extract()[1],
                    #'hometeam global record' : scores.xpath('//*[@id="'+idgame+'"]/div[1]/div/div[1]/div/div/ul/li[2]/div[1]/div[2]/span[1]/text()').get(),
                    #'hometeam home record' : scores.xpath('//*[@id="'+idgame+'"]/div[1]/div/div[1]/div/div/ul/li[2]/div[1]/div[2]/span[2]/text()').get()
                }
           

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

# Start the crawling using the spider you defined above
process.crawl(BookingSpider)
process.start()

#client = boto3.client('s3',aws_access_key_id=os.environ['AWS_ACCESS_KEY'],aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])

#upload_file_bucket = "nflpredictor-scrapy"
#upload_file_key = filename

#client.upload_file(path+filename,upload_file_bucket,upload_file_key)