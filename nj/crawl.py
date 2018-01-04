import requests
import csv
import re
from lxml import etree
import time
import random
#获取页面
def getHtml(url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    hd = {"User-Agent": user_agent}
    print("get:"+url)
    try:
        r = requests.get(url,headers=hd,timeout=30)
        r.raise_for_status()
        r.encoding =r.apparent_encoding
        fillHtml(r.text)
    except:
        print("get:"+url+"  error")

#对抓取内容进行处理
def fillHtml(html):
    doc = etree.HTML(html)
    nodes_list = doc.xpath("/html/body/div[3]/div[1]/div[5]/div[2]/ul/li")
    for node in nodes_list[:-1]:

        if node.xpath("./div[3]/div[2]/b/text()"):
            price = node.xpath("./div[3]/div[2]/b/text()")[0]
        else:
            price = ""

        if node.xpath("./div[2]/h2/a/text()[1]"):
            title = node.xpath("./div[2]/h2/a/text()[1]")[0].strip()
        else:
            title = ""

        if node.xpath("./div[2]/p[2]/a[1]/text()[1]"):
            street = node.xpath("./div[2]/p[2]/a[1]/text()[1]")[0]
        else:
            street = ""

        if node.xpath("./div[2]/p[2]/a[2]/text()[1]"):
            community = node.xpath("./div[2]/p[2]/a[2]/text()[1]")[0]
        else:
            community = ""

        url = node.xpath("./div[1]/a/@href")[0]

        with open("rent.csv", "a",newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([title,street,community,price,url])

    may_page = doc.xpath('//*[@id="bottom_ad_li"]/div[2]')
    for page in may_page:
        # 若存在下一页，则爬取下一页
        if page.xpath('./a[@class="next"]/@href'):
            #限制爬虫下载速度
            time.sleep(random.randint(5,30))
            getHtml(page.xpath('./a[@class="next"]/@href')[0])
        else:
            print("end")


if __name__ == '__main__':
    start_url = "http://nj.58.com/chuzu/0/pn1/"
    getHtml(start_url)

