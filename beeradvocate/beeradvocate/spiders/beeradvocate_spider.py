from scrapy import Spider, Request
from beeradvocate.items import BeeradvocateItem
import re

class Beeradvocate(Spider):
    name = 'beeradvocate_spider'
    allowed_domains = ['www.beeradvocate.com']
    start_urls = ['https://www.beeradvocate.com/beer/styles/']

    def parse(self, response):
    	styles = response.xpath('//div[@class = "stylebreak"]//li/a/@href').extract()
    	styles_urls = ['https://www.beeradvocate.com{}'.format(i) for i in styles]
    	for url in styles_urls:
            yield Request(url=url, callback=self.parse_styles_page)

    def parse_styles_page(self, response):
        print("+"*55)
        print("AYYYYYY")
        print("+"*55)

        beer_urls = response.xpath('//td[@class = "hr_bottom_light"]/a/@href').extract()

        adv_urls = ['https://www.beeradvocate.com{}'.format(i) for i in beer_urls]
        for url in adv_urls:
            yield Request(url=url, callback=self.parse_beer_page)

    def parse_beer_page(self, response):
        page = response.xpath('//div[@class="mainContent"]')

        for value in page:
        	beer_name = response.xpath('//div[@class="titleBar"]/h1/text()').extract()
        	brewery = response.xpath('//*[@id="info_box"]/div[2]/dl/dd[7]/a/text()').extract()
        	beer_type = response.xpath('//a[@class="Tooltip"]/b/text()').extract()
        	abv = response.xpath('////*[@id="info_box"]/div[2]/dl/dd[2]/span/b/text()').extract()
        	avg_rating = response.xpath('//span[@class="ba-ravg Tooltip"]/text()').extract()
        	num_ratings = response.xpath('//span[@class="ba-ratings Tooltip"]/text()').extract()
        	style_rank = response.xpath('////*[@id="info_box"]/div[2]/dl/dd[1]/a[2]/text()').extract()
        	total_rank = response.xpath('//*[@id="info_box"]/div[2]/dl/dd[3]/a').extract()
        	adv_score = response.xpath('//span[@class="ba-score Tooltip"]/b/text()').extract()
        	beer_desc = response.xpath('////*[@id="ba-content"]/div[4]/div[2]/text()').extract()
        	item = BeeradvocateItem()
        	item['beer_name'] = beer_name
        	item['brewery'] = brewery
        	item['beer_type'] = beer_type
        	item['abv'] = abv
        	item['style_rank'] = style_rank
        	item['avg_rating'] = avg_rating
        	item['num_ratings'] = num_ratings
        	item['adv_score'] = adv_score
        	item['beer_desc'] = beer_desc
        	item['total_rank'] = total_rank
        	yield item
        

