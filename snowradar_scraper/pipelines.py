from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class OnthesnowCleaningPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        required_fields = ['name', 'snowfall_24h', 'base_depth']
        
        # Überprüfen, ob die erforderlichen Felder vorhanden sind
        if not all(adapter.get(field) for field in required_fields):
            raise DropItem(f"Missing required fields in {item}")
        
        # Bereinigen des 'name'-Feldes
        adapter['name'] = adapter['name'].strip()
        
        # Bereinigen der numerischen Felder
        numeric_fields = ['snowfall_24h', 'base_depth', 'open_trails', 'total_trails', 'open_lifts', 'total_lifts']
        for field in numeric_fields:
            if field == 'base_depth':
                adapter[field] = self.clean_base_depth(adapter.get(field))
            else:
                adapter[field] = self.clean_numeric(adapter.get(field))
        
        return item

    def clean_numeric(self, value):
        # Wenn der Wert None ist, auf 0.0 setzen
        if value is None:
            return 0.0
        # Entfernen von Anführungszeichen und Leerzeichen
        value = value.replace('"', '').strip()
        try:
            # Umwandeln in eine Gleitkommazahl
            return float(value)
        except ValueError:
            # Wenn ein Fehler auftritt, auf 0.0 setzen
            return 0.0

    def clean_base_depth(self, value):
        if '-' in value:
            min_val, max_val = value.split('-')
            min_val = self.clean_numeric(min_val)
            max_val = self.clean_numeric(max_val)
            return (min_val + max_val) / 2
        return self.clean_numeric(value)