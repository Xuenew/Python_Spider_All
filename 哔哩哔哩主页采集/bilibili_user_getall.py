# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2023/5/22

import datetime
import time
import requests

from hashlib import md5
from urllib.parse import quote
from retrying import retry

# 代理
def get_proxy():
    return {}

# Md5 加密函数 32 返回32位的加密结果
def md5_use(text: str) -> str:
    result = md5(bytes(text, encoding="utf-8")).hexdigest()
    return result

# 通过时间字符形式 返回时长格式
def unify_duration_format(duar_str_or_s: str):
    """
    01:11 -> 71,'00:01:11'
    00:01:11 -> 71,'00:01:11'
    :param duar_str: '01:11' or '00:01:11'
    :return:  71, '00:01:11'
    """
    error = 0, ''

    def hms(m: int, s: int, h=0):
        if s >= 60:
            m += int(s / 60)
            s = s % 60  #
        if m >= 60:
            h += int(m / 60)
            m = m % 60
        return h * 60 * 60 + m * 60 + s, str(h).zfill(2) + ':' + str(m).zfill(2) + ':' + str(s).zfill(2)

    try:
        s = int(duar_str_or_s)
    except:
        pass
    else:
        return hms(m=s % 3600 // 60, s=s % 60, h=s // 3600)
    try:
        if duar_str_or_s:
            duar_list = duar_str_or_s.split(':')
            if len(duar_list) == 2:
                return hms(m=int(duar_list[0]), s=int(duar_list[1]))
            elif len(duar_list) == 3:
                return hms(m=int(duar_list[1]), s=int(duar_list[2]), h=int(duar_list[0]))
            else:
                return error
        else:
            return error
    except Exception as e:
        return error

# 哔哩哔哩加密
def bilibili_jiami(keyword,mid,pn):
    wts = int(time.time())
    key = "keyword={keyword}&mid={mid}&order=pubdate&order_avoided=true&platform=web&pn={pn}&ps=30&tid=0&web_location=1550101&wts={wts}".format(keyword=keyword,
                                                                                                                                                mid=mid, pn=pn,
                                                                                                                                                wts=wts  )
    # salt = "72136226c6a73669787ee4fd02a74c27" # 老版本的盐
    salt = "5a73a9f6609390773b53586cce514c2e" # 2023 0609 新
    w_rid = md5_use(key+salt)
    return w_rid,wts

# 解析ifno
def analysis_parms(info_json):
    lis = info_json.get("data",{}).get("list",{}).get("vlist",[])
    now_count = int(info_json.get("data",{}).get("page",{}).get("pn"))*int(info_json.get("data",{}).get("page",{}).get("ps"))
    all_count = int(info_json.get("data",{}).get("page",{}).get("count"))
    has_more = True if now_count<=all_count else False
    lis_dic_ifno = []
    for each in lis:
        dic_info = dict()
        dic_info["play_num"] = each.get("play","")
        dic_info["like_num"] = each.get("photo","")
        dic_info["vid"] = each.get("aid","")
        dic_info["comment_num"] = each.get("comment","")
        dic_info["url"] = "https://www.bilibili.com/video/{}".format(each.get("bvid",""))
        dic_info["title"] = each.get("title","")
        duration, duration_str = unify_duration_format(each.get("length",""))
        dic_info["duration"] = duration_str
        dic_info["cover"] = each.get("pic","")
        dic_info["uid"] = each.get("mid","")
        dic_info["author_name"] = each.get("author","")
        dic_info["author_url"] = "https://space.bilibili.com/{}".format(each.get("mid",""))
        dic_info["pubtime"] = each.get("created","")
        if dic_info["pubtime"]:
            dic_info["pubtime"] = datetime.datetime.fromtimestamp(int(str(dic_info["pubtime"])[:10])).strftime("%Y-%m-%d %H:%M:%S")
        dic_info["photoUrl"] = each.get("pic","") # 这个是默认的播放的地址 完整版的
        lis_dic_ifno.append(dic_info)
    return lis_dic_ifno,has_more
# 通过链接获取对应的信息
@retry(stop_max_attempt_number=9, wait_fixed=20)
def get_parms(userId="",pcursor=1,keyword=""):

    headers = {
        'authority': 'api.bilibili.com',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'zh-CN,zh;q=0.9',
    }

    w_rid,wts = bilibili_jiami(quote(keyword),str(userId),str(pcursor))
    params = {
        'mid': str(userId),
        'ps': '30',
        'tid': '0',
        'pn': str(pcursor),
        'keyword': keyword,
        'order': 'pubdate',
        'platform': 'web',
        'web_location': '1550101',
        'order_avoided': 'true',
        'w_rid': w_rid,
        'wts': wts,
    }
    cookies = {
        'bsource': 'search_baidu',
        'innersign': '1',


    }

    response = requests.get('https://api.bilibili.com/x/space/wbi/arc/search', headers=headers,cookies=cookies, params=params,proxies=get_proxy(),timeout=10)


    return response.json()


# 主要的执行的函数
def run(userId="",pcursor=1,max_list_page=1,last_list=None,keyword=""):
    """
    userId 用户ID
    pcursor 起始页
    max_list_page 截止页
    keyword 搜索关键词 默认空
    """
    # last_list = []
    if last_list is None:
        last_list = []
    try:
        ever_page_info = get_parms(userId=userId,pcursor=pcursor,keyword=keyword)
        lis_dic_ifno,has_more = analysis_parms(ever_page_info)
        last_list.extend(lis_dic_ifno)
        # print(pcursor,has_more)
        if pcursor<max_list_page and has_more :
            pcursor+=1
            return run(userId=userId,pcursor=pcursor,max_list_page=max_list_page,last_list=last_list,keyword=keyword)
    except Exception as e:
        return last_list
    return last_list
if __name__ == '__main__':
    """
    pn 翻页 /每页30条
    """
    userId = "3493089977042945" #
    pcursor = 1 # 启始页
    max_list_page = 3 # 终止页面
    keyword = "老公" # 搜索关键词
    info = run(userId=userId,pcursor=pcursor,max_list_page=max_list_page,keyword=keyword)
    print(info)
    print(len(info))
