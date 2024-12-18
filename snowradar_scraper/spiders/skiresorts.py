import scrapy
from snowradar_scraper.items import SkiresortItem

class SkiresortsSpider(scrapy.Spider):
    name = "skiresorts"
    allowed_domains = ["skiresort.info"]
    start_urls = ["https://skiresort.info/ski-resorts/"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'snowradar_scraper.pipelines.SkiresortPipeline': 300,
        }
    }

    def parse(self, response):
        max_page = int(response.css('ul.pagination li:last-child a::attr(href)').get().split('page/')[-1].strip('/'))
        urls = [f'{self.start_urls[0]}{"page/"+str(i)+"/" if i>1 else ""}' for i in range(1, max_page + 1)]
        for url in urls:
            yield scrapy.Request(url, self.parse_links)

    def parse_links(self, response):
        # Debug: Print the full HTML content
        print("="*50)
        print("URL:", response.url)
        print("Response body:")
        print(response.body.decode())
        print("="*50)

        links = response.css('a.pull-right.btn::attr(href)').getall()
        for link in links:
            yield scrapy.Request(response.urljoin(link), self.parse_details)

    def parse_details(self, response):
        # Debug: Print the full HTML content
        print("="*50)
        print("URL:", response.url)
        print("Response body:")
        print(response.body.decode())
        print("="*50)

        base = 'div.overview-resort-infos '
        item = SkiresortItem()
        selectors = {
            'name': 'h2.h3.text-cut::text',
            'slopes': base + 'a[href*="snow-report"] .info-text::text',
            'lifts': base + 'a#resortInfo-lift .info-text::text',
            'snow': base + 'a[href*="snow-report"] .fa-snowflake-o + .info-text::text',
            'weather': base + 'a[href*="weather"] .info-text::text',
        }

        for field, selector in selectors.items():
            item[field] = response.css(selector).get()
            if item[field]:
                item[field] = item[field].strip()

        yield item
