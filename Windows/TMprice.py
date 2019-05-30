import re
import HTMLInfo, sys, threading, time
from lxml import html
from selenium import webdriver

driver_lock = threading.Lock()


class TMprice(object):
    def __init__(self, url):
        self.url = url
        HTMLInfo.REFERER = url
        r = HTMLInfo.get_html(url)
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
        sku_id_list = []
        if self.info:
            sku_map_pattern = re.compile(r',"skuMap":{";(.*?)}}},')
            sku_info = re.findall(sku_map_pattern, self.info)
            sku_id_pattern = re.compile(r'"skuId":"(.*?)"')
            stock_pattern = re.compile(r',"stock":(.*?)},')
            if sku_info:
                sku_list = re.findall(sku_id_pattern, sku_info[0])
                stock_list = re.findall(stock_pattern, sku_info[0])
                if stock_list:
                    for i, v in enumerate(stock_list):
                        if int(v) == 0:
                            continue
                        else:
                            sku_id_list.append(sku_list[i])

        return sku_id_list

    def get_info_2dictionary(self, driver):
        sale_price = ""
        jpg = ""
        promotion = ""
        price = ""
        data_dict = {}
        if self.info:
            title_pattern = re.compile(r',"title":(.*?),')
            title = re.findall(title_pattern, self.info)[0]
            title = re.sub('"', '', title)
            driver_lock.acquire()
            driver.get(self.url)
            # time.sleep(0.2)
            try:
                price = driver.find_element_by_xpath('//dl[@id="J_StrPriceModBox"]/dd/span[@class="tm-price"]').text
                sale_price = driver.find_element_by_xpath('//dl[@id="J_PromoPrice"]//span[@class="tm-price"]').text
                jpg = driver.find_element_by_xpath('//img[@id="J_ImgBooth"]').get_attribute('src')
                promotion = driver.find_element_by_xpath('//dl[@class="tm-shopPromo-panel"]//dd').text
            except:
                pass
            data_dict["URL"] = self.url
            data_dict["NAME"] = title
            data_dict["PRICE"] = (sale_price if sale_price else price)
            data_dict["JPG"] = jpg
            data_dict["PROMOTION"] = promotion
            driver_lock.release()
        if not data_dict["JPG"] or not data_dict["PRICE"] or not data_dict["NAME"]:
            data_dict = {}

        return data_dict

    def is_single_product(self):
        tree = html.fromstring(self.html)
        status = tree.xpath('//div[@class="tb-sku"]//dt[@class="tb-metatit"]/text()')
        if status:
            if '颜色分类' in status:
                return False

        return True

    def get_real_item_link(self, url):
        url_list = []
        tm = TMprice(url)
        if tm.is_single_product():
            url_list.append(url)
        else:
            for i in tm.get_skuid():
                url_pattern = url + "&skuId=" + i
                url_list.append(url_pattern)

        return url_list

    def get_item_list(self, item_list):
        tree = html.fromstring(self.html)
        status = tree.xpath('//script/text()')
        if status:
            page_info = re.compile(r'g_page_config = (.*?)};')
            url_pattern = re.compile(r'"detail_url":"(.*?)",')
            for i in status:
                if re.search(page_info, i):
                    status = i
                    break
            info = re.findall(page_info, status)[0] + '}'

            url_list = re.findall(url_pattern, bytes(info.encode()).decode('unicode-escape'))
            for i in url_list:
                i = re.sub('//', 'https://', i)
                if re.search("https://detail.tmall.com/", i):
                    item_list = self.get_real_item_link(i)
                    for j in item_list:
                        if j not in item_list:
                            item_list.append(j)

# if __name__ == '__main__':
# tmall = TMprice('''"https://detail.tmall.com/item.htm?spm=a230r.1.14.37.MxAmy6&id=36856935572&ns=1&abbucket=3")#'''
#     tmall = TMprice("https://detail.tmall.com/item.htm?id=41995475605&ns=1&abbucket=0")
#     tmall.get_skuid()
#     tmall.get_info_2dictionary()
