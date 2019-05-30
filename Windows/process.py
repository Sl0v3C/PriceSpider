import HTMLInfo
import genHTML
import re
import time


def process(url):
    start = time.time()
    info = HTMLInfo.HTMLinfo(url)
    info.shop()
    info.get_goods()
    info.replace_goods()
    info.create_url()
    info.get_items()
    try:
        info.multi_process()  # multi threads (4)
    except Exception as ex:
        print(ex)

    genHTML.create_html(info.info_list)

    print("Done!")
    end = time.time()
    print("costs %0.2f seconds" % (end - start))


urlList = []


def get_info_from_url_link():
    with open("cfg/urlLink", "r") as f:
        for line in f.readlines():
            url = re.sub('\n', '', line)
            if re.search('http', url) and not re.search('^#', url):
                urlList.append(url)


if __name__ == '__main__':
    get_info_from_url_link()
    genHTML.clear_html()
    if urlList:
        for i in urlList:
            process(i)
