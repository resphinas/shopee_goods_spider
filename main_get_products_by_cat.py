"""
author: wes
create time: 2022 10.27
last chage: 2022 12/8
history version:
  1 -> please ignore this version! selenium auto  2022 11 destroy in 2022 12 due to the error and eficiency (the reference code is chrom_get_list.py)
  2 -> pure code requests 2022 12.02 - 2022 12.08
    a.iterate update until now
    b.coming cross the capture due to High frequency requests
        there are some solutions:
            b.1: Docked with the Super Hawk coding platform, but found that his return value seemed to be a bit correct (the code is )
            b.2: Write your own image recognition code (I think the most efficient scheme is difficult)
            b.3: Use the company's employees to build a coding platform for verification code printing

  description : support all platforms by set the config.py or use the super arguments to implent it
  more info please see the readme.file of the root

  capture_api(when blocked by the server pleease update the the param ac_cer_d of cookies) :
            api(change the anti_bot_tracking_id from the error our codes report)
                https://shopee.sg/verify/traffic?anti_bot_tracking_id=51f75c5a-37c3-4eef-86aa-69fb8387b30a&app_key=Search.PC&client_id=&is_initial=true&next=https%3A%2F%2Fshopee.sg%2Fsearch%3Fkeyword%3Dphone&redirect_type=2&scene=crawler_item&should_replace_history=true
作者：wes

创建时间：2022年10月27日

上次更改：2023年01月13日

历史版本：

    1->请忽略此版本！由于错误和效率，selenium auto 2022 11在2022 12年销毁（参考代码为chrom_get_list.py）

    2->纯代码请求2022 12.02-2022 12.08

        a、 迭代更新到现在

        b、 由于高频请求而被ip反扒捕获

            有一些解决方案：

            b、 1：与超级鹰编码平台对接，但发现他的返回值似乎有点不正确，并且由于验证码刷新频繁，返回值时间太久。（就没必要考虑了）

            b、 2：编写自己的图像识别代码（我认为最有效的方案，不过有一定难度）

            b、 3：利用公司员工构建验证码打码的平台(出错率为0的方案 )



    description:通过设置config.py或使用超级参数来实现它，支持所有平台

    更多信息请参阅根目录的readme文件



    capture_api（当被服务器阻止时，请更新cookie的参数ac_cer_d）：

        api（从错误代码报告中更改anti_bot_tracking_id）
                https://shopee.sg/verify/traffic?anti_bot_tracking_id=51f75c5a-37c3-4eef-86aa-69fb8387b30a&app_key=Search.PC&client_id=&is_initial=true&next=https%3A%2F%2Fshopee.sg%2Fsearch%3Fkeyword%3Dphone&redirect_type=2&scene=crawler_item&should_replace_history=true

"""
import re
import argparse
import multiprocessing
import config
import traceback
import datetime
from external_api import send_to_monitor
from rich.progress import Progress
from request_function import socket_request_for_shopee_fit_all
from get_single_product import shopee_item_info_test
from tools import save_tool
import threadpool
import time
from tools.normal_function import (
    get_source
)

# 定义存储文件的目录
PRODUCTS_PATH = 'data/polymerization_products/products_{}/'


def shopee_Test(id, m_name, newest):
    """
    获取单页数所有商品基础信息
    :param id: 分类id
    :param m_name: 分类名
    :param newest: 请求新页数的偏差
    :return: itemids 单页数的所有商品item 和 店铺id shopids
    """
    # 处理 关键词 让空格全部变成 +
    m_name = m_name.replace(" ", "+")
    # 实际运行api
    api_url = "/api/v4/search/search_items?by=sales&limit=60&match_id={}&limit=60&newest={}".format(id, newest)
    host_url = config.need_host
    # 报错容忍次数初始值
    tmp_num = 0
    while True:
        tolerate_num = 3
        try:
            res = socket_request_for_shopee_fit_all(api_url, config.single_host, api_url)
            itemids = []
            shopids = []
            # 页数没东西时进行错误回传
            try:
                if len(res['items']) == 0:
                    print(res)
                    print("locate in main: 68")
                    return "limited"
            except Exception as file:
                print(res)
                traceback.print_exc()
                print("locate in main: 73")
                return "limited"
            break
        except Exception as file:
            # 超出容忍值再报错
            if tmp_num > tolerate_num:
                print(" socket error locate in main: 73")
                print(file)

            tmp_num += 1
            time.sleep(2)
    # 添加单页的商品id  店铺id 到列表中
    for single in res['items']:
        itemids.append(single['itemid'])
        shopids.append(single['shopid'])

    return itemids, shopids


def single_product(max_page, total, sig_index, sig_total_index, le, m_id, m_name, m_url, page_index, mutex):
    """
    单个商品的详细数据获取
    :param max_page:最大页数
    :param total:当前总数
    :param sig_index: 线程id 为线程数的余数
    :param sig_total_index:  线程总任务进度
    :param le: 线程总任务数
    :param m_id: 商品id
    :param m_name: 商品名称
    :param m_url: 商品url
    :param page_index: 当前页数索引
    :param mutex: 线程锁 暂时用不上
    :return: 返回单分类单页所有商品信息字典
    """
    global main_time, bars

    i = page_index
    # 因为url的固定设置 需要把 空格改成 '+' 字符
    try:
        m_name = "+".join(m_name.split(" "))
    except:
        pass

    api_url_ = "/api/v4/search/search_items?by=sales&limit=60&match_id={}&limit=60&newest={}".format(str(m_id)[1:],
                                                                                                     i * 60)

    while True:
        # 获取单页商品信息
        # 单页商品基础信息(商品id 店铺id)的回传
        callbacks = shopee_Test(str(m_id)[1:], m_name, i * 60)
        # 三种不同的回传 分别是 ip问题  页数限制问题(可能为其他隐性问题) 和正常回传
        if not callbacks:
            progress.update(bars[sig_index], advance=1,
                            description="[red]{} [white] nothing here [red] id->{}：{}/{} ,cat->{},id->{} ".format(
                                config.single_host, sig_index, sig_total_index, le, m_name, m_id))

            print("ip invalid, please swap!")
            continue

        elif callbacks == "limited":
            print("api: {},id: {} more pages limited, in page {}".format(api_url_, sig_index, i))
            progress.update(bars[sig_index], advance=1,
                            description="[red]{} [white] limited [red] id->{}：{}/{} ,cat->{},id->{}".format(
                                config.single_host, sig_index, sig_total_index, le, m_name, m_id))
            return "limited"

        else:
            itemids, shopids = callbacks[0], callbacks[1]
            progress.update(bars[sig_index], advance=1,
                            description="[red]{} [white] nothing here [red] id->{}：{}/{} ,cat->{},id->{} ".format(
                                config.single_host, sig_index, sig_total_index, le, m_name, m_id))

            break
    single_page_products = []

    # 如果爬取页数商品的回传不为none   则遍历单页所有商品单个信息
    if callbacks != None:
        for index in range(len(itemids)):
            # 單頁截斷進行小量測試
            # if index == 2:
            #     break
            # if index == 0:#
            temp_bar_time = time.time()

            time_ = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            # 进行时间的运算 提取出 当前总运行时间的小时 分钟 秒数
            all_time = int(temp_bar_time - main_time)
            h = int(all_time / 3600)
            m = int((int(all_time) % 3600) / 60)
            s = int(int(all_time) % 60)

            # 分钟数未满一时 速度为当前采集总量每分钟 满一时则为 每分钟量
            if m > 0:
                speed = int(total.get() / m)
            else:
                speed = int(total.get())
            # 为了减少监控端压力, 只传入单线程id为0
            if sig_index == 0:
                send_to_monitor.send_api("shopee_{}".format(config.single_host.split('.')[-1]),
                                         "Shopee({}) id:{} pro:{}/{} ,60_prodcuts_process: {}/{}, page: {}/{}, total:{},total_time:{}"
                                         ", ave(/m): {} ,最后心跳时间为{}".format(config.single_host, sig_index,
                                                                                  sig_total_index, le,
                                                                                  index + 1, len(shopids), i, max_page,
                                                                                  total.get(),
                                                                                  int(temp_bar_time - main_time), speed,
                                                                                  time_))
            # print("[red]Doing Task {},page_process {}/{}, total:{},total_time:{}, average_time(/min): {}".format(sig_index,index+1,len(shopids),total.get(),int(temp_bar_time -main_time), speed))
            # 更新进度条
            progress.update(bars[sig_index], advance=1,
                            description="[red]{} id->{}：{}/{} ,cat->{},id->{} [green]60_process:{}/{}[red]"
                                        ", page:{}/{}, [green]total:{},[red]time:[{}:{}:{}], ave(/m): {} ,[green]最后心跳时间为{}".format(
                                config.single_host, sig_index, sig_total_index, le, m_name, m_id, index + 1,
                                len(shopids), i, max_page, total.get(),
                                h, m, s, speed, time_))

            # 获取单商品所有信息
            product_info = shopee_item_info_test(api_url_, sig_index, itemids[index], shopids[index], m_name,
                                                 total.get())

            # 如果获取到的单个商品数据正常 则添加total总数
            if product_info != False:
                single_page_products.append(product_info)
                mutex.acquire()
                total.set(total.get() + 1)
                mutex.release()

            # print(total)
        print("线程 id {} 当前页数{}完毕".format(sig_index, i))
    # 生成当前最新事件
    time_ = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    info = "爬取商品列表页中,当前所有三级类目进度为{}/{}: +".format(sig_index + 1, le) + '[' + "▓" * int(
        ((sig_index / le * 100) // 4)) + "-" * int((((
                                                             le - sig_index) / le * 100) // 2)) + ']' + ",页面进度为{}/50,当前爬取商品总数为{},最后心跳时间为{} 当前爬取链接为{}".format(
        i, total.get(), time_, m_url[:-1] + str(i))

    # 转发日志到监控端 暂时弃用
    # send_to_monitor.send_api('shopee', info)
    # print(info)
    return single_page_products


def spider(total, sig_index, sig_total_index, le, m_id, m_name, m_url, mutex):
    """

    :param total: 传入的线程共享总数变量
    :param sig_index: 单个线程的id
    :param sig_total_index: 单个进程分配的线程任务总数的进度
    :param le: 单线程任务总数
    :param m_id: 商品id
    :param m_name: 商品名称
    :param m_url: 商品url
    :param mutex: 线程/进程锁 暂时弃用
    :return:
    """

    # global total
    # print("Fawfwa")
    all_pages_products = []
    # 自定义最大页数
    if config.max_page_defalt != None:
        max_page = config.max_page_defalt
    else:
        max_page = 50

    # 循环遍历50页获取每页的商品
    for i in range(0, max_page):
        page = i
        # 执行单页数据采集
        call_back_one_page = single_product(max_page, total, sig_index, sig_total_index, le, m_id, m_name, m_url, i,
                                            mutex)
        if call_back_one_page == "limited":
            save_tool.save_shops_checkpoint(sig_total_index, total.get(), config.single_host)
            continue
        # 存储单分类全部页数到变量中供结束后进行单分类的json存储
        all_pages_products += call_back_one_page

    # 指定页数采集完成之后 进行数据的存储
    save_tool.save_products_to_json(PRODUCTS_PATH, m_name, all_pages_products, config.single_host)


def make_loop_thread(li_single, total, process_id, platform, checkpoint_flag):
    """
    单个进程的 线程任务分配
    :param li_single: 线程任务总数的任务列表
    :param total: 线程间共享变量
    :param process_id:
    :param platform: 采用的平台 如sg
    :param checkpoint_flag: 是否进行存储flag
    :return:
    """
    global progress, bars, main_time

    # 重新设定单个进程的所有config 参数  必须放到这一层级 因为在主程序中 无法跨文件修改配置文件 只能在单个进程中进行设置
    config.select_host = platform
    config.need_host = config.backup_hosts[config.select_host]
    config.single_host = re.findall('ttps://(.*?)/', config.need_host)[0]

    # 定义程序起始时间 便于后面的相关时间计算
    main_time = time.time()

    # 制作多线程共享进度监控条 每个进程间独立分配
    with Progress() as progress:
        bars = [progress.add_task("[red]Task id:{},total {}/{}".format(i, 0, total.get()),
                                  ) for i in range(config.thread_num)]

        time.sleep(1)
        print(
            """
    ========================================================================================
                进程中线程总数为{},进程数量为{},分配方案为{}个线程单次进程
                
    ========================================================================================
        """.format(len(li_single), config.process_num, config.thread_num))
        # 制作线程池
        pool = threadpool.ThreadPool(config.thread_num)

        # 执行线程任务
        requests = threadpool.makeRequests(spider, li_single)
        [pool.putRequest(req) for req in requests]
        # 等待全部线程执行完毕
        pool.wait()


if __name__ == '__main__':
    # 单元测试单个分类列表页测试时用
    # shopee_Test(11071756,"test", 60)
    # input("section test")
    global progress, total
    import ctypes

    print("""
　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　
　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　
　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　
　　　　　　　＃＃　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　＃＃　　　　　　　　　　　　
　　　　　　　＃＃＃　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　＃＃＃　　　　　　　　　　　
　　　　　　　　＃＃　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　＃＃　　　　　　　　　　　　
　　　　　　　　＃　　　　　　　　＃＃＃＃＃＃　　　　　　　　　　　　　　　　　　＃　　　　　　　　　　　　
　　　　　　　　＃　　＃＃＃＃＃＃＃＃＃＃＃＃＃　　　　　　　　　　　＃　　　　　＃　　　　　＃　　　　　　
　　　　　　　　＃　　＃＃＃＃＃＃＃　　　　　　　　　　　　　　　　　＃　　　　　＃　＃＃＃＃＃＃　　　　　
　　　　＃＃　　＃　　＃＃　　＃＃＃　　　　　　　　　　　　　　　　　＃＃＃＃＃＃＃＃＃＃＃＃＃＃　　　　　
　　　　＃＃＃＃＃＃＃＃＃　　　＃　　　　　　　　　　　　　　　　　　＃＃＃＃＃＃＃　　　　＃＃　　　　　　
　　　　＃＃＃＃＃＃＃＃＃　　＃＃　　　　　　　　　　　　　　　　　　＃＃　　　　＃　　　＃＃　　　　　　　
　　　　　＃　　＃　　＃＃　　＃＃＃＃　　　　　　　　　　　　　　　　＃＃　　　　＃　　＃＃　　　　　　　　
　　　　　＃　　＃　＃＃　　　＃＃　＃＃＃　　　　　　　　　　　　　　＃＃　　　　＃　＃＃＃＃　　　　　　　
　　　　　＃　＃＃＃＃＃　　　＃＃　　＃＃＃　　　　　　　　　　　　　＃＃＃＃＃＃＃＃＃＃＃　　　　　　　　
　　　　＃＃＃＃＃＃＃＃＃　　＃＃　　　＃＃＃　　　　　　　　　　　＃＃　＃＃＃＃　　＃＃＃　　　　　　　　
　　　　＃＃＃　＃　＃　　　　＃＃　　　＃＃＃　　　　　　　　　　　＃＃　　＃＃　　　＃＃　　　　　　　　　
　　　　　＃　　＃　＃＃　　　＃＃　　　　＃　　　　　　　　　　　　＃＃　　＃＃＃　＃＃　　　　　　　　　　
　　　　　　　　＃　　＃＃　　＃＃　　　　　　　　　　　　　　　　　＃＃　　　＃＃＃＃＃　　　　　　　　　　
　　　　　　　＃＃＃＃＃＃＃　＃＃　　　　　　　　　　　　　　　　＃＃　　　　　＃＃＃　　　　　　　　　　　
　　　＃＃＃＃＃＃＃　＃＃　　＃＃　　　　　　　　　　　　　　　　＃＃　　　　＃＃＃＃＃　　　　　　　　　　
　　　＃＃＃＃　　　　　＃　　＃＃　　　　　　　　　　　　　　　＃＃　　　　＃＃＃　＃＃＃　　　　　　　　　
　　　＃　　　　　　　　　　　＃＃　　　　　　　　　　　　　　　＃＃　　＃＃＃＃　　　＃＃＃　　　　　　　　
　　　　　　　　　　　　　　　＃＃　　　　　　　　　　　　　　＃＃　＃＃＃＃　　　　　　＃＃＃＃＃＃＃　　　
　　　　　　　　　　　　　　　＃＃　　　　　　　　　　　　　　＃＃＃＃＃　　　　　　　　　＃＃＃＃＃＃　　　
　　　　　　　　　　　　　　　　＃　　　　　　　　　　　　　　　＃＃　　　　　　　　　　　　　　　　　　　　
　　 虾皮跨12平台采集程序,支持站点如下 ["pl","cl","co","mx","br","sg","my","ph","th","vn","tw","id"]

    ===============使用方法 ===================================================================
        
        当前版本支持平台 :  pl cl co mx br sg my ph th vn id tw 台湾站需要台湾ip指定虾皮特殊代理,详情见
                                                        sdkdns软件中的 tw台湾-03 shopee 1.0x 代理 
                                                        对应扩展名请查看 shopee.com 或 config.py
        
        运行命令: 
                python main_get_products_by_cat.py --host sg --checkpoint --spider_type --max_page_defalt
        
        参数说明: 
                host         采集的站点 字符串型 可选 默认为 sg
                checkpoint    是否读档 bool值 可选 默认为 False
                spider_type   采集形式 bool值 可选 默认为 False
                max_page_defalt 最大页数 数字型 可选 默认为 2
                
        监控上报服务器: 39.98.162.234:5555
        
    =========================================================================================
    启动程序中...  如需修改参数请输入超参数 未设置则采取config 中的默认参数
            
    参数优先级:    超参数(argparse) > 配置文件(config.py)
            
    """)
    time.sleep(5)
    # 超参数
    parser = argparse.ArgumentParser()
    # 添加相关超参数  目前建议只使用 --host 和 --check_point 因为其他暂没有过多共享测试  需要修改移步至config.py
    parser.add_argument('--host', type=str, required=False, default="sg", help="Specify the site platform name",
                        choices=["pl", "cl", "co", "mx", "br", "sg", "my", "ph", "th", "vn", "tw", "id"])
    parser.add_argument('--checkpoint', required=False, action='store_true', default=config.checkpoint,
                        help="Whether to extract progress from existing progress ")
    parser.add_argument('--spider_type', required=False, default=config.spider_type,
                        help="the defalut mode is \n1 : spider use local categories \n2: spider use backup's api")
    parser.add_argument('--max_page_defalt', required=False, default=config.max_page_defalt,
                        help="set the max page each category has")
    args = parser.parse_args()
    platform = args.host
    checkpoint_flag = args.checkpoint
    lastest_ip = config.get_proxy()
    print("""
    =========================================================================================
        当前最新ip为: {}
    =========================================================================================
    """.format(lastest_ip))
    time.sleep(2)
    multiprocessing.freeze_support()
    processes = []
    # 构建 total 总数用于 线程间的共享
    total = multiprocessing.Manager().Value(ctypes.c_int, 0)
    # 理解用
    # 获取total 值
    # print(total.get())
    # 设定total 值
    # total.set(total.get()+1)
    # print(total.get())
    # input()/

    # 过去 指定进程数量的 线程任务列表
    process_distribute_li_, total0 = get_source(total, checkpoint_flag, platform)
    # 设置一个允许n个进程并发的进程池
    pool = multiprocessing.Pool(processes=config.process_num)

    process_ids_li = [i for i in range(config.process_num)]

    for divided_single_process in range(len(process_distribute_li_)):
        # 将进程仍入进程池，mission 后面的这个含有 i 的tuple 代表给mission的参数
        processes.append(multiprocessing.Process(target=make_loop_thread, args=(
        process_distribute_li_[divided_single_process], total, process_ids_li[divided_single_process], platform,
        checkpoint_flag)))

    # 线程启动
    for p in processes:
        time.sleep(0.2)
        p.start()

    # 线程守护
    for p in processes:
        p.join()
