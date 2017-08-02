# -*- coding: utf-8 -*-
import scrapy

we_are_on_page = 1

class GiftSpider(scrapy.Spider):
    name = 'gift'
    allowed_domains = ['giftcardmall.am']
    start_urls = ['https://www.giftcardmall.am/en/?page=1']
    # or we can scrap from https://www.giftcardmall.am/en/all-cards
    # from one page

    def parse(self, response):
    	global we_are_on_page
    	cards = response.css("div.card")
    	if len(cards) > 0:
    		for card in cards:
    			name = card.css("h4 a::text").extract()[0]
    			link = card.css("h4 a::attr(href)").extract()[0]
    			price_texts = card.css("div.row p.card_sum::text").extract()
    			if len(price_texts) == 1:
    				# fixed price
    				avg_price = float(price_texts[0])
    			elif len(price_texts) >= 2:
    				# replace could be done with regex, but NO, Thanks.
    				avg_price = (float(price_texts[0]) + float(price_texts[1].replace(" - ", "")) )/2.0
    			yield {
    				name: {
    					"price": avg_price,
    					"link": link
    				}
    			}
    		we_are_on_page += 1
    		yield scrapy.Request("https://www.giftcardmall.am/en/?page=" + str(we_are_on_page))
