import scrapy


class DanTriSpider(scrapy.Spider):
    name = "dantri"
    start_urls = [
        'https://dantri.com.vn/suc-khoe.htm'
    ]

    def parse(self, response):

        for article in response.css('div.mt3.clearfix.eplcheck a.fon6'):
            yield response.follow(article, callback=self.parse_detail_post)

        for next_page in response.css('div.fr a.fon27.mt1.mr2'):
            yield response.follow(next_page, callback=self.parse)

    def parse_detail_post(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        content = ''
        for p in response.css('div.fon34.mt3.mr2.fon43.detail-content p::text').getall():
            content += p.strip()
        if content != '':
            yield {
                'time': extract_with_css('span.fr.fon7.mr2.tt-capitalize::text'),
                'title': extract_with_css('h1.fon31.mgb15::text'),
                'thumbnail': extract_with_css('div.fon34.mt3.mr2.fon43.detail-content img::attr(src)'),
                'description': response.css('h2.fon33.mt1.sapo::text').getall()[1].strip(),
                'content': content,
                'author': extract_with_css('div.fon34.mt3.mr2.fon43.detail-content p strong')
            }