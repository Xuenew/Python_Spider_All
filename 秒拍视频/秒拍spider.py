# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2021/1/18

import datetime
import json
import random
import time
import uuid
import requests

from hashlib import md5
from urllib import parse
from urllib.parse import quote

proxies = {}
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
        if s > 60:
            m += 1
        if m > 60:
            h += 1
        return h * 60 * 60 + m * 60 + s, str(h).zfill(2) + ':' + str(m).zfill(2) + ':' + str(s).zfill(2)
    try:
        s = int(duar_str_or_s)
    except:
        pass
    else:
        return hms(m=s % 3600//60, s=s % 60, h=s//3600)
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

# Md5 加密函数 32 返回32位的加密结果
def md5_use(text:str)->str:
    result = md5(bytes(text, encoding="utf-8")).hexdigest()
    # print(result)
    return result

# 获取代理
# 获得代理函数
def get_proxy():
    return proxies

config = {
    # 秒拍
    "video_search_offset": {"start": 1, "end": 2, "pagesize": 20, "start_page": 0},

}

class MiaopaiVideo():
    # 时间戳
    current_ts = str(int(time.time()))
    # 伪造UUID，也叫做GUID(C#)
    fake_uuid = str(uuid.uuid1())
    # APP版本
    app_version = '7.2.60'

    # 搜索接口 key_words 搜索的关键词 默认3
    APISearch = "https://b-api.ins.miaopai.com/1/search/media.json?count=20&page={page}&key={key_words}"

    def __init__(self, use_proxy=True):
        self.proxy = get_proxy() if use_proxy else None

    ###################################
    def get_cpAbid(self):
        s1 = random.randint(1,19)
        s2 = random.randint(1,29)
        if random.randint(0,1):
            return '1-102,{}-100,2-1,{}-101,5-200,2-201'.format(s1,s2)
        else:
            return '1-102,{}-100,2-1,{}-101'.format(s1,s2)

    # md5 加密
    def get_md5(self, source):
        if isinstance(source, str):
            source = source.encode('utf-8')
        return md5(source).hexdigest()

    ###################################

    # 秒拍解密响应
    def _decode_resp_content(self,resp_content):
        """解密请求响应的数据
        :param resp_content: 请求响应的content"""

        def bytes_to_int(data, offset):
            result = 0
            for i in range(4):
                result |= (data[offset + i] & 0xff) << (8 * 1)
            return result

        def reverse_bytes(i):
            return ((i >> 24) & 0xFF) | ((i >> 8) & 0xFF00) | ((i << 8) & 0xFF0000) | (i << 24)

        if len(resp_content) <= 8:
            return ''
        dword0 = bytes_to_int(resp_content, 0)
        dword1 = bytes_to_int(resp_content, 4)
        x = 0
        if (dword0 ^ dword1) == -1936999725:
            x = reverse_bytes(dword1 ^ bytes_to_int(resp_content, 8))
        buffer_size = len(resp_content) - 12 - x
        if buffer_size <= 0:
            return ''
        else:
            buffer = bytearray()
            for index in range(buffer_size):
                buffer.append((resp_content[8 + index] ^ resp_content[12 + index]) & 0xff)
            return buffer.decode('utf8')

    # 获取响应
    def get_response(self,key_words:str="梁家辉",page:int=3,**kwargs):
      # url = "https://b-api.ins.miaopai.com/1/search/media.json?count=20&page=3&key=%E6%A2%81%E5%AE%B6%E8%BE%89"
      # url = "https://b-api.ins.miaopai.com/1/search/media.json?count=20&page=3&key={}".format(quote(key_words))
      url = self.APISearch.format(key_words=quote(key_words),page=page)
      # timestamp = int(datetime.datetime.now().timestamp())

      payload = {}
      # headers = {
      #   'cp-uniqueId': '8ac4508c-ca93-30ac-b310-61d9b4ea91a2',
      #   'cp-os': 'android',
      #   'cp_kid': '0',
      #   'cp-ver': '7.2.78',
      #   'cp-uuid': '8ac4508c-ca93-30ac-b310-61d9b4ea91a2',
      #   'cp-abid': '1-10,2-1',
      #   'cp-channel': 'xiaomi_market',
      #   'cp-time': '1600245983',
      #   'cp-sver': '9',
      #   # 'cp-sign': 'fd3a76b879d6182925add2c5182071de',
      #   'cp-vend': 'miaopai',
      #   'cp-appid': '424',
      #   'Host': 'b-api.ins.miaopai.com',
      #   'User-Agent': 'okhttp/3.3.1',
      #   'Cookie': 'acw_tc=7b39758516002460160502434e5c514791eb6d8c44782e71955cd0f42e2fad'
      # }
      headers = {
          "Accept-Encoding": "gzip",
          'User-Agent': 'okhttp/3.3.1',
          'Connection': 'Keep-Alive',
          "Host": 'b-api.ins.miaopai.com',
          'cp_ver': '7.2.60',
          'cp_appid': '424',
          'cp_sver': '5.1.1',
          'cp_channel': 'xiaomi_market',
          'cp_os': 'android',
          'cp_vend': 'miaopai',
      }

      # cp_uuid = uuid.uuid1().__str__()
      headers['cp_sign'] = self.get_cp_sign(url)
      # print(headers)
      headers['cp_time'] = str(self.current_ts)
      headers['cp_uuid'] = self.fake_uuid
      headers['cp_abid'] = self.get_cpAbid()
      headers['Cache-Control'] = 'no-cache'

      response = requests.get(url, headers=headers, data = payload,verify=False,proxies=self.proxy)

      return response.content

    # 获取cp_sign参数值
    def get_cp_sign(self,target_url: str):
        sign_raw_str = 'url=' + parse.urlparse(target_url).path + \
                       'unique_id=' + self.fake_uuid + \
                       'version=' + self.app_version + \
                       'timestamp=' + self.current_ts + \
                       '4O230P1eeOixfktCk2B0K8d0PcjyPoBC'
        return md5((sign_raw_str.encode(encoding='utf-8'))).hexdigest()

    # 解析秒拍
    def get_parse(self,respose_text):
        # print(respose_text.replace("]}00","]}").replace("]}0","]}"))
        task_list = [] # 解析的结果集
        dic_info = json.loads(respose_text.replace("]}00","]}").replace("]}0","]}"))
        # dic_info = json.loads(respose_text.replace("]}0","]}"))
        # print(dic_info)
        if "result" in dic_info and dic_info["result"]:
            for each in dic_info["result"]:
                video_dict = {}
                video_dict["video2_title"] = each["description"]
                video_dict["video2_id"] = each["smid"]
                video_dict["video2_url"] = "http://n.miaopai.com/media/{}.html".format(each["smid"])
                video_dict["video2_author"] = each["user"]["nick"]
                video_dict["video2_url_hash"] = md5_use(video_dict.get("video2_url"))
                video_dict["video2_platform"] = "秒拍视频"
                duration_str_temp = each.get('meta_data', [])[0].get('upload', {}).get('length', '') if each.get('meta_data', []) else ''
                duration, duration_str = unify_duration_format(duration_str_temp)
                video_dict["video2_duration"] = duration  # 时长（秒数）
                video_dict["video2_duration_str"] = duration_str  # 时长（字符串）
                task_list.append(video_dict)
            return task_list
    # 获取video的返回值
    def search_video(self,search_key: str,**kwargs):
        _start = config["video_search_offset"]["start"]
        _end = config["video_search_offset"]["end"]
        task_list = []
        if kwargs.get("page_num"):
            if config["video_search_offset"]["start_page"] == 0:
                _start = int(kwargs.get("page_num")) - 1
                _end = int(kwargs.get("page_num"))
            elif config["video_search_offset"]["start_page"] == 1:
                _start = int(kwargs.get("page_num"))
                _end = int(kwargs.get("page_num")) + 1

        for page in range(_start, _end):
            respose_text = self._decode_resp_content(self.get_response(key_words=search_key,page=page))
            print(respose_text)
            for each in self.get_parse(respose_text):
                task_list.append(each)

        return task_list


search_songs = MiaopaiVideo(use_proxy=True).search_video

if __name__ == '__main__':
    kwags = {
    }
    info = search_songs(search_key="周杰伦", **kwags)  # 1109 没数据就对了
    print(info)
