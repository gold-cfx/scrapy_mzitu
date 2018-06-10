# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

import scrapy
from scrapy.contrib.pipeline.images import  ImagesPipeline
from scrapy.exceptions import DropItem


class MzituPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        folder = item['classification']
        folder1 = item['title']
        folder1 = re.sub(r'[？\\*|“<>:/]', '', folder1)
        name = item['name'] + request.url.split('/')[-1]
        full_name = f'{folder}/{folder1}/{name}'
        print(full_name)
        return full_name

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            print('pipe-' + image_url)
            referer = item['url']
            print('referer-' + referer)
            yield scrapy.Request(image_url, meta={'item':item, 'referer':referer})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("No result")
        print(item)
        return item
