#!/usr/bin/env python
# encoding: utf-8
'''
#-------------------------------------------------------------------#
#                   CONFIDENTIAL --- CUSTOM STUDIOS                 #
#-------------------------------------------------------------------#
#                                                                   #
#                   @Project Name : juyi_data_xiapi                 #
#                                                                   #
#                   @File Name    : change_ip_windows_timely.py                      #
#                                                                   #
#                   @Programmer   : Adam                            #
#                                                                   #
#                   @Start Date   : 2023/1/5 15:27                 #
#                                                                   #
#                   @Last Update  : 2023/1/5 15:27                 #
#                                                                   #
#-------------------------------------------------------------------#
# Classes:                                                          #
#                                                                   #
#-------------------------------------------------------------------#
'''
import re
import time

import requests
import requests

url = "http://39.98.162.234:5555/"

payload = {}
headers = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Accept-Language': 'zh-CN,zh;q=0.9',
  'Cache-Control': 'no-cache',
  'Connection': 'keep-alive',
  'Pragma': 'no-cache',
  'Referer': 'http://39.98.162.234:5555/',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}
try:
    target_ip = open('target_ip.txt','r',encoding="utf-8").read().strip()
except:
    open('target_ip.txt', 'w', encoding="utf-8")
    target_ip = open('target_ip.txt','r',encoding="utf-8").read().strip()

while True:
  time.sleep(0.5)
  print("heart beat!")
  try:
    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)
    ip = re.findall('ip_get:(.*?) ,end',response.text)[0] + ":8888"
    print("xiapi : ", ip)
    if ip != target_ip:
      target_ip = ip
      print("检测到更换ip,正在同步")
      with open('target_ip.txt','w',encoding="utf-8") as file:
        file.write(ip)


  except Exception as fi:
    print(fi)
    time.sleep(1)
    continue