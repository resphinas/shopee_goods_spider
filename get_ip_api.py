import re
import requests
# import config
def get_ip(ip_api_url):
    return "124.230.8.214:4224"
    url = ip_api_url

    payload={}
    headers = {
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'Accept-Language': 'zh-CN,zh;q=0.9',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'Pragma': 'no-cache',
      'Referer': 'http://jahttp.zhimaruanjian.com/',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }
    while True:
        response = requests.request("GET", url, headers=headers, data=payload)
        if '"code":111' in response.text:
            continue
        else:
            break
    print(response.text)

    if re.findall("\d*\.\d*\.\d*\.\d*:\d*",response.text) == 0:
        print("error : ip池供应商回传错误")
        input("checking !!!!!!!!!!!!!!!!!!!")
    else:
        ip = re.findall("\d*\.\d*\.\d*\.\d*:\d*",response.text)[0]
        print("ip報錯 切換至最新ip {}".format(ip))
    return ip
