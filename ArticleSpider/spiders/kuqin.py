# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import ArticelItem

class KuqinSpider(scrapy.Spider):
    name = 'kuqin'
    allowed_domains = ['www.kuqin.com']
    start_urls = ['http://www.kuqin.com']

    def parse(self, response):
        post_urls=response.css(".list-boxes h2 a::attr(href)").extract()
        for post_url in post_urls:
            post_url=parse.urljoin(response.url,post_url)
            print(post_url)
            yield Request(url=post_url,callback=self.parse_detail)
        next_url=response.xpath("//div[@class='pagination']/ul/li[10]/a/@href").extract()[0]
        if next_url:
            next_url = parse.urljoin(response.url, next_url)
            print(next_url)
            yield Request(url=next_url,callback=self.parse)



    def parse_detail(self,response):
        article_item=ArticelItem()

        title=response.xpath("//div[@class='tc-box first-box article-box']/h2/text()").extract()[0]
        # [<Selector xpath="//div[@class='tc-box first-box article-box']/h2/text()" data='2018年中盘点：江小白走心文案合集！'>]
        # [<Selector xpath="//div[@class='tc-box first-box article-box']/h2" data='<h2>2018年中盘点：江小白走心文案合集！</h2>'>]
        create_date=response.xpath("//div[@class='article-infobox']/span/text()").extract()[0]
        create_date=re.match("(.*)\s",create_date).group(1).strip()
        author=response.xpath("//div[@class='kq__article-power']/p/text()").extract()[1]
        content=response.xpath("//div[@id='article_content']").extract()[0]
        print(title)
        print(create_date)
        print(author)
        print(content)

        article_item["title"]=title
        article_item["create_date"]=create_date
        article_item["author"]=author
        article_item["content"]=content

        yield article_item
