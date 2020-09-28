# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/6/28

from fake_useragent import UserAgent
from Crypto.Cipher import AES

import base64
import requests, pprint,json


class WangYiYun():

    def __init__(self):
        self.params = ""
        self._i = "l6Brr86UeZ6C3Bsw" # 默认使用此字符串
        # 使用默认_i 配套的encSecKey
        self.encSecKey = "7ca9b5ba8b13044f47ed74c388df912ac84758122acbedc64111f2ac83232b01d3ce16f7195a39c7e064b4c0240b5c1d52624dc13c22ec820d76dfe32db43e496aeacced5be3ca9108c78a85bb389f1edf8d8c9fced02024ba9490401b4ce062cc50764d0a24294e07bb229271391b5a3640e924ee1ed15435dc6e288f1fa873"
        self.headers =  {
            'authority': 'music.163.com',
            'user-agent': UserAgent().random,
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*',
            'origin': 'https://music.163.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://music.163.com/song?id=1426301364',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': '_iuqxldmzr_=32; _ntes_nnid=5f8ee04e745645d13d3f711c76769afe,1593048942478; _ntes_nuid=5f8ee04e745645d13d3f711c76769afe; WM_TID=XqvK2%2FtWaSBEUBRBEEN7XejGE%2FL0h6Vq; WM_NI=iN6dugAs39cIm2K2R9ox28GszTm5oRjcvJCcyIuaI1dccEVSjaHEwhc8FuERfkh3s%2FFP0zniMA5P4vqS4H3TJKdQofPqezDPP4IR5ApTjuqeNIJNZkCvHMSY6TtEkCZUS3k%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb2e57dbababf88b879a8b08fa2d84f869f9fbaaa50a3f599a5d650939b8dadd52af0fea7c3b92aab92fa85f86d83adfddae243afee85d3d133ada8fed9c679ba8ca3d6ee5aaabdbaabc269bb97bb82cc3ba8bdada6d559aabf88a6f664a1e88a96c85aa6b5a8d4f2258690009bed638f9ffbb1b77eb38dfca9b2608a95acb2ee6e94afab9bc75c94ec87b3b84bb48ca696f46f8e9786afd96181aa88aed253f68cbca6ea499a8b9dd4ea37e2a3; JSESSIONID-WYYY=tI8MIKMCRBuyCYnUJMCyUTlp%2Fufv5xIfCquvp7PJ4%2BuXod%5CXH%5CB0icDZw8TNlwHUHOW%2B2t%2BCuXyC4VZ%5C19OrzaDE%5Ck0F0dAZQh7KcVxUoHKpqUdiVzPu8NxCK9cJRG%5C%5CPTvtqxjFerd1%2BBa4%2F%5C8PESa4pvvRaQF6jljjsibX%5CrcPsH0I%3A1593347447142',
        }

    # 搜索歌曲接口
    API_Serch_Songs = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
    # 歌曲评论
    API_Comments_Song = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token=' # 音乐ID可替换
    # 歌曲歌词
    API_Lyric_Songs = 'https://music.163.com/weapi/song/lyric?csrf_token='

    # crypt_js_complex python 复写cryptjs
    def crypt_js_complex(self,text):
        BS = AES.block_size
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode('utf-8')
        unpad = lambda s: s[0:-s[-1]]

        key = bytes(self._i, encoding="utf-8")
        text = text.encode("utf-8")
        IV = b'0102030405060708'

        cipher = AES.new(key, mode=AES.MODE_CBC, IV=IV)
        # cipher2 = AES.new(key, mode=AES.MODE_CBC, IV=IV)  # 加密和解密，cipher对象只能用一次

        # print(text)
        encrypted = pad(text)
        # print(encrypted)
        encrypted = cipher.encrypt(encrypted)
        # print(encrypted)
        encrypted = base64.b64encode(encrypted).decode("utf-8")
        # print("第二次加密结果", encrypted)

        return encrypted

    # crypt_js_complex 的基础
    def crypt_js_complex_base(self,text):
        BS = AES.block_size
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode('utf-8')
        unpad = lambda s: s[0:-s[-1]]

        key = b'0CoJUm6Qyw8W8jud'
        text = text.encode("utf-8")
        IV = b'0102030405060708'

        cipher = AES.new(key, mode=AES.MODE_CBC, IV=IV)
        # cipher2 = AES.new(key, mode=AES.MODE_CBC, IV=IV)  # 加密和解密，cipher对象只能用一次

        # print(text)
        encrypted = pad(text)
        # print(encrypted)
        encrypted = cipher.encrypt(encrypted)
        # print(encrypted)
        encrypted = base64.b64encode(encrypted).decode("utf-8")
        # print("第一次加密结果", encrypted)
        return encrypted

    # 获得parms参数值
    def get_params(self,text):
        return self.crypt_js_complex(
            self.crypt_js_complex_base(text),)

    # 搜索歌曲接口
    def serch_songs(self,name,offset=0):
        """

        :param name:str
        :param offset:int 偏移量 默认第一页 例如 0 30 60 90
        :return 接口数据
        """
        text = '{"hlpretag":"<span class=\\"s-fc7\\">","hlposttag":"</span>","#/discover":"","s":"%s","type":"1","offset":"%s","total":"false","limit":"30","csrf_token":""}'%(name,offset*30)
        # payload = 'params={params}&encSecKey={encSecKey}'.format(params=self.get_params(text),encSecKey=self.encSecKey)
        print(text)
        params = (
            ('csrf_token', ''),
        )

        data = {
            'params': self.get_params(text),
            'encSecKey': self.encSecKey
        }
        print(data)
        response = requests.post(self.API_Serch_Songs, headers=self.headers, params=params,
                                 data=data)
        self._dispose(json.loads(response.text))

    # 歌曲评论抓取
    def comment_song(self,songid:str,offset:int=0):
        """"
        :param songid：str 歌曲ID
        :param offset：int 翻页 默认第一页 0 20 40
        :return 接口数据
        """
        text = '{"rid":"R_SO_4_%s","offset":"%s","total":"true","limit":"20","csrf_token":""}'%(songid,offset*20)


        params = (
            ('csrf_token', ''),
        )

        data = {
            'params': self.get_params(text),
            'encSecKey': self.encSecKey
        }
        response = requests.post(self.API_Comments_Song.format(songid), headers=self.headers,
                                 params=params, data=data)
        self._dispose(json.loads(response.text))
    # 歌词爬取
    def lyric_song(self,songid:str):
        """
        :param songid str 歌曲ID
        :return 接口数据
        """
        # 歌词接口加密参数原型
        text = '{"id":"%s","lv":-1,"tv":-1,"csrf_token":""}'%(songid)

        params = (
            ('csrf_token', ''),
        )

        data = {
            'params': self.get_params(text),
            'encSecKey': self.encSecKey
        }

        response = requests.post(self.API_Lyric_Songs, headers=self.headers, params=params, data=data)
        self._dispose(json.loads(response.text))

    # 处理爬虫获取到的数据，这里我就输出值
    def _dispose(self, data):
        pprint.pprint(data)
        return data

    # 主函数 测试
    def wangyi_main(self):
        # 搜索接口
        self.serch_songs("旧账",0)
        #歌曲评论接口
        # self.comment_song("25639331",0)
        # 歌词接口
        # self.lyric_song("1351615757") # 旧账
        pass
if __name__ == '__main__':
    wangyi = WangYiYun()
    wangyi.wangyi_main()

