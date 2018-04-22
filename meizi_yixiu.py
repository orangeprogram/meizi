# -*- coding: utf-8 -*-

import requests 
from lxml import html 
import os 
import time 
from multiprocessing import Queue,Process
from Queue import Empty as QueueEmpty


def header():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'Hm_lvt_a521ae282c3c2742707c26ac9d3a8c59=1524118747; Hm_lpvt_a521ae282c3c2742707c26ac9d3a8c59=1524119034',
        'Host': 'www.tu11.com',
        'If-Modified-Since': 'Wed, 18 Apr 2018 15:22:41 GMT',
        'If-None-Match': "80f6641729d7d31:3b5",
        # 'Referer': 'http://www.tu11.com/neihantupian/list_40_2.html',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    }
    return headers


# 获取主页列表
def getPage():
    urls = []
    for i in range(1,4):
        baseUrl = 'http://www.tu11.com/neihantupian/list_40_{}.html'.format(i)
        selector = html.fromstring(requests.get(baseUrl).content)
        for i in selector.xpath('//ul[@id="masonryList"]/li/div/a/@href'):
            urls.append(i)
        time.sleep(3)
    return urls


# 图片链接列表， 标题
# url是详情页链接
def getPiclink(url,queue):

    # 接下来的链接放到这个列表
    jpgList = []
    for i in url:
        sel = html.fromstring(requests.get('http://www.tu11.com' + i,).content)
          # 图片地址在src标签中
        jpg = sel.xpath('//div[@class="nry"]/p/img/@src')
        # 图片链接放进列表
        for i in jpg:
            queue.put(i)
        time.sleep(5)
    return jpgList





# 下载图片
def downloadPic(queue):
    k = 1
    # 图片数量
    # count = len(piclist)
    dirName = os.path.abspath('.') + 'yixiu'
    # 新建文件夹
    if not os.path.exists(dirName):
        os.mkdir(dirName)
    while True:
        try:
            value = queue.get(True, 10)
            # for i in piclist:
            # 文件写入的名称：当前路径／文件夹／文件名
            filename = '%s/%s.jpg' % (dirName, k)
            print u'开始下载图片:%s 第%s张' % (dirName, k)
            with open(filename, "wb") as jpg:
                jpg.write(requests.get(value).content)
                time.sleep(0.5)
            k += 1
        except  QueueEmpty:
            break




if __name__ == '__main__': 
    urls = getPage()
    queue = Queue()
    getter_process = Process(target=getPiclink, args=(urls, queue))
    putter_process = Process(target=downloadPic, args=(queue,))
    putter_process.start()
    getter_process.start()