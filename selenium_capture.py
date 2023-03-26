#!/usr/bin/env python
# encoding: utf-8
'''
#-------------------------------------------------------------------#
#                   CONFIDENTIAL --- CUSTOM STUDIOS                 #
#-------------------------------------------------------------------#
#                                                                   #
#                   @Project Name : juyi_data_xiapi                 #
#                                                                   #
#                   @File Name    : selenium_capture.py                      #
#                                                                   #
#                   @Programmer   : Adam                            #
#                                                                   #
#                   @Start Date   : 2023/1/6 11:27                 #
#                                                                   #
#                   @Last Update  : 2023/1/6 11:27                 #
#                                                                   #
#-------------------------------------------------------------------#
# Classes:                                                          #
#                                                                   #
#-------------------------------------------------------------------#
'''


# coding = utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import time




# 打开chrome浏览器
class CaptchaProcess():
    def __init__(self, tracking_id,  ):
        self.captcha_api = "https://shopee.sg/verify/captcha?anti_bot_tracking_id={}&app_key=Search.PC&client_id=1&next=https%3A%2F%2Fshopee.sg%2Fverify%2Ftraffic&redirect_type=2&scene=crawler_item&should_replace_history=true".format(tracking_id)
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.huakuai = None
        self.tracks = None

    def open_page(self):
        # 打开shopee 验证码界面
        self.driver.get(self.captcha_api)


    def get_snap(self):  # 对目标网页进行截屏。这里截的是全屏
        self.driver.save_screenshot('full_snap.png')
        page_snap_obj = Image.open('full_snap.png')
        return page_snap_obj


    def get_image(self):  # 对验证码所在位置进行定位，然后截取验证码图片
        img = self.driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div/div/div/div/div[2]/div[1]/div[1]/img')
        time.sleep(2)
        location = img.location
        print(location)
        size = img.size
        left = location['x']
        top = location['y']
        right = left + size['width']
        bottom = top + size['height']

        page_snap_obj = self.get_snap()
        image_obj = page_snap_obj.crop((left, top, right, bottom))
        # image_obj.show()
        image_obj = image_obj.convert("RGB")
        image_obj.save("need_picture.jpg")
        return image_obj  # 得到的就是验证码

    def get_track(self, distance):  # distance为传入的总距离
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.8
        # 初速度
        v = 20

        while current < distance:
            if current < mid:
                # 加速度为2
                a = 8
            else:
                # 加速度为-2
                a = -1.5
            v0 = v
            # 当前速度
            v = v0 + a * t
            # 移动距离
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    def move_to_gap(self, distance):  # slider是要移动的滑块,tracks是要传入的移动轨迹
        self.tracks = self.get_track(distance)
        self.huakuai = self.driver.find_element_by_class_name("G3AxnX")
        ActionChains(self.driver).click_and_hold(self.huakuai).perform()
        for x in self.tracks:
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.driver).release().perform()

    def get_cookies(self):
        time.sleep(4)
        cookies = self.driver.get_cookies()
        exist_flag = False
        for i in cookies:

            if "AC_CERT_D" == i['name']:
                with open("ac_cert_d.txt", "w", encoding="utf-8") as file:
                    file.write(cookies['AC_CERT_D'])
                    print("cookie值已更新,当前最新值为 {}".format(i['value']))
        if not exist_flag:
            print("未获取到需要的参数如下",cookies)
#!/usr/bin/env python
# coding:utf-8

import requests
from hashlib import md5

class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password =  password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }


    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def PostPic_base64(self, base64_str, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
            'file_base64':base64_str
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


if __name__ == '__main__':
    captcha = CaptchaProcess("bad76a0c-eca7-412b-97ea-35c4c2d6d6d9")
    captcha.open_page()

    while True:
        captcha.driver.refresh()
        captcha.open_page()
        captcha.get_snap()
        captcha.get_image()
        chaojiying = Chaojiying_Client('resphina', 'a4754604072', '9101')	#用户中心>>软件ID 生成一个替换 9101
        im = open('need_picture.jpg', 'rb').read()													#本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
        res = chaojiying.PostPic(im, 9101)	#1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()
        pic_str = res['pic_str']
        print(res)
        x = int(pic_str.split(",")[0])
        captcha.move_to_gap(x)
        captcha.get_cookies()
        #print chaojiying.PostPic(base64_str, 1902)  #此处为传入 base64代码
        input("next")










