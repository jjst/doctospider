# -*- coding: utf-8 -*-
import re

import dateparser
import scrapy
from w3lib.html import remove_tags


class DoctolibSpider(scrapy.Spider):
    name = 'doctolib'
    allowed_domains = ['doctolib.fr']
    start_urls = [ 'https://www.doctolib.fr/vaccination-covid-19/rosheim?ref_visit_motive_ids[]=6970&ref_visit_motive_ids[]=7005' ]

    def parse(self, response):
        for post in response.css("#sr_content .box"):
            yield scrapy.Request(response.urljoin(post.css('a::attr(href)').extract_first()),
                                 callback=self.parse_property)

        next_page = response.css('.next_page a::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_property(self, response):
        ber = response.css('.ber-hover img::attr(alt)').re_first('BER (.*)')
        contains_gas = re.search('gas', response.css(
            '#smi-tab-content_holder').extract_first(), re.IGNORECASE)
        if (ber and ber.upper().startswith(("A", "B", "C"))) or contains_gas:
            yield {
                'url': response.url,
                'address': response.css('#address_box h1::text').extract_first().strip(),
                'price': response.css("#smi-price-string::text").extract_first(),
                'overview': [remove_tags(feature) for feature in response.css('#overview li').extract()],
                'ber_rating': ber,
                'facilities': response.css('#facilities li::text').extract(),
                'images': response.xpath('//img[contains(@style, "max-width:700px;")]/@src').extract(),
                'last_updated': dateparser.parse(response.xpath(
                    '(//*[@class="description_extras"]/h3[contains(text(), "Date Entered")])[1]/following-sibling::text()'
                ).extract_first().split(' ')[0])
            }
