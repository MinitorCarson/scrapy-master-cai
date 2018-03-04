# -*- coding: utf-8 -*-
#
"""
 爬取列表上所有职位的url（仅仅是url~~）（请忽视）
"""

from scrapy import Request
from scrapy.spiders import Spider
from scrapyspider.items import DoubanMovieItem, jobItem, ZhilianUrlItem


class DoubanMovieTop250Spider(Spider):
    name = 'douban_movie_top250'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):      # 此函数用来把url转换为request，转换之前还可以进行“增加头”等做法
        #jl=工作地点，kw=关键字，p=页码
        url='http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%85%A8%E5%9B%BD&kw=%E5%A4%A7%E6%95%B0%E6%8D%AE&sm=0&p=1'
        yield Request(url, headers=self.headers)  # request（请求）第一页的搜索url

    def parse(self, response):

        item2 = ZhilianUrlItem()
        job_tables = response.xpath('//div[@class="newlist_list_content"]/table')  # 得到一堆工作
        del job_tables[0]
        for job_table in job_tables:
            item2['url'] = job_table.xpath(
                './/a[@target="_blank"]/@href').extract()[0]
            print item2['url']
            # item['ranking'] = movie.xpath(
            #     './/div[@class="pic"]/em/text()').extract()[0]
            # item['movie_name'] = movie.xpath(
            #     './/div[@class="hd"]/a/span[1]/text()').extract()[0]
            # item['score'] = movie.xpath(
            #     './/div[@class="star"]/span[@class="rating_num"]/text()'
            # ).extract()[0]
            # item['score_num'] = movie.xpath(
            #     './/div[@class="star"]/span/text()').re(ur'(\d+)人评价')[0]
            yield item

        next_url = response.xpath('//li[@class="pagesDown-pos"]/a/@href').extract()
        if next_url:
            next_url = next_url[0]
            yield Request(next_url, headers=self.headers) # request（请求）下一页的搜索url

