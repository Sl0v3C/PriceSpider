# PriceSpider
Price Spider is a Python tool to get price &amp; promotion from JD, Tmall, Amazon, BeiBei.  
This tool just for testing or learning usage.  
Please do not use it for illegal purposes. The author is not responsible for the consequences.

Content:
- [Requirements](https://github.com/Sl0v3C/PriceSpider#requirements)  
&nbsp;&nbsp;&nbsp;&nbsp;1. [Linux](https://github.com/Sl0v3C/PriceSpider#linux-verison-requirements)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1\.1 [chromedriver](https://github.com/Sl0v3C/PriceSpider#chromedriver-for-chrome-browser-1)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1\.2 [geckodriver](https://github.com/Sl0v3C/PriceSpider#geckodriver-for-firefox-browser-1)  
- [Configuration](https://github.com/Sl0v3C/PriceSpider#configuration)  
&nbsp;&nbsp;&nbsp;&nbsp;1. [urlLink](https://github.com/Sl0v3C/PriceSpider#cfgurllink)  
&nbsp;&nbsp;&nbsp;&nbsp;2. [PRODUCT](https://github.com/Sl0v3C/PriceSpider#cfgproduct)
- [Usage](https://github.com/Sl0v3C/PriceSpider#usage)

## Requirements
When you use the tool, sometimes the tool will launch your browser automatically.So you should satisfy some requirements, then this tool can launch your browser and get the info you care about.  

### Linux verison requirements  
Only tested for Ubuntu, you can have a try for other Linux OS.
Tool now only supports Chrome & Firefox in Linux OS.
#### chromedriver for Chrome browser
The tool will automatically copy the chromedriver to /usr/local/bin/.   
Please make sure your chrome browser version is adapted to the chromedriver version.  
You can download the [chromedriver](http://chromedriver.storage.googleapis.com/index.html) for your chrome version and copy it to A64 or X86 in the tool folder to replace the default one(A64 stands for the 64bit OS & X86 stands fo the 32bit OS).

* The tool contains chromedriver is 2.22 supports Chrome v49-52.

#### geckodriver for Firefox browser  
The tool also will copy the geckodriver to /usr/local/bin/.  
Please make sure your Firefox broser version is adapted to geckodriver verison.        
You can download the [geckodriver](https://github.com/mozilla/geckodriver/releases) for your Firefox version. And copy it to the A64 or X86 in the tool folder. 

* The tool contains the geckodriver v0.17 suports Firefox 52 and greater.
 
## Configuration
You should config some files before you run the tool.
#### cfg/urlLink
This file save the e-shop links, you can delete the ``` # ``` at the beginnig of the url link to enable get info from this link.
<pre># You can add '#' at the beginning of the line to cancel getting info from the shop
#http://search.jd.com/Search?keyword=GOODS&enc=utf-8&page=
#https://www.amazon.cn/s/&keywords=GOODS&page=
https://s.taobao.com/search?q=GOODS&tab=mall&s=
#http://d.beibei.com/search/GOODS-.html
</pre>

#### cfg/PRODUCT
This file save the product you want to get the info.  
Now the tool only support one product.
<pre>
LEGO
</pre>

## Usage
When you finish the configurate and satisfy the requirements then you can execute the``` ./env.sh ```.

***
# PriceSpider中文README
Price Spider是一个可以帮助用户从各大电商网站如京东，天猫，亚马逊，贝贝等抓取价格和优惠的一款Python工具。  
本工具旨在测试或者学习用途，请勿用于非法用途或商业牟利。  
若本工具被用于非法用途，造成一切后果与本作者无关。

目录:
- [要求](https://github.com/Sl0v3C/PriceSpider#要求)  
&nbsp;&nbsp;&nbsp;&nbsp;1. [Linux版本要求](https://github.com/Sl0v3C/PriceSpider#linux版本要求)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1\.1 [Chrome浏览器](https://github.com/Sl0v3C/PriceSpider#chrome浏览器chromedriver-1)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1\.2 [Firefox浏览器](https://github.com/Sl0v3C/PriceSpider#firefox浏览器geckodriver-1)  
- [配置](https://github.com/Sl0v3C/PriceSpider#配置)  
&nbsp;&nbsp;&nbsp;&nbsp;1. [urlLink](https://github.com/Sl0v3C/PriceSpider#cfgurllink-1)  
&nbsp;&nbsp;&nbsp;&nbsp;2. [PRODUCT](https://github.com/Sl0v3C/PriceSpider#cfgproduct-1)  
- [用法](https://github.com/Sl0v3C/PriceSpider#用法)  

## 要求
当你使用本工具时，某些时候工具会自动地启动你的浏览器来抓取商品信息，所以必须满足一些条件，这样工具才能顺利地启动浏览器。

### Linux版本要求
现阶段只在Ubuntu系统上测试过，当然你可以尝试在其他Linux发行版中运行。
工具目前在Linux系统中只支持Chrome和Firefox两种浏览器
#### Chrome浏览器(chromedriver)
工具会自动地拷贝chromedriver到/usr/local/bin目录下。  
请确保你的浏览器版本和chromedriver的版本是相对应的。  
你可以通过[chromedriver](http://chromedriver.storage.googleapis.com/index.html)链接下载与你浏览器版本对应的chromedriver版本，并替换掉工具中对应64位系统的A64或者32位系统的X86目录中的默认版本。

* 本工具自带的chromedriver是2.22版本的，支持Chrome版本49-52。

#### Firefox浏览器(geckodriver)  
工具会自动地拷贝geckodriver到/usr/local/bin目录下。  
请确保你的Firefox浏览器版本与geckodriver版本保持对应关系。  
你也可以通过[geckodriver](https://github.com/mozilla/geckodriver/releases)链接下载与你的Firefox浏览器版本对应的版本，记得替换掉工具目录中的原始版本。

* 工具自带的geckodriver是0.17版本的，支持Firefox版本52或更高。
 
## 配置
在使用工具前，你需要配置一些文件，诸如希望抓取的商品名称，需要抓取的网站等。
#### cfg/urlLink
这个文件用于保存电商网页的地址，你可以通过在网址的头部添加或删除``` # ```来启用或禁用抓取该网址。
<pre># You can add '#' at the beginning of the line to cancel getting info from the shop
#http://search.jd.com/Search?keyword=GOODS&enc=utf-8&page=
#https://www.amazon.cn/s/&keywords=GOODS&page=
https://s.taobao.com/search?q=GOODS&tab=mall&s=
#http://d.beibei.com/search/GOODS-.html
</pre>

#### cfg/PRODUCT
该文件用于保存你想要抓取的商品名称，目前只支持保存一个商品名称。
<pre>
乐高
</pre>

## 用法
当你完成了上述配置，并且满足了前面的要求，你可以通过执行``` ./env.sh ```。
