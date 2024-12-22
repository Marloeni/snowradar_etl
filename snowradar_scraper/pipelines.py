# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import psycopg2
import os
import logging

class SnowradarScraperPipeline:
    def process_item(self, item, spider):
        return item

class SkiresortPipeline:
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
            fields = ['name', 'slopes', 'lifts', 'snow', 'weather']
            self.cur.execute(f"INSERT INTO skiresort_details ({','.join(fields)}) VALUES ({','.join(['%s']*len(fields))})",
                [item.get(f) for f in fields])
            self.conn.commit()
        except Exception as e:
            logging.error(f"Error inserting item into database: {e}")
        return item

    def __del__(self):
        if self.cur: self.cur.close()
        if self.conn: self.conn.close()
