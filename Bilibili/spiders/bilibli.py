# -*- coding: utf-8 -*-
import json
import re
from datetime import datetime

import scrapy
from scrapy.http import Request
from Bilibili.items import BilibiliUserInfoItem, BilibiliUserStarItem, BilibiliUserUpStarItem, InputProcessorItemLoader


class BilibliSpider(scrapy.Spider):
    name = 'bilibili'
    allowed_domains = ['api.bilibili.com']
    start_urls = ['https://api.bilibili.com/x/space/acc/info?mid=98627270&jsonp=jsonp']
    followers_url = 'https://api.bilibili.com/x/relation/followers?' \
                    'vmid={}&pn={}&ps=20&order=desc&jsonp=jsonp&callback=__jp{}'
    followings_url = 'https://api.bilibili.com/x/relation/followings?' \
                     'vmid={}&pn={}&ps=20&order=desc&jsonp=jsonp&callback=__jp{}'

    def parse(self, response):
        """
        1.解析个人信息
        2.请求关注/粉丝地址
        3.请求播放量/阅读数地址
        :param response:
        :return:
        """
        user_data = json.loads(response.text)['data']
        item_loader = InputProcessorItemLoader(item=BilibiliUserInfoItem())
        item_loader.add_value('birthday', [user_data.get('birthday')])
        item_loader.add_value('face', [user_data.get('face')])
        item_loader.add_value('level', [user_data.get('level')])
        item_loader.add_value('mid', [user_data.get('mid')])
        item_loader.add_value('name', [user_data.get('name')])
        item_loader.add_value('official_desc', [user_data['official'].get('desc',), ])
        item_loader.add_value('official_role', [user_data['official'].get('role')])
        item_loader.add_value('official_title', [user_data['official'].get('title')])
        item_loader.add_value('rank', [user_data.get('rank')])
        item_loader.add_value('sex', [user_data.get('sex')])
        item_loader.add_value('sign', [user_data.get('sign')])
        item_loader.add_value('top_photo', [user_data.get('top_photo')])
        item_loader.add_value('vip_status', [user_data['vip'].get('status')])
        item_loader.add_value('vip_theme_type', [user_data['vip'].get('theme_type')])
        item_loader.add_value('vip_type', [user_data['vip'].get('type')])
        item_loader.add_value('up_data', [datetime.now()])

        yield item_loader.load_item()

        star_url = 'https://api.bilibili.com/x/relation/stat?' \
                   'vmid={}&jsonp=jsonp&callback=__jp3'.format(user_data.get('mid'))
        star_up_url = 'https://api.bilibili.com/x/space/upstat?' \
                      'mid={}&jsonp=jsonp&callback=__jp4'.format(user_data.get('mid'))

        # 请求关注/粉丝地址
        yield Request(url=star_url,
                      callback=self.star_parse)
        # 请求播放量/阅读数地址
        yield Request(url=star_up_url,
                      meta={'mid': user_data.get('mid')},
                      callback=self.stat_up_parse)

    def star_parse(self, response):
        """
        1.解析关注/粉丝数量
        2.请求关注列表地址
        3.请求粉丝列表地址
        :param response:
        :return:
        """
        data = re.match('__jp3\((.*)\)', response.text)
        user_data = json.loads(data.group(1))['data']
        item_loader = InputProcessorItemLoader(item=BilibiliUserStarItem())
        item_loader.add_value('mid', [user_data.get('mid')])
        item_loader.add_value('follower', [user_data.get('follower')])
        item_loader.add_value('following', [user_data.get('following')])
        item_loader.add_value('up_data', [datetime.now()])

        yield item_loader.load_item()

        # 请求粉丝列表地址
        yield Request(url=self.followers_url.format(user_data.get('mid'), 1, 10),
                      headers={'Referer': 'https://space.bilibili.com/{}/fans/fans'.format(user_data.get('mid'))},
                      callback=self.followers_detail_parse)
        # 请求关注列表地址
        yield Request(url=self.followings_url.format(user_data.get('mid'), 1, 12),
                      headers={'Referer': 'https://space.bilibili.com/{}/fans/fans'.format(user_data.get('mid'))},
                      callback=self.followings_detail_parse)

    def stat_up_parse(self, response):
        """
        1.解析播放量/阅读数数量
        :param response:
        :return:
        """
        data = re.match('__jp4\((.*)\)', response.text)
        user_data = json.loads(data.group(1))['data']
        item_loader = InputProcessorItemLoader(item=BilibiliUserUpStarItem())
        item_loader.add_value('mid', [response.meta.get('mid')])
        item_loader.add_value('archive_view', [user_data['archive'].get('view')])
        item_loader.add_value('article_view', [user_data['article'].get('view')])
        item_loader.add_value('up_data', [datetime.now()])

        yield item_loader.load_item()

    def followers_detail_parse(self, response):
        """
        1.解析粉丝的mid地址
        2.获取下一页
        :param response:
        :return:
        """
        tar_num = response.url.split('__jp')[-1]
        data = re.match('__jp{}\((.*)\)'.format(tar_num), response.text)
        user_data = json.loads(data.group(1))
        if user_data.get('data'):
            for user in user_data['data']['list']:
                user_url = 'https://api.bilibili.com/x/space/acc/info?mid={}&jsonp=jsonp'.format(user['mid'])
                yield Request(url=user_url,
                              headers={'Referer': 'https://space.bilibili.com/{}'.format(user['mid'])},
                              callback=self.parse)

        # 获取下一页 平台限制只能查看前五页
        for num in range(2, 6):
            yield Request(url=self.followers_url.format(user_data.get('mid'), num, 10+(num-1)*2),
                          headers={'Referer': 'https://space.bilibili.com/{}/fans/fans'.format(user_data.get('mid'))},
                          callback=self.followers_detail_parse)

    def followings_detail_parse(self, response):
        """
        1.解析关注的mid地址
        2.获取下一页
        :param response:
        :return:
        """
        tar_num = response.url.split('__jp')[-1]
        data = re.match('__jp{}\((.*)\)'.format(tar_num), response.text)
        user_data = json.loads(data.group(1))
        if user_data.get('data'):
            for user in user_data['data']['list']:
                user_url = 'https://api.bilibili.com/x/space/acc/info?mid={}&jsonp=jsonp'.format(user['mid'])
                yield Request(url=user_url,
                              headers={'Referer': 'https://space.bilibili.com/{}'.format(user['mid'])},
                              callback=self.parse)

        # 获取下一页 平台限制只能查看前五页
        for num in range(2, 6):
            yield Request(
                url=self.followings_url.format(user_data.get('mid'), num, 12+(num-1)*2),
                headers={'Referer': 'https://space.bilibili.com/{}/fans/fans'.format(user_data.get('mid'))},
                callback=self.followings_detail_parse)
