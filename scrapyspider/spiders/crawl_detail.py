# -*- coding: utf-8 -*-
#
"""
 爬取工作详情的Spider（这里是重点）
"""


from scrapy import Request
from scrapy.spiders import Spider
from scrapyspider.items import jobItem
from scrapyspider.items import ZhilianUrlItem
import matplotlib.pyplot as plt
#from wordcloud import WordCloud
import jieba



class crawl_detail(Spider):    # 爬工作详情
    name = 'crawl_detail'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }
    start_urls = []

    def __init__(self):
        # 把'words.txt'的词取出来做词云
        # text_from_file_with_apath = open('words.txt').read()
        # wordlist_after_jieba = jieba.cut(text_from_file_with_apath, cut_all=True)
        # wl_space_split = " ".join(wordlist_after_jieba)
        # my_wordcloud = WordCloud().generate(wl_space_split)
        # plt.imshow(my_wordcloud)
        # plt.axis("off")
        # plt.show()

        # 添加第一页的搜索url（下面三种分别是：搜索职位列表、普通职位详情、校园职位详情）
        self.start_urls.append('http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%85%A8%E5%9B%BD&kw=%E5%A4%A7%E6%95%B0%E6%8D%AE&sm=0&p=1')
        #self.start_urls.append('http://jobs.zhaopin.com/120019970289260.htm?ssidkey=y&ss=201&ff=03&sg=4ac37027be424c4eb43d6192e565241e&so=3')
        #self.start_urls.append('https://xiaoyuan.zhaopin.com/job/CC000131952J90000087000')

        # 读取对应路径（里面存了所有url），并把全部url放到start_urls里面去供解析
        # links = open('D:/za/fuwuwaibao/git/scrapy-tutorial-main/scrapyspider/myurls')
        # for line in links:
        #     # 一定要去掉换行符，如果有换行符则无法访问网址，真他妈坑爹
        #     line = line[:-1]
        #     self.start_urls.append(line)
        #     # break

    # def start_requests(self):      # 此函数用来把url转换为request，转换之前还可以进行“增加头”等做法
    #     #jl=工作地点，kw=关键字，p=页码
    #     #url='http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%85%A8%E5%9B%BD&kw=%E5%A4%A7%E6%95%B0%E6%8D%AE&sm=0&p=1'
    #     url = 'http://jobs.zhaopin.com/250897935250039.htm?ssidkey=y&ss=201&ff=03&sg=ffe1b1324e3c493ebef6125f2f72869d&so=1'
    #     yield Request(url, headers=self.headers)

    def parse(self, response):
        # 处理response（回应）的html并解析，两种情况：
        # 1. 请求（request）的是搜索页面：获得一大堆详情url放到start_urls数组里面
        # 2. 请求（request）的是详情界面：切割获得职位详情得到item

        # 获得两个参数来判断是“搜索界面”还是“详情界面”
        search_url_type = response.xpath(
            './/div[@class="seach_yx"]/span/text()').extract()
        detail_url_type = response.xpath(
            './/div[@class="welfare-tab-box"]/span/text()').extract()

        # 普通职位详情页面时，得到job详情item：
        if len(detail_url_type)!=0: # 说明这是“职位详情界面”，以下使用xpath做解析
            print '职位详情界面'
            item = jobItem()
            item['job_name'] = response.xpath(
                './/div[@class="inner-left fl"]/h1/text()').extract()[0]
            item['job_form'] = response.xpath(
                './/ul[@class="terminal-ul clearfix"]/li[4]/strong/text()').extract()[0]
            item['job_type'] = response.xpath(
                './/ul[@class="terminal-ul clearfix"]/li[8]/strong/a/text()').extract()[0]
            item['work_location'] = response.xpath(
                './/ul[@class="terminal-ul clearfix"]/li[2]/strong/a/text()').extract()[0]
            item['job_salary'] = response.xpath(
                './/ul[@class="terminal-ul clearfix"]/li[1]/strong/text()').extract()[0]
            item['demand_people'] = response.xpath(
                './/ul[@class="terminal-ul clearfix"]/li[7]/strong/text()').re(ur'(\d+)人')[0]
            item['education_level'] = response.xpath(
                './/ul[@class="terminal-ul clearfix"]/li[6]/strong/text()').extract()[0]
            item['work_experience'] = response.xpath(
                './/ul[@class="terminal-ul clearfix"]/li[5]/strong/text()').extract()[0]
            item['job_description'] = response.xpath(
                './/ul[@class="tab-ul"]/li[1]/text()').extract()[0]
            item['company_name'] = response.xpath(
                './/div[@class="company-box"]/p[@class="company-name-t"]/a/text()').extract()[0]
            item['company_size'] = response.xpath(
                './/ul[@class="terminal-ul clearfix terminal-company mt20"]/li[1]/strong/text()').extract()[0]
            print item['company_size']
            yield item

        elif len(search_url_type)!=0: # 不是“详情界面”的情况下，如果是“搜索界面”
            print '搜索职位界面'
            # 搜索页面时，把得到的url都放到start_urls里面：
            job_tables = response.xpath('//div[@class="newlist_list_content"]/table')  # 得到一堆工作
            del job_tables[0]  # 第一行是列名（职位名称、年龄等），删除
            for job_table in job_tables:
                the_url = job_table.xpath('.//a[@target="_blank"]/@href').extract()[0]
                #self.start_urls.append(the_url)    # 爬虫队列新增url
                yield Request(the_url, headers=self.headers)

            next_url = response.xpath('//li[@class="pagesDown-pos"]/a/@href').extract()
            if next_url:
                next_url = next_url[0]
                #self.start_urls.append(next_url)
                yield Request(next_url, headers=self.headers)

        else:
            print '其他界面'

