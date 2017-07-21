#!/usr/bin/python3.4

import json
import re
import HTMLInfo, sys
from lxml import html

class AMZprice(object):
    def __init__(self, url):
        self.url = url
        HTMLInfo.REFERER = url
        r = HTMLInfo.getHTML(url)
        if r.encoding:
           self.html = r.content.decode(r.encoding)
        else:
           self.html = r.content.decode('utf-8')

    def get_url_page(self):

        return 1

    def create_url(self, url_list):
        page = self.get_url_page()
        for i in range(1, int(page) + 1):
            url_list.append(self.url + str(i))

    def get_itemlist(self, item_list):
        tree = html.fromstring(self.html)
        status = tree.xpath('//a[@class="a-link-normal a-text-normal"]//@href')
        if status:
            for i in status:
                    if re.search('^/gp/', i):
                        i = "https://www.amazon.cn" + i

                    if re.search('/gp/help/|/mobile-apps/', i):
                        continue

                    if i not in item_list and re.search("https://www.amazon.cn/", i):
                        item_list.append(i)


    def get_product_jpg(self):
        jpg = ""
        jpg_list = []
        tree = html.fromstring(self.html)
        status = tree.xpath('//div[@id="leftCol"]//@data-a-dynamic-image')
        if status:
            status = eval(str(status[0]))
            for i in status.keys():
                jpg_list.append(i)
            jpg = jpg_list[0]

        return jpg

    def get_product_name(self):
        name = ""
        tree = html.fromstring(self.html)
        #status = tree.xpath('//div[@id="a-page"]/div[@id="dp"]/div[@id="dp-container"]/div[@id="centerCol"]//span[@id="productTitle"]/text()')
        status = tree.xpath('//span[@id="productTitle"]/text()')
        if status:
            name = re.sub('\n| ', '', status[0])

        return name

    def get_product_price(self):
        price = ""
        tree = html.fromstring(self.html)
        status = tree.xpath('//span[@id="priceblock_ourprice"]/text()|//span[@id="priceblock_saleprice"]/text()\
|//span[@class="a-size-medium a-color-price inlineBlock-display offer-price a-text-normal price3P"]/text()')
        if status:
            price = re.sub('￥', '', status[0])
            
        return price        

    def get_product_promotion(self):
        promotion = ""
        tree = html.fromstring(self.html)
        status = tree.xpath('//span[@class="apl_m_font"]/text()')
        if status:
           promotion = re.sub('\n| ', '', status[0])

        return promotion

#if __name__ == '__main__':
#    amz = AMZprice("https://www.amazon.cn/%E7%8E%A9%E5%85%B7/dp/B012NOETAM/ref=sr_1_2/462-7323484-1300758?ie=UTF8&qid=1498473073&sr=8-2-spons&keywords=LEGO&th=1")
#    amz.get_product_price()
