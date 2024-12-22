import scrapy
from snowradar_scraper.items import SkiresortItem

class SkiresortsSpider(scrapy.Spider):
    name = "skiresorts"
    start_urls = ["https://www.skiresort.info/ski-resorts/"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'snowradar_scraper.pipelines.SkiresortCleanupPipeline': 200,
            'snowradar_scraper.pipelines.SkiresortDatabasePipeline': 300,
        }
    }

    def parse(self, response):
        max_page = int(response.css('ul.pagination li:last-child a::attr(href)').re_first(r'page/(\d+)/'))
        for i in range(1, max_page + 1):
            url = f'{self.start_urls[0]}{"page/"+str(i)+"/" if i > 1 else ""}'
            yield scrapy.Request(url, self.parse_links)

    def parse_links(self, response):
        links = response.css('a.pull-right.btn::attr(href)').getall()
        for link in links:
            yield scrapy.Request(response.urljoin(link), self.parse_details)

    def parse_details(self, response):
        item = SkiresortItem()
        base = 'div.overview-resort-infos '
        selectors = {
            'name': 'h1.headlineoverview span.fn::text',
            'opened_slopes': base + 'a[href*="snow-report"] .info-text::text',
            'total_slopes': base + 'a[href*="snow-report"] .info-text::text',
            'opened_lifts': base + 'a#resortInfo-lift .info-text::text',
            'total_lifts': base + 'a#resortInfo-lift .info-text::text',
            'snow': base + 'a[href*="snow-report"] .fa-snowflake-o + .info-text::text',
            'status': base + 'a[href*="weather"] .info-text::text',
            'low_temp': base + 'a[href*="weather"] .info-text::text',
            'high_temp': base + 'a[href*="weather"] .info-text::text',
        }

        for field, selector in selectors.items():
            item[field] = response.css(selector).get(default='').strip()

        if item['opened_slopes']:
            slopes = item['opened_slopes'].split('/')
            item['opened_slopes'], item['total_slopes'] = slopes[0].strip(), slopes[1].strip() if len(slopes) > 1 else None

        if item['opened_lifts']:
            lifts = item['opened_lifts'].split('/')
            item['opened_lifts'], item['total_lifts'] = lifts[0].strip(), lifts[1].strip() if len(lifts) > 1 else None

        if item['low_temp']:
            weather = item['low_temp'].split('/')
            item['low_temp'], item['high_temp'] = weather[0].replace('°C', '').strip(), weather[1].replace('°C', '').strip() if len(weather) > 1 else None

        item['location'] = ', '.join(response.css('div.overview-resort-infos p a::text').getall()).strip()

        yield item
