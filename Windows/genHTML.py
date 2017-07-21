#!/usr/bin/python3.4

import os, threading

def genHTMLheader():
    return '''<!DOCTYPE html> 
<html> 

<body>
    <table border="1">
'''

def genHTMLfooter():
   return '''
    </table>

</body>
</html>
'''

def genProductHTML(icon, jpg, url, name, price, promotion):
    if not price or not jpg or not name or not url:
        return ""
    TR = '''        <tr>
            <td><img src=''' + "\"" + jpg + "\"" +  '''width=\"250\" height=\"200\"/></td>
            <td width=\"800\"><a href=''' + "\"" + url + "\" target=\"_blank\"" + ">" + name + '''</a></td>
            <td><img src=''' + "\"" + icon + "\"" +  '''width=\"25\" height=\"25\"/></td>
            <td align=\"center\" width=\"100\"><font color=\"Crimson\"><b>'''  + price + '''</b></font></td>
            <td width=\"450\"><font color=\"DarkGreen\"><b>''' + promotion + '''</b></font></td>
        </tr>
'''
    
    TR = TR.encode("gbk", "ignore")
    return TR

def clearHTML():
    if os.path.exists("HTML_Src/output.html"):
        os.remove("HTML_Src/output.html")

def writeItem(i, File):
    File.write(genProductHTML(i["ICON"], i["JPG"], i["URL"], i["NAME"], i["PRICE"], i["PROMOTION"]).decode("gbk"))

def createHTML(infolist):
    with open("HTML_Src/output.html", "a") as f:
        f.write(genHTMLheader())
    
        length = len(infolist)
        for i in infolist[::4]:
            index = infolist.index(i)
            task_list = []

            t1 = threading.Thread(target=writeItem,args=(i, f))
            task_list.append(t1)
   
            if (index + 1) < length:
                t2 = threading.Thread(target=writeItem,args=(infolist[index + 1], f))
                task_list.append(t2)
            if (index + 2) < length:
                t3 = threading.Thread(target=writeItem,args=(infolist[index + 2], f))
                task_list.append(t3)
            if (index + 3) < length:
                t4 = threading.Thread(target=writeItem,args=(infolist[index + 3], f))
                task_list.append(t4)

            for t in task_list:
                t.start()
  
            for t in task_list:
                t.join()

        f.write(genHTMLfooter())

