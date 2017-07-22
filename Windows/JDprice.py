#!/usr/bin/python3.4

import json
import re
import HTMLInfo, sys
from lxml import html
from urllib import request

class JDprice(object):
    def __init__(self, url):
        self.url = url
        HTMLInfo.REFERER = url 
        r = HTMLInfo.getHTML(url)
        self.html = r
        self.info = self.get_product()

    def get_url_page(self):
        tree = html.fromstring(self.html)
        page = tree.xpath('//div[@id="J_filter"]//div[@id="J_topPage"]//span[@class="fp-text"]/i/text()')
        if page:
           page = page[0]
        else:
           print("Error: Cannot get the pages")
           sys.exit()
   
        return int(page) if int(page) < 2 else 2

    def create_url(self, url_list):
        page = self.get_url_page()
        for i in range(1, int(page) + 1):
            url_list.append(self.url + str(i))

    def get_itemlist(self, itemlist):
        tree = html.fromstring(self.html)
        status = tree.xpath('//div[@id="J_goodsList"]//div[@class="p-name p-name-type-2"]//@href')
        for item in status:
            if re.search('//item.jd.com', item):
                item = re.sub('//', 'https://', item)
            if item not in itemlist:
                itemlist.append(item)

    def get_product(self):
        PRODUCT = re.compile(r'compatible: true,(.*?)};', re.S)
        product_info = re.findall(PRODUCT, self.html)
        if product_info:
           return product_info[0]

        return None

    def get_product_jpg(self):
        JPG = re.compile(r"src: '(.*?)',")
        jpg = "http://img10.360buyimg.com/n1/" + re.findall(JPG, self.info)[0]

        return jpg

    def get_product_skuid(self):
        SKUID = re.compile(r'skuid: (.*?),')
        skuid = re.findall(SKUID, self.info)[0]

        return skuid

    def get_product_cate(self):
        CAT = re.compile(r"cat: \[(.*?)\],")
        cat = re.findall(CAT, self.info)[0]

        return cat

    def get_vendorId(self):
        VID = re.compile(r'venderId:(.*?),')
        vid = re.findall(VID, self.info)[0]

        return vid

    def get_shopId(self):
        SID = re.compile(r"shopId:'(.*?)',")
        sid = re.findall(SID, self.info)[0]

        return sid

    def get_product_promotion(self):
        discount = {}
        content = ""
        vip = ""
        skuid = self.get_product_skuid()
        cat = self.get_product_cate()
        venderId = self.get_vendorId()
        shopId = self.get_shopId()

        # 2_2813_51976_0 stands for Shanghai; 1_72_2799_0 means Beijing
        url = "http://cd.jd.com/promotion/v2?&skuId=" + skuid + "&area=2_2813_51976_0&shopId=" + shopId + "&venderId=" + venderId + "&cat=" + cat
        prom = json.loads(request.urlopen(url).read().decode("gbk"))

        if "skuCoupon" in  prom.keys():
            if prom["skuCoupon"]:
                for i in prom["skuCoupon"]:
                    discount[i["discount"]] = i["quota"]

        if "prom" in prom.keys():
            if "tags" in prom["prom"].keys():
                if prom["prom"]["tags"]:
                    if prom["prom"]["tags"][0]["name"] == "会员特价":
                        vip = prom["prom"]["tags"][0]["name"]
       
            if "pickOneTag" in prom["prom"].keys():
                if prom["prom"]["pickOneTag"]:
                    content = prom["prom"]["pickOneTag"][0]["content"]

        sale = ""
        gift = ""
        if discount:
            for i in discount.keys():
                sale += "满减：满" + str(discount[i]) + "减" + str(i) + "<br />"
        if vip:
            vip = str(vip) + "<br />"
        if content:
            gift = "满赠：" + str(content) + "<br />"

        promotion = vip + sale + gift

        return promotion

    def get_product_name(self):
        name = ""
            NAME = re.compile(r"name: '(.*?)',")
            name = re.findall(NAME, self.info)[0]
        except:
            pass

        return bytes(name.encode()).decode('unicode-escape')

    def get_product_price(self):
        price = ""
        pprice = ""
        DATE = {}
        skuid = self.get_product_skuid()
        r = HTMLInfo.getHTML("https://d.jd.com/lab/get?callback=lab")
        MATCH = re.compile(r"lab\(\[(.*?)\]\)")
        for i in eval(re.findall(MATCH, r)[0]):
            if re.match('www.jd.com', i['url']):
                date = i["startOn"]

        date = str(date) + "1608370126"
          
        # this url to get the price for JD
        url = "http://p.3.cn/prices/mgets?&type=1&pduid=" + date + "&skuIds=J_" + skuid

        # response.json() can return the json-encoded content of a response
        status = json.loads(request.urlopen(url).read().decode("gbk"))

        if status:
            if 'tpp' in  status:
                pprice = "PLUS价:<br />" + status['tpp']
            if 'p' in status:
                price = "京东价:<br />" + status['p']
        return price + "<br />" + pprice

#if __name__ == '__main__':
#    jd = JDprice("https://item.jd.com/4488334.html")
#    print(jd.get_product_price())
