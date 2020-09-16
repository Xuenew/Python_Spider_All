# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/6/30
import json
import random
from xtools import md5_use
import requests, pprint
from fake_useragent import UserAgent
from hashlib import md5
from retrying import retry
class XiaMi:
    ua = UserAgent()
    DOMAIN = "https://www.xiami.com"

    # 各个API接口地址
    # 每日音乐推荐
    APIDailySongs = "/api/recommend/getDailySongs"
    # 排行榜音乐
    APIBillboardDetail = "/api/billboard/getBillboardDetail"
    # 所有排行榜
    APIBillboardALL = "/api/billboard/getBillboards"
    # 歌曲详情信息
    APISongDetails = "/api/song/getPlayInfo"
    # 搜索音乐接口
    APISearch = "/api/search/searchSongs"
    # 歌曲单独一首详情
    APISingleSongInfo = "/api/song/initialize"
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "user-agent": self.ua.random,
            "Proxy-Tunnel": str(random.randint(1, 10000))
        }
        self.session.get(self.DOMAIN)

    def _get_api_url(self, api):
        return self.DOMAIN + api

    # 获取每日推荐的30首歌曲
    def get_daily_songs(self):
        url = self._get_api_url(self.APIDailySongs)
        params = {
            "_s": self._get_params__s(self.APIDailySongs)
        }
        result = self.session.get(url=url, params=params).json()
        self._dispose(result)

    # 获取虾米音乐的音乐排行榜
    def get_billboard_song(self, billboard_id: int = 0):
        '''
        :param billboard_id: 各类型的排行榜
        :return: 排行榜音乐数据
        '''
        if not hasattr(self, "billboard_dict"):
            self._get_billboard_dict_map()

        assert hasattr(self, "billboard_dict"), "billboard_dict获取失败"
        pprint.pprint(self.billboard_dict)
        if billboard_id == 0:
            billboard_id = input("输入对应ID，获取排行榜信息")
        assert billboard_id in self.billboard_dict, "billboard_id错误"

        url = self._get_api_url(self.APIBillboardDetail)
        _q = '{\"billboardId\":\"%s\"}' % billboard_id
        params = {
            "_q": _q,
            "_s": self._get_params__s(self.APIBillboardDetail, _q)
        }
        result = self.session.get(url=url, params=params).json()
        self._dispose(result)

    # 生成一个排行榜对应的字典映射
    def _get_billboard_dict_map(self):
        billboard_dict = {}
        billboards_info = self.get_billboard_all()
        try:
            if billboards_info["code"] == "SUCCESS":
                xiamiBillboards_list = billboards_info["result"]["data"]["xiamiBillboards"]
                for xiamiBillboards in xiamiBillboards_list:
                    for xiamiBillboard in xiamiBillboards:
                        id = xiamiBillboard["billboardId"]
                        name = xiamiBillboard["name"]
                        billboard_dict[id] = name
                self.billboard_dict = billboard_dict
        except Exception:
            pass

    # 获取所有的排行榜信息
    def get_billboard_all(self):
        url = self._get_api_url(self.APIBillboardALL)
        params = {
            "_s": self._get_params__s(self.APIBillboardALL)
        }
        result = self.session.get(url=url, params=params).json()
        self._dispose(result)

    # 获取歌曲详情信息
    def get_song_details(self, *song_ids) -> dict:
        '''
        :param song_ids: 歌曲的id，可以为多个
        :return: 歌曲的详情信息
        '''
        assert len(song_ids) != 0, "参数不能为空"

        for song_id in song_ids:
            if not isinstance(song_id, int):
                raise Exception("每个参数必须为整型")

        url = self._get_api_url(self.APISongDetails)
        _q = "{\"songIds\":%s}" % list(song_ids)
        params = {
            "_q": _q,
            "_s": self._get_params__s(self.APISongDetails, _q)
        }
        result = self.session.get(url=url, params=params).json()
        return self._dispose(result)

    # 获取虾米单独一首歌曲详情
    def get_song_single_info(self, *song_id_str) -> dict:
        '''
        :param song_ids: 歌曲的id，可以为多个
        :return: 歌曲的详情信息
        '''


        url = self._get_api_url(self.APISingleSongInfo)
        _q = "{\"songId\":\"%s\"}" % (song_id_str)
        params = {
            "_q": _q,
            "_s": self._get_params__s(self.APISingleSongInfo, _q)
        }
        result = self.session.get(url=url, params=params).json()
        return self._dispose(result)

    # 获取歌曲的下载地址
    def get_song_download_url(self, *song_ids):
        download_url_dict = {}
        song_details = self.get_song_details(*song_ids)
        songPlayInfos = song_details["result"]["data"]["songPlayInfos"]
        for songPlayInfo in songPlayInfos:
            song_download_url = songPlayInfo["playInfos"][0]["listenFile"] or songPlayInfo["playInfos"][1]["listenFile"]
            song_id = songPlayInfo["songId"]
            download_url_dict[song_id] = song_download_url

        print("歌曲下载地址为:", download_url_dict)

    # 处理爬虫获取到的数据，这里我就输出值
    def _dispose(self, data):
        # pprint.pprint(data)
        return data

    # 获取加密字符串_s
    def _get_params__s(self, api: str, _q: str = "") -> str:
        '''
        :param api: URL的地址
        :param _q:  需要加密的参数
        :return: 加密字符串
        '''
        xm_sg_tk = self._get_xm_sg_tk()
        data = xm_sg_tk + "_xmMain_" + api + "_" + _q
        return md5(bytes(data, encoding="utf-8")).hexdigest()

    # 获取xm_sg_tk的值，用于对数据加密的参数
    def _get_xm_sg_tk(self) -> str:
        xm_sg_tk = self.session.cookies.get("xm_sg_tk", None)
        assert xm_sg_tk is not None, "xm_sg_tk获取失败"
        return xm_sg_tk.split("_")[0]

    # 获取虾米搜索结果
    def _get_xm_serch(self,song_name='在希望的田野上',page=2):
        url = self._get_api_url(self.APISearch)
        _q = '{"key":"%s","pagingVO":{"page":%s,"pageSize":30}}'%(song_name,page)
        params = {
            "_q": _q,
            "_s": self._get_params__s(self.APISearch, _q)
        }
        # 测试
        # print(self._get_params__s(self.APISearch, _q)) # 打印   _s
        result = self.session.get(url=url, params=params).json()
        return result

    # 对搜索结果进行解析的函数
    def parms_search_songs(self,info):
        result_list =[]
        if "code" in info and info["code"] == "SUCCESS" and "result" in info and info["result"] and info["result"]["data"] and info["result"]["data"]["songs"]:
            for each in info["result"]["data"]["songs"]:

                if "S_OFF" not in each["bizTags"]: #
                    # print("S_OFF not in 在{}".format(each["bizTags"]))
                    dic_ = {}
                    dic_["audio2_albumName"] = each["albumName"]
                    dic_["audio2_artistName"] = each["singers"]
                    dic_["audio2_songName"] = each["songName"]
                    dic_["audio2_songId"] = each["songId"]
                    dic_["audio2_platform"] = "虾米音乐"
                    dic_["audio2_songStringId"] = each['songStringId'] # 字符形式的ID
                    dic_["audio2_url"] = "https://www.xiami.com/song/{}".format(dic_["audio2_songStringId"])
                    dic_["audio2_url_hash"] = md5_use(text=dic_["audio2_url"])

                    result_list.append(dic_)
                # else:
                #     print("S_OFF 在{}".format(each["bizTags"]))
        return result_list

    # 虾米 容易尝试失败 单独的一次请求
    @retry(stop_max_attempt_number=5,wait_fixed=600)
    def get_response_single(self,url,params,proxy={},num=0):
        if proxy:
            result = self.session.get(url=url, headers=self.headers,params=params,proxies=proxy).json()
        elif not proxy:
            result = self.session.get(url=url, headers=self.headers,params=params).json()
        if "rgv587_flag" in result:
            # print("虾米音乐未获取成功 重新尝试")
            if num < 5:
                self.session = requests.Session()
                self.session.get(self.DOMAIN)
                return self.get_response_single(url,params,proxy=proxy, num=num + 1)
            else:
                print(" 单个页面请求尝试过多")
                return []
        return result
    # 获取虾米搜索结果
    # @retry(stop_max_attempt_number=5,wait_fixed=600)
    def search_songs(self,song_name='在希望的田野上',proxy={},num=0):
        result_list = []
        for page in range(config["xiami_search_offset"]["start"],config["xiami_search_offset"]["end"]):

            url = self._get_api_url(self.APISearch)
            _q = '{"key":"%s","pagingVO":{"page":%s,"pageSize":30}}'%(song_name,page)
            params = {
                "_q": _q,
                "_s": self._get_params__s(self.APISearch, _q)
            }
            # 测试
            # print(self._get_params__s(self.APISearch, _q)) # 打印   _s
            if proxy:
                result = self.get_response_single(url=url,params=params,proxy=proxy)
            else:
                result = self.get_response_single(url=url,params=params)
            # print(reget_song_single_infosult)
            # self._dispose(result)
            # if "rgv587_flag" in result:
            #     print("虾米音乐未获取成功 重新尝试")
            #     if num<5:
            #         self.session = requests.Session()
            #         self.session.get(self.DOMAIN)
            #         return self.search_songs(song_name=song_name,proxy=proxy,num=num+1)
            #     else:
            #         print("尝试过多")
            #         return []
            for each in self.parms_search_songs(result):
                result_list.append(each)

        # print(result_list)
        return result_list
    def test(self):
            # self.get_daily_songs()
            # self._get_xm_sg_tk()
            # self.get_billboard_song(332)
            # self.get_billboard_all()
            # self.get_song_details(1813243760)
            # self.get_song_details(1806922983) # 测试 走在田野的路上
            # self.get_song_download_url(1813243760)
            self._get_xm_serch()
            pass
    def back_search_parms(self,name):
        url = self._get_api_url(self.APISearch)
        detail_info_list = []
        for page in range(config["xiami_search_offset"]["start"],config["xiami_search_offset"]["end"]):
            detail_info_dic = {}
            _q = '{"key":"%s","pagingVO":{"page":%s,"pageSize":30}}' % (name, page)
            params = {
                "_q": _q,
                "_s": self._get_params__s(self.APISearch, _q)
            }
            detail_info_dic['params'] = params
            detail_info_dic['headers'] = self.headers
            detail_info_dic['requir_way'] = "GET"
            detail_info_dic['url'] = self._get_api_url(self.APISearch)
            detail_info_list.append(detail_info_dic)
        # print(detail_info_list)
        return detail_info_list

    def get_play_info_db(self,  *song_id_str):
        info_dict = self.get_song_single_info(*song_id_str)
        song_info = info_dict.get('result', {}).get('data', {}).get('songDetail', {})
        play_info_db = dict()
        play_info_db['stats_view'] = song_info.get('playCount')
        play_info_db['stats_share'] = song_info.get('shareCount')
        play_info_db['stats_like'] = song_info.get('favCount')
        play_info_db['stats_comment'] = info_dict.get('result', {}).get('data', {}).get('songExt', {}).get('commentCount')
        return play_info_db
if __name__ == '__main__':
    xm = XiaMi()
    xm.back_search_parms(name='路在何方')
    # xm.test()
    proxy = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": config["proxyHost"],
        "port": config["proxyPort"],
        "user": config["proxyUser"],
        "pass": config["proxyPass"],
    }
    proxies = {
        "http": proxy,
        "https": proxy,
    }
    # xm.search_songs(song_name='七里香',proxy=proxies)
    # print(xm.get_song_details(379345))
    # print(xm.get_song_single_info("nnkRGy619bc").get('result', {}).get('data', {}).get('songDetail', {}).get('playCount'))
    # # playCount shareCount(fenxaing) favCount(xihuan)
    # print(xm.get_song_single_info("nnkRGy619bc").get('result', {}).get('data', {}).get('songExt', {}).get('commentCount'))
    # # commentCount
    # print(json.dumps(xm.get_song_single_info("nnkRGy619bc")))
    print(xm.get_play_info_db("xLDghmbd8d0"))