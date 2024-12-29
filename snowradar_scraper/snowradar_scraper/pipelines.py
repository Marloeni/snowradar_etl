# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy

class SnowradarScraperPipeline:
    def process_item(self, item, spider):
        return item
    
class CleanDataPipeline:
    def process_item(self, item, spider):
        # Überprüfen, ob die erforderlichen Felder vorhanden sind
        if not item.get('resort_name') or not item.get('snowfall_24h') or not item.get('base_depth'):
            raise scrapy.exceptions.DropItem(f"Missing required fields in {item}")

        # Bereinigen der Felder
        item['resort_name'] = item['resort_name'].strip()
        item['snowfall_24h'] = self.clean_numeric(item['snowfall_24h'])
        item['base_depth'] = self.clean_base_depth(item['base_depth'])
        item['open_trails'] = self.clean_numeric(item['open_trails'])
        item['total_trails'] = self.clean_numeric(item['total_trails'])
        item['open_lifts'] = self.clean_numeric(item['open_lifts'])
        item['total_lifts'] = self.clean_numeric(item['total_lifts'])
        return item

    def clean_numeric(self, value):
        # Entfernen von Anführungszeichen und Umwandlung in Zahl
        value = value.replace('"', '').strip()
        try:
            return float(value)
        except ValueError:
            return None

    def clean_base_depth(self, value):
        # Entfernen von Anführungszeichen und Berechnung des Durchschnitts, falls zwei Zahlen vorhanden sind
        value = value.replace('"', '').strip()
        if '-' in value:
            try:
                parts = value.split('-')
                avg_depth = (float(parts[0]) + float(parts[1])) / 2
                return avg_depth
            except ValueError:
                return None
        return self.clean_numeric(value)

    def clean_open_trails(self, value):
        return self.clean_numeric(value)

    def clean_open_lifts(self, value):
        return self.clean_numeric(value)