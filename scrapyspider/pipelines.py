# -*- coding: utf-8 -*-
# encoding=utf-8

"""
 处理items的地方，以下有几个pipeline
 不同的pipeline有不同的处理item的方式
 在setting选择启用哪一个pipeline
"""

import codecs
import json
# import  xlsxwriter
from twisted.enterprise import adbapi
# import MySQLdb
# import MySQLdb.cursors

# 保存item到json文件
class JsonWithEncodingPipeline(object):
    """保存到文件中对应的class
       1、在settings.py文件中配置
       2、在自己实现的爬虫类中yield item,会自动执行"""
    def __init__(self):
        self.file = codecs.open('info.json', 'w', encoding='utf-8')   #打开储存的文件

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"  #转为json的
        print line
        print('++++++++++++     开始储存      ++++++++++++')
        self.file.write(line.decode("unicode_escape"))      #写入文件中(先从unicode转回中文再写入)
        print('++++++++++++     储存完成      ++++++++++++')
        return item

    def spider_closed(self, spider):  #爬虫结束时关闭文件
        self.file.close()

# 保存item到数据库中
class ScrapyspiderPipeline(object):
    """保存item到数据库中
           1、在settings.py文件中配置
           2、在自己实现的爬虫类中yield item,会自动执行"""

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        """1、@classmethod声明一个类方法，而对于平常我们见到的则叫做实例方法。
           2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
           3、可以通过类来调用，就像C.f()，相当于java中的静态方法"""
        dbparams = dict(
            host=settings['MYSQL_HOST'],  # 读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb',
                                       **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)  # 相当于dbpool付给了这个类，self中可以得到

    # pipeline默认调用
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)  # 调用插入的方法
        query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        return item

    # 写入数据库中
    def _conditional_insert(self, tx, item):
        # print item['name']
        sql = "insert into zhilian(ranking,movie_name,score,score_num) values(%s,%s,%s,%s)"
        params = (item["ranking"], item["movie_name"], item["score"], item["score_num"])
        tx.execute(sql, params)

    # 错误处理方法
    def _handle_error(self, failue, item, spider):
        print '--------------database operation exception!!-----------------'
        print '-------------------------------------------------------------'
        print failue

# 保存ZhilianUrlItem到myurls文件当中
class ZhilianFistPipeline(object):

    def open_spider(self, spider):
        print('++++++++++++    打开文件    ++++++++++++')
        self.fp = codecs.open('myurls', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        if 'http://jobs.zhaopin.com/' in item['url']:
            print('++++++++++++             ++++++++++++')
            print('++++++++++++    存储中    ++++++++++++')
            # id  =  'A' + str(self.id + 1)
            # # print('*****************', id, '***************************************')
            # self.worksheet.write(id, item['url'])
            # self.id = self.id +1
            self.fp.writelines(item['url'] + "\n")
            print('++++++++++++     ok      ++++++++++++')

            return item
        else:
            pass

            # def spider_closed(self, spider):

    # def spider_closed(self, spider):
    def spider_closed(self, spider):
        print('++++++++++++           ++++++++++++')
        print('++++++++++++    结束    ++++++++++++')
        self.fp.close()
        print('++++++++++++    ok    ++++++++++++')

# 空的pipeline，用来测试
class TestPipeline(object):

    def open_spider(self, spider):
        print('++++++++++++    open_spider    ++++++++++++')

    def process_item(self, item, spider):
        print('++++++++++++    process_item    ++++++++++++')

    def spider_closed(self, spider):
        print('++++++++++++    spider_closed    ++++++++++++')

