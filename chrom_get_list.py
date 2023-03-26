"""
author: wes
create time: 2022 10.27
last chage: 2022 11.15
selenium 必须用3.14.0
"""


import datetime



from external_api import send_to_monitor
import time
import json
import requests
import re
import urllib.parse
import csv
from jsonsearch import JsonSearch
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import DesiredCapabilities
from tools.save_tool import save_products_to_json
from selenium.webdriver.chrome.options import Options
from threading import Thread
from tools import save_tool


PRODUCTS_PATH = 'data/products/{}/'


def get_log_async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper

def create_driver(
        show: bool =False
) :
    """
    创建浏览器驱动
    :param show: 是否弹出浏览器页面
    :return: 浏览器驱动
    """
    chrome_options = Options()
    chrome_options.add_argument("--no-sanbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    #chrome_options.add_argument('blink-settings=imagesEnabled=false')
    chrome_options.add_experimental_option('w3c', False)
    # chrome_options.add_argument('--disk-cache-dir=cache')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--verbose')
    chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--proxy-server=http://127.0.0.1:8888')

    chrome_options.page_load_strategy = 'none'
    prefs = {
        'profile.default_content_setting_values':
            {
                'notifications': 2
            },
        'profile.password_manager_enabled': False,
        'credentials_enable_service': False
    }
    chrome_options.add_experimental_option('prefs', prefs)
    #chrome_options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    chrome_options.binary_location = "/usr/bin/google-chrome"
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTph, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
    chrome_options.add_argument('user-agent=%s'%ua)
    if not show:
        chrome_options.add_argument("--headless")

    # 开发者模式防止被识别出
    # 网址：https://blog.csdn.net/dslkfajoaijfdoj/article/details/109146051
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option('w3c', False)
    caps = {

        'browserName': 'chrome',
        'loggingPrefs': {
            'browser': 'ALL',
            'driver': 'ALL',
            'performance': 'ALL',
        },
        'goog:chromeOptions': {
            'perfLoggingPrefs': {
                'enableNetwork': True,
            },
            'w3c': False,
        },
    }
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # newer: goog:loggingPrefs
    driver = webdriver.Chrome(desired_capabilities= caps,chrome_options=chrome_options)

    # # 执行cdp命令
    # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    #     "source": """
    #                             Object.defineProperty(navigator, 'webdriver', {
    #                               get: () => undefined
    #                             })
    #                           """
    # })

    return driver


def get_web_element_from_dict_if_it_is(element_to_check_for_dict):
    if type(element_to_check_for_dict) is dict:
        first_element_value = list(element_to_check_for_dict.values())[0]
        element_to_check_for_dict = driver.create_web_element(element_id=first_element_value)
    return element_to_check_for_dict



def get_web_element_from_dict_if_it_is(element_to_check_for_dict):
    if type(element_to_check_for_dict) is dict:
        first_element_value = list(element_to_check_for_dict.values())[0]
        element_to_check_for_dict = driver.create_web_element(element_id=first_element_value)
    return element_to_check_for_dict

def spider(driver,sig_index, le,m_id,m_name,m_url):
        global total
        while True:
            try:
                driver.get(m_url)
                break
            except Exception as file:
                time.sleep(1.5)
                print(file,"出现错误 需要排查 显示等待调用错误")
                return
        # input("check")
        # print('check')
        # error_count = time.time()
        for i in range(50):
            # print(driver.page_source)
            # if 'No results found' in driver.page_source
            temp_time = int(time.time())
            while True:
                try:
                    #实时时间
                    time_ = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

                    if int(time.time()-temp_time) >20:
                        save_tool.save_wrong_shop(time_ +': '+ m_url)
                        return


                    info = "(菲律宾) 爬取商品列表页中,当前所有三级类目进度为{}/{}: +".format(sig_index+1,le)+ '['+"▓" * int(((sig_index/le*100)// 4)) + "-" * int((((le-sig_index)/le*100)// 2)) +']'  + ",页面进度为{}/50,当前爬取商品总数为{},最后心跳时间为{} 当前爬取链接为{},{}".format(i,total,time_,m_url,str(i))

                    logs_raw = driver.get_log("performance")
                    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
                    #传入anti混淆参数 无效 备用
                    # # 过滤log日志 拿到api分发 请求给flask需要的tiem request json
                    #
                    # for iq in logs:
                    #     if iq['method'] == 'Network.requestWillBeSent' and 'items' in str(iq):
                    #
                    #         pprint.pprint(iq)
                    #         url = iq['params']['request']['url']
                    #         headers = iq['params']['request']['headers']
                    #         package ={'url': url,'headers':headers}
                    #         print("prepare the json for  flask api: \n\t\t",package)
                    #         ret = post('http://localhost:50055/analyze/', json=package)
                    #         print(ret.text)
                    #         print()
                    #         print("\n\n\n")
                    # input("cjceokcop")
                    # input()


                    def log_filter(log_):
                        return (
                            # is an actual response
                                log_["method"] == "Network.responseReceived"
                                # and json
                                and "application/json" in log_["params"]["response"]["mimeType"] and 'items' in log_["params"]["response"]["url"]
                        )
                    session_infor = None
                    #过滤log日志 拿到需要的tiem
                    for log in filter(log_filter, logs):
                        request_id = log["params"]["requestId"]
                        resp_url = log["params"]["response"]["url"]
                        print(f"Caught {resp_url}")
                        session_infor = driver.execute("executeCdpCommand",
                                                       {'cmd': 'Network.getResponseBody',
                                                        'params': {'requestId': request_id}})[
                            'value']
                        # print(session_infor)


                    category_path = PRODUCTS_PATH.format(m_name)

                    # print(driver.page_source)
                    # print(a)
                    # print(session_infor,"Fawfawfwf")
                    if len(session_infor) > 10:
                        save_products_to_json(category_path, m_id, m_name, session_infor['body'])
                    total += 50

                    break
                except Exception as file:
                    # print(file,'dddddddd')
                    send_to_monitor.send_api('shopee_ph',info + "   非致命警告: {}".format(str(file)))

                    time.sleep(1)
                    # input()

            # 转发日志到监控端
            send_to_monitor.send_api('shopee_ph', info)
            while True:
                try:
                    btn1 = driver.find_element(By.CSS_SELECTOR,'#main > div > div:nth-child(3) > div > div > div.container.Xnlvof > div.SoEFNz > div > div.m76OK- > div > button.shopee-icon-button.shopee-icon-button--right')
                    driver.execute_script("arguments[0].click();", btn1)
                    # btn1.click()
                    break
                except:
                    pass

    # return page_items



def main():
    global driver,total
    #读取分类文件
    with open("spider_categories.json", 'r', encoding="utf-8") as file:
        true = True
        false = False
        null = None
        content = eval(file.read())
    #resume_flag = input("继续爬取还是开始全新爬取(1.继续 2.全新): ").strip()
    resume_flag = '1'
    #读取存档点, 获取上一次的 页数和total商品量 继续爬取

    checkpoint = save_tool.get_shops_checkpoint() if resume_flag.strip() == '1' else (0,0)
    print(checkpoint)
    begin_point= checkpoint[0]
    total = checkpoint[1]
    # print(content)
    driver = create_driver()
    driver.set_window_size(1800,1800)
    driver.maximize_window()
    print(begin_point,len(content))
    # input("check")
    # total = 3142200
    for sig_index  in range(begin_point,len(content)):
        single = content[sig_index]
        s_id = single['s_category_id']
        s_name = single['s_category_name']

        s_url = "https://ph.xiapibuy.com/e-cat.{}".format(s_id[1:])+ '?page=0&sortBy=sales'
        print("当前id为: {},链接为: {}".format(s_id, s_url))
        spider(driver,sig_index,len(content[1:]), s_id,s_name, s_url)
        save_tool.save_shops_checkpoint(sig_index,total)
        # first = 0
        # save_products_to_json(products_root= PRODUCTS_PATH , m_uid= m_id, data= page_items)
        # input()

if __name__ == '__main__':
    main()
