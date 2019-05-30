import os
import threading


def gen_html_header():
    return '''<!DOCTYPE html> 
<html> 

<body>
    <table border="1">
'''


def gen_html_footer():
    return '''
    </table>

</body>
</html>
'''


def gen_product_html(icon, jpg, url, name, price, promotion):
    if not price or not jpg or not name or not url:
        return ""
    tr = '''        <tr>
            <td><img src=''' + "\"" + jpg + "\"" + '''width=\"250\" height=\"200\"/></td>
            <td width=\"800\"><a href=''' + "\"" + url + "\" target=\"_blank\"" + ">" + name + '''</a></td>
            <td><img src=''' + "\"" + icon + "\"" + '''width=\"25\" height=\"25\"/></td>
            <td align=\"center\" width=\"100\"><font color=\"Crimson\"><b>''' + str(price) + '''</b></font></td>
            <td width=\"450\"><font color=\"DarkGreen\"><b>''' + str(promotion) + '''</b></font></td>
        </tr>
'''

    return tr


def clear_html():
    if os.path.exists("html/output.html"):
        os.remove("html/output.html")


def write_item(i, w_file):
    w_file.write(gen_product_html(i["ICON"], i["JPG"], i["URL"], i["NAME"], i["PRICE"], i["PROMOTION"]))


def create_html(infolist):
    with open("html/output.html", "a") as f:
        f.write(gen_html_header())

        length = len(infolist)
        for i in infolist[::4]:
            index = infolist.index(i)
            task_list = []

            t1 = threading.Thread(target=write_item, args=(i, f))
            task_list.append(t1)

            if (index + 1) < length:
                t2 = threading.Thread(target=write_item, args=(infolist[index + 1], f))
                task_list.append(t2)
            if (index + 2) < length:
                t3 = threading.Thread(target=write_item, args=(infolist[index + 2], f))
                task_list.append(t3)
            if (index + 3) < length:
                t4 = threading.Thread(target=write_item, args=(infolist[index + 3], f))
                task_list.append(t4)

            for t in task_list:
                t.start()

            for t in task_list:
                t.join()

        f.write(gen_html_footer())
