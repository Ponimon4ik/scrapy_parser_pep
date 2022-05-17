import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        for pep_link in response.css(
                '#numerical-index tbody > tr'
                ' > td.num > a::attr(href)').getall():
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        pep = response.css('ul.breadcrumbs > li + li + li::text').get()
        data = {
            'number': int(pep.replace('PEP ', '')),
            'name': response.css('#pep-content h1.page-title::text').get(),
            'status': response.css('dt:contains("Status") + dd::text').get()
        }

        yield PepParseItem(data)
