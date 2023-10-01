import scrapy
from scrapy import Selector
from liepincom.items import LiepincomItem


class LiepinSpider(scrapy.Spider):
    name = 'liepin'
    allowed_domains = ['liepin.com']
    start_urls = ['https://liepin.com/career/java']

    # 预先准备好待爬取页面的URL
    def start_requests(self):
        for page in range(5):
            yield scrapy.Request(
                url=f'https://www.liepin.com/career/java/pn{page}/'
            )


    def parse(self, response):
        sel = Selector(response)
        # 用不同的xpath路径方式进行解析，多体会xpath解析方式的强大与方便之处
        position = sel.xpath('/html/body/div/div/div/div[1]/div/div[1]/ul/li/div/div/div[1]/div/a[1]/div[1]/div/div[1]/text()').extract()  # 完整路径
        city = sel.xpath('//div[@class="job-title-box"]//span[@class="ellipsis-1"]/text()').extract()  #手写xpath路径
        salary = sel.xpath('//*[@id="main-container"]/div/div/div[1]/div/div[1]/ul/li/div/div/div/div/a/div[1]/span/text()').extract()  # 浏览器给出的路径
        year = sel.xpath('//*[@id="main-container"]/div/div/div[1]/div/div[1]/ul/li/div/div/div[1]/div/a[1]/div[2]/span[1]/text()').extract()
        edu = sel.xpath('//*[@id="main-container"]/div/div/div[1]/div/div[1]/ul/li/div/div/div[1]/div/a[1]/div[2]/span[2]/text()').extract()
        company = sel.xpath('//div[@data-nick="job-detail-company-info"]//div[@class="job-company-info-box"]/span/text()').extract()
        company_size = sel.xpath('//div[@data-nick="job-detail-company-info"]//div[@class="company-tags-box ellipsis-1"]//span[last()]/text()').extract()

        for a, b, c, d, e, f, g in zip(position,city,salary,year,edu,company,company_size):
            liepin_item = LiepincomItem()
            liepin_item['position'] = a
            liepin_item['city'] = b
            liepin_item['salary'] = c
            liepin_item['year'] = d
            liepin_item['edu'] = e
            liepin_item['company'] = f
            liepin_item['company_size'] = g
            # 注意不要用return，否则遍历一次就返回完毕了
            yield liepin_item
