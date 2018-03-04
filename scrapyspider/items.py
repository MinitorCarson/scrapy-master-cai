# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 豆瓣电影
class DoubanMovieItem(scrapy.Item):
    # 排名
    ranking = scrapy.Field()
    # 电影名称
    movie_name = scrapy.Field()
    # 评分
    score = scrapy.Field()
    # 评论人数
    score_num = scrapy.Field()

# 豆瓣电影
class zhilianItem(scrapy.Item):
    # 排名
    ranking = scrapy.Field()
    # 电影名称
    movie_name = scrapy.Field()
    # 评分
    score = scrapy.Field()
    # 评论人数
    score_num = scrapy.Field()

# 只有url的item
class ZhilianUrlItem(scrapy.Item):
    url = scrapy.Field()

# 工作职位item
class jobItem(scrapy.Item):
    #职位名称
    job_name = scrapy.Field()
    # 工作性质
    job_form = scrapy.Field()
    # 职位类别
    job_type = scrapy.Field()
    # 工作地址
    work_location = scrapy.Field()
    # 职位月薪
    job_salary = scrapy.Field()
    # 招聘人数
    demand_people = scrapy.Field()
    # 最低学历
    education_level = scrapy.Field()
    # 工作年限（经验）
    work_experience = scrapy.Field()
    # 职位描述
    job_description = scrapy.Field()
    # 公司名字
    company_name = scrapy.Field()
    # 公司规模
    company_size = scrapy.Field()