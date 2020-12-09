import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SuperJobSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']  # Список разрешенных доменов
    start_urls = ['https://www.superjob.ru/vakansii/pekar-konditer.html?geo%5Bt%5D%5B0%5D=4']

    def parse(self, response: HtmlResponse):
        vacancies_links = response.xpath("//a[contains(@class, 'icMQ_ _6AfZ9 f-test-link')]/@href").extract()
        for link in vacancies_links:
            yield response.follow(link, callback=self.vacancy_parse)
        next_page = response.xpath("//a[contains(@class, 'f-test-button-dalshe')]/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        else:
            return

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").extract_first()
        salary = response.xpath("//span[contains(@class, '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz')]//text()").extract()
        vacancy_link = response.url
        vacancy_source = self.allowed_domains[0]
        yield JobparserItem(item_name=name, item_salary=salary, item_link=vacancy_link, item_source=vacancy_source)
