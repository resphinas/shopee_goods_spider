
import json
import os
def save_products_to_json(category_path,m_uid,m_name,data):
    #如果products/{m_id}文件夹不存在则创立
    file_path = '{}/{}.txt'.format(category_path,m_uid)
    if not os.path.exists(category_path):
        os.mkdir(category_path)
    #追加方式写入文件
    with open(file_path, 'a+', encoding= ' utf-8') as file:
        file.write(data)
def save_shops_checkpoint(num, total):
    with open('checkpoint/goods_checkpoint.txt','w',encoding='utf-8') as file:
        file.write('{} {}'.format(num, total))
def get_shops_checkpoint():
    with open('checkpoint/goods_checkpoint.txt','r',encoding='utf-8') as file:
        content = file.read().strip().split(" ")
        num = content[0]
        total = content[1]
        print(int(num), int(total))
    return [int(num), int(total)]

def save_wrong_shop(error_info):
    with open('data/error.txt', 'a+', encoding= "utf-8") as file:
        file.write(error_info)
import json
import os
def save_products_to_json(category_path,m_name,data, host):
    host = host.split(".")[-1]
    #如果products/{m_id}文件夹不存在则创立
    category_path = category_path.format(host)
    file_path = '{}/{}.json'.format(category_path,m_name)
    print(file_path)
    if not os.path.exists(category_path):
        os.mkdir(category_path)
    #追加方式写入文件
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data,file,indent=2, ensure_ascii= False)
def save_shops_checkpoint(num, total, host):
    host = host.split(".")[-1]
    with open('checkpoint/goods_checkpoint_{}.txt'.format(host),'w',encoding='utf-8') as file:
        file.write('{} {}'.format(num, total))
def get_shops_checkpoint(host):
    host = host.split(".")[-1]
    try:
        with open('checkpoint/goods_checkpoint_{}.txt'.format(host),'r',encoding='utf-8') as file:
            content = file.read().strip().split(" ")
            num = content[0]
            total = content[1]
            # print(int(num), int(total))
    except:
        with open('checkpoint/goods_checkpoint_{}.txt'.format(host), 'w', encoding='utf-8') as file:
            file.write("0 0")
        return 0,0
    return [int(num), int(total)]

def save_wrong_shop(error_info):
    with open('data/error.txt', 'a+', encoding= "utf-8") as file:
        file.write('{}\n'.format(error_info))

# category_path = '../data/polymerization_products/products_{}/'
# m_name = "test"
# data = {"d":"fa"}
#
# host = "shopee.sg".split('.')[-1]
# save_products_to_json(category_path,m_name,data, host)