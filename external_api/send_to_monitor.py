import requests

def send_api(platform, status):
    """
    To send report to our monitor server 39.98.162.234:5555
    :param platform: like [jd 1688 alibaba shopee_[sg,ph,tl,idn,vn,tw,ml,bz,mxc,clb,pl,chile] alibaba tm tb ]
    :param status:  return {"status":"success!"} if pass the validation
    :return:
    """
    url = "http://39.98.162.234:5555//analyze/?platform={}&status={}".format(platform, status)

    headers = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    try:
        response = requests.session().get( url, headers=headers, verify=False)
        # print(response.text)

    except Exception as file:
        print("日志上传失败,报错如下: \n {}".format(file))



"""
使用说明：
    调用函数 monitor_api(patform,status):
        传入所爬平台作为参数一 平台类别格式为 [jd,1688,alibaba,shopee_[sg,ph,tl,idn,vn,tw,ml,bz,mxc,clb,pl,chile,alibaba,tm,tb]
        当前两个ip 状态 的为change_ip_1 change_ip_2
        传入当前状态作为参数二 如 关键词10/20 店铺20/30 页数10/10 关键词平均用时为56s, 店铺平均用时为32s,当前程序总用时为4000s,当前速度为1个/min       等
    如 send_api('jd',"关键词10/20 店铺20/30 页数10/10 关键词平均用时为56s, 店铺平均用时为32s,当前程序总用时为4000s,当前速度为1个/min ")

    成功调用： response返回success
    错误调用： response返回error


    监控界面
                点击 http://39.98.162.234:5555  查看当前抓取实时状态

"""
# test为专用测试接口
if __name__ == '__main__':

    # send_api(platform='alibaba', status="测试2023 1/5")
    # send_api(platform='change_ip_2', status="")
    # 全部清零
    for i in ["shopee_sg","shopee_ph","shopee_tl","shopee_idn","shopee_vn","shopee_tw","shopee_my","shopee_bz","shopee_mxc","shopee_clb","shopee_pl","shopee_chile","alibaba","tm","tb","alibaba","jd","1688"]:
        send_api(i,"")