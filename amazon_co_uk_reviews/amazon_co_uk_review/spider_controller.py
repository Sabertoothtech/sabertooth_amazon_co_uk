import sys
import os

from scrapy.crawler import CrawlerProcess

from amazon_co_uk_review.spiders.amazon_reviews import AmazonReviewsSpider

def crawl(asin):

    FILE_NAME = 'amazon_reviews.json'
    SETTINGS = {
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'FEED_FORMAT': 'json',
            'FEED_URI': FILE_NAME,
            'CONCURRENT_ITEMS': 1
            }

    os.remove(FILE_NAME)

    process = CrawlerProcess(SETTINGS)
    process.crawl(AmazonReviewsSpider,asin=asin)
    process.start()

    with open(FILE_NAME) as result:
        return result

def main():
    
    if len(sys.argv)==1:
        print("No categories entered")
        exit()

    FILE_NAME = 'amazon_products.json'
    SETTINGS = {
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'FEED_FORMAT': 'json',
            'FEED_URI': FILE_NAME,
            'CONCURRENT_ITEMS': 1
            }

    os.remove(FILE_NAME)

    process = CrawlerProcess(SETTINGS)
    process.crawl(AmazonReviewsSpider,asin=sys.argv[1])
    process.start()

    with open(FILE_NAME,'r') as result:
        print(result.read())

if __name__ == "__main__":
    main()
