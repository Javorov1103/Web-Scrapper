import datetime
from saraPenProductSrapper import SaraPenProdcutSpider
import scrapy
from scrapy.crawler import CrawlerProcess
import csv


class SaraPenSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://sarapenbg.com/product-category/%d0%bc%d1%8a%d0%b6%d0%ba%d0%b8-%d0%be%d0%b1%d1%83%d0%b2%d0%ba%d0%b8/%d0%b5%d0%b6%d0%b5%d0%b4%d0%bd%d0%b5%d0%b2%d0%bd%d0%b8-%d0%bc%d1%8a%d0%b6%d0%ba%d0%b8-%d0%be%d0%b1%d1%83%d0%b2%d0%ba%d0%b8/',
    ]
    
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'myjki_obuvki.csv',
        'LOG_ENABLED': False,
    }

    def parse(self, response):
        for quote in response.css('div.product-small'):
            yield {
                'category': quote.css('p.category::text').extract_first(),
                'product': quote.css('a.woocommerce-LoopProduct-link::text').extract_first(),
                'price': quote.css('bdi::text').extract_first(),
                'productLink': quote.css('a.woocommerce-LoopProduct-link::attr("href")').extract_first()
            }

        # next_page = response.css('li.next a::attr("href")').extract_first()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
            
begin_time = datetime.datetime.now()

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(SaraPenSpider)
process.start()

# with open('myjki_obuvki.csv', newline='') as csv_file:
#     reader = csv.DictReader(csv_file, delimiter=',')
#     for row in reader:
#         process.crawl(SaraPenProdcutSpider,start_urls=[row['productLink']])
#         process.start()

