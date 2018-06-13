# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose, MapCompose, Join, TakeFirst
import re


clean_text = Compose(MapCompose(lambda v: v.strip()), Join())   

#clean_text = Compose(MapCompose(lambda v: v.upper()), Join())   


def procesor_test(text):
	text = ','.join([v.strip() for v in text ])
	#text = clean_text(text)
	return '"""' + text.strip() + '"""'

def quote_field(text):
	text = clean_text(text)
	return '"""' + text.strip() + '"""'

def get_provider(url):
	try:
		return  re.search('providers/([^/]+)',url[0] ).group(1)
	except:
		return 'Not found'

def get_university(text):
	text = text[0]
	text = clean_text(text)
	return text

class MoocsItem(scrapy.Item):
	# define the fields for your item here like:
	course_title = scrapy.Field(output_processor=clean_text)
	course_instructors = scrapy.Field(output_processor=quote_field)
	course_description = scrapy.Field(output_processor=quote_field)    
	course_key_concepts = scrapy.Field(output_processor=procesor_test)
	course_link = scrapy.Field()
	course_provider =  scrapy.Field(output_processor=get_provider)
	course_cost = scrapy.Field(output_processor=clean_text)
	university = scrapy.Field(output_processor=get_university)
	## reviews

class MoocsReviewItem(scrapy.Item):
	course_title = scrapy.Field(output_processor=clean_text)
	review_body = scrapy.Field(output_processor=quote_field)
	course_stage = scrapy.Field(output_processor=quote_field)
	user_name = scrapy.Field(output_processor=clean_text)
	review_date = scrapy.Field(output_processor=clean_text)
	score = scrapy.Field(output_processor=clean_text)



class MyItemLoader(ItemLoader):
    default_item_class = MoocsItem
    course_title = clean_text

