import requests
import csv
import re
from lxml import etree
import time

def getHtml(url):
    print("get:"+url)
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding =r.apparent_encoding
        fillHtml(r.text)
    except:
        return ""
    return url

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
        if page.xpath('./a[@class="next"]/@href'):
            #time.sleep(2)
            getHtml(page.xpath('./a[@class="next"]/@href')[0])
        else:
            print("end")



if __name__ == '__main__':
    start_url = "http://nj.58.com/chuzu/0/pn1/"
    getHtml(start_url)

