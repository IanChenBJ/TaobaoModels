

from scrapy import Spider
from selenium import webdriver
import time
from ..items import TaobaommItem
from scrapy.http import HtmlResponse
import os

class Taobaomm_Spider(Spider):
    name = 'taobaomm'
    allowed_domains = ['taobao.com']
    start_urls = [
        "https://www.taobao.com/market/mm/tnlmmt.php?spm=719.1001036.1998606013.1.kgZJ7r"
    ]

    def pages_parse(self):

        driver = webdriver.PhantomJS()
        driver.get(self.start_urls[0])
        #driver.implicitly_wait(30)
        #driver.maximize_window()
        pages = []
        while True:
            driver.execute_script('document.body.scrollTop=0')
            time.sleep(3)
            driver.execute_script('document.body.scrollTop=500')
            time.sleep(3)
            driver.execute_script('document.body.scrollTop=1000')
            time.sleep(3)
            driver.execute_script('document.body.scrollTop=1800')
            time.sleep(3)
            driver.execute_script('document.body.scrollTop=2200')
            time.sleep(3)
            driver.execute_script('document.body.scrollTop=3000')
            time.sleep(3)

            content = driver.page_source.encode('gbk', 'ignore')
            pages.append(content)
            try:
                next_page = driver.find_element_by_xpath('//a[text()="下一页"]').click()
            except:
                print('已经是最后一页，没有下一页！')
                driver.quit()
                return pages





    def parse(self, response):

        '''
            代码块1：

            以下代码依据预加载全部页面后，获得统一路径 src 的思路而写。

        '''

        #pages = self.pages_parse()
        #n = 1

        #for page in pages:

        #    print('这是第{num}页'.format(num=n))
        #    print('这是第{num}页'.format(num=n))
        #    print('这是第{num}页'.format(num=n))
        #    print('这是第{num}页'.format(num=n))
        #    print('这是第{num}页'.format(num=n))
        #    print('\n\n')

        #    os.chdir('c:\\users\\cy\\desktop')
        #    with open('page{num}.html'.format(num=n),'wb') as f:
        #        f.write(page)

        #    n = n + 1

        '''
            这是另一个网页（https://mm.taobao.com/guide/acquisition_list.htm?spm=719.100103615.0.0.w76Q0D&col_album_id=10000867805）
            的图片解析。

           os.chdir('c:\\users\\cy\\desktop')
           with open('new.html','wb') as f:
                f.write(content)
           print('Html 生成！')

           res = HtmlResponse(url=self.start_urls[0],encoding='gbk',body=page)
           block = res.xpath('//div[@id="J_MmWaterFall"]/div[contains(@class,"mm-p-w-cell")]')
           print('xpath路径生成！')
           for sel in block:
                print('生成Item！')
                item = TaobaommItem()
                imageLink = sel.xpath('./div[@class="mm-p-w-img"]/img/@src').extract()[0]
                item['image_url'] = 'https:' + imageLink
                yield item
       '''
        # 以第六页（最后一页）的 HTML 文件作为 body 生成HtmlResponse，进而使用xpath
        # 只有所有页面加载完毕，完整的html才能稳定下来，所需抓取的图片url才能统一定位为src，而不是一部分为lazyload
        #res = HtmlResponse(url=self.start_urls[0],encoding='gbk',body=pages[5])
        #block = res.xpath('//div[@class="bg-content"]/ul[contains(@class,"pro-list w1190 clearfix")]/li[@class="pro-item posr"]')
        #for sel in block:
        #    item = TaobaommItem()
        #    item['image_url'] = 'https:' + sel.xpath('./a/img/@src').extract()[0]

       #     try:
       #         item['name'] = sel.xpath('./a/div/h4/text()').extract()[0]
       #         item['desc'] = sel.xpath('./a/div/p/text()').extract()[0]
       #     except:
       #         item['name'] = '_'
       #         item['desc'] = '标签'

       #     yield item

       # --------------------------------------------------------------------------------------------------------------

        driver = webdriver.PhantomJS()
        driver.get(self.start_urls[0])
        time.sleep(3)
        page = driver.page_source.encode('gbk','ignore')
        driver.quit()
        res = HtmlResponse(url=self.start_urls[0],encoding='gbk',body=page)
        block = res.xpath('//div[@class="bg-content"]/ul[contains(@class,"pro-list w1190 clearfix")]/li[@class="pro-item posr"]')
        for sel in block:
            item = TaobaommItem()
            item['image_url'] = 'https:' + sel.xpath('./a/img/@data-ks-lazyload').extract()[0]

            try:
                item['name'] = sel.xpath('./a/div/h4/text()').extract()[0]
                item['desc'] = sel.xpath('./a/div/p/text()').extract()[0]
            except:
                item['name'] = ''
                item['desc'] = '标签'

            yield item







