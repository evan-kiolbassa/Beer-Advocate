# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BeeradvocateItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    beer_name = scrapy.Field()
    brewery = scrapy.Field()
    beer_type = scrapy.Field()
    abv = scrapy.Field()
    style_rank = scrapy.Field()
    avg_rating = scrapy.Field()
    num_ratings = scrapy.Field()
    total_rank = scrapy.Field()
    adv_score = scrapy.Field()
    beer_desc = scrapy.Field()
