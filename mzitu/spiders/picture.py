# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.selector import Selector

from mzitu.items import MzituItem


class PictureSpider(CrawlSpider):
    name = 'picture'
    allowed_domains = ['www.mzitu.com']
    start_urls = ['http://www.mzitu.com/all/']

    rules = (
        # Rule(LinkExtractor(allow=r'http://www.mzitu.com/\d+')),
        Rule(LinkExtractor(allow=r'http://www.mzitu.com/\d+',
                           deny=r'http://www.mzitu.com/\d+/\d+'), callback='parse_item'),
    )
    urls = []

    def parse_item(self, response):
        sel = Selector(response)
        item = MzituItem()
        item['classification'] = sel.xpath('/html/body/div[2]/div[1]/div[1]/a[2]/text()').extract_first(default="N/A")
        item['title'] = sel.xpath('/html/body/div[2]/div[1]/div[1]/text()[3]').extract_first(default="N/A")
        item['name'] = sel.xpath('/html/body/div[2]/div[1]/div[4]/span[1]/text()').extract_first(default="N/A")
        max_num = sel.xpath('./*//div[@class="pagenavi"]/a[last()-1]/span/text()').extract_first(default="N/A")
        print(max_num)
        item['url'] = response.url
        for num in range(1, int(max_num)+1):
            n_url = response.url + '/' + str(num)
            print('pic-' + n_url)
            yield scrapy.Request(n_url, callback=self.imgurl)
        item['image_urls'] = self.urls
        print('ij')
        yield item

    def imgurl(self, response):
        img_url = response.xpath('/html/body/div[2]/div[1]/div[3]/p/a/img/@src').extract_first(default="N/A")
        print(img_url)
        self.urls.append(img_url)


