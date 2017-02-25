# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request


class TaobaommPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):

        yield Request(item['image_url'],meta={'item':item})

    def item_completed(self, results, item, info):
        image_path = [ x['path'] for ok,x in results if ok ]
        if not image_path:
            raise DropItem('Item中不包含不图片')
        item['image_path'] = image_path
        return item

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        filepath = 'full/' + '{0}_{1}.jpg'.format(item['name'],item['desc'])
        return filepath
