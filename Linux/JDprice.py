import json
import re

from lxml import html

import HTMLInfo
import sys


class JDPrice(object):
    def __init__(self, url):
        self.url = url
        HTMLInfo.REFERER = url
        r = HTMLInfo.get_html(url)
        self.html = r.text
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
        status = tree.xpath('//div[@id="J_goodsList"]//div[@class="p-img"]//@href')
        for item in status:
            if re.search('^//item.jd.com', item):
                item = re.sub('//', 'https://', item)
            if item not in itemlist:
                itemlist.append(item)

    def get_product(self):
        product_pattern = re.compile(r'compatible: true,(.*?)};', re.S)
        product_info = re.findall(product_pattern, self.html)
        if product_info:
            return product_info[0]

        return None

    def get_product_jpg(self):
        jpg_pattern = re.compile(r"src: '(.*?)',")
        jpg = "http://img10.360buyimg.com/n1/" + re.findall(jpg_pattern, self.info)[0]

        return jpg

    def get_product_skuid(self):
        sku_id_pattern = re.compile(r'skuid: (.*?),')
        sku_id = re.findall(sku_id_pattern, self.info)[0]

        return sku_id

    def get_product_cate(self):
        cat_pattern = re.compile(r"cat: \[(.*?)\],")
        cat = re.findall(cat_pattern, self.info)[0]

        return cat

    def get_vendorId(self):
        vid_pattern = re.compile(r'venderId:(.*?),')
        vid = re.findall(vid_pattern, self.info)[0]

        return vid

    def get_shopId(self):
        sid_pattern = re.compile(r"shopId:'(.*?)',")
        sid = re.findall(sid_pattern, self.info)[0]

        return sid

    def get_product_promotion(self):
        discount = {}
        content = ""
        vip = ""
        sku_id = self.get_product_skuid()
        cat = self.get_product_cate()
        vender_id = self.get_vendorId()
        shop_id = self.get_shopId()

        # 2_2813_51976_0 stands for Shanghai; 1_72_2799_0 means Beijing
        url = "http://cd.jd.com/promotion/v2?&skuId=" + sku_id + "&area=2_2813_51976_0&shopId=" + shop_id + "&venderId=" + vender_id + "&cat=" + cat
        prom = HTMLInfo.get_html(url).content.decode('gbk')
        try:
            if prom.find('You have triggered an abuse') < 0:
                prom = json.loads(prom)
                if "skuCoupon" in prom.keys():
                    if prom["skuCoupon"]:
                        for i in prom["skuCoupon"]:
                            discount[i["discount"]] = i["quota"]

                if "prom" in prom.keys():
                    if "tags" in prom["prom"].keys():
                        if prom["prom"]["tags"]:
                            if prom["prom"]["tags"][0]["name"] == u'会员特价':
                                vip = prom["prom"]["tags"][0]["name"]

                    if "pickOneTag" in prom["prom"].keys():
                        if prom["prom"]["pickOneTag"]:
                            content = prom["prom"]["pickOneTag"][0]["content"]
        except Exception as ex:
            print('get_product_promotion ', ex)

        sale = ""
        gift = ""
        if discount:
            for i in discount.keys():
                sale += u'满减：满' + str(discount[i]) + u'减' + str(i) + "<br />"
        if vip:
            vip = str(vip) + "<br />"
        if content:
            gift = u'满赠：' + str(content) + "<br />"

        promotion = vip + sale + gift

        return promotion

    def get_product_name(self):
        name = ""
        try:
            name_pattern = re.compile(r"name: '(.*?)',")
            name = re.findall(name_pattern, self.info)[0]
        except Exception as ex:
            print(ex)
        return bytes(name.encode()).decode('unicode-escape')

    def get_product_price(self):
        price = ""
        plus_price = ""
        date = {}
        sku_id = self.get_product_skuid()
        r = HTMLInfo.get_html("https://d.jd.com/lab/get?callback=lab")
        match_pattern = re.compile(r"lab\(\[(.*?)\]\)")
        try:
            json_data = json.loads(re.findall(match_pattern, r.text)[0])
        except Exception as ex:
            print('get_product_price Ex:', ex)
        if re.match('www.jd.com', json_data['url']):
                date = json_data["startOn"]

        date = str(date) + "1608370126"

        # this url to get the price for JD
        url = "http://p.3.cn/prices/mgets?&type=1&pduid=" + date + "&skuIds=J_" + sku_id

        # response.json() can return the json-encoded content of a response
        status = HTMLInfo.get_html(url).json()[0]

        if status:
            if 'tpp' in status:
                plus_price = u"PLUS价:<br />" + status['tpp']
            if 'p' in status:
                price = u"京东价:<br />" + status['p']
        return price + "<br />" + plus_price


if __name__ == '__main__':
    jd = JDPrice("https://item.jd.com/4488334.html")
    print(jd.get_product_price())
