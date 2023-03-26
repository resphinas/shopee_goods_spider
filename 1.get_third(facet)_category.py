# <<<<<<< HEAD
# <<<<<<< HEAD
# =======
# >>>>>>> ef66537047f57bb0fce770bd0685c4e8fa176823
# import json
# import requests
# import re
# with open("categories.json",'r',encoding="utf-8") as file:
#   content = eval(file.read())
#
#
# import os
# def get_all():
#   url = "https://deo.shopeemobile.com/shopee/shopee-pcmall-live-sg/homepage/965.21a4202b4d14f53b4d76.js"
#   payload = {}
#   headers = {
#     'authority': 'deo.shopeemobile.com',
#     'accept': '*/*',
#     'accept-language': 'zh-CN,zh;q=0.9',
#     'referer': 'https://shopee.ph/',
#     'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'script',
#     'sec-fetch-mode': 'no-cors',
#     'sec-fetch-site': 'cross-site',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
#   }
#
#   response = requests.request("GET", url, headers=headers, data=payload).text
#
#   # print(response.text)
#   with open('third.txt', 'w', encoding='utf-8') as file:
#     file.write(response)
#   return response
#
# def spider_parent_info(query_id):
#   url = "https://shopee.ph/api/v4/search/get_fe_category_detail?catids=" +query_id
#   headers = {
#     'authority': 'shopee.ph',
#     'x-shopee-language': 'en',
#     # 'x-requested-with': 'XMLHttpRequest',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
#     # 'x-api-source': 'pc',
#     # 'accept': '*/*',
#     # 'sec-fetch-site': 'same-origin',
#     # 'sec-fetch-mode': 'cors',
#     # 'sec-fetch-dest': 'empty',
#     # 'referer': 'https://shopee.sg/Car-Seats-cat.' + query_id,
#     'accept-language': 'zh-CN,zh;q=0.9',
#   }
#
#   response = requests.request("GET", url, headers=headers).text
#   # print(response)
#   # input()
#   null = None
#   false = False
#   true = True
#
#   try:
#     li = eval(response)['data']['categories'][0]
#   except Exception as file:
#     return 0
#     pass
#   need = {}
#   need['id'] = '1' + query_id
#   need['name'] = li['name']
#   need['parents'] = li['parent_cat_id']
#   need['display_name'] = li['display_name']
#   # b_id = li[]
#   return need
#
# def extract(response):
#   true = True
#   false =False
#   null = None
#   response = eval(response.split("""5:e=>{"use strict";e.exports=JSON.parse('""")[-1][:-7])['cats']
#   items = list(response.keys())
#   # print(items,len(items))
#   res = []
#   all = []
#   count = 0
#   for j  in range(0,len(items)):
#     count +=1
#     print("{}/{}".format(count,len(items)))
#     single_info = spider_parent_info(query_id= items[j])
#     if single_info ==0:
#       continue
#     # di = {}
#     # if len(single_info) != 3:
#     #   continue
#
#     # di['b_category_id'] = single_info[0]['id']
#     # di['b_category_name'] = single_info[0]['name']
#     # di['b_category_url'] = None
#     #
#     # di['m_category_id'] = single_info[1]['id']
#     # di['m_category_name'] = single_info[1]['name']
#     # di['m_category_url'] = None
#     #
#     # di['s_category_id'] = single_info[2]['id']
#     # di['s_category_name'] = single_info[2]['name']
#     # di['s_category_url'] = i[1]
#     all.append(single_info)
#     # print(di)
#     # input("check")
#
#   return all
#
# def main():
#   global need
#   need = []
#   response = get_all()
#   res = extract(response)
#   with open("all_categories.txt",'w',encoding="utf-8") as file:
#     file.write(str(res))
#
# if __name__ == '__main__':
# <<<<<<< HEAD
# =======
import json
import requests
import re
with open("categories.json",'r',encoding="utf-8") as file:
  content = eval(file.read())



def get_all():
  # 进入虾皮某站点主页 获取a步骤中的网络请求url 并且进行更改
  url = "https://deo.shopeemobile.com/shopee/shopee-pcmall-live-sg/homepage/481.964947fa00b0a0788711.js"
  payload = {}
  headers = {
    'authority': 'deo.shopeemobile.com',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'referer': 'https://shopee.sg/',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
  }

  response = requests.request("GET", url, headers=headers, data=payload).text

  # print(response.text)
  with open('third.txt', 'w', encoding='utf-8') as file:
    file.write(response)
  return response

def spider_parent_info(query_id):
  #		进入虾皮单个分类 获取a步骤中的第二个网络请求url 并且进行更改

  url = "https://shopee.sg/api/v4/search/get_fe_category_detail?catids=" +query_id

  headers = {
    'authority': 'shopee.sg',
    'x-shopee-language': 'en',
    # 'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    # 'x-api-source': 'pc',
    # 'accept': '*/*',
    # 'sec-fetch-site': 'same-origin',
    # 'sec-fetch-mode': 'cors',
    # 'sec-fetch-dest': 'empty',
    # 'referer': 'https://shopee.sg/Car-Seats-cat.' + query_id,
    'accept-language': 'zh-CN,zh;q=0.9',
  }

  response = requests.request("GET", url, headers=headers).text
  # print(response)
  # input()
  null = None
  false = False
  true = True

  try:
    li = eval(response)['data']['categories'][0]
  except Exception as file:
    return 0
    pass
  need = {}
  need['id'] = '1' + query_id
  need['name'] = li['name']
  need['parents'] = li['parent_cat_id']
  need['display_name'] = li['display_name']
  # b_id = li[]
  return need

def extract(response):
  true = True
  false =False
  null = None
  response = eval(response.split("""strict";e.exports=JSON.parse('""")[-1][:-7])['cats']
  items = list(response.keys())
  # print(items,len(items))
  res = []
  all = []
  count = 0
  for j  in range(0,len(items)):
    count +=1
    print("{}/{}".format(count,len(items)))
    single_info = spider_parent_info(query_id= items[j])
    if single_info ==0:
      continue

    all.append(single_info)
    # print(di)
    # input("check")

  return all

def main():
  global need
  need = []
  response = get_all()
  res = extract(response)
  with open("all_categories.txt",'w',encoding="utf-8") as file:
    file.write(str(res))

if __name__ == '__main__':
# >>>>>>> 2af216d (shopee)
# =======
# >>>>>>> ef66537047f57bb0fce770bd0685c4e8fa176823
    main()