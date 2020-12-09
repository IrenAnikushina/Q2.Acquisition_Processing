import scrapy
from scrapy.http import HtmlResponse
from lmparser.items import LmparserItem
from scrapy.loader import ItemLoader


class LmSpider(scrapy.Spider):
    name = 'lm'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        super(LmSpider, self).__init__()
        self.start_urls = [
            f'https://leroymerlin.ru/search/?q={search}&family=0ff39b10-7d6a-11ea-8b72-41915831461b&suggest=true']

    def parse(self, response: HtmlResponse):
        items_links = response.xpath("//uc-plp-item-new/@href").extract()
        for link in items_links:
            yield response.follow(link, callback=self.items_parse)
        next_page = response.xpath(
            "//div[@class='service-panel-wrapper']//div[contains(@class,'next')]/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        else:
            return

    def items_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=LmparserItem(), response=response)
        loader.add_xpath('item_name', "//h1/text()")
        # item_name = response.xpath("//h1/text()").extract_first()
        loader.add_xpath('item_photo', "//img[@alt='product image']/@src")
        # item_photo = response.xpath("//img[@alt='product image']/@src").extract()
        loader.add_value('item_link', response.url)
        # item_link = response.url
        loader.add_xpath('item_price', "//span[@slot='price']/text()")
        # item_price = response.xpath("//uc-pdp-price-view[@class='primary-price']//span/text()").extract()
        loader.add_xpath('spec_name', "//dl/div/dt/text()")
        # spec_name = response.xpath("//dl/div/dt/text()")
        loader.add_xpath('spec_value', "//dl/div/dd/text()")
        # spec_value = response.xpath("//dl/div/dd/text()")
        loader.add_value('specifications', {})
        # specifications = {}
        yield loader.load_item()
        # yield LmparserItem(item_name=item_name, item_photo=item_photo, item_link=item_link,
        #                     item_description=item_description,item_price=item_price, spec_name=spec_name,
        #                     spec_value=spec_value, specifications=specifications)
