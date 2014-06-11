# Scrapy settings for autohome project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'autohome'

SPIDER_MODULES = ['autohome.spiders']
NEWSPIDER_MODULE = 'autohome.spiders'

#ITEM_PIPELINES={'autohome.pipelines.AutohomePipeline':100}
ITEM_PIPELINES={'scrapy.contrib.pipeline.images.ImagesPipeline':1,'autohome.pipelines.AutohomePipeline':100}
IMAGES_STORE='./images'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'autohome (+http://www.yourdomain.com)'
