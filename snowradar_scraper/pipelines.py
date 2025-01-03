from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class OnthesnowCleaningPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        required_fields = ['name', 'snowfall_24h', 'base_depth']
        
        # Check if required fields are present
        if not all(adapter.get(field) for field in required_fields):
            raise DropItem(f"Missing required fields in {item}")
        
        # Clean 'name' field
        adapter['name'] = adapter['name'].strip()
        
        # Clean numeric fields
        numeric_fields = ['snowfall_24h', 'base_depth', 'open_trails', 'total_trails', 'open_lifts', 'total_lifts']
        for field in numeric_fields:
            adapter[field] = self.clean_base_depth(adapter.get(field)) if field == 'base_depth' else self.clean_numeric(adapter.get(field))
        
        return item

    def clean_numeric(self, value):
        if value is None:
            return 0.0
        value = value.replace('"', '').strip()
        try:
            return float(value)
        except ValueError:
            return 0.0

    def clean_base_depth(self, value):
        if '-' in value:
            min_val, max_val = value.split('-')
            return (self.clean_numeric(min_val) + self.clean_numeric(max_val)) / 2
        return self.clean_numeric(value)