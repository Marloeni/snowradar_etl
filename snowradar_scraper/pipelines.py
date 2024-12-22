# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: htt

import psycopg2
import os
import logging
from scrapy.exceptions import DropItem

class SkiresortCleanupPipeline:
    def process_item(self, item, spider):
        print("✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅")
        for field in item:
            if item[field]:
                item[field] = self.clean(item[field])
                item[field] = self.convert(item[field], field)
            else:
                item[field] = None

        if not item.get('name'):
            raise DropItem(f"Missing name in {item}")

        return item

    def clean(self, text):
        if isinstance(text, str):
            text = text.strip().replace('\n', ' ').replace('\r', ' ')
            text = text.replace('\xa0', ' ')
        return text

    def convert(self, value, field):
        conversions = {
            'name': lambda v: v.replace('Ski resort', '').strip(),
            'opened_slopes': int,
            'total_slopes': int,
            'opened_lifts': int,
            'total_lifts': int,
            'snow': lambda v: int(v.replace('\xa0', ' ').replace('&nbsp;', ' ').replace('cm', '').strip()) if v else None,
            'low_temp': lambda v: int(v.replace('°C', '').strip()) if v else None,
            'high_temp': lambda v: int(v.replace('°C', '').strip()) if v else None,
            'location': lambda v: v  # No special conversion for location
        }
        try:
            return conversions.get(field, lambda v: v)(value)
        except (ValueError, TypeError):
            return None

class SkiresortDatabasePipeline:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            fields = ['name', 'opened_slopes', 'total_slopes', 'opened_lifts', 'total_lifts', 'snow', 'status', 'low_temp', 'high_temp', 'location']
            self.cur.execute(f"INSERT INTO skiresort_details ({','.join(fields)}) VALUES ({','.join(['%s']*len(fields))})",
                [item.get(f) for f in fields])
            self.conn.commit()
        except Exception as e:
            logging.error(f"Error inserting item into database: {e}")
            self.conn.rollback()  # Rollback der Transaktion bei Fehlern
        return item

    def __del__(self):
        if self.cur: self.cur.close()
        if self.conn: self.conn.close()