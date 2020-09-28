# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/9/3
import json

import requests
from lxml import etree
from tort_download_unit.baidu_img_ocr import general_word # have
from fake_useragent import UserAgent

test_url = ""
headers = {
    'authority': 'www.bilibili.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    # 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    "user-agent": UserAgent().random,
        }

# 获得 验证码图片 和对应的input框值
def _get_toke_and_img(url):
    res =requests.get(url=url,headers=headers)
    res.apparent_encoding
    select = etree.HTML(res.text)
    # print(res.text)
    info = "".join(select.xpath("//div[@class='txt-item']//text()")) # 是否含有，人机识别
    info2 = "".join(select.xpath("//div[@class='error-text']//text()")) # 是否含有，视频不见了
    # img_base64 = select.xpath("//div[@class='box-pic']/img/@src")
    # img_base64 = img_base64[0] if img_base64 else ""
    if "The request was rejected because of the bilibili security control policy" in info: # 人机识别
        headers["Referer"] = url
        img_base64 = requests.get("https://sec.biliapi.net/th/captcha/get", headers=headers)
        img_base64 = img_base64.text
        # true = True
        # false = False
        # none = None
        # Null = None
        # print(type(eval(img_base64)))
        # img_base64 = eval(json.loads(img_base64))["data"]["captcha"]["imageBase64String"]
        json_text = json.loads(img_base64)
        # print(json_text)
        img_base64 = json_text["data"]["captcha"]["imageBase64String"]
        # token = "".join(select.xpath("//input[@id='hidden-input']/@value"))
        token = json_text["data"]["captcha"]["token"]
        # print(img_base64,token)
        # print(info)

        print("需要有人机校验")
        if img_base64:
            print("图片有base64")
            # print(img_base64)
            img_words = general_word(img_base64)
            # print("token是 = {} 识别的图片是 = {}".format(token,img_words))
            # print("识别的图片是 {}".format(img_words))
            clear_orc(token=token,key=img_words)
            return 0,0
        else:
            # print("没抓到base64")
            return 0,0
    elif "视频不见了" in info2: # 新的情况  下架
        print("视频不见了!!!")
        return -888,0
    else:
        print("没有人机校验这个东西 是否找到？？/",info,info2)
        return 0,0
# 验证码解决
def clear_orc(token,key):
    url = "https://sec.biliapi.net/th/captcha/check"

    payload = 'token={token}&key={key}'.format(token=token,key=key)
    headers = {
      'Connection': 'keep-alive',
      'Accept': '*/*',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
      'Content-Type': 'application/x-www-form-urlencoded',
      'Origin': 'https://www.bilibili.com',
      'Sec-Fetch-Site': 'cross-site',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Dest': 'empty',
      'Referer': 'https://www.bilibili.com/video/av37366708',
      'Accept-Language': 'zh-CN,zh;q=0.9'
    }

    response = requests.request("POST", url, headers=headers, data = payload)

    # print(response.text)
    dic_info = json.loads(response.text)
    if dic_info["code"] != -1:
        print("token是 = {} 识别的图片是 = {}".format(token, key))
        print("哔哩哔哩 识别成功！！！")
        return True
    else:
        print("token是 = {} 识别的图片是 = {}".format(token, key))
        print("哔哩哔哩 识别失败 请重试！！！")
        print(response.text)
        return False
if __name__ == '__main__':
    # clear_orc(token="TloYSj55", key="rsab")
    # clear_orc(token="BJ3Bgt8D", key="6att")
    # exit(0)
    general_word("")