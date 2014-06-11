# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

import sqlite3
import os
import hashlib

class AutohomePipeline(object):
    def __init__(self):
        self.db_name='autohome.db'
        dispatcher.connect(self.db_init, signals.spider_opened)
        dispatcher.connect(self.db_dispose, signals.spider_closed)

    def process_item(self, item, spider):
        if item['image_urls'] and item['series_id']:
            for image_url in item['image_urls']:
                val=(image_url,hashlib.sha1(image_url).hexdigest(),item['series_id'])
                self.conn.execute('insert into tbl_image values (?,?,?)',val)
            self.conn.commit()
        return item
    
    def db_init(self):
        if os.path.exists(self.db_name):
            self.conn=sqlite3.connect(self.db_name)
        else:
            self.conn=sqlite3.connect(self.db_name)
            self.conn.execute("create table if not exists tbl_image (img_url text,img_hash text,series_id integer)")
            self.conn.commit()
    
    def db_dispose(self):
        if self.conn:
            self.conn.close()