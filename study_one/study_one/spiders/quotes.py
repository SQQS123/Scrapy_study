# -*- coding: utf-8 -*-
import scrapy
from study_one.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            # 不适用item
            # text = quote.css('.text::text').extract_first()
            # author = quote.css('.author::text').extract_first()
            # tags = quote.css('.tags .tag::text').extract()
            # 使用item
            item = QuoteItem()
            item['text'] = quote.css('.text::text').extract_first()
            item['author'] = quote.css('.author::text').extract_first()
            item['tags'] = quote.css('.tags .tag::text').extract()
            yield item

        # 处理下一页
        # 得到下一页的url
        next = response.css('.pageer .next a::attr("href")').extract_first()
        # 把相对url构建为绝对url例如抓取到的下一页地址是/page/2,则urljoin方法处理后得到的结果就是:http://quotes.toscrape.com/page/2/
        url = response.urljoin(next)
        # 指定下一页的地址和回调函数。直到执行到最后一页
        yield  scrapy.Request(url=url, callback=self.parse)

