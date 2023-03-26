#!/usr/bin/env python
# encoding: utf-8
'''
#-------------------------------------------------------------------#
#                   CONFIDENTIAL --- CUSTOM STUDIOS                 #
#-------------------------------------------------------------------#
#                                                                   #
#                   @Project Name : juyi_data_xiapi                 #
#                                                                   #
#                   @File Name    : get_backups.py                      #
#                                                                   #
#                   @Programmer   : Adam                            #
#                                                                   #
#                   @Start Date   : 2023/1/12 15:45                 #
#                                                                   #
#                   @Last Update  : 2023/1/12 15:45                 #
#                                                                   #
#-------------------------------------------------------------------#
# Classes:                                                          #
#                                                                   #
#-------------------------------------------------------------------#
'''
#!/usr/bin/env python
# encoding: utf-8
'''
#-------------------------------------------------------------------#
#                   CONFIDENTIAL --- CUSTOM STUDIOS                 #
#-------------------------------------------------------------------#
#                                                                   #
#                   @Project Name : juyi_data_jingdong_keyword_to_good                 #
#                                                                   #
#                   @File Name    : get_backups.py                      #
#                                                                   #
#                   @Programmer   : Adam                            #
#                                                                   #
#                   @Start Date   : 2023/1/11 20:24                 #
#                                                                   #
#                   @Last Update  : 2023/1/11 20:24                 #
#                                                                   #
#-------------------------------------------------------------------#
# Classes:                                                          #
#                                                                   #
#-------------------------------------------------------------------#
'''

# -*- encoding: utf-8 -*-
# @Time   : 2023/1/10 16:55
# @Author : Vic
import json
from pprint import pprint
import requests


class GetStandbyCategory:
    """
    获取待爬取的分类列表
    """

    def __init__(self):
        self.index_url = "http://juyi.51xckj.com/api/product/category/condition"  # 未配置到settings，方便移植

    def get_standby_category(self, website_name: str):
        """
        获取服务器映射的站点分类
        @param website_name:JD,TB,TM,STATION_1688,PDD,ALI,YMS_USA,XP_SINGAPORE,XP_VIETNAM,XP_PHILIPPINES,XP_THAILAND,
        XP_MEXICO,XP_INDONESIA,XP_BRAZIL,XP_CHILE,XP_COLOMBIA,XP_MALAYSIA,XP_POLAND,XP_TW
        @return:
        """
        retry_num = 0

        data = {
                "platforms": [website_name]
            }
        try:
            res = requests.post(url=self.index_url, json=data, timeout=10)
            standyb_list = res.text
        except:
            print("后端请求出错, 请验证后再运行程序")
        # print(standyb_list)
        return json.loads(standyb_list)["data"]


if __name__ == '__main__':
    gs = GetStandbyCategory()
    excludes = []
    correct_category = []
    for i in """
    XP_SINGAPORE,XP_VIETNAM,XP_PHILIPPINES,XP_THAILAND,
        XP_MEXICO,XP_INDONESIA,XP_BRAZIL,XP_CHILE,XP_COLOMBIA,XP_MALAYSIA,XP_POLAND,XP_TW
    """.split(","):
        # if "PHILIPPIN" not in i:
        #     continue
        coroutine = gs.get_standby_category(website_name=i.strip())

        if coroutine !=[]:
            # pprint("分类 {} {} {}".format(i, coroutine, len(coroutine)))
            correct_category.append(i.strip())
        else:
            excludes.append(i.strip())
    print(correct_category)
    print(excludes)
