import re
from get_ip_api import get_ip
#是否开启随机代理模式 优先级最高
proxy = False
#是否开启固定代理模式
target_flag =False
target_proxy = "127.0.0.1:33210"
target_file_flag = False

# 爬取模式
# 1: 本地分类全类爬取
# 2: 动态分类动态爬取
#默认为 模式1  请通过超参数进行修改
spider_type = 1

#自定义末级分类采集页数
#None: 按采集程序智能识别最大页数
# 数字: 按自定义页数采集 必须大于等于0 小于50 的证书
# 提示 如最大页数为2 则设置2  实际程序中受到接口参数为 range(0,2) = 0,1
max_page_defalt = 2

#设置线程数 推荐数量为37
thread_num = 1


#设置进程数  推荐数量为3
process_num = 1

#获取随机ip代理时用  当前状态  : 弃用
ip_api_url = "http://api.proxy.ipidea.io/getProxyIp?num=1&return_type=txt&lb=1&sb=0&flow=1&regions=us&protocol=http"

#是否读档
checkpoint = False

# 後端接口与本地匹配字典
local_backups = {'vn':'XP_VIETNAM', 'ph':'XP_PHILIPPINES', 'cl':'XP_CHILE', 'my':'XP_MALAYSIA', 'tw':'XP_TW', 'sg':'XP_SINGAPORE', 'th': 'XP_THAILAND', 'mx':'XP_MEXICO', 'id':'XP_INDONESIA', 'br':'XP_BRAZIL','co':'XP_COLOMBIA', 'pl':'XP_POLAND'}

#各平台站点
backup_hosts = {"pl":"https://shopee.pl/" , #ok
                "cl":"https://shopee.cl/" , #ok
                "co":"https://shopee.com.co/" , #ok
                "mx":"https://shopee.com.mx/" ,#ok
                "br":"https://shopee.com.br/" ,#ok
                "sg":"https://shopee.sg/",#socket 可行
                "my":"https://shopee.com.my/", #socket 可行
                "ph":"https://shopee.ph/", #socket 可行
                "th":"https://shopee.co.th/", #socket 可行
                "vn":"https://shopee.vn/", #socket 可行
                "tw":"https://shopee.tw/",
                "id":"https://shopee.co.id/" #socket 可行
                }


select_host = "cl"
need_host = backup_hosts[select_host]
single_host = re.findall('ttps://(.*?)/',need_host)[0]

br_headers = {
"accept": "application/json",
"accept-encoding": "gzip, deflate, br",
"accept-language": "zh-CN,zh;q=0.9",
"af-ac-enc-dat": "AAcyLjUuMC0yAAABhS4izBUAAA7CAuAAAAAAAAAAAuvlR3weVVU60ykHUkkzSmQs+0sol/82EyfDx/bVRcPaaRvYm6/AMx6LSpoTdPFTsS3fKgun0IrV61IXZnIllxCRFup2D1gYRPH79G8+i2Aeb7zsNtGDj9cL8Asw813ikLnKoCVr4l3fuyugWFRp1Qe6rTHJGZBVPbG6m89nsDLLDwgG5xoTlPCAqrBcwADPmfermZMS99ksTip4iyWZxQP+WmEm5EuoJQgI6nY5eCmyhkmD4HThl5TjUnyZisue7aWxtehPu7N70xtTDcHg3wmMUa2R+Pauq8cKY3SotpKL1pPKWJf7Ii6ulIGCuoQClFlVhPyX/zYTJ8PH9tVFw9ppG9ibnkHEUB14rHUebq8JcaWvLTOCoBzhRKmUO439gBG9LIjBUDPJ/Fz4D5PsTtJ62WeGnbI2KS5LUeXSWBpl59AI5gYJCX7CT9Ut1dzLOvVE0Rl8EQl6E1RwOgFd2KVjgKprW5JdW8YfywX1otVvVkVU1wsNXts5GyAjI8vnGItu2NO3eLkh8HnUyi6Hw1/itIk+dvrx2cDNAh/WiazMgcgB2IpWoI3lzvoPKDx96WVQBxEd5/le2ngmePC+WGsrwe6QUQJfq3K1AG1EpKO616ktiwbY7P9KHML6aQtF4FlKd6x7LmbUKDtOOQPXo6adSCgMwsXNNYTyK3HSzCGoV/4BXUckfn/aqZ2EUBMC3PvgG/UJYfJy7sHEMhm1yOdrF0U4C7jmWDcFCMr+GYq1E5L5+opWoI3lzvoPKDx96WVQBxHpaZ1BcwHcCXLOb3JmD/34hAJG77Wiv3h8+QSVcnFcYr1EtvsTmxjnCzBEa6+AecM5gAAJEAbg9IkzYPLXPwi598jZ/901tpYwiYTjGF/2xIkHl1HqyESYMNSS8O5naAcTeUAhbodJtmu4kLBVAN/IDe4LpjRu9mRyVhJkALpVyW9oi9wjYiPXVXoHt38VZKt5R7jEhjvz+WyTm/WWgrub",
"cache-control": "no-cache",
"content-type": "application/json",
"pragma": "no-cache",
"referer": "https://shopee.com.br/Roupas-Femininas-cat.11059998?page=0&sortBy=sales",
"sec-ch-ua": "\"Google Chrome\";v=\"107\", \"Chromium\";v=\"107\", \"Not=A?Brand\";v=\"24\"",
"sec-ch-ua-mobile": "?0",
"sec-ch-ua-platform": "\"Windows\"",
"sec-fetch-dest": "empty",
"sec-fetch-mode": "cors",
"sec-fetch-site": "same-origin",
# "sz-token": "obGBwsb9uFAMEgaTl4te+A==|WHI4PAmPPw9NeYxDHtb8HE65+39NAYsMqrqf2A3jHJargCyGL30tkSA3wqcGfZ81s4KsH+2UlzfUt8kuSlsxvcaS8MrSAU8gDQ==|Va3Eo3y9J9sOKDAO|06|3",
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
"x-api-source": "pc",
# "x-csrftoken": "aZVxxgqPyDQVp89WBG2KOuYK11fAMSEm",
# "x-requested-with": "XMLHttpRequest",
# "x-sap-access-f": "3.2.107.2.0|13|2.5.0-2_5.1.0_0_158|f9f99d436d624a12aa4761d29c07ee1a5faf4142d78242|10900|1100",
# "x-sap-access-s": "4N_RTpkpvb-MRTNNJSUvNbi4FM4zEOAKjdeKuC8hv5E=",
# "x-sap-access-t": "1671516644",
"x-shopee-language": "pt-BR"
}


sg_headers = {
    "accept": "application/json",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "af-ac-enc-dat": "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",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "pragma": "no-cache",
    "referer": "https://shopee.sg/search?keyword=essential%20oils",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    "x-api-source": "pc",
    "x-requested-with": "XMLHttpRequest",
    "x-shopee-language": "en"
}

id_headers = {
    "accept": "application/json",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "af-ac-enc-dat": "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",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "cookie": "SPC_R_T_ID=Py6KX4OxoSW48pN6BesvctFPEG66puarl/9Ptappd+KEjZ4Zta0J2Drs8eLNaMU8QwX895xN1mtoyIvXIBRqV21n7S5hEFCZkcx2eBcWj8uycSNjlfdPNGm25Jka+Aach7MApQVScKi7TkTYsFTSCMdppzrf4eeOF0f3MEPxrOs=; SPC_R_T_IV=YlNUY1IybmdwaGVMSjJJeA==; SPC_T_ID=Py6KX4OxoSW48pN6BesvctFPEG66puarl/9Ptappd+KEjZ4Zta0J2Drs8eLNaMU8QwX895xN1mtoyIvXIBRqV21n7S5hEFCZkcx2eBcWj8uycSNjlfdPNGm25Jka+Aach7MApQVScKi7TkTYsFTSCMdppzrf4eeOF0f3MEPxrOs=; SPC_T_IV=YlNUY1IybmdwaGVMSjJJeA==; SPC_F=NDkHXXK3bGzJRmtzh0uzj69nS5BZ1ubN; REC_T_ID=36e87e65-6bd5-11ed-a4d2-f4ee081da1ed; _gcl_au=1.1.630937402.1669279920; _ga_SW6D8G0HXK=GS1.1.1669440634.2.0.1669440634.60.0.0; _fbp=fb.2.1669440635236.1022982724; _tt_enable_cookie=1; _ttp=228ce8d0-9908-4392-9fdc-8cb71e82b425; _ga=GA1.3.297464369.1669279924; cto_bundle=uNTnh193dEZvJTJGdWcwaGdDalZlaFIwJTJGckRrZUU1cFRkU3FwJTJCYlZWaUs0eGlRZktZcUtIYWRwWUxOUWZOU3VRUiUyRlFNdzdtUzBFQm1NaXdTQmdlYWZENWRwJTJGTzU3Z254UDljQzNBWkN2OHNTNkJ4SGV1eUZCcUlnaVlVNkVYZ1YxZWs3NUJLR2lpcFNYcjVvSldkVDl2OXpLRHR3JTNEJTNE; __LOCALE__null=ID; csrftoken=xTz3qijOXKcxrHz9aafAqD71Petp4kAE; SPC_SI=jteiYwAAAABybnlqUDVLQjy4pwAAAAAAb2FPS3ZnWkg=; _QPWSDCXHZQA=0e432a53-2374-4eee-912c-d0d4824a38f6; shopee_webUnique_ccd=CR2Ldtmx%2BP9txW2aWs831w%3D%3D%7C3fiFlqwjL9bUfpIkoCTDUbFrDBfBi7XyvWAn0VsFxWzOSZnNSau9CPPzYhOCHUoUf3sJK3LN9vEIW%2Bgk8aF5vP5b5vBbWNhPwA%3D%3D%7COxEX2S8Z6lKXr4vL%7C06%7C3; ds=fdbdc7ba36e4b8f92eb7d4d732a384d0; AC_CERT_D=U2FsdGVkX1//cqrdKN5DFxIe4LHeVPsTd/Pa4VbZgoavLY1LOljldcEUn3vyoEnOUvzsz9BM5g+T0ie+d5bQC3l+GD97h1gMbbWl6mxzGC6hlaDkLXD9IepgkONr4EiuqGm2GJfDx1fzbIxIvYUWTnEYW2l0CaFxGgc9ZXrBIwRyPUzxMgySEWv/m8rU+t2x4VhbEwdngB3IXjK5RI7nwGWVXS+xLAtPeBho51rJR+s=",
    "pragma": "no-cache",
    "referer": "https://shopee.co.id/search?keyword=phone&page=1&sortBy=sales",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sz-token": "CR2Ldtmx+P9txW2aWs831w==|3fiFlqwjL9bUfpIkoCTDUbFrDBfBi7XyvWAn0VsFxWzOSZnNSau9CPPzYhOCHUoUf3sJK3LN9vEIW+gk8aF5vP5b5vBbWNhPwA==|OxEX2S8Z6lKXr4vL|06|3",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    "x-api-source": "pc",
    "x-csrftoken": "xTz3qijOXKcxrHz9aafAqD71Petp4kAE",
    "x-requested-with": "XMLHttpRequest",
    "x-sap-access-f": "3.2.86.2.0|13|2.5.0-2_5.5.108_0_160|2549d1e2b2d54740ac17226602dd9292aa696de8c8f744|10900|100",
    "x-sap-access-s": "U9yUbVdxlyb0-iYqXPmuGzHzawczgEWMVv-Os6nErgo=",
    "x-sap-access-t": "1672211141",
    "x-shopee-language": "id"
}

#socket headers
"""
Connection: keep-alive

"""
socket_headers = """
GET {} HTTP/1.1
Host: {}
Pragma: no-cache
Cache-Control: no-cache
sec-ch-ua: "Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"
sec-ch-ua-mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36
Content-Type: application/json
X-API-SOURCE: pc
Accept: application/json
X-Shopee-Language: en
X-Requested-With: XMLHttpRequest
af-ac-enc-dat: gawgwagawgawggasafgp
sec-ch-ua-platform: "Windows"
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://{}/search?keyword=phone&page=1
Accept-Language: zh-CN,zh;q=0.9
Cookie: AC_CERT_D={}

"""

socket_headers = """GET {} HTTP/1.1
Host: {}
Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache
sec-ch-ua: "Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"
sec-ch-ua-mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36
Content-Type: application/json
X-API-SOURCE: pc
Accept: application/json
X-Shopee-Language: en
X-Requested-With: XMLHttpRequest
af-ac-enc-dat: AAcyLjUuMy0yAAABhqtrweEAAA1NApAAAAAAAAAAAsd6dMgubQZggd7b95AjwU6tLynmCw1e2zkbICMjy+cYi27Y0+a5OMQi1EvLALu2hfxigpXCxc01hPIrcdLMIahX/gFdRyR+f9qpnYRQEwLc++Ab9b7bUTZsY/iWdlBElO+vdLLi0npRYQN/Vdf9bl98mKNnRyR+f9qpnYRQEwLc++Ab9dLR0iVpSnVbQkfWXM2rAcijPFs13SwHHQaeeumHIvrCXKo8sCf4Rf8zqP+fZJAzmCJYpQy8lG5fkeEDlEX2WdDwZa/TgisZHMMNnFYD1FdWBayVwSyGafNOD4lT/5qnViLKauKHPojhVzIrb8KXdNadmMRS/4LY4cxWA5yjifBR0RySdhyhKzToeXrsCr/7VtvXqTHiAIOhfdRSDm1pQOF9Gfk9OtzMZXWsVPrXy1CEtKOM88EpeDij9mo6pQWRKe7v2AuGibWBf9B1YY0ANUJOnxyhchG5+vNqajGknw6qu/MBKkeeCy63JLNmnmKQb5f/NhMnw8f21UXD2mkb2JuyyLCD+z6tPHxk5FqNW+djBOw29qtN6WPMkVdI5ot0ufm5zHMDo/4eXEjxrR7QQhOX/zYTJ8PH9tVFw9ppG9iboaIsW0g+fOd9LkfUx40Nfm445jXDpkXwTFwVIIZrNCct1pPKmbFnUaHuRVUEC/c3Udj5ezC++IStzk2qp2TU1K3etn3xYryQlhezyX7fJGW0mw/grqtU7H4VQVL1+dN007w4KlhEKhBxsc0Q0uTSrvqm5ZQMI1CdazWBBIWTJLQN6EYWN7Tgib54AauaPlnkafnYhJmz3co0R2bE/8ubQTWLFmDpurF7uGFHmW4xl9MmQtYQFWY6ableHqpgYLF6Fo59krnpY6vlUYf0sNlTng==
sec-ch-ua-platform: "Windows"
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://{}/search?keyword=phone&page=1
Accept-Language: zh-CN,zh;q=0.9
Cookie: AC_CERT_D={}"""
#代理ip

single_product_headers = {
    "accept": "application/json",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "af-ac-enc-dat": "AAcyLjUuMC0yAAABhShtPfMAACGcBUAAAAAAAAAAAuvlR3weVVU60ykHUkkzSmQs+0sol/82EyfDx/bVRcPaaRvYm9s78/+0guOvFpjnchyUcXqLgB24ZeMPbScpG5UFHnWHtM7CogKty7CqxZ57sh3kY5f/NhMnw8f21UXD2mkb2Js4fgyhyOmWOwejDo7KtGV7rA8DVnMNiVB98RiMGSQSUAPbNapd0f2YWrZeeD5kSusu8Opa8IltpeO2Q02w+uvixcuS7ZpeUEeIyfOHCog3TeeGQltO5F/pZnhwI3c4yrHM5mKSSehkdIKmHwPftARD5bJIzbH4iHLfM/+8VwnQsnYBJs7F9X98z5mat5oniF23dYwzCNGysKvEWlK86TvYHpVLndZH1QiISW/zd3WZyZI0GXoiwmVGi2EqoH+RFdDApePT51oLkMakTnIokbSmOciSV0FXvz1Rx5rxXG31Q+iKsjYBh6CNJJLD1ev1uXoTl/62ry4ZG1NOUfhk3pGhLSZm5v8BEdGdAcoUi4/K2LRBztOhP+aoKHExL00xi8Ori7B2rfPSWKVnrSzG1Bh97SMTMSBZOqlBJTevAexBekiKg+z2kVX7n8DUBLY2SqdD9WNdyqHaBh16RQTMYfM8Qv2nKavpF0QLmM98fvdN+UDcwbI1KRfxRU/CWtZ5rwYeEcc9Q3o3OkL4UaEwcAMbVv5VbPk7cuyopbhssT4I5Y56PPYv+YZk+G5O1pX0W+TbtbowGqWcaD1eNhBDw4gYAninxRNNa6CcvQi/B2JAl+GBtit3jZtiD+ueEH9DJH/llIufi4ofrQvQTjR2FzkMQNai1l39gAeJKxAXKYoc25viRp6qQy9sXrXU/kdb1U9cqY27ivMgr82D2jGo5w7DWDNDesLEPm7UteYJ+jBj+M3MG4vNJ0OQoMJQt+Yy1Zao8uz5nm2cMG9wcbHpvAMPIg+XG4UJrejD8n3h+R0nNFrteeAbgrplHBK7FMQrri72gxRRt0eh+z2UM767QyGa0G21OMMd7B6gDzXCKudys4WJ4TdMsW9SSq4vGSw9e4UgfstrT7ODMHJzIOeDDRjZ1tGAJU5xcxzXSIjsbBfd7ZwdGQpFPqphYU6nFuDLorVyVJHHbToOiOvaqEduGA1PcNrhLuqHxGjuzZPJi5EH7V5HcYAVIQ7w1sKoFDQu6s3qpXQz19VHd13Elqy56im+nB0ZCkU+qmFhTqcW4MuitXJUkcdtOg6I69qoR24YDU+LSJFokYNWvYV8PjuFrhJUpmp/PY8ahuZrZmObSiRdP49CiZdL1Ewb1tgrFu3rfn16ZB2BjlACRSDzWwReLu9bpr6OhSdVF2qIZGNkmfUTqLaoyAORnEFZXbnk/SdUd8psbkawomPVxiXO0rMYs4ewvSIS5sxF2ZN4mMNZNlP2sWOc2T3Vu0kipiZi3ZsbKCJbHumreSKdDydqpqckzYUO/8EEa6zh74N1tYzQs0HTZjwx6kUyGTjZL9LtGofJhE+VJq0ugNRuVVxxEqqfV69OHMtbevJq31gNLa1o+CKIg+2F8hhFnKe0vYCwAf0cuRUzVqg8CqZnzuNqp5ssny55X2FDNXLJQGBsWcPBW+5U+BECwtogvveqioJXR7TbTolaAStVT5DhHk9cN0IM1xEj4zLnRrYJL7/lQ80tsj7KyUWp+KOsMG49WlUfad0aZT0F/jvWI528weWYgWihMcbmC03c4cRtlih/1nDh0zmvzBN5QCFuh0m2a7iQsFUA38g85fhZvkEbcLJBRsZSHE+i5qS2X0E21G5o51UcSUpjpWZyTbiy4HlSdPkv+xKQJ1o=",
    "content-type": "application/json",
    "cookie": "__LOCALE__null=SG; REC_T_ID=1cfb935c-7f4d-11ed-80fe-2cea7fa8ab17; SPC_SI=inmZYwAAAAAzU1N6WVZkTLhwvgAAAAAASFgxSllBa1Q=; SPC_F=dODUb34naXrN0EzywVDE4h476XSFVFqj; _gcl_au=1.1.588685476.1671420470; csrftoken=RMHexBuoZYVZX06d6RRxRvZTx6fFPG6j; _fbp=fb.1.1671420470311.1896672065; _tt_enable_cookie=1; _ttp=_dvj6_f-zpDGD4vTwqaXBrEJbfj; _QPWSDCXHZQA=a9fc0a30-6823-404c-d098-e194d1ec0512; shopee_webUnique_ccd=OcK9ys32SQAhUAQrrbKOxA%3D%3D%7CFiDjnjsEyQtn7hFiL5ILd2Ba6o6y5KYJNC01tqL5CtRXe%2F5gAJJSPvPz46ZfAMKlRxbhZpPLzzkipSQXZ7S0GJcZODb6q1eVtT4%3D%7CFwkRICHu6bTC3p6c%7C06%7C3; ds=7fc6bfb63c451bcd525889cbc9e7b348; AMP_TOKEN=%24NOT_FOUND; _gid=GA1.2.544433248.1671420506; _dc_gtm_UA-61921742-7=1; SPC_CLIENTID=ZE9EVWIzNG5hWHJOcrovfdxrarbrqcpe; SPC_ST=.M2lLeGF0ZThVQWFhcWF4bAJjHp+zArhGdoh21Y9CJWULV2CYziAjR6It1BunQEAMuwRLSQKJDlJ9QaRwNnxkd6H8r8BhtpbPu4XDcbYMBlWFc5/mzzwDsnrFRTk/TPlI1KIKO9w6nlWQG5ufy1WscdWXR3B/U6ly5IjkjwIa0cht400HsivaeIwcDR/ig9ZGZjXuB5BbFYGHTxhH+Jghbw==; SPC_U=923188063; SPC_T_ID=CojcLoVx4wdVBKM4GURMhZzuK2849sJnwnKtvwiQanBVmW4WnfcPdF+4lae1HOBrvS9EBhvEyHwkabgxdlxmqfE2LFm5wMWSQaDujRS5kGcCCwQ7q5EEanS3HaCytOQtxAbsoCtjUk1DF72yvqZ4sPStHrY/qeglDEp/AzyTgpQ=; SPC_T_IV=QkpZZmVlTTNDOEVySnFJdQ==; SPC_R_T_ID=CojcLoVx4wdVBKM4GURMhZzuK2849sJnwnKtvwiQanBVmW4WnfcPdF+4lae1HOBrvS9EBhvEyHwkabgxdlxmqfE2LFm5wMWSQaDujRS5kGcCCwQ7q5EEanS3HaCytOQtxAbsoCtjUk1DF72yvqZ4sPStHrY/qeglDEp/AzyTgpQ=; SPC_R_T_IV=QkpZZmVlTTNDOEVySnFJdQ==; _ga_4572B3WZ33=GS1.1.1671420472.1.1.1671420526.6.0.0; SPC_EC=YlNDOUJrdVNPb1lpWVpzZAYfHnn5atuqVtqH68S3jUMzbp/DOYHoVeAy0aW+clC9VQVdDyQNQa0zpn3nOJDpt8SU0vsB394jr9JAVIrTqiuLm6lZ7pzgC4lpcYL2cbV7WXsNL47DUKssH+Id91pkK7OCeZVl2FviAjnN0niex5s=; _ga=GA1.2.988558329.1671420472",
    "referer": "https://shopee.sg/LionShield-iPhone-14-Pro-Max-Screen-Protector-13-12-11-XR-XS-Max-Plus-Tempered-Glass-Clear-Matte-Bluelight-Privacy-i.75632239.2285321333?sp_atk=79f37cdb-bb20-454f-b69e-b487f6e70600&xptdk=79f37cdb-bb20-454f-b69e-b487f6e70600&is_from_signup=true",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    "x-api-source": "pc",
    "x-csrftoken": "RMHexBuoZYVZX06d6RRxRvZTx6fFPG6j",
    "x-requested-with": "XMLHttpRequest",
    "x-shopee-language": "en"
}


def get_AC_CERT_D():

    try:
        with open('ac_cert_d.txt', "r", encoding="utf-8") as file:
            return file.read().strip()
    except:
        with open('ac_cert_d.txt', "w", encoding="utf-8") as file:
            return "nothing put in ac_cert_d"

# 所有网络请求时都会用到的方案 待优化: 不管是何种方法 应避免做重复的工作 推荐采用redis 或者 队列
def get_proxy():
    if proxy:
        ip_new = get_ip(ip_api_url)
        proxy_detail = "https://{}".format(ip_new)

    elif target_flag:
        ip_new = target_proxy
        proxy_detail = "http://{}".format(ip_new)
        return proxy_detail

    else:
        ip_new = None
        proxy_detail = None

    # ip_new = "124.230.8.214:4224"

    if not target_flag and not proxy:
        proxy_detail = ""
    # with open('count_ip.txt', 'r', encoding="utf-8") as file:
    #     count = int(file.read().strip())
    # print("當前ip耗量為{}".format(count))
    # with open('count_ip.txt','w',encoding="utf-8") as file:
    #     count +=1
    #     file.write(str(count))
    # print(" get ip {}".format(proxy_detail))
    if target_file_flag:
        with open("target_ip.txt", "r", encoding="utf-8") as file:
            proxy_detail = "http://{}".format(file.read().strip())
    return proxy_detail

# print(get_proxy())