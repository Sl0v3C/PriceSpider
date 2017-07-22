#!/usr/bin/python3.4

import requests, re, JDprice, threading, sys, AMZprice, TMprice, BBprice
from lxml import html
from selenium import webdriver

REFERER = ""

header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'referer':REFERER
}

LINEBREAK = re.compile('\n')
JD = re.compile('search.jd.com')
AMZ = re.compile('www.amazon.cn')
TM = re.compile('s.taobao.com')
BB = re.compile('d.beibei.com')

def getInfoFromJD(item, infolist, driver):
    jd = JDprice.JDprice(item)
    Dict = {}
    Dict["ICON"] = "icon/JD.png"
    Dict["URL"] = item
    Dict["NAME"] = jd.get_product_name()
    Dict["PRICE"] = jd.get_product_price()
    Dict["JPG"] = jd.get_product_jpg()
    Dict["PROMOTION"] = jd.get_product_promotion()
    infolist.append(Dict)

def getInfoFromAMZ(item, infolist, driver):
    amz = AMZprice.AMZprice(item)
    Dict = {}
    Dict["ICON"] = "icon/AMZ.png"
    Dict["URL"] = item
    Dict["NAME"] = amz.get_product_name()
    Dict["PRICE"] = amz.get_product_price()
    Dict["JPG"] = amz.get_product_jpg()
    Dict["PROMOTION"] = amz.get_product_promotion()
    infolist.append(Dict)

def getInfoFromTM(item, infolist, driver):
    tm = TMprice.TMprice(item)
    Dict = {}
    Dict = tm.get_info_2dictionary(driver)
    if Dict:
        Dict["ICON"] = "icon/TM.jpg"
        infolist.append(Dict)

def getInfoFromBB(item, infolist, driver):
    bb = BBprice.BBprice(item)
    Dict = {}
    Dict["ICON"] = "icon/BB.jpg"
    Dict["URL"] = item
    Dict["NAME"] = bb.get_product_name()
    Dict["PRICE"] = bb.get_product_price()
    Dict["JPG"] = bb.get_product_jpg()
    Dict["PROMOTION"] = bb.get_product_promotion()
    infolist.append(Dict)

def createJdURL(URL, urllist):
    jd = JDprice.JDprice(URL)
    jd.create_url(urllist)

def createAmzURL(URL, urllist):
    amz = AMZprice.AMZprice(URL)
    amz.create_url(urllist)

def createTmURL(URL, urllist):
    tm = TMprice.TMprice(URL)
    tm.create_url(urllist)

def createBbURL(URL, urllist):
    bb = BBprice.BBprice(URL)
    bb.create_url(urllist)

def getJdItemList(URL, itemlist):
    jd = JDprice.JDprice(URL)
    jd.get_itemlist(itemlist)

def getAmzItemList(URL, itemlist):
    amz = AMZprice.AMZprice(URL)
    amz.get_itemlist(itemlist)

def getTmItemList(URL, itemlist):
    tm = TMprice.TMprice(URL)
    tm.get_itemlist(itemlist)

def getBbItemList(URL, itemlist):
    bb = BBprice.BBprice(URL)
    bb.get_itemlist(itemlist)

CALLBACK = {
    "JD":getInfoFromJD,
    "AMZ":getInfoFromAMZ,
    "TM":getInfoFromTM,
    "BB":getInfoFromBB,
}

getTypeItemList = {
    "JD":getJdItemList,
    "AMZ":getAmzItemList,
    "TM":getTmItemList,
    "BB":getBbItemList,
}

createTypeURL = {
    "JD":createJdURL,
    "AMZ":createAmzURL,
    "TM":createTmURL,
    "BB":createBbURL,
}

class HTMLinfo(object):
    def __init__(self, url):
        self.url = url
        self.product = None
        self.URL = None
        self.itemlist = []
        self.URLlist = []
        self.pages = None
        self.Type = None
        self.Dict = {}
        self.infolist = []

    def shop(self):
        if re.search(JD, self.url):
            self.Type = "JD"
        elif re.search(AMZ, self.url):
            self.Type = "AMZ"
        elif re.search(TM, self.url):
            self.Type = "TM"
        elif re.search(BB, self.url):
            self.Type = "BB"
        else:
            print("Error: Wrong type shop!!!")
            sys.exit()

    def multiProcess(self):
        length = len(self.itemlist)
        if self.Type == "TM":
            driver = getWebdriver()
            if not driver:
                sys.exit()
            # Need check in my patches to use this function
            #driver.minimize_window() 
        else:
            driver = None

        for i in self.itemlist[::4]:
            index = self.itemlist.index(i)
            task_list = []

            callback = CALLBACK[self.Type]
 
            t1 = threading.Thread(target=callback,args=(i, self.infolist, driver))
            task_list.append(t1)
            if (index + 1) < length:
                t2 = threading.Thread(target=callback,args=(self.itemlist[index + 1], self.infolist, driver))
                task_list.append(t2)
            if (index + 2) < length:
                t3 = threading.Thread(target=callback,args=(self.itemlist[index + 2], self.infolist, driver))
                task_list.append(t3)
            if (index + 3) < length:
                t4 = threading.Thread(target=callback,args=(self.itemlist[index + 3], self.infolist, driver))
                task_list.append(t4)
            for t in task_list:
                t.start()
  
            for t in task_list:
                t.join()

        if self.Type == "TM":
            driver.quit()

    def getGoods(self):
        with open("cfg/PRODUCT", "r", encoding='UTF-8') as f:
            for line in f.readlines():
                product = re.sub(LINEBREAK, '', line)
        self.product = product

    def replaceGoods(self):
        GOODS = re.compile('GOODS')
        new = re.sub(LINEBREAK, '', self.url)
        self.URL = re.sub(GOODS, self.product, new)

    def getItemList(self):
        if self.URLlist:
            for URL in self.URLlist:
                getTypeItemList[self.Type](URL, self.itemlist)
        else:
            print("There is no URL links!!")
            sys.exit()

    def createURL(self):
        createTypeURL[self.Type](self.URL, self.URLlist)

def getWebdriver():
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
                print("Error: Webdriver cannot access the browser!")

    return driver

def getHTML(url):
    r = requests.get(url, headers=header, timeout=30)

    return r


