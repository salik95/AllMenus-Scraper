# -*- coding: utf-8 -*-
import scrapy
import csv
import json
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

state_name = 'Texas'
data = {}
data[state_name] = {}
url = []

class AlmenSpider(scrapy.Spider):
	name = 'almen'
	start_urls = url

	def __init__(self):
		dispatcher.connect(self.spider_closed, signals.spider_closed)
		with open(state_name + '.csv') as csvfile:
			for item in csvfile:
				data[state_name][item.split(',')[0].strip('\n')] = []
				url.append(item.split(',')[1].strip('\n') + '-/')
	
	def parse(self, response):
		for href in response.css('li.restaurant-list-item .name a::attr(href)').extract():
			yield response.follow('https://www.allmenus.com' + href, self.parse_author)

	def parse_author(self, response):
		city_name = response.css('ul.s-list-inline-breadcrumb li a::text').extract()[1].strip()
		rest_name = response.css('div.restaurant-summary h1 span::text').extract_first().strip()

		rest_address = response.css('a.menu-address::text').extract_first()
		if rest_address is None:
			rest_address = 'N/A'
		else:
			rest_address = rest_address.strip()

		rest_number = response.css('a.menu-phone-number::text').extract_first()
		if rest_number is None:
			rest_number = 'N/A'
		else:
			rest_number = rest_number.strip()

		rest_cuisine = response.css('li.cuisine a::text').extract()
		if not rest_cuisine:
			rest_cuisine = 'N/A'

		rest_website = response.css('a.menu-link::attr(href)').extract_first()
		if rest_website is None:
			rest_website = 'N/A'
		else:
			rest_website = rest_website.strip()

		rest_price = response.css('span.active-dollar::text').extract_first()
		if rest_price is None:
			rest_price = 'N/A'
		else:
			rest_price = str(len(rest_price)) + '/5'

		menu = {}
		for item in response.css('li.menu-category'):
			
			category_name = item.css('div.category-name::text').extract_first()
			menu[category_name] = []
			
			for dish in item.css('li.menu-items'):
				
				dish_name = dish.css('span.item-title::text').extract_first()
				
				dish_price = dish.css('span.item-price::text').extract_first()
				if dish_price is None or dish_price is '':
					dish_price = 'N/A'
				else:
					dish_price = dish_price.strip('\n').strip('\r').strip()
					if dish_price is None or dish_price is '':
						dish_price = 'N/A'
				
				dish_description = dish.css('p.description::text').extract_first()
				if dish_description is None or dish_description is '':
					dish_description = 'N/A'
				else:
					dish_description = dish_description.strip('\n').strip('\r').strip()

				menu[category_name].append([dish_name, dish_price, dish_description])
		
		if not menu:
			menu = 'N/A'
		
		try:
			data[state_name][city_name].append({'Restaurant Name':rest_name, 'Restaurant Address':rest_address, 'Restaurant Phone Number':rest_number, 'Restaurant Cuisine':rest_cuisine, 'Restaurant Website':rest_website, 'Restaurant Price':rest_price, 'Restaurant Menu':menu})
		except:
			pass
		
		pass

	def spider_closed(self, spider):
		print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
		with open(state_name + '.json', 'w') as fp:
			json.dump(data, fp)
		print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')