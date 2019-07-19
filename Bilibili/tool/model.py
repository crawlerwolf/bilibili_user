# -*- coding: utf-8 -*-
# author = crawlerwolf
from peewee import *


db = MySQLDatabase(
    database='test',
    host='127.0.0.1',
    port=3306,
    user='root',
    password='root',
    charset='utf8',
    use_unicode=True
)


class BaseModel(Model):
    class Meta:
        database = db


class BilibiliUserInfo(BaseModel):
    mid = IntegerField(primary_key=True)
    birthday = CharField(default='')
    face = CharField(default='', max_length=300)
    level = IntegerField(default=0)
    name = CharField(default='')
    official_desc = CharField(default='')
    official_role = IntegerField(default=0)
    official_title = CharField(default='')
    rank = IntegerField(default=0)
    sex = CharField(max_length=5)
    sign = CharField(default='')
    top_photo = CharField(default='', max_length=300)
    vip_status = IntegerField(default=0)
    vip_theme_type = IntegerField(default=0)
    vip_type = IntegerField(default=0)
    up_data = DateTimeField()


class BilibiliUserStar(BaseModel):
    user_info = ForeignKeyField(BilibiliUserInfo, primary_key=True)
    following = IntegerField(default=0)
    follower = IntegerField(default=0)
    up_data = DateTimeField()


class BilibiliUserUpStar(BaseModel):
    user_info = ForeignKeyField(BilibiliUserInfo, primary_key=True)
    archive_view = IntegerField(default=0)
    article_view = IntegerField(default=0)
    up_data = DateTimeField()


if __name__ == "__main__":
    db.create_tables([BilibiliUserInfo, BilibiliUserStar, BilibiliUserUpStar])
