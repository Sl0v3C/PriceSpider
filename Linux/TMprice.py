#!/usr/bin/python3.4

import json
import re
import HTMLInfo, sys, threading, time
from lxml import html
from selenium import webdriver

driver_lock = threading.Lock()

class TMprice(object):
    def __init__(self, url):
        self.url = url
        HTMLInfo.REFERER = url
        r = HTMLInfo.getHTML(url)
        if r.encoding:
           self.html = r.content.decode(r.encoding)
        else:
           self.html = r.content.decode('utf-8')
        self.info = self.get_info()

    def get_info(self):
        info = ""
        tree = html.fromstring(self.html)
        status = tree.xpath('//script/text()')
        if status:
            for i in status:
                if re.search('TShop.Setup', i):
                    return i

        return info

    def get_url_page(self):

        return 44

    def create_url(self, url_list):
        page = self.get_url_page()
        for i in range(1, int(page / 44) + 1):
            url = re.sub('s=0$', 's=', self.url)
            url_list.append(url + str(page))

    def get_skuid(self):
        skuidlist = []
        stocklist = []
        if self.info:
            SKUMAP = re.compile(r',"skuMap":{";(.*?)}}},')
            skuinfo = re.findall(SKUMAP, self.info)
            SKUID = re.compile(r'"skuId":"(.*?)"')
            STOCK = re.compile(r',"stock":(.*?)},')
            if skuinfo:
                skulist = re.findall(SKUID, skuinfo[0])
                stocklist = re.findall(STOCK, skuinfo[0])
                if stocklist:
                    for i, v in enumerate(stocklist):
                        if int(v) == 0:
                            continue
                        else:
                            skuidlist.append(skulist[i])

        return skuidlist

    def get_info_2dictionary(self, driver):
        saleprice = ""
        jpg = ""
        promotion = ""
        price = ""
        Dict = {}
        if self.info:
            TITLE = re.compile(r',"title":(.*?),')
            title = re.findall(TITLE, self.info)[0]
            title = re.sub('"', '', title)
            driver_lock.acquire()
            driver.get(self.url)
            #time.sleep(0.2)
            try:
                price = driver.find_element_by_xpath('//dl[@id="J_StrPriceModBox"]/dd/span[@class="tm-price"]').text
                saleprice = driver.find_element_by_xpath('//dl[@id="J_PromoPrice"]//span[@class="tm-price"]').text
                jpg = driver.find_element_by_xpath('//img[@id="J_ImgBooth"]').get_attribute('src')
                promotion = driver.find_element_by_xpath('//dl[@class="tm-shopPromo-panel"]//dd').text
            except:
                pass
            Dict["URL"] = self.url
            Dict["NAME"] = title
            Dict["PRICE"] = (saleprice if saleprice else price)
            Dict["JPG"] = jpg
            Dict["PROMOTION"] = promotion
            driver_lock.release()
        if not Dict["JPG"] or not Dict["PRICE"] or not Dict["NAME"]:
            Dict = {}

        return Dict

    def isSingleProduct(self):
        tree = html.fromstring(self.html)
        status = tree.xpath('//div[@class="tb-sku"]//dt[@class="tb-metatit"]/text()')
        if status:
            if '颜色分类' in status:
                return False

        return True

    def get_real_item_link(self, url):
        url_list = []
        tm = TMprice(url)
        if tm.isSingleProduct():
            url_list.append(url)
        else:
            for i in tm.get_skuid():
                URL = url + "&skuId=" + i
                url_list.append(URL) 
        
        return url_list
  
    def get_itemlist(self, item_list):
        tree = html.fromstring(self.html)
        status = tree.xpath('//script/text()')
        if status:
            PAGEINFO = re.compile(r'g_page_config = (.*?)};')
            URL = re.compile(r'"detail_url":"(.*?)",')
            for i in status:
                if re.search(PAGEINFO, i):
                    status = i
                    break
            info = re.findall(PAGEINFO, status)[0] + '}'
           
            urllist = re.findall(URL, bytes(info.encode()).decode('unicode-escape'))
            for i in urllist:
                i = re.sub('//', 'https://', i)
                if re.search("https://detail.tmall.com/", i):
                    itemlist = self.get_real_item_link(i)
                    for i in itemlist:
                        if i not in item_list:
                            item_list.append(i)

#if __name__ == '__main__':
     #tmall = TMprice('''"https://detail.tmall.com/item.htm?spm=a230r.1.14.37.MxAmy6&id=36856935572&ns=1&abbucket=3")#'''
#     tmall = TMprice("https://detail.tmall.com/item.htm?id=41995475605&ns=1&abbucket=0")
#     tmall.get_skuid()
#     tmall.get_info_2dictionary()
