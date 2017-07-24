# PriceSpider
Price Spider is a Python tool to get price &amp; promotion from JD, Tmall, Amazon, BeiBei.  

## Requirements
When you use the tool, sometimes the tool will launch your browser automatically.So you should satisfy some requirements, then this tool can launch your browser and get the info you care about.  
### Windows verison requirements
If you use this tool in Windows version, you should notice below requirements.  
Now the tool supports Chrome, Firefox & IE. Every browser need the driver for itself to work properly, so you just make sure you satisfy the requirement of the one of the three browsers is enough.  
#### chromedriver for Chrome browser
The tool will automatically copy the chromedriver.exe to the system32.   
Please make sure your chrome browser version is adapted to the chromedriver version.  
You can download the [chromedriver](http://chromedriver.storage.googleapis.com/index.html) for your chrome version and copy it to A64 or X86 in the tool folder to replace the default one(A64 stands for the 64bit OS & X86 stands fo the 32bit OS).   

* The tool contains the chromedriver v2.30 which supports the chrome v58-60.
* If you cannot launch the chrome browser after the version check, you should uninstall the chrome and delete the folder realted to Chrome and re-install it with the default configuration.

#### IEDriverServer for Internet Explorer browser  
The tool also will copy the IEDriverServer.exe to the system PATH.  

* On IE 7 or higher on Windows Vista or Windows 7, you must set the Protected Mode settings for each zone to be the same value. The value can be on or off, as long as it is the same for every zone. To set the Protected Mode settings, choose "Internet Options..." from the Tools menu, and click on the Security tab. For each zone, there will be a check box at the bottom of the tab labeled "Enable Protected Mode".
* Additionally, "Enhanced Protected Mode" must be disabled for IE 10 and higher. This option is found in the Advanced tab of the Internet Options dialog.
* For IE11 only, you will need to execute the```IE11_regedit_update.bat```firstly
#### geckoriver for Firefox browser  
The tool also will copy the geckodriver.exe to the system PATH.  
Please make sure your Firefox broser version is adapted to geckodriver verison.        
You can download the [geckodriver](https://github.com/mozilla/geckodriver/releases) for your Firefox version. And copy it to the A64 or X86 in the tool folder. 

* The tool contains the geckodriver v0.18 suports Firefox 53 and greater.
 
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
When you finish the configurate and satisfy the requirements then you can execute the```run.bat```

***
# PriceSpider中文README
Price Spider是一个可以帮助用户从各大电商网站如京东，天猫，亚马逊，贝贝等抓取价格和优惠的一款Python工具。

## 要求
当你使用本工具时，某些时候工具会自动地启动你的浏览器来抓取商品信息，所以必须满足一些条件，这样工具才能顺利地启动浏览器。
### Windows版本要求
如果你将使用该工具的Windows版本，请注意满足以下的要求。  
本工具现支持Chrome，Firefox和IE浏览器。每一个浏览器都需要它独特的driver来满足自动化工作，所以你只需要确保满足三个浏览器其中的一个要求即可。
#### Chrome浏览器(chromedriver)
工具会自动的将chromedriver.exe拷贝到system32目录。  
请确保你的浏览器版本和chromedriver的版本是相对应的。  
你可以通过[chromedriver](http://chromedriver.storage.googleapis.com/index.html)链接下载与你浏览器版本对应的chromedriver版本，并替换掉工具中对应64位系统的A64或者32位系统的X86目录中的默认版本。

* The tool contains the chromedriver v2.30 which supports the chrome v58-60.
* 工具自带的chromedriver是2.30版本的，支持Chrome浏览器版本v58-60.
* 如果你满足了版本匹配的情况下仍然无法自动启动Chrome浏览器，请尝试卸载它并删除与之相关的所有目录，同时重新安装并保持默认安装配置不变。

#### IE浏览器(IEDriverServer)
工具会拷贝IEDriverServer.exe到系统PATH，以便能够运行。

* 针对windows vista和windows 7上的IE7或者更高的版本，必须在IE选项设置的安全选项栏里保证4个区域的保护模式是一致的，即全部勾选启用或者全部不勾选禁用。
* 针对IE10或更高的版本，则必须在IE选项中的高级选项中，取消增强保护模式。
* 只针对IE11的版本，需要在运行run.bat之前先运行```IE11_regedit_update.bat```
#### Firefox浏览器(geckoriver)
工具会拷贝geckodriver.exe到系统PATH，以便其能够运行。
请确保你的Firefox浏览器版本与geckodriver版本保持对应关系。  
你也可以通过[geckodriver](https://github.com/mozilla/geckodriver/releases)链接下载与你的Firefox浏览器版本对应的版本，记得替换掉工具目录中的原始版本。

* 工具自带的geckodriver是0.18版本的，支持Firefox 53或更高。

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
当你完成了上述配置，并且满足了前面的要求，你可以通过执行```run.bat```
