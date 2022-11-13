# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
#import psycopg2


class BookingscraperPipeline:

    # def __init__(self):
    #     hostname = 'xxx'
    #     port = 'xxx'
    #     username = 'xxx'
    #     password = 'xxxx' # your password
    #     database = 'kayak-project'

    #     ## Create/Connect to database
    #     self.connection = psycopg2.connect(host=hostname, port=port, user=username, password=password, dbname=database)

    #     ## Create cursor, used to execute commands
    #     self.cur = self.connection.cursor()

    #     ## Create quotes table if none exists
    #     self.cur.execute("""
    #     CREATE TABLE IF NOT EXISTS kayak(
    #         id serial PRIMARY KEY, 
    #         hotel_city text,
    #         hotel_url text,
    #         hotel_name text,
    #         hotel_description text,
    #         hotel_score text,
    #         hotel_coord text
    #     )
    #     """)


    # def process_item(self, item, spider):

    #     ## Define insert statement
    #     self.cur.execute(""" insert into kayak (hotel_city, hotel_url, hotel_name, hotel_description, hotel_score, hotel_coord) values (%s,%s,%s,%s,%s,%s)""", (
    #         item["hotel_city"],
    #         item["hotel_url"],
    #         item["hotel_name"],
    #         item["description"],
    #         item["score"],
    #         item["coord"]
    #     ))

    #     ## Execute insert of data into database
    #     self.connection.commit()
    #     return item

    # def close_spider(self, spider):

    #     ## Close cursor & connection to database 
    #     self.cur.close()
    #     self.connection.close()
    pass
