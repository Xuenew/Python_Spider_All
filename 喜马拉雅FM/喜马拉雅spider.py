# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2022/7/10

import datetime
import time
import hashlib
import random
import json
import requests, pprint

from urllib.parse import quote
from hashlib import md5


config = {
    "xi_ma_la_ya": {"start": 1, "end": 2, "pagesize": 30, "start_page": 1},
}

# 关于 User_Agent_Pc
class UserAgent_Base():
    random = ""

# Md5 加密函数 32 返回32位的加密结果
def md5_use(text: str) -> str:
    result = md5(bytes(text, encoding="utf-8")).hexdigest()
    return result

# 通过时间获得一个固定格式的 时长格式
def get_duration_str(seconds: float, like: str = "%02d:%02d:%02d"):
    """
    71  -> 01:11
    """
    m, s = divmod(float(seconds), 60)
    h, m = divmod(m, 60)
    # print(like % (h, m, s))
    return like % (h, m, s)


# 爬取喜马拉雅的音乐的类
class XiMaLaYa(object):

    def __init__(self):
        self.headers = {
            'authority': 'www.ximalaya.com',
            "user-agent": UserAgent_Base().random,
            "Proxy-Tunnel": str(random.randint(1, 10000)),
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'accept': '*/*',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.ximalaya.com/search/sound/%E6%88%91%E4%BB%AC%E4%B8%8D%E4%B8%80%E6%A0%B7/p1',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': ''
        }

    def getServerTime(self):
        """
        获取喜马拉雅服务器的时间戳
        :return:
        """
        # 这个地址就是返回服务器时间戳的接口
        serverTimeUrl = "https://www.ximalaya.com/revision/time"
        response = requests.get(serverTimeUrl,headers = self.headers)
        return response.text

    def getSign(self,serverTime):
        """
        生成 xm-sign
        规则是 md5(ximalaya-服务器时间戳)(100以内随机数)服务器时间戳(100以内随机数)现在时间戳
        :param serverTime:
        :return:
        """
        nowTime = str(round(time.time()*1000))

        sign = str(hashlib.md5("himalaya-{}".format(serverTime).encode()).hexdigest()) + "({})".format(str(round(random.random()*100))) + serverTime + "({})".format(str(round(random.random()*100))) + nowTime
        # 将xm-sign添加到请求头中
        self.headers["xm-sign"] = sign
        # return sign

    # 统一请求响应函数
    def unify_requests(self,method="GET",url="",headers={},proxies={},data={}):
        if method=="GET":
            response = requests.get(url, headers=headers,proxies=proxies,data=data,timeout=5)
            return response


    # 解析搜索的结果的函数
    def parms_search_songs(self,result):
        result = result.text
        info_dic = json.loads(result)
        result_list = []
        #
        if "data" in info_dic and "track" in info_dic["data"] and "docs" in info_dic["data"]["track"] and info_dic["data"]["track"]["docs"]:
            for each in info_dic["data"]["track"]["docs"]:
                if int(each["duration"])<350:
                    dic_ = {}
                    dic_["audio2_albumName"] = each["albumTitle"]
                    dic_["audio2_artistName"] = each["nickname"]
                    dic_["audio2_songName"] = each["title"]
                    dic_["audio2_songId"] = each["id"]
                    dic_["audio2_songtime"] = datetime.datetime.fromtimestamp(int(each["createdAt"]/1000)).strftime("%Y-%m-%d %H:%M:%S") # 时间
                    dic_["audio2_platform"] = "喜马拉雅"
                    dic_["audio2_duration_intsec"] = int(each["duration"]) # 音乐时长 2021 02 25 新加功能 秒
                    dic_["audio2_duration_strsec"] = get_duration_str(seconds=each["duration"]) # 音乐时长 2021 02 25 新加功能 格式化
                    dic_["audio2_albumid"] = each["albumId"]
                    dic_["audio2_url"] = "https://www.ximalaya.com{trackUrl}".format(trackUrl=each["trackUrl"])
                    dic_["audio2_url_hash"] = md5_use(text=dic_["audio2_url"])
                    result_list.append(dic_)
        return result_list

    # 查找歌曲
    def search_songs(self, song_name='在希望的田野上', proxy={}, num=0,**kwargs):
        self.headers["referer"]="https://www.ximalaya.com/search/sound/{}/p1".format(quote(song_name))
        result_list = []
        _start = config["xi_ma_la_ya"]["start"]
        _end = config["xi_ma_la_ya"]["end"]

        if kwargs.get("page_num"):
            if config["xi_ma_la_ya"]["start_page"]==0:
                _start = kwargs.get("page_num")-1
                _end = kwargs.get("page_num")
            elif config["xi_ma_la_ya"]["start_page"]==1:
                _start = kwargs.get("page_num")
                _end = kwargs.get("page_num") + 1

        for page in range(_start,_end):
            url = "https://www.ximalaya.com/revision/search/main?kw={song_name}&page={page}&spellchecker=true&condition=relation&rows=20&device=iPhone&core=track&fq=&paidFilter=false".format(song_name=quote(song_name),page=page)

            if proxy:
                self.getSign(self.getServerTime())

                result = self.unify_requests(url=url, headers=self.headers,proxies=proxy)
            else:
                self.getSign(self.getServerTime())

                result = self.unify_requests(url=url,headers=self.headers)
            for each in self.parms_search_songs(result):
                result_list.append(each)
        return result_list
    def get_single(self):
        pass

search_songs = XiMaLaYa().search_songs
if __name__ == '__main__':

    proxies = {

    }
    each = {
        "page_num": 1,
        "search_key_words": "道德经",

    }

    # print(wy.search_songs(song_name="丑八怪",proxy=proxies))
    info = search_songs(song_name=each["search_key_words"],proxy=proxies, **each)
    print(len(info))
    print(info)

