# -*- coding: utf-8 -*-



import os
import requests
from lxml import etree
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs",prefs)
chrome_options.add_argument("--headless")
chrome_path = '/home/ghost/Downloads/chromedriver'

# 设置图片存储路径
PICTURES_PATH = os.path.join(os.getcwd(),'pictures/')

# 设置headers
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Referer': "http://www.mmjpg.com"
}

class Spider(object):
    def __init__(self,page_num):
        self.page_num = page_num
        self.page_urls = ["http://www.mmjpg.com"]
        self.girl_urls = []
        self.girl_name = ''
        self.pic_urls = []

    # 获取页面url方法
    def get_page_urls(self):
        if int(self.page_num) > 1:
            for n in range(2,int(self.page_num)+1):
                page_url = "http://www.mmjpg.com/home/" + str(n)
                self.page_urls.append(page_url)
        elif int(self.page_num) == 1:
            pass
    
    def get_girl_urls(self):
        for page_url in self.page_urls:
            html = requests.get(page_url).content
            selector = etree.HTML(html)
            self.girl_urls += (selector.xpath('//span[@class="title"]/a/@href'))

    def get_pic_urls(self):
        driver = webdriver.Chrome(chrome_path, chrome_options=chrome_options)
        print(self.girl_urls)
        for girl_url in self.girl_urls:
            driver.get(girl_url)
            time.sleep(3)
            # page = driver.find_element_by_partial_link_text(u'全部图片')
            # driver.execute_script("arguments[0].scrollIntoView(false);", page)
            # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, u'全部图片'))).click()
            driver.execute_script("window.scrollBy(0,1300)")
            
            driver.find_element_by_xpath('//em[@class="ch all"]').click()
            time.sleep(2)
            html = driver.page_source
            selector = etree.HTML(html)
            self.girl_name = selector.xpath('//div[@class="article"]/h2/text()')[0]
            self.pic_urls = selector.xpath('//div[@id="content"]/img/@data-img')
            try:
                self.download_pic()
            except Exception as e:
                pass


    def download_pic(self):
        try:
            os.mkdir(PICTURES_PATH)
        except:
            pass
        girl_path = PICTURES_PATH + self.girl_name
        try:
            os.mkdir(girl_path)
        except Exception as e:
            pass
        img_name = 0
        for pic_url in self.pic_urls:
            img_name += 1
            img_data = requests.get(pic_url, headers=headers)
            pic_path = girl_path + '/'+ str(img_name) + '.jpg'
            if os.path.isfile(pic_path):
                pass
            else:
                with open(pic_path, 'wb') as f:
                    f.write(img_data.content)
                    f.close()
        return


    def start(self):
        self.get_page_urls()
        self.get_girl_urls()
        self.get_pic_urls()


if __name__ == '__main__':
    page_num = input("webpage:")
    mmjpg_spider = Spider(page_num)
    mmjpg_spider = Spider(page_num)
    mmjpg_spider.start()