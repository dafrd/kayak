import scrapy
#from booking.items import BookingItem
from scrapy.utils.response import open_in_browser
from scrapy.shell import inspect_response
from statistics import mean
import datetime
from dateutil.parser import parse 

class BookingSpider(scrapy.Spider):
    name = 'booking'
    allowed_domains = ['booking.com']
    site_url = "https://www.booking.com/index.fr-fr.html"

    custom_settings = {
        'FEED_EXPORT_FIELDS': ["booking_id", "name", "hotel_type", "scrapy_date", "start_date",
                                "end_date", "checkin_date", "checkout_date", "gap", "lat", "lng", "price_un", "price", "star_rating", "review_score",
                                "number_of_reviews", "number_of_rooms", "uri"],
    }

    def __init__(self, *args, **kwargs):
        super(BookingSpider, self).__init__(*args, **kwargs)
        self.city  = kwargs.get('city')
        self.start_date  = kwargs.get('start_date') # 2020/09/20
        self.end_date  = kwargs.get('end_date')
        self.gap  = int(kwargs.get('gap') or "1")

        if self.start_date is None:
            self.start_date = datetime.datetime.today() + datetime.timedelta(days=1)
        else: 
            self.start_date  = datetime.datetime.strptime(self.start_date, '%Y/%m/%d')

        if self.end_date is None:
            self.end_date = self.start_date + datetime.timedelta(days=30)
        else: 
            self.end_date  = datetime.datetime.strptime(self.end_date, '%Y/%m/%d')

        if self.end_date < self.start_date:
            raise Exception("end_data les than start_date")

    def start_requests(self):
        now = self.start_date
        while now <= self.end_date:
            print(now)
            yield scrapy.Request(self.site_url, 
                                callback=self.parse,
                                cb_kwargs=dict(checkin=now), dont_filter=True)
            now = now + datetime.timedelta(days=self.gap)