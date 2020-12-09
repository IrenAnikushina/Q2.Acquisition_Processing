import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']  # Список разрешенных доменов
    start_urls = [
        'https://hh.ru/search/vacancy?clusters=true&area=1&search_field=name&search_field=description&enable_snippets=true&salary=&st=searchVacancy&text=python']

    def parse(self, response: HtmlResponse):
        vacancies_links = response.xpath("//span/a[contains(@class,'bloko-link')]/@href").extract()
        for link in vacancies_links:
            yield response.follow(link, callback=self.vacancy_parse)
        next_page = response.xpath("//a[contains(@class,'HH-Pager-Controls-Next')]/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        else:
            return

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").extract_first()
        salary = response.xpath("//p[@class='vacancy-salary']//text()").extract()
        vacancy_link = response.url
        vacancy_source = self.allowed_domains[0]
        yield JobparserItem(item_name=name, item_salary=salary, item_link=vacancy_link,
                            item_source=vacancy_source)
