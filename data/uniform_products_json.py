import os
import re
def get_filePath(path):
    global c
    '''
    input: 文件路径path
    '''
    file_or_dir = os.listdir(path)
    # print(file_or_dir)
    for file_dir in file_or_dir:
        file_or_dir_path = os.path.join(path,file_dir)
        # 判断该路径是不是路径，如果是，递归调用
        if os.path.isdir(file_or_dir_path):
            # print('Path: '+ file_or_dir_path)
            #递归
            get_filePath(file_or_dir_path)
        else:
            if 'txt' in  file_or_dir_path:
                # print('File: '+ file_or_dir_path)
                # id = re.findall('(.*?)_',file_or_dir_path)[0].split('\\')[-1]

                # print(lp+'\want\\{}.jpg'.format(c))
                temp = []
                file = open(file_or_dir_path, "r", encoding='utf-8')
                content = file.read()
                if '"items":[{"item_basic' not in content:
                    continue
                ids = re.findall('"itemid":(.*?),',content)

                # [temp.append(pp) for pp in ids if pp not in temp]
                # print(len(ids),len(temp))

                with open("excluded_log","a+",encoding="utf-8") as file:
                    file.write(file_or_dir_path + " " + str(len(ids)) + " " + str(len(temp)))

                # file.close()
                # # if 'data":[{"items":' in content:
                # #     print(file_or_dir_path)
                # if '"items":[{"item_basic' in content:
                #     content = content.replace('"items":[{"item_basic":','"data":[{"items":')
                #     file = open(file_or_dir_path, "w", encoding='utf-8')
                #     file.write(content)
                #     file.close()
                #     print(file_or_dir_path)

get_filePath('products')