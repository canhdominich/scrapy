import scrapy

class firstSpider(scrapy.Spider):
    name = "first"
    start_urls = [
        'https://vnexpress.net/suc-khoe',
    ]

    def parse(self, response):
        articles = response.css('section.sidebar_1 article.list_news h4.title_news a::attr(href)')
        for article in articles:
            yield response.follow(article, callback=self.parse_detail_post)

        # next_page = response.css('section.sidebar_1 div.pagination.mb10 a.next::attr(href)')
        # next_page = response.xpath('.//div[@class="pagination mb10"]/a[@class="next"]/@href').extract()
        # next_page = response.xpath("//li[@class='pgIt pgAt']/a[@class='pgLnk']")
        next_page = response.xpath('//a[@class="next"]/preceding-sibling::a[1]/text()').get()
        if next_page :
            next_href = next_page[0]
            yield response.follow(next_href, callback=self.parse)

    def parse_detail_post(self, response):
        content = ''
        for p in response.css('p.Normal::text').getall():
            content += p.strip()
        if content != '':
            yield{
                'time' : response.css('span.time.left::text').get(),
                'title' : response.css('h1.title_news_detail.mb10::text').get().strip('\n'),
                'thumbnail': response.css('table tbody tr td img::attr(src)').get(),
                'description' : response.css('p.description::text').get().strip('\n'),
                'content': content,
                'author' : response.css('p.author_mail strong::text').get()
            }





