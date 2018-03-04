# -*- coding: utf-8 -*-
#
# 启动爬虫系统（填写name，选择要用的spider)


from scrapy import cmdline

#name = 'douban_movie_top250'
name='crawl_detail'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())
