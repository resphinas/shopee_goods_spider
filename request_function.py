#!/usr/bin/env python
# encoding: utf-8
'''
#-------------------------------------------------------------------#
#                   request function                                #
#-------------------------------------------------------------------#
#                                                                   #
#                   @Project Name : juyi_data_xiapi                 #
#                                                                   #
#                   @File Name    : request_function.py                      #
#                                                                   #
#                   @Programmer   : Adam                            #
#                                                                   #
#                   @Start Date   : 2023/1/4 13:46                 #
#                                                                   #
#                   @Last Update  : 2023/1/4 13:46                 #
#                                                                   #
#-------------------------------------------------------------------#
# Classes:                                                          #
#                                                                   #
#-------------------------------------------------------------------#
'''
# -*- coding : UTF-8 -*-
import json
import traceback
import socket
import ssl
import gzip
import time
import socks
import urllib.request
import re
import config


def socket_request_for_shopee_fit_all(api_url_,host, api):
    # print("##############",host,api)
    # print(re.findall('http://(.*?):',config.get_proxy())[0])

    while True:
        try:

            while True:
                try:
                    #代理版本
                    # print(config.get_proxy())
                    origin_ip = config.get_proxy()
                    # ip = re.findall('http://(.*?):',/ origin_ip)[0]
                    # port = origin_ip.split(":")[-1]
                    #
                    # print(ip, port, host)
                    # socks.setdefaultproxy(socks.SOCKS5, ip, int(port))
                    # # socks.set_default_proxy(socks.HTTP, addr=ip, port=80)  # 设置socks代理
                    # socket.socket = socks.socksocket
                    # # # socket.setdefaulttimeout(7)
                    # #
                    # sock = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
                    # #单元测试站点 连通性
                    # host = 'sg'
                    # sock.connect((host, 443))

                    #非代理版本
                    socket.setdefaulttimeout(999999)
                    sock = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), ciphers='DEFAULT@SECLEVEL=2')
                    sock.connect((host, 443))
                    break
                except Exception as file:
                    # time.sleep(0.5)、
                    traceback.print_exc()
                    print(file)
                    print("socket 连接失败，可能是代理ip暂时性失效或者永久失效")
                    time.sleep(1)
                    try:
                        sock.shutdown(2)
                        sock.close()
                    except:
                        pass

                    # continue


                    # print(file)
                    # time.sleep(1)
            s = config.socket_headers.format(api, host, host, config.get_AC_CERT_D())

            print(s)
            # input("dddddddddd")
            s = s.strip().split('\n')
            for i in s:
                sock.send((str(i)+str('\r\n')).encode())
            sock.send('Connection: close\r\n\r\n'.encode())
            buffer = []
        # while True:
            try:

                while True:
                    d = sock.recv(1024)
                    if d:
                        buffer.append(d)
                    else:
                        break

            except Exception as file:
                # time.sleep(0.5)
                traceback.print_exc()
                print(file, "track: request_function_94")
                try:
                    sock.shutdown(2)
                    sock.close()
                except:
                    pass
                # print(file)
                continue
            res = []
            data = b''.join(buffer)
            try:
                need = data.decode('utf-8')
            except:
                return False
            if "90309999" in need:
                if "crawler_item" in need:
                    spider_attack = "crawler_item"
                else:
                    spider_attack = "just 90309999"
                print(need)
                print("被检测到轨迹 -> , 当前ip为 {} ,回传为{}, 建议更换cookie参数".format(15, spider_attack))
                tracking_id = re.findall('"tracking_id":"(.*?)"', need)[0]
                print("验证码回传api 为　https://shopee.sg/verify/captcha?anti_bot_tracking_id={}&app_key=Search.PC&client_id=1&next=https%3A%2F%2Fshopee.sg%2Fverify%2Ftraffic&redirect_type=2&scene=crawler_item&should_replace_history=true".format(tracking_id))
                print(need)
                time.sleep(10)
                # input("checking ")
                continue
                # print(need.strip())
                # print(response)
                return False
            break
        except Exception as file:

            if "由于连接方在一段时间后没有正确答复或连接的主机没有" not in str(file):
                print(file)
            print(file, "track: request_function_118")
            print("上一级 url : {}".format(api_url_))
            try:
                sock.shutdown(2)
                sock.close()
            except:
                pass
            exstr = traceback.format_exc()
            print(exstr)
            time.sleep(1)
            continue

    # print(need)
    # input("check")
    origin = need
    need = need.split('\n')
    for i in need:
        if len(i.strip()) > 1000 or '":' in i:
            # print(i)
            # input("next")
            res.append(i)
    # print(res)
    # input("check res")
    res= "".join(res)
    need = res.split('strict-origin-when-cross-origin')[-1]
    # if '{"bff_meta"' in res:
    #     need = '{"bff_meta"' + res.split('{"bff_meta"')[-1]
    # else:
    #     if '{"error":null,' in res:
    #         print("yes")
    #         input("yes")
    #         need = '{"error":null,' + res.split('{"error": null,')[-1]
    # print(need[-1000:10000])
    # print(need)
    # input("checkl ")
    need = need.replace("\n","").replace("\r","").replace("\t","")
    # with open('buffer.txt', "w", encoding="utf-8") as file:
    #     file.write(need)
    # print(origin)
    # input()
    try:
        need = json.loads(need)
    except Exception as file:
        if '{"error":4,"error_msg":"","data":null,"is_indexable":true}' not in str(file):

            # print(api)
            # print("qqqqqqqqqqqqqq",need)
            # input("check")
            # print("need")
            # print(config.socket_headers.format(api, host, host))
            print("locate in line 184: sorcket_connet in request_function error -> ", host, api)

        # input("check 1889189")
    # input("check")
    #
    # if "images" in str(need):
    #     print("yes")
    # else:
    #     print("false")
    # print(need)
    sock.shutdown(2)
    sock.close()
    return need
# socket_request_for_shopee_fit_all('shopee.sg', "/api/v4/search/search_items?by=sales&keyword=phone&limit=60&newest=60&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2")
# socket_request_for_shopee_fit_all("shopee.sg","/api/v4/item/get?itemid=10086103476&shopid=497222599")
# for i in range(10000):
#     print(i)
#     socket_request_for_shopee_fit_all("afawf", 'shopee.tw', "/api/v4/search/search_items?by=sales&limit=60&match_id=11040840&newest=0")
#     input("next")