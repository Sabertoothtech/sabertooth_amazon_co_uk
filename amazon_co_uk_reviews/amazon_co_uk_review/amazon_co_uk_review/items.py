# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ReviewItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    Asin = scrapy.Field()
    Product_Title = scrapy.Field()
    Brand = scrapy.Field()
    Reviewed_Product_Attribute = scrapy.Field()
    Review_Author = scrapy.Field()
    Review_Rate = scrapy.Field()
    Review_Date = scrapy.Field()
    Review_Header = scrapy.Field()
    Review_Text = scrapy.Field()
    Review_Rating = scrapy.Field()
    Review_Comment_Count = scrapy.Field()
    No_of_people_reacted_helpful = scrapy.Field()
    Author_Profile = scrapy.Field()
    URL = scrapy.Field()
    Review_URL = scrapy.Field()
