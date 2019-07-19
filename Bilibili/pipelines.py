# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BilibiliPipeline(object):
    def process_item(self, item, spider):
        return item


class ToMysqlPipline(object):
    def process_item(self, item, spider):
        self.do_insert(item)
        return item

    def do_insert(self, item):
        item.get_insert_sql()
