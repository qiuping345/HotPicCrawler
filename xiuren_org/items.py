# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#the Item for AlbumList
class AlbumListItem(scrapy.Item):
    listName = scrapy.Field()
    link = scrapy.Field()
    lastAccessTime = scrapy.Field()

# for the next page link of AlbumList
class AlbumListNextPageItem(scrapy.Item):
    link = scrapy.Field()

# for the Album page
class AlbumItem(scrapy.Item):
    link = scrapy.Field()
    lastAccessTime = scrapy.Field()

# for each photo in an Album
class PhotoItem(scrapy.Item):
    linkThumb = scrapy.Field()
    linkDetail = scrapy.Field()
    heightThumb = scrapy.Field()
    widthThumb = scrapy.Field()
    heightDetail = scrapy.Field()
    widthDetail = scrapy.Field()

