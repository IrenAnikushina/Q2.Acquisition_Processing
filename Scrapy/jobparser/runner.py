# Для запуска нашего паука. Удобно для отладки
# Подключаем основные классы scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.superjobru import SuperJobSpider
from jobparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhruSpider)
    process.crawl(SuperJobSpider)

    process.start()
