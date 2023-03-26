import time

import requests
import config
from request_function import socket_request_for_shopee_fit_all

def get_shopee_shop_info(sig_index, shop_id):

    api_url = "api/v4/product/get_shop_info?shopid={}".format(shop_id)
    host_url = config.need_host
    url = host_url + api_url

    payload = {}
    headers = {
        'authority': config.single_host,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        # 'Cookie': 'REC_T_ID=a65e94c2-63f0-11ed-a4e1-d6bc5e03be11; SPC_F=GVt6FCIJj4CJDB30KHAn5EwbKIsB3Xj2; SPC_R_T_ID=XW77O6gdv5sT7QZdRaTH4zeCvghGJxYFzjZN8IoR0RZ6LmovwlmV7UAGYVKT3/5nsQ+voEnW7F7J9zOT+O/NeCrw94n05CoiwmbCzxdzjW90mZfzwceecJm/J5E1oprd28ZjZJxk6mzA8jsSzij0eg0zFeeYWMrQOdr3yXVnXQw=; SPC_R_T_IV=RkV5WFVjNktURU8yRURYbA==; SPC_SI=P5OJYwAAAABqdE14RXJhdfhWcAEAAAAAOWxwZEF4YnI=; SPC_T_ID=XW77O6gdv5sT7QZdRaTH4zeCvghGJxYFzjZN8IoR0RZ6LmovwlmV7UAGYVKT3/5nsQ+voEnW7F7J9zOT+O/NeCrw94n05CoiwmbCzxdzjW90mZfzwceecJm/J5E1oprd28ZjZJxk6mzA8jsSzij0eg0zFeeYWMrQOdr3yXVnXQw=; SPC_T_IV=RkV5WFVjNktURU8yRURYbA=='
    }
    # 循环请求当前借口 增大容错率
    while True:
        try:
            connect = requests.request("GET", url, headers=headers, data=payload, timeout=20)
            response = connect.text
            connect.close()
            import json
            need = json.loads(response)
            di = {}

            di['item_count'] = need['data']['item_count']

            break
        except Exception as file:
            time.sleep(0.5)
            try:
                print(response)
            except:
                pass
            print("线程跟踪 :{} ,报错: {}".format(sig_index, file))

    # print("获取店铺信息成功")
    # response = requests.session().get( url, headers=headers, data=payload, proxies=proxies, timeout=10)

    # response.close()

    di['store_place'] = need['data']['place']
    di['is_official_shop'] = need['data']['is_official_shop']
    di['rating_star'] = need['data']['rating_star']
    di['response_rate'] = need['data']['response_rate']
    di['store_name'] = need['data']['name']
    di['store_create_time'] = need['data']['ctime']
    di['follower_count'] = need['data']['follower_count']
    di['rating_bad'] = need['data']['rating_bad']
    di['rating_good'] = need['data']['rating_good']
    di['rating_normal'] = need['data']['rating_normal']
    di['store_logo_url'] = "https://cf.{}/file/".format(config.single_host) + need['data']['account']['portrait'] + "_tn"

    return di


def shopee_item_info_test(api_url_,sig_index, itemid, shopid, m_name, total, test_status = False, test_platform = None):
    """
    获取单个商品的所有可用信息 并且回传字典
    其中核心为两个网络请求功能
        1. socket_request_for_shopee_fit_all 函数 获取单个商品的所有可用信息
        2. get_shopee_shop_info函数 单独获取当前商店的相关信息
    :param sig_index: 总数 -> config 中 线程数余数相关的 伪线程id
    :param itemid: 商品id
    :param shopid: 店铺id
    :param m_name: 分类名
    :param total: 获取商品的总数
    :param api_url_: 单个商品请求的api构造
    :return: di 字典  返回单个商品的字典信息
    """
    api_url = "/api/v4/item/get?itemid={}&shopid={}".format(itemid, shopid)
    if test_status:
        host_url = config.backup_hosts[test_platform]
        print("测试 站点为 :{}".format(host_url))
        print("测试URL 为 :{}".format(host_url+api_url))
    total += config.thread_num
    tolerate_num = 3
    tmp_num = 0
    while True:

        try:
            # 获取单商品api回传信息
            need = socket_request_for_shopee_fit_all(api_url_, config.single_host, api_url)
            di = {}
            di["product_id"] = need["data"]["itemid"]
            di["category"] = m_name
            di["shop_id"] = need["data"]["shopid"]

            break
        except Exception as file:
            # 超出容忍错误报错
            if tolerate_num < tmp_num:
                print(file)
                print("socket 在 single_product 中出错")
                return False
            time.sleep(2)
            tmp_num += 1

            continue
    # 将所有可用字段进行字典封存
    di["category"] = m_name
    di["shop_id"] = need["data"]["shopid"]
    di["price_min"] = need["data"]["price_min"] / 100000
    di["price_max"] = need["data"]["price_max"] / 100000
    di["price"] = need["data"]["price"] / 100000
    di["stock"] = need["data"]["stock"]
    di["discount"] = need["data"]["discount"]
    di["historical_sold"] = need["data"]["historical_sold"]
    di["sold"] = need["data"]["sold"]
    di["name"] = need["data"]["name"]
    di["ctime"] = need["data"]["ctime"]
    di["description"] = need["data"]["description"]
    di["catid"] = need["data"]["catid"]
    di["brand"] = need["data"]["brand"]
    scores = need["data"]["item_rating"]
    temp_rating_count2 = {}
    temp_rating_count2['comment_count'] = scores['rating_count'][0]
    temp_rating_count2['one_star_count'] = scores['rating_count'][1]
    temp_rating_count2['two_star_count'] = scores['rating_count'][2]
    temp_rating_count2['three_star_count'] = scores['rating_count'][3]
    temp_rating_count2['four_star_count'] = scores['rating_count'][4]
    temp_rating_count2['five_star_count'] = scores['rating_count'][5]

    di["comment_info"] = temp_rating_count2
    di["like_num"] = need["data"]["liked"]
    di["total_comment"] = need["data"]["cmt_count"]
    di["shopee_verify"] = need["data"]["shopee_verified"]
    di["attributes"] = need["data"]["tier_variations"]
    # 图片字段的特定解析
    for sigle_attribute_index, sigle_attribute in enumerate(di["attributes"]):
        di["attributes"][sigle_attribute_index]["images"] = ["https://cf.shopee.sg/file/" + image_token for image_token
                                                             in sigle_attribute["images"]] if \
        di["attributes"][sigle_attribute_index]["images"] != None else None

    di["main_image"] = ["https://cf.{}/file/".format(config.single_host) + image_token for image_token in need["data"]["images"]]
    di["store_place"] = need["data"]["shop_location"]
    di["origin_category"] = need["data"]["categories"]

    # 店铺字段单独请求借口
    di_shop = get_shopee_shop_info(sig_index, di["shop_id"])
    di["store_info"] = di_shop
    return di
"""
  "商品id": 1600957548,
  "店铺_id": 35925244,
"""

"""
  "商品id": 1600957548,
  "店铺_id": 35925244,
"""


"""

pl 测试专用 参数
17878381313 758348282

sg 测试专用参数 
9338819034   262807707
"""
# 单元测试用
# shopee_item_info_test("测试专用id 000",9338819034, 262807707, "测试专用", 0,test_status=True ,test_platform = "sg")
# input("second")
# shopee_item_info_test(itemid = None, shopid = None)
# shopee_shop_info_test()
