from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from snowradar_scraper.spiders.skiresorts import SkiresortsSpider

print("✅")


process = CrawlerProcess(get_project_settings())
process.crawl(SkiresortsSpider)
process.start()
