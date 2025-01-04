from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID
from geopy.geocoders import Nominatim

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
    
class OnthesnowGeolocationPipeline:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="snowradar_scraper")

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        location = self.geolocator.geocode(adapter.get('name'))
        if location:
            adapter['latitude'] = location.latitude
            adapter['longitude'] = location.longitude
        else:
            raise DropItem(f"Could not find location for {adapter.get('name')}")
        return item
    
class OnthesnowAppwritePipeline:
    def __init__(self):
        self.client = Client()
        self.client.set_endpoint('http://localhost/v1')
        self.client.set_project('676ebea7001f5da0fb4a')
        self.client.set_key('standard_fed19494a38cfbe01c7490d3b701ad4fef9205025dfd9e8217b42ef795eeec214f67b6726abb7ebfb33f0e4eb2d375552d8a15c3b6683e984c51aaec3e3d80c6bc7bb4fbd1755274c8ff837563b85d82592cc318d03aa1f5707503b402a2e6750f815a3ff4bc2610543bebed6a0d547e8bbc60f6235d4c2c1e6fbc55caf5169d')
        self.databases = Databases(self.client)
        self.database_id = '676ebeec00043b21655b'
        self.collection_id = '677037cc00346c307697'

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        document_data = {
            'name': adapter.get('name'),
            'snowfall_24h': adapter.get('snowfall_24h'),
            'base_depth': adapter.get('base_depth'),
            'open_trails': adapter.get('open_trails'),
            'total_trails': adapter.get('total_trails'),
            'open_lifts': adapter.get('open_lifts'),
            'total_lifts': adapter.get('total_lifts'),
            'latitude': adapter.get('latitude'),
            'longitude': adapter.get('longitude')
        }

        # Remove keys with None values to avoid issues with missing attributes
        document_data = {k: v for k, v in document_data.items() if v is not None}
        
        self.databases.create_document(
            database_id=self.database_id,
            collection_id=self.collection_id,
            document_id=ID.unique(),
            data=document_data
        )
        return item
