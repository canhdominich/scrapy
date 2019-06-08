# import time
from datetime import datetime
import scrapy
# from ..items import PostItem

class VietNamNetSKSpider(scrapy.Spider):
    """
    Main scrapy Vietnamnet
    """
    name = "vietnamnet"

    def start_requests(self):
        """
        start requests
        :return:
        """
        urls = [
            'https://vietnamnet.vn/vn/suc-khoe/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.get_link_category)

    def get_link_category(self, response):
        """
        get link category
        :param response:
        :return:
        """

        links = []
        category_main_div = response.xpath('//div[@class="w-660 d-ib va-top pos-rel"]')
        for category_div in category_main_div:
            first_new = category_div.xpath('./div[@class="Top-Cate clearfix m-t-20 p-b-20 bor-bt-sp"]/div[@class="w-360 left m-r-20"]/div[@class="top-one-cate"]')
            links.append(first_new.xpath('./a/@href').extract_first())

            seconds_news = category_div.xpath('./div[@class="Top-Cate clearfix m-t-20 p-b-20 bor-bt-sp"]/div[@class="w-280 left clearfix"]/div[@class="BoxCate BoxStyle5"]/ul[@class="height-list va-top"]/li')
            for sk in seconds_news:
                links.append(sk.xpath('./a/@href').extract_first())

            old_news = category_div.xpath('./div[@class="list-content list-content-loadmore lagre m-t-20 clearfix"]/div[@class="clearfix item"]')
            for sk in old_news:
                links.append(sk.xpath('./a/@href').extract_first())

        for lk in links:
            if lk.find("http") < 0:
                lk = 'https://vietnamnet.vn' + lk
            yield scrapy.Request(url=lk, callback=self.get_detail_post)

    def get_detail_post(self, response):
        """
        get detail post
        :param response:
        :return:
        """
        page = []

        self.logger.info('Link Detail Post %s' % response.url)
        sub_new = response.xpath('//div[@class="ArticleDetail w-590 d-ib"]')
        # item = PostItem()
        if sub_new:
            content = ''
            array_cont = []
            thumnail = ""
            title = sub_new.xpath('./h1/text()').extract_first()
            time_news = sub_new.xpath('./div[@class="ArticleDateTime clearfix m-t-10"]/span[@class="ArticleDate  right"]/text()').extract_first()
            # description = sub_new.xpath('./div[@class="ArticleContent"]/div[@class="bold ArticleLead"]/h2/p[@class="t-j"]/span[@class="bold"]/text()').extract_first()
            description = response.css('p.t-j span.bold::text').get()
            lst_content = sub_new.xpath('./div[@class="ArticleContent"]')
            for c in lst_content:
                sub_content = c.xpath('.//p/text()').extract()
                content += sub_content
                array_cont.append(sub_content)
            author = array_cont[-1]

            page.append({  'time': time_news,
                           'title': title,
                           'thumbnail': thumbnail,
                           'description': description,
                           'content': content,
                           'author': author,
                        })
        print(page)