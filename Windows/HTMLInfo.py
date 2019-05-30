import AMZPrice
import BBPrice
import JDPrice
import TMprice
import re
import requests
import sys
import threading
from selenium import webdriver

REFERER = ""

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.36',
    'referer': REFERER
}

line_break_pattern = re.compile('\n')
JD = re.compile('search.jd.com')
AMZ = re.compile('www.amazon.cn')
TM = re.compile('s.taobao.com')
BB = re.compile('d.beibei.com')


def get_info_from_jd(item, infolist, driver):
    jd = JDPrice.JDPrice(item)
    data_dict = {"ICON": "icon/JD.png", "URL": item, "NAME": jd.get_product_name(), "PRICE": jd.get_product_price(),
                 "JPG": jd.get_product_jpg(), "PROMOTION": jd.get_product_promotion()}
    infolist.append(data_dict)


def get_info_from_amazon(item, info_list, driver):
    amz = AMZPrice.AMZPrice(item)
    data_dict = {"ICON": "icon/AMZ.png", "URL": item, "NAME": amz.get_product_name(), "PRICE": amz.get_product_price(),
                 "JPG": amz.get_product_jpg(), "PROMOTION": amz.get_product_promotion()}
    info_list.append(data_dict)


def get_info_from_tmall(item, infolist, driver):
    tm = TMprice.TMprice(item)
    data_dict = tm.get_info_2dictionary(driver)
    if data_dict:
        data_dict["ICON"] = "icon/TM.jpg"
        infolist.append(data_dict)


def get_info_from_beibei(item, infolist, driver):
    bb = BBPrice.BBPrice(item)
    data_dict = {"ICON": "icon/BB.jpg", "URL": item, "NAME": bb.get_product_name(), "PRICE": bb.get_product_price(),
                 "JPG": bb.get_product_jpg(), "PROMOTION": bb.get_product_promotion()}
    infolist.append(data_dict)


def create_jd_url(urls, url_list):
    for url in urls:
        jd = JDPrice.JDPrice(url)
        jd.create_url(url_list)


def create_amazon_url(urls, url_list):
    for url in urls:
        amz = AMZPrice.AMZPrice(url)
        amz.create_url(url_list)


def create_tmall_url(urls, url_list):
    for url in urls:
        tm = TMprice.TMprice(url)
        tm.create_url(url_list)


def create_beibei_url(urls, url_list):
    for url in urls:
        bb = BBPrice.BBPrice(url)
        bb.create_url(url_list)


def get_jd_items(url, item_list):
    jd = JDPrice.JDPrice(url)
    jd.get_itemlist(item_list)


def get_amazon_items(url, item_list):
    amz = AMZPrice.AMZPrice(url)
    amz.get_item_list(item_list)


def get_tmall_items(url, item_list):
    tm = TMprice.TMprice(url)
    tm.get_item_list(item_list)


def get_beibei_items(url, item_list):
    bb = BBPrice.BBPrice(url)
    bb.get_itemlist(item_list)


CALLBACK = {
    "JD": get_info_from_jd,
    "AMZ": get_info_from_amazon,
    "TM": get_info_from_tmall,
    "BB": get_info_from_beibei,
}

getTypeItemList = {
    "JD": get_jd_items,
    "AMZ": get_amazon_items,
    "TM": get_tmall_items,
    "BB": get_beibei_items,
}

createTypeURL = {
    "JD": create_jd_url,
    "AMZ": create_amazon_url,
    "TM": create_tmall_url,
    "BB": create_beibei_url,
}


class HTMLinfo(object):
    def __init__(self, url):
        self.url = url
        self.products = []
        self.products_urls = []
        self.item_list = []
        self.url_list = []
        self.pages = None
        self.type = None
        self.data_dict = {}
        self.info_list = []

    def shop(self):
        if re.search(JD, self.url):
            self.type = "JD"
        elif re.search(AMZ, self.url):
            self.type = "AMZ"
        elif re.search(TM, self.url):
            self.type = "TM"
        elif re.search(BB, self.url):
            self.type = "BB"
        else:
            print("Error: Wrong type shop!!!")
            sys.exit()

    def multi_process(self):
        length = len(self.item_list)
        if self.type == "TM":
            driver = get_web_driver()
            if not driver:
                sys.exit()
            # Need check in my patches to use this function
            # driver.minimize_window()
        else:
            driver = None

        for i in self.item_list[::4]:
            index = self.item_list.index(i)
            task_list = []

            callback = CALLBACK[self.type]

            t1 = threading.Thread(target=callback, args=(i, self.info_list, driver))
            task_list.append(t1)
            if (index + 1) < length:
                t2 = threading.Thread(target=callback, args=(self.item_list[index + 1], self.info_list, driver))
                task_list.append(t2)
            if (index + 2) < length:
                t3 = threading.Thread(target=callback, args=(self.item_list[index + 2], self.info_list, driver))
                task_list.append(t3)
            if (index + 3) < length:
                t4 = threading.Thread(target=callback, args=(self.item_list[index + 3], self.info_list, driver))
                task_list.append(t4)
            for t in task_list:
                t.start()

            for t in task_list:
                t.join()

        if self.type == "TM":
            driver.quit()

    def get_goods(self):
        with open("cfg/PRODUCT", "r", encoding='UTF-8') as f:
            for line in f.readlines():
                product = re.sub(line_break_pattern, '', line)
                self.products.append(product)

    def replace_goods(self):
        goods_pattern = re.compile('GOODS')
        new = re.sub(line_break_pattern, '', self.url)

        self.products_urls = [re.sub(goods_pattern, product, new) for product in self.products]

    def get_items(self):
        if self.url_list:
            for url in self.url_list:
                getTypeItemList[self.type](url, self.item_list)
        else:
            print("There is no URL links!!")
            sys.exit()

    def create_url(self):
        createTypeURL[self.type](self.products_urls, self.url_list)


def get_web_driver():
    driver = None
    try:
        driver = webdriver.Firefox()
    except:
        try:
            driver = webdriver.Chrome()
        except:
            try:
                driver = webdriver.Ie()
            except:
                print("Error: Web driver cannot access the browser!")

    return driver


def get_html(url):
    r = requests.get(url, headers=header, timeout=30)

    return r
