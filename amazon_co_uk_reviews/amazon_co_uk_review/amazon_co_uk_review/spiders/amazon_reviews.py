import scrapy
import re

from scrapy.http import request
from ..user_agents import random_user_agent
from ..loaders import ReviewLoader
from datetime import datetime
from ..helper import extract_number


class AmazonReviewsSpider(scrapy.Spider):
    name = 'amazon_reviews'
    allowed_domains = ['www.amazon.co.uk']
    start_urls = ['http://www.amazon.co.uk/']
    position = 0
    asin =  'B07ZZW3KJY'
    # 'B08DCL3L8Y'
# 'B07B428M7F'
    def start_requests(self):

        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
            
        headers['User-Agent'] = random_user_agent()

        request_url = 'https://www.amazon.co.uk/product-reviews/'+self.asin+'/'

        yield scrapy.Request(
            url=request_url,
            callback=self.parse,
            headers=headers,
            meta={'page':1}
            )

    def parse(self, response):

        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

        urls = response.xpath('.//a[@data-hook="review-title"]/@href').extract()
        for url in urls:

            headers['User-Agent'] = random_user_agent()
            request_url = response.urljoin(url)
            yield scrapy.Request(
                url=request_url,
                callback=self.get_data,
                headers=headers,
                meta={'request_url':request_url})

        next_page_url = response.xpath('.//a[text()="Next page"]/@href').extract_first()
        if next_page_url:
            headers['User-Agent'] = random_user_agent()
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse,
                headers=headers,
                meta={'page':response.meta.get('page')+1})

    def get_data(self, response):

        item_loader = ReviewLoader(response=response)

        item_loader.add_value('Asin',self.asin)
        item_loader.add_xpath('Product_Title','.//a[@data-hook="product-link"]/text()')
        item_loader.add_xpath('Brand','.//span[@id="cr-arp-byline"]/a/text()')
        item_loader.add_xpath('Reviewed_Product_Attribute','.//a[@data-hook="format-strip"]/text()')
        item_loader.add_xpath('Review_Author','.//span[@class="a-profile-name"]/text()')

        item_loader.add_xpath('Review_Header','.//a[@data-hook="review-title"]/span/text()')
        item_loader.add_xpath('Review_Text','.//span[@data-hook="review-body"]/span/text()')
        
        item_loader.add_value('Review_Rating',int(extract_number(response.xpath('.//i[@data-hook="review-star-rating"]/span/text()').extract_first())))
        item_loader.add_value('No_of_people_reacted_helpful',int(extract_number(response.xpath('.//span[@data-hook="helpful-vote-statement"]/text()').extract_first())))

        review_date_raw = response.xpath('.//span[@data-hook="review-date"]/text()').extract_first()
        review_date = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)( \d{1,2}, \d{4})', review_date_raw)
        if review_date:
            item_loader.add_value('Review_Date',datetime.strptime(review_date.group(),'%B %d, %Y').strftime('%d %b %y'))

        item_loader.add_value('URL','https://www.amazon.co.uk/dp/'+self.asin)
        item_loader.add_value('Author_Profile',response.urljoin(response.xpath('.//a[@class="a-profile"]/@href').extract_first()))
        item_loader.add_value('Review_URL',response.meta.get('request_url'))

        yield item_loader.load_item()

