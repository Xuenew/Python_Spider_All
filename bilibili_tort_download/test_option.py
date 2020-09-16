# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/9/3

"""":cvar
哔哩哔哩的下载 得到链接之后 分两步骤才能下载，先去请求资源才能第二次请求能够下载
"""


import requests
import requests
from Task_Compar_Config import Config_Of_Compar as config

def get_bilibili_mv(url1,file_name):
    # url1 为视频链接、url2为音频链接
    url1 = url1
    # url1= "http://upos-sz-mirrorcos.bilivideo.com/upgcxcode/64/99/225729964/225729964-1-30032.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1599107607&gen=playurl&os=cosbv&oi=2071626969&trid=fc4a664251e348bfae7da2965b4d51b4u&platform=pc&upsig=9ef15d6944e230f40c4802ef1330e4cb&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mid=0&orderid=0,3&agrr=0&logo=80000000"
    # url2='http://upos-hz-mirrorks3u.acgvideo.com/upgcxcode/03/88/98958803/98958803-1-30216.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1579519469&gen=playurl&os=ks3u&oi=1971869869&trid=99ee525d6c7f4bc8a414a537797e31f3u&platform=pc&upsig=ce817a7120709c60ac43cf095de05c8d&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mid=352741151'
    headers1={
        'Host': 'cn-hbwh2-cmcc-bcache-04.bilivideo.com',
        'Connection': 'keep-alive',
        'Access-Control-Request-Method': 'GET',
        'Origin': 'https://www.bilibili.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3970.5 Safari/537.36',
        'Access-Control-Request-Headers': 'range',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Referer': 'https://www.bilibili.com/video/av56643958?t=262',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    headers2={
        'Host': 'cn-hbwh2-cmcc-bcache-04.bilivideo.com',
        'Connection': 'keep-alive',
        'Origin': 'https://www.bilibili.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3970.5     Safari/537.36',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Referer': 'https://www.bilibili.com/video/av56643958?t=262',
        'Accept-Encoding': 'identity',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Range': 'bytes=0-907',
        'Range': 'bytes=0-4639000'
    }
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
    session=requests.session()
    session.options(url=url1,headers=headers1,proxies=proxies)
    res=session.get(url=url1,headers=headers2,proxies=proxies)
    # print(res)
    if res.status_code==206:
        # print(res.content)
        print("ok")
        with open('{}.mp4'.format(file_name),'wb') as fp:
            fp.write(res.content)
            fp.flush()
            fp.close()


def get_qq_mv(url1,file_name):
    res=requests.get(url=url1)
    # print(res)
        # print(res.content)
    print("ok")
    with open('{}.mp4'.format(file_name),'wb') as fp:
        fp.write(res.content)
        fp.flush()
        fp.close()

if __name__ == '__main__':
    qqurl = "http://mv.music.tc.qq.com/6CB11930B0C08927CDC6106C253ED882C374CFA8B7CF17A41365129AA21276033C190AF148D54C15C9D80FC497059CC7ZZqqmusic_default/1049_M21073590036WZlj1aAg5F1001549149.f20.mp4?fname=1049_M21073590036WZlj1aAg5F1001549149.f20.mp4"
    bilibiliurl = 'http://upos-sz-mirrorks3.bilivideo.com/upgcxcode/34/65/65676534/65676534-1-30280.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1599189325&gen=playurl&os=ks3bv&oi=2071626969&trid=330755295f4b45fea23c6a80f308466au&platform=pc&upsig=307b4e2a1b3d07cf1b7b1d84f38a4478&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mid=0&orderid=0,3&agrr=1&logo=80000000'
    # get_qq_mv(qqurl,"wbl_qq")
    get_bilibili_mv(bilibiliurl,"wbl_bili")



    """":cvar
    
    {'down_load_url_list': [['http://upos-sz-mirrorhw.bilivideo.com/upgcxcode/34/65/65676534/65676534-1-30032.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1599189325&gen=playurl&os=hwbv&oi=2071626969&trid=330755295f4b45fea23c6a80f308466au&platform=pc&upsig=63654e451e3d02050bba19beea41c132&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mid=0&orderid=0,3&agrr=1&logo=80000000'], 
    ['http://upos-sz-mirrorks3.bilivideo.com/upgcxcode/34/65/65676534/65676534-1-30280.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1599189325&gen=playurl&os=ks3bv&oi=2071626969&trid=330755295f4b45fea23c6a80f308466au&platform=pc&upsig=307b4e2a1b3d07cf1b7b1d84f38a4478&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mid=0&orderid=0,3&agrr=1&logo=80000000']]}

    """