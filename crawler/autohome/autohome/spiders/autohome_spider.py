from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider 
from scrapy.http import Request
from autohome.items import *

import urlparse
import re

class AutohomeSpider(BaseSpider):
    name="autohome"
    allowed_domains=["autohome.com.cn","autoimg.cn"]
    start_urls=["http://car.autohome.com.cn/AsLeftMenu/As_LeftList.ashx?typeId=1&brandId=0&fctId=0&seriesId=0&ievs=0"]
    image_host="http://car.autohome.com.cn/pic/"

    def parse(self,response):
        ptn_brand=re.compile('brand-(\d+)[.]html')
        rlt_brand=ptn_brand.findall(response.body)
        for rlt in rlt_brand:
            rlt_url=self.image_host+"brand-"+rlt+".html"
            yield Request(rlt_url,callback=self.parse_auto_brand)
    def parse_auto_brand_list(self,response):
        ptn_brand=re.compile('brand-(\d+)[.]html')
        rlt_brand=ptn_brand.findall(response.body)
        for rlt in rlt_brand:
            rlt_url=self.image_host+"brand-"+rlt+".html"
            #print rlt_url
            yield Request(rlt_url,callback=self.parse_auto_brand)
    def parse_auto_brand(self,response):
        ptn_series=re.compile('href=["]?/pic/series/(\d+)[.]html["]')
        rlt_series=ptn_series.findall(response.body)
        for rlt in rlt_series:
            rlt_url=urlparse.urljoin(self.image_host, "/pic/series/"+rlt+"-1.html")
            yield Request(rlt_url,callback=self.parse_auto_series)
    def parse_auto_series(self,response):
        ptn_series=re.compile('src=["]([^"]*?autoimg.cn/upload/[^"]*?)["]')
        rlt_series=ptn_series.findall(response.body)
        image_list=list()
        for rlt in rlt_series:
            rlt_url=urlparse.urljoin(response.url,rlt)
            #thumb pic to normal pic
            rlt_url=rlt_url.replace("t_","u_")
            image_list.append(rlt_url)
        item=CarImageItem()
        item["image_urls"]=image_list
        item["series_id"]=re.search(r'\d+',response.url).group()
        yield item
        ptn_nextpg=re.compile('page-item-next.*?href=["](.*?)["]')
        rlt_nextpg=ptn_nextpg.findall(response.body)
        for rlt in rlt_series:
            rlt_url=urlparse.urljoin(response.url,rlt)
            yield Request(rlt_url,callback=self.parse_auto_series)
        
        
            