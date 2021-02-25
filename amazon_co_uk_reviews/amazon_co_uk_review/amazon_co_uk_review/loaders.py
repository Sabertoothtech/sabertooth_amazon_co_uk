from scrapy.loader import ItemLoader
from itemloaders.processors import Join, MapCompose, TakeFirst, Identity
from w3lib.html import remove_tags
from .items import ReviewItem

def filter_empty(_s):
    return _s or None

class ReviewLoader(ItemLoader):
    default_item_class = ReviewItem

    default_output_processor = TakeFirst()

    Reviewed_Product_Attribute_out = Join(separator=' | ')

    def __init__(self, response):
        super(ReviewLoader, self).__init__(response=response)

        self.images_in = MapCompose(response.urljoin, str.strip) 