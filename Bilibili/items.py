# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from datetime import datetime

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose

from Bilibili.tool.model import BilibiliUserInfo, BilibiliUserStar, BilibiliUserUpStar


class BilibiliItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class InputProcessorItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def date_birthday(value):
    return datetime.strptime(value, "%m-%d")


class BilibiliUserInfoItem(scrapy.Item):
    birthday = scrapy.Field(
        input_processor=MapCompose(date_birthday)
    )
    face = scrapy.Field()
    level = scrapy.Field()
    mid = scrapy.Field()
    name = scrapy.Field()
    official_desc = scrapy.Field()
    official_role = scrapy.Field()
    official_title = scrapy.Field()
    rank = scrapy.Field()
    sex = scrapy.Field()
    sign = scrapy.Field()
    top_photo = scrapy.Field()
    vip_status = scrapy.Field()
    vip_theme_type = scrapy.Field()
    vip_type = scrapy.Field()
    up_data = scrapy.Field()

    # 入库
    def get_insert_sql(self):
        user_info = BilibiliUserInfo(mid=self.get('mid'))
        user_info.birthday = self.get('birthday', '')
        user_info.face = self.get('face', '')
        user_info.level = self.get('level', 0)
        user_info.name = self.get('name', '')
        user_info.official_desc = self.get('official_desc', '')
        user_info.official_role = self.get('official_role', 0)
        user_info.official_title = self.get('official_title', '')
        user_info.rank = self.get('rank', 0)
        user_info.sex = self.get('sex', '')
        user_info.sign = self.get('sign', '')
        user_info.top_photo = self.get('top_photo', '')
        user_info.vip_status = self.get('vip_status', 0)
        user_info.vip_theme_type = self.get('vip_theme_type', 0)
        user_info.vip_type = self.get('vip_type', 0)
        user_info.up_data = self.get('up_data')

        existed_user_info = BilibiliUserInfo.select().where(BilibiliUserInfo.mid == self.get('mid'))
        if existed_user_info:
            user_info.save()  # 存在则更新
        else:
            user_info.save(force_insert=True)  # 不存在则添加


class BilibiliUserStarItem(scrapy.Item):
    mid = scrapy.Field()
    following = scrapy.Field()
    follower = scrapy.Field()
    up_data = scrapy.Field()

    # 入库
    def get_insert_sql(self):
        user_info = BilibiliUserInfo(mid=self.get('mid'))
        user_star = BilibiliUserStar(user_info=user_info)
        user_star.following = self.get('following', 0)
        user_star.follower = self.get('follower', 0)
        user_star.up_data = self.get('up_data')

        existed_user_star = BilibiliUserStar.select().where(BilibiliUserStar.user_info == user_info)
        if existed_user_star:
            user_star.save()  # 存在则更新
        else:
            user_star.save(force_insert=True)  # 不存在则添加


class BilibiliUserUpStarItem(scrapy.Item):
    mid = scrapy.Field()
    archive_view = scrapy.Field()
    article_view = scrapy.Field()
    up_data = scrapy.Field()

    # 入库
    def get_insert_sql(self):
        user_info = BilibiliUserInfo(mid=self.get('mid'))
        user_up_star = BilibiliUserUpStar(user_info=user_info)
        user_up_star.archive_view = self.get('archive_view', 0)
        user_up_star.article_view = self.get('article_view', 0)
        user_up_star.up_data = self.get('up_data')

        existed_user_up_star = BilibiliUserUpStar.select().where(BilibiliUserUpStar.user_info == user_info)
        if existed_user_up_star:
            user_up_star.save()  # 存在则更新
        else:
            user_up_star.save(force_insert=True)  # 不存在则添加
