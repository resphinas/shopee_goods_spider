#!/usr/bin/env python
# encoding: utf-8
'''
#-------------------------------------------------------------------#
#                   CONFIDENTIAL --- CUSTOM STUDIOS                 #
#-------------------------------------------------------------------#
#                                                                   #
#                   @Project Name : juyi_data_xiapi                 #
#                                                                   #
#                   @File Name    : normal_function.py                      #
#                                                                   #
#                   @Programmer   : Adam                            #
#                                                                   #
#                   @Start Date   : 2023/1/12 15:41                 #
#                                                                   #
#                   @Last Update  : 2023/1/12 15:41                 #
#                                                                   #
#-------------------------------------------------------------------#
# Classes:                                                          #
#                                                                   #
#-------------------------------------------------------------------#
'''
import json
import time
import multiprocessing
import config
from tools import save_tool
from get_backups import GetStandbyCategory

def get_categories(spider_type, host):
    # print("当前采集模式为 {},站点为 {}".format(spider_type, host))
    try:
        with open("category_info/shopee_categories_{}.json".format(host), "r", encoding="utf-8") as file:
            true = True
            false = False
            null = None
            categories_origin = eval(file.read())
    except:
        with open("../category_info/shopee_categories_{}.json".format(host), "r", encoding="utf-8") as file:
            true = True
            false = False
            null = None
            categories_origin = eval(file.read())
    # input("number of cats: {}".format(len(categories_origin)))
    if spider_type == 1:
        need_categories = categories_origin

    elif spider_type == 2:
        # 制造单元测试 一级类目数据列表
        # 后端接口获取任务
        gs = GetStandbyCategory()
        website_name = config.local_backups[host]
        print("    抽取 来源平台为 {}".format(website_name))
        coroutine = gs.get_standby_category(website_name)

        # print(coroutine)
        # print(coroutine, type(coroutine))
        # 单机无后端测试用
        # fake_need_cats = ["家用电器"]
        # gs = GetStandbyCategory()
        # coroutine = gs.get_standby_category(website_name="JD")

        need_categories = []
        for check_cat in coroutine:
            #暂时没有写其他的逻辑
            if "Others" in check_cat:
                continue
            check_cat = check_cat.strip()
            # print(check_cat)
            #循环原始  提供的分类进行需要的匹配
            for category in categories_origin:
                # print(category)
                # input("")
                if category["b_category_name"] == check_cat or category["m_category_name"] == check_cat or category["s_category_name"] == check_cat:
                        if category not in need_categories:
                            need_categories.append(category)
        # print(need_categories, len(need_categories), len(categories_origin))
        get_string_type_di = {"1": {"string":"本地实际任务数量", "value": len(need_categories)}, "2": {"string":"动态接口数量","value": len(need_categories)}}
        print("""
    ========================================================================================
                分类获取完毕 原始本地分类数量: {}  {}: {}, 
    ========================================================================================
                 """.format(len(categories_origin), get_string_type_di[str(config.spider_type)]["string"], get_string_type_di[str(config.spider_type)]["value"]))

    elif type(spider_type) != "int":
        print("spider_type 类型错误 请验证config中参数")
        exit()
    return need_categories

# get_categories(2, config.single_host.split(".")[-1])

def get_source(total,checkpoint_flag, platform):
    # global driver,total,bars,main_time
    print("""
    ========================================================================================
                读取分类文件中 读取文件为 {}
    ========================================================================================
             """.format("category_info/shopee_categories_{}.json".format(platform)))
    content = get_categories(config.spider_type, platform)
    # with open("category_info/shopee_categories_{}.json".format(platform), 'r', encoding="utf-8") as file:
    #     false = False
    #     true = True
    #     null = None
    #     content = eval(file.read())


    #设置协成锁
    mutex = multiprocessing.Lock()
    resume_flag = "2"

    #定义程序初始时间
    #读取存档点, 获取上一次的 页数和total商品量 继续爬取

    if checkpoint_flag:

        checkpoint = save_tool.get_shops_checkpoint(platform)
        begin_point= checkpoint[0]

        print("""
    ========================================================================================
                启用进度存档 当前进度为 {}/{} 进度读取站点为 {}
    ========================================================================================
             """.format(begin_point,len(content),platform))
    else:
        begin_point= 0
        print("""
    ========================================================================================
                未启用进度存档
    ========================================================================================
        """)
    time.sleep(2)
    # total = 3142200
    #创建数量为线程量的进度监控对象
    process_distribute_li_ = []
    #进程分割处理
    divid =int((len(content)-begin_point)/ config.process_num)
    time.sleep(2)



    time.sleep(1)
    #分割完后的节点
    divid_stop = [i*divid for i in range(config.process_num+1)][1:]

    li_single = []
    sig_g = 0
    # print("begin: {}, all: {}".format(begin_point, len(content)))
    # input("check the process")
    #进行线程任务和进程任务的分配
    for sig_index  in range(begin_point,len(content)):
        process_need_index = sig_index
        single = content[sig_index]
        s_id = single['s_category_id']
        s_name = single['s_category_name']
        b_name = single['b_category_name']
        # if "Others" in s_name:
        #     print(b_name, s_name)
        #     continue
        s_url = "{}g-cat.{}".format(config.need_host,s_id[1:])+ '?page=0&sortBy=relevancy' #sales
        # print("当前id为: {},链接为: {}".format(s_id, s_url))
        # sig_index = sig_index% config.thread_num

        # sig_index == sig_index%(config.thread_num)
        li_single.append((None,
                          {"total":total,"sig_index": sig_g, "sig_total_index": process_need_index,"le": len(content[1:]), "m_id": s_id, "m_name": s_name, "m_url": s_url, "mutex":mutex}))

        sig_g +=1
        if sig_g == config.thread_num:
            sig_g = 0
        #进程任务调度
        if process_need_index+1  in divid_stop:
            process_distribute_li_.append(li_single)
            del li_single
            li_single = []

            # print(len(li_single))
    # for i in process_distribute_li_:
    #     print(len(i))
    # print(len(process_distribute_li_), len(process_distribute_li_[0]))
    # input("checking")
    return process_distribute_li_,0
# get_categories(2, "cl")