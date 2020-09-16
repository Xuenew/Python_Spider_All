# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/9/02
import random
from you_get.common import *
import requests
from Task_Compar_Config import Config_Of_Compar as config
from Task_Compar_Config import proxies
from fake_useragent import UserAgent
from task_tool_unit import match1
from tort_download_unit.bilibili_tort_download.bilibili_ocr import _get_toke_and_img
from tort_download_unit.bilibili_tort_download.bilibili_download_base import download_urls # 给出下载链接 下载

stream_types = [
    {'id': 'flv_p60', 'quality': 116, 'audio_quality': 30280,
     'container': 'FLV', 'video_resolution': '1080p', 'desc': '高清 1080P60'},
    {'id': 'hdflv2', 'quality': 112, 'audio_quality': 30280,
     'container': 'FLV', 'video_resolution': '1080p', 'desc': '高清 1080P+'},
    {'id': 'flv', 'quality': 80, 'audio_quality': 30280,
     'container': 'FLV', 'video_resolution': '1080p', 'desc': '高清 1080P'},
    {'id': 'flv720_p60', 'quality': 74, 'audio_quality': 30280,
     'container': 'FLV', 'video_resolution': '720p', 'desc': '高清 720P60'},
    {'id': 'flv720', 'quality': 64, 'audio_quality': 30280,
     'container': 'FLV', 'video_resolution': '720p', 'desc': '高清 720P'},
    {'id': 'hdmp4', 'quality': 48, 'audio_quality': 30280,
     'container': 'MP4', 'video_resolution': '720p', 'desc': '高清 720P (MP4)'},
    {'id': 'flv480', 'quality': 32, 'audio_quality': 30280,
     'container': 'FLV', 'video_resolution': '480p', 'desc': '清晰 480P'},
    {'id': 'flv360', 'quality': 16, 'audio_quality': 30216,
     'container': 'FLV', 'video_resolution': '360p', 'desc': '流畅 360P'},
    # 'quality': 15?
    {'id': 'mp4', 'quality': 0},

    {'id': 'jpg', 'quality': 0},
]
dry_run = False
json_output = False
force = False
skip_existing_file_size_check = False
player = None
extractor_proxy = None
cookies = None
output_filename = None
auto_rename = False
insecure = False
import ssl
import socket
import logging
from urllib import request,  error

def urlopen_with_retry(*args, **kwargs):
    retry_time = 3
    for i in range(retry_time):
        try:
            if insecure:
                # ignore ssl errors
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                return request.urlopen(*args, context=ctx, **kwargs)
            else:
                return request.urlopen(*args, **kwargs)
        except socket.timeout as e:
            logging.debug('request attempt %s timeout' % str(i + 1))
            if i + 1 == retry_time:
                raise e
        # try to tackle youku CDN fails
        except error.HTTPError as http_error:
            logging.debug('HTTP Error with code{}'.format(http_error.code))
            if i + 1 == retry_time:
                raise http_error
# 通过url下载哔哩哔哩文件
def bilibili_download_urls(bili_url, title, ext='mp4',proxies=proxies,output_dir=config["system_path"]+"/"+config["tort_path"])->"bool":

    try:
        urls, size = bilibili_down_load(bili_url, proxy=proxies)
        if isinstance(urls,list): # 正常情况
            if urls: # ocr识别成功
                headers = bilibili_headers(referer=bili_url)
                download_urls(urls, title, ext, size, headers=headers,
                                      output_dir=output_dir,
                                      merge=True,
                                      av=True
                                      )
                return True
            else:
                return False
        if isinstance(urls,int): # 错误的情况
            return urls # 错误情况返回错误代码

    except Exception as e:
        print(e)
        return False
# 哔哩哔哩的头 headers
def bilibili_headers(referer=None, cookie=None):
    # a reasonable UA
    # ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    ua = '{}'.format(UserAgent().random)
    # print(ua)
    headers = {'Accept': '*/*', 'Accept-Language': 'en-US,en;q=0.5', 'User-Agent': ua}
    if referer is not None:
        headers.update({'Referer': referer})
    if cookie is not None:
        headers.update({'Cookie': cookie})
    return headers

# 哔哩哔哩下载地址
def bilibili_down_load(bili_url,proxy=proxies):
    # 仿照 you-get
    stream_qualities = {s['quality']: s for s in stream_types}
    headers = {
        "Proxy-Tunnel": str(random.randint(1, 10000)),
        'authority': 'www.bilibili.com',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        # 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        "user-agent": UserAgent().random,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://search.bilibili.com/all?keyword=beatbox&from_source=nav_search&spm_id_from=333.851.b_696e7465726e6174696f6e616c486561646572.9&order=totalrank&duration=0&tids_1=3&tids_2=193',
        'accept-language': 'zh-CN,zh;q=0.9',
        # '$cookie': 'CURRENT_FNVAL=16; _uuid=39019883-BF03-8583-5980-65F1AB32A8B437048infoc; buvid3=A1AF6CF2-8DE1-41D4-82FA-331AAF700F4953938infoc; rpdid=|(u)~lJ|l|lJ0J\'ul))Y)m)uu; LIVE_BUVID=AUTO4115905671332477; sid=lubz9xqt; DedeUserID=101681207; DedeUserID__ckMd5=dfc9ce597d1ee703; SESSDATA=4e33cf62%2C1609722422%2Ca87cf*71; bili_jct=96dcdd930c28d4d499acbf1c31b4ebb7; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1594256989; PVID=1; bsource=search_baidu; finger=351232418; blackside_state=1',
    }

    if proxy:
        response = requests.get(bili_url, headers=headers)

    else:
        response = requests.get(bili_url, headers=headers,proxies=proxy)

    # print(response.text)
    playinfo_text_ = match1(response.text, r'__playinfo__=(.*?)</script><script>')  # FIXME
    playinfo_ = json.loads(playinfo_text_) if playinfo_text_ else None
    if playinfo_ is None:
        print("需要ocr 识别的时刻来临了！！！！")
        statu_code,erro_info = _get_toke_and_img(url=bili_url)
        return statu_code,erro_info
    # print(playinfo_)
    playinfo = playinfo_
    if playinfo and "data" in playinfo:
        quality = playinfo['data']['quality']

        if 'durl' in playinfo['data']:
            src, size = [], 0
            for durl in playinfo['data']['durl']:
                src.append(durl['url'])
                size += durl['size']
            # print(src)
            return src,size
        # DASH formats
        if 'dash' in playinfo['data']:
            audio_size_cache = {}
            # print(playinfo)
            for video in playinfo['data']['dash']['video']:
                if video['id'] == playinfo['data']["quality"]:
                    # prefer the latter codecs!
                    s = stream_qualities[video['id']]
                    format_id = 'dash-' + s['id']  # prefix
                    container = 'mp4'  # enforce MP4 container
                    desc = s['desc']
                    audio_quality = s['audio_quality']
                    baseurl = video['baseUrl']
                    headers["referer"] = bili_url
                    size = url_size(baseurl, headers=bilibili_headers(referer=bili_url))

                    # find matching audio track
                    if playinfo['data']['dash']['audio']:
                        audio_baseurl = playinfo['data']['dash']['audio'][0]['baseUrl']
                        for audio in playinfo['data']['dash']['audio']:
                            if int(audio['id']) == audio_quality:
                                audio_baseurl = audio['baseUrl']
                                break
                        if not audio_size_cache.get(audio_quality, False):
                            headers = bilibili_headers(referer=bili_url)
                            audio_size_cache[audio_quality] = url_size(audio_baseurl,
                                                                            headers=headers)
                        size += audio_size_cache[audio_quality]

                        return [[baseurl], [audio_baseurl]],size

                    return [[baseurl]],size

down_load_videos = bilibili_download_urls

if __name__ == '__main__':
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
    # 代理
    # link = bilibili_down_load(bili_url="https://www.bilibili.com/video/BV1Kp4y1i7Nj?from=search&seid=2986944384836383482",proxy=proxies)
    # av
    # link = bilibili_down_load(bili_url="http://www.bilibili.com/video/av37366708",proxy=proxies)
    # link = bilibili_down_load(bili_url="http://www.bilibili.com/video/av16431951",proxy={})
    # bilibili_down_load(bili_url="https://www.bilibili.com/video/BV1aJ41127vy?spm_id_from=333.851.b_62696c695f7265706f72745f646f756761.30",proxy=proxies)# 十分钟视频
    # 无代理
    # link = bilibili_down_load(bili_url="https://www.bilibili.com/video/BV1Kp4y1i7Nj?from=search&seid=2986944384836383482",proxy={})
    # link = bilibili_down_load(bili_url="http://www.bilibili.com/video/av87539984",proxy={})
    # print(link)
    bilibili_download_urls(bili_url="https://www.bilibili.com/video/av370511961",proxies=proxies,title="testyiyang",output_dir="/Users/quanlifang/Desktop/和晞科技/hexikeji_all/video_compar_zhuanxiang_bili_v001")
    # bilibili_download_urls(bili_url="http://www.bilibili.com/video/av16431951",proxies=proxies,title2="test",output_dir2="/Users/quanlifang/Desktop/和晞科技/hexikeji_all/video_compar_zhuanxiang_bili_v001",**{"info_only": False,
    #                                                                              "output_dir": '/Users/quanlifang/Desktop/和晞科技/hexikeji_all/video_compar_zhuanxiang_bili_v001',
    #                                                                              "merge": True,"title":"test"})


"[['http://cn-sdjn3-cu-v-02.bilivideo.com/upgcxcode/15/58/26805815/26805815_da3-1-30016.m4s?expires=1599214538&platform=pc&ssig=lc6dWrqaFPgoFZWasJFncg&oi=2071626969&trid=92a4238864304b1ba41c007e27ea8cb5u&nfc=1&nfb=maPYqpoel5MI3qOUX6YpRA==&cdnid=8164&mid=0&cip=27.221.127.131&orderid=0,3&agrr=1&logo=80000000'], " \
"['http://cn-sdyt-cu-v-06.bilivideo.com/upgcxcode/15/58/26805815/26805815_da3-1-30216.m4s?expires=1599214538&platform=pc&ssig=N52xrFSMhZKHo_skWDQLfQ&oi=2071626969&trid=92a4238864304b1ba41c007e27ea8cb5u&nfc=1&nfb=maPYqpoel5MI3qOUX6YpRA==&cdnid=1936&mid=0&cip=61.156.196.135&orderid=0,3&agrr=1&logo=80000000']]" \
" xxxjxxxxx mp4 15535851"