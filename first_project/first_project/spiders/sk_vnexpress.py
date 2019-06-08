import scrapy


class VnExpressSpider(scrapy.Spider):
    name = "vnexpress"
    start_urls = [
        'https://vnexpress.net/suc-khoe'
    ]

    def parse(self, response):
        for href in response.css('section.box_category hgroup a.first'):
            yield response.follow(href, callback=self.parse_posts)

    def parse_posts(self, response):

        for article in response.css('article.list_news h4.title_news a'):
            yield response.follow(article, callback=self.parse_detail_post)

        if response.xpath('//a[@class="next"]/preceding-sibling::a[1]/text()').get() is not "6":
            for next_page in response.css('a.next'):
                yield response.follow(next_page, callback=self.parse_posts)

    def parse_detail_post(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        content = ''
        for p in response.css('p.Normal::text').getall():
            content += p.strip()
        if content != '':
            yield {
                'time': extract_with_css('span.time.left::text'),
                'title': extract_with_css('h1.title_news_detail.mb10::text'),
                'thumbnail': extract_with_css('table tbody tr td img::attr(src)'),
                'description': extract_with_css('p.description::text'),
                'content': content,
                'author': extract_with_css('p.author_mail strong::text')
            }