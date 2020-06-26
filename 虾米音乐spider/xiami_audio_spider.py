# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/6/25

import requests, pprint
from fake_useragent import UserAgent
from hashlib import md5


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
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "user-agent": self.ua.random
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
        pprint.pprint(data)
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
        print("data ",data)
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
        print(result)
        # self._dispose(result)
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


if __name__ == '__main__':
    xm = XiaMi()
    xm.test()