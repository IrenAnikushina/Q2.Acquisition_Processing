from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lmparser.spiders.lm import LmSpider
from lmparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LmSpider, search='фотообои город')
# %D1%84%D0%BE%D1%82%D0%BE%D0%BE%D0%B1%D0%BE%D0%B8%20%D0%B3%D0%BE%D1%80%D0%BE%D0%B4
    process.start()