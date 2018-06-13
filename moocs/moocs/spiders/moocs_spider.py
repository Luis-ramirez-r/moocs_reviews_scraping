# -*- coding: utf-8 -*-
import scrapy
from scrapy import  Request
from scrapy.loader import ItemLoader

from urlparse import urljoin 
from moocs.items import MoocsItem,MoocsReviewItem



class MoocsSpiderSpider(scrapy.Spider):
	name = "moocs_spider"
	#allowed_domains = ["https://www.coursetalk.com/subjects/data-science/courses"]
	start_urls = (
	    'https://www.coursetalk.com/subjects/business/courses',
	)


	def parse(self, response):
		courses_xpath = '//*[@class="course-listing-card"]//a[contains(@href, "/courses/")]/@href'
		courses_url = [urljoin(response.url,relative_url)  for relative_url in response.xpath(courses_xpath).extract()]  
		for course_url in courses_url[0:3]:
			print course_url
			yield Request(url=course_url, callback=self.parse_reviews)
		next_page_url =   response.xpath('//*[@class="js-course-pagination"]//a[contains(@aria-label,"Next")]/@href').extract_first()
		yield Request(url=next_page_url, callback=self.parse)


	def parse_reviews(self, response):
		#print response.body
		l = ItemLoader(item=MoocsItem(), response=response)
		l.add_xpath('course_title', '//*[@class="course-header-ng__main-info__name__title"]//text()')
		l.add_xpath('course_description', '//*[@class="course-info__description"]//p/text()')
		l.add_xpath('course_instructors', '//*[@class="course-info__instructors__names"]//text()')
		l.add_xpath('course_key_concepts', '//*[@class="key-concepts__labels"]//text()')
		l.add_value('course_link', response.url)
		l.add_value('course_provider', response.url)
		l.add_xpath('course_cost', '//*[@class="course-details-panel__course-cost"]//text()')
		l.add_xpath('university', '//*[@class="course-info__school__name"]//text()[2]')
		#'//*[@class="course-info__school__name"]'
		item = l.load_item()

		for review in response.xpath('//*[@class="review-body"]'):
		    r = ItemLoader(item=MoocsReviewItem(), response=response, selector=review)
		    r.add_value('course_title', item['course_title'])
		    r.add_xpath('review_body', './/div[@class="review-body__content"]//text()')
		    r.add_xpath('course_stage', './/*[@class="review-body-info__course-stage--completed"]//text()')
		    r.add_xpath('user_name', './/*[@class="review-body__username"]//text()')
		    r.add_xpath('review_date', './/*[@itemprop="datePublished"]/@datetime')
		    r.add_xpath('score', './/*[@class="sr-only"]//text()')

		    yield r.load_item()
		yield item
		reviews_pages = response.xpath('//*[@class="pagination__page-number"]//@href').extract()
		print "*"*10
		print reviews_pages
		for reviews_url in reviews_pages:
			yield Request(url=reviews_url, callback=self.parse_reviews)


