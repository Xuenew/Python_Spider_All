# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xujian,time:2023/3/21

import requests
import re

from retrying import retry

# 获取代理
def get_proxy():
    return {}

@retry(stop_max_attempt_number=6, wait_fixed=1000)
def short_to_long_get_res(url):

    cookies = {
    }

    headers = {
        'authority': 'mp.weixin.qq.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }

    response = requests.get(url, cookies=cookies, headers=headers,
                            proxies=get_proxy(), timeout=5)
    return response


# 获得响应之后进行解析
def parse_html_res(res):
    long_url_index = "".join(re.findall(r'_g\.msg_link =(.*);',res.text))
    biz = "".join(re.findall(r'__biz=(.*?)&',long_url_index))
    mid = "".join(re.findall(r'mid=(.*?)&',long_url_index))
    idx = "".join(re.findall(r'idx=(.*?)&',long_url_index))
    sn = "".join(re.findall(r'sn=(.*?)&',long_url_index))
    long_url = "https://mp.weixin.qq.com/s?__biz={biz}&mid={mid}&idx={idx}&sn={sn}".format(biz=biz,mid=mid,idx=idx,sn=sn)
    return long_url

# 主调度函数
def run(url):
    res = short_to_long_get_res(url)
    long_url = parse_html_res(res)
    dic_ = {}
    dic_["short_url"] = url
    dic_["long_url"] = long_url
    dic_["platform_name"] = "微信"
    if long_url:
        return dic_
    else:
        return {}


get_long_url = run
if __name__ == '__main__':
    url = "https://mp.weixin.qq.com/s/i2pcIC3zXrgsTXH79OB_kg"

    info = run(url)
    print(info)
