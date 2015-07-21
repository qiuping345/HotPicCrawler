from __future__ import absolute_import
import scrapy
import urllib
from xiuren_org.items import * 
from scrapy.linkextractors import LinkExtractor

imgCount = 0
class XiurenOrgSpider(scrapy.Spider):
    name = "xiuren"
    allowed_domains = ["www.xiuren.org"]
    start_urls = [
        "http://www.xiuren.org"
    ]

    def parse(self, response):
        if response.url in self.start_urls:
            albumLists = self.parseCategory(response)
        print len(albumLists)

        #get album links in each list page
        for album in albumLists:
            yield scrapy.Request(album['link'], callback=self.parseAlbums)

    def parseAlbums(self, response):
        #fetch all album link in a list
        albums = []
        for sel in response.xpath('//*[contains(@class, "content")]'):
            album = AlbumItem()
            album['link'] = sel.xpath('a/@href').extract_first().encode('utf-8') 
            print album['link']
            albums.append(album)

        #TODO : fetch albums in next page of the same category
        nextPageSel = response.xpath('//a[contains(@class, "next")]/@href')
        if len(nextPageSel) > 0:
            nextPage = nextPageSel.extract_first().encode('utf-8')
            yield scrapy.Request(nextPage, callback=self.parseAlbums)
        #else:
            #last page of this category/tag, so do nothing.

        #TODO : for each album, get all the links of images
        for anAlbum in albums:
            yield scrapy.Request(anAlbum['link'], callback=self.parseImagesInAlbum)

    def parseImagesInAlbum(self, response):
        print "response url: " + response.url
        photos = []
        for sel in response.xpath('//span[contains(@class, "photoThum")]'):
            photoItem = PhotoItem()
            selATag = sel.xpath('.//a')
            photoItem['linkDetail'] = selATag.xpath('@href').extract_first().encode('utf-8')
            photoItem['linkThumb'] = selATag.xpath('.//img/@src').extract_first().encode('utf-8')
            photos.append(photoItem)
            global imgCount
            imgCount = imgCount + 1
            print imgCount
            print "detail: " + photoItem['linkDetail']  + " , Thumb: " + photoItem['linkThumb']


    def parseCategory(self, response):
        # collect all category/tag links
        categoryList = []
        for sel in response.xpath("//ul/li"):
            if len(sel.xpath('a/@href')) > 0:
                category = AlbumListItem()
                category['link'] = sel.xpath('a/@href').extract_first().encode('utf-8')
                #currently, only focus on TuiGirls
                #if(category['link'] == 'http://www.xiuren.org/category/TuiGirl.html'):
                #    categoryList.append(category)
                categoryList.append(category)
        return categoryList
