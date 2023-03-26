# <<<<<<< HEAD
# <<<<<<< HEAD
# =======
# >>>>>>> ef66537047f57bb0fce770bd0685c4e8fa176823
# import json
#
# with open("all_categories.txt", 'r', encoding="utf-8") as file:
#     content = eval(file.read())
# li = {}
# for i in content:
#     li[i['id']] = i
# co = 0
# need = []
# for i in content:
#     if i['parents'] == None:
#         continue
#     if len(i['parents']) != 2:
#         continue
#     parents = i['parents']
#     di = {}
#     di['s_category_id'] = i['id']
#     di['s_category_name'] = i['name']
#     di['s_category_names'] = i['display_name']
#     di['b_category_id'] = li['1'+str(parents[0])]['id']
#     di['b_category_name'] = li['1'+str(parents[0])]['name']
#     di['b_category_names'] = li['1'+str(parents[0])]['display_name']
#     di['m_category_id'] = li['1'+str(parents[1])]['id']
#     di['m_category_name'] = li['1'+str(parents[1])]['name']
#     di['m_category_names'] = li['1'+str(parents[1])]['display_name']
#     need.append(di)
# with open('spider_categories.json','w',encoding="utf-8") as file:
#     json.dump(need,file)
#     # print(co)
#
# <<<<<<< HEAD
# =======
import json

with open("all_categories.txt", 'r', encoding="utf-8") as file:
    content = eval(file.read())
li = {}
for i in content:
    li[i['id']] = i
co = 0
need = []
for i in content:
    if i['parents'] == None:
        continue
    if len(i['parents']) != 2:
        continue
    parents = i['parents']
    di = {}
    di['s_category_id'] = i['id']
    di['s_category_name'] = i['name']
    di['s_category_names'] = i['display_name']
    di['b_category_id'] = li['1'+str(parents[0])]['id']
    di['b_category_name'] = li['1'+str(parents[0])]['name']
    di['b_category_names'] = li['1'+str(parents[0])]['display_name']
    di['m_category_id'] = li['1'+str(parents[1])]['id']
    di['m_category_name'] = li['1'+str(parents[1])]['name']
    di['m_category_names'] = li['1'+str(parents[1])]['display_name']
    need.append(di)
with open('spider_categories.json','w',encoding="utf-8") as file:
    json.dump(need,file)
    # print(co)

# >>>>>>> 2af216d (shopee)
# =======
# >>>>>>> ef66537047f57bb0fce770bd0685c4e8fa176823
