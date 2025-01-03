import scrapy
from scrapy_playwright.page import PageMethod
from snowradar_scraper.items import OnthesnowItem

class OnthesnowSpider(scrapy.Spider):
    name = "onthesnow"
    allowed_domains = ["www.onthesnow.com"]
    start_urls = ["https://www.onthesnow.com/skireport"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", "#onetrust-accept-btn-handler"),
                        PageMethod("click", "#onetrust-accept-btn-handler"),
                        PageMethod("wait_for_selector", "button.styles_viewEU__VcoHT"),
                        PageMethod("click", "button.styles_viewEU__VcoHT"),
                    ],
                },
            )

    def parse(self, response):
        country_links = response.css("div.styles_regions__8b2js a::attr(href)").getall()
        for link in country_links:
            yield response.follow(link, self.parse_country)

    def parse_country(self, response):
        rows = response.css("table.styles_table__0oUUB tbody tr")
        for row in rows:
            item = OnthesnowItem()
            item['name'] = row.css("td a span.h4::text").get()
            item['snowfall_24h'] = row.css("td:nth-child(2) span.h4::text").get()
            item['base_depth'] = row.css("td:nth-child(3) span.h4::text").get()
            open_trails = row.css("td:nth-child(4) span.h4::text").get()
            open_lifts = row.css("td:nth-child(5) span.h4::text").get()
            
            if open_trails:
                item['open_trails'], item['total_trails'] = self.split_open_total(open_trails)
            if open_lifts:
                item['open_lifts'], item['total_lifts'] = self.split_open_total(open_lifts)
            
            yield item

    def split_open_total(self, value):
        if '/' in value:
            open_value, total_value = value.split('/')
            return open_value.strip(), total_value.strip()
        return value.strip(), value.strip()