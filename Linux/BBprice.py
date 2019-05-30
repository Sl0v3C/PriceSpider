#!/usr/bin/python3

import re

from lxml import html

import HTMLInfo


class BBPrice(object):
    def __init__(self, url):
        self.url = url
        r = HTMLInfo.get_html(url)
        if r.encoding:
            self.html = r.content.decode(r.encoding)
        else:
            self.html = r.content.decode('utf-8')

    def create_url(self, url_list):
        url_list.append(self.url)

    def get_itemlist(self, item_list):
        tree = html.fromstring(self.html)
        status = tree.xpath(
            '/html/body/div[@id="container"]/div[@id="content"]/div[@class="show-body"]/ul[@id="my-search-pc"]/li[@class="view-ItemListItem"]/a/@href')
        if status:
            for i in status:
                if i not in item_list and re.search("www.beibei.com/detail", i):
                    item_list.append(i)

    def get_product_jpg(self):
        tree = html.fromstring(self.html)
        status = tree.xpath(
            '//div[@class="side-wrapper"]/div[@class="carousel-wrapper carousel-control view-CarouselControl"]/div[@class="main-img-cont clearfix"]/a/img/@rel')
        if status:
            jpg = status[0]
            return jpg

    def get_product_name(self):
        name = ""
        tree = html.fromstring(self.html)
        status = tree.xpath('//div[@class="main-wrapper"]/div[@class="title"]/h3/text()')
        if status:
            for i in status:
                if not re.search('^\n$', i):
                    name = re.sub('^\n| ', '', i)
        return name

    def get_product_price(self):
        price = ""
        s_price = ""
        little = ""
        integer = ""
        info = ""
        tree = html.fromstring(self.html)
        status = tree.xpath('//a[@class="add-to-cart-btn view-AddBtn"]//span[@class="price-wrap"]/span[@class="price-integer"]/text()\
                            |//a[@class="add-to-cart-btn view-AddBtn"]//span[@class="price-wrap"]/span[@class="price-little"]/text()')
        sale_status = tree.xpath('//a[@class="pintuan-buy-btn view-PintuanBuyBtn"]//span[@class="price-wrap"]/span[@class="price-integer"]/text()\
                                |//a[@class="pintuan-buy-btn view-PintuanBuyBtn"]//span[@class="price-wrap"]/span[@class="price-little"]/text()')

        disable = tree.xpath('//div[@class="ops view-BuyBar"]/a[@class="add-to-cart-btn disable"]/text()')
        if disable:
            info = disable[0]

        if status:
            for i in status:
                if re.search('^\.', i):
                    little = i
                else:
                    integer = i
            price = "单独购买: " + integer + little

        if sale_status:
            for i in sale_status:
                if re.search('^\.', i):
                    little = i
                else:
                    integer = i
            s_price = "2人团: " + integer + little

        return price + "<br />" + s_price + info

    def get_product_promotion(self):
        promotion = ""
        tree = html.fromstring(self.html)
        status = tree.xpath('//span[@class="promotions-info return-info view-ReturnInfo"]/text()')
        if status:
            for i in status:
                if not re.search('^\n', i):
                    promotion = re.sub('^\n| ', '', i)
        return promotion

# if __name__ == '__main__':
#     bb = BBprice("http://you.beibei.com/detail/102985355-1038678.html#sid=16")
#     url_list = []
#     bb.get_product_price()
#     bb.get_product_jpg()
#     bb.get_product_name()
#    bb.get_product_promotion()
