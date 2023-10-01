# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import openpyxl
import pymysql
from itemadapter import ItemAdapter

# 保存数据到Mysql数据库
class MysqlPipeline:

    def __init__(self):
        self.conn = pymysql.connect(host='localhost',port=3306,
                                    user='root',password='1234',
                                    database='spider')
        self.cursor = self.conn.cursor()

    def close_spider(self,spider):
        self.conn.commit()
        self.conn.close()

    # 回调函数，让scrapy框架主动调用我们的方法（callback），上述其他方法都是调用框架给我们的方法（call）,每有一个数据就调用一次
    def process_item(self, item, spider):
        db_post = item.get('position', '')
        db_city = item.get('city', '')
        db_salary = item.get('salary', '')
        db_year = item.get('year', '')
        db_edu = item.get('edu', '')
        db_company = item.get('company', '')
        db_company_size = item.get('company_size', '')

        self.cursor.execute(
            'insert into liepin_zhaopin (position, city, salary, year, edu, company, company_size) values (%s,%s,%s,%s,%s,%s,%s)',
            (db_post, db_city, db_salary, db_year, db_edu, db_company, db_company_size)
        )
        return item


# 保存数据到excel
class LiepincomPipeline:

    def __init__(self):
        # 创建工作簿
        self.wb = openpyxl.Workbook()
        # 拿到默认被激活的工作表
        self.ws = self.wb.active
        self.ws.title = '招聘信息'
        self.ws.append(('岗位','城市','薪水','工作年限','学历','公司名称','公司规模'))

    def close_spider(self,spider):
        self.wb.save('招聘数据.xlsx')

    # 回调函数，让scrapy框架主动调用我们的方法（callback），上述其他方法都是调用框架给我们的方法（call）
    def process_item(self, item, spider): # 得到数据并写入excel文件中
        db_post = item.get('position','')
        db_city = item.get('city','')
        db_salary = item.get('salary','')
        db_year = item.get('year','')
        db_edu = item.get('edu','')
        db_company = item.get('company','')
        db_company_size = item.get('company_size','')
        self.ws.append((db_post, db_city, db_salary, db_year, db_edu, db_company, db_company_size))
        return item
