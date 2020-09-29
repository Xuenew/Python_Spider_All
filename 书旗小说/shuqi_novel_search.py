# -*- coding:utf-8 -*-
# Chance favors the prepared mind.
# author : pyl owo,
# time : 2020/9/21
import datetime
import json
import random
import re
import time
from hashlib import md5

from fake_useragent import UserAgent
import requests
# 获取代理
def get_proxy():
    pass

# 统一请求函数
def unify_requests(method="GET",url="",headers={},proxies={},data={},verify=False,cookies={}):
    if method=="GET":
        response = requests.get(url, headers=headers,proxies=proxies,data=data,cookies=cookies,timeout=5)
        return response
    else:
        response = requests.post(url, headers=headers,proxies=proxies,data=data,verify=verify,cookies=cookies,timeout=5)
        return response

# 书旗小说
class SFQingNovel:
    def __init__(self, use_proxy=True):
        self.proxy = get_proxy() if use_proxy else None
    """:cvar
    有三点反爬，
    1，禁用右键
    2，sign
    3，headers里的 authorization 属性
    """

############################################################
    # Md5 加密函数 32 返回32位的加密结果
    def md5_use(self, text: str) -> str:
        result = md5(bytes(text, encoding="utf-8")).hexdigest()
        # print(result)
        return result

    # 获取加密 sign timestamp
    def shuqi_jiami(self, book_id: str, time_stamp: str = str(int(time.time())), use_pwd='37e81a9d8f02596e1b895d07c171d5c9',
                    user_id="8000000"):
        """    function i(t, n, e) {
            var o = Object.keys(t).filter(function(t) {
                return !Array.isArray(n) || -1 !== n.indexOf(t)
            }).sort().map(function(n) {
                return t[n]
            }).join("") + (e || n);
            return a()(o)
        }"""
        """"""
        # 改写规则就是简单的拼接 艹
        info = self.md5_use(book_id + time_stamp + user_id + use_pwd)
        # 打印 sign 时间戳 以及 书籍ID
        # print(info,book_id,time_stamp)
        return info

    # 获得 authorization 的值 （在请求里面 需要re）
    def shuqi_get_header_token(self, book_id: str):
        # response = requests.get("https://t.shuqi.com/cover/{}".format(book_id))
        response = unify_requests(url="https://t.shuqi.com/cover/{}".format(book_id), proxies=self.proxy)
        # print(response.text)
        token = re.findall(r'"token":"(.*?)"', response.text)
        token = token[0] if token else ""
        if token:
            # print(token)
            return token
        else:
            return ""







#####################################3 以上👆 加密

    # 获得响应
    def get_response(self, novel_url,  time_stamp: str = str(int(time.time())), user_id: str = "8000000", **kwargs):
        if kwargs.get('qin_quan_id_int'):
            bookId = str(kwargs.get('qin_quan_id_int'))
        elif novel_url:
            bookId = str(novel_url).split('?')[0].split('/')[-1]
        else:
            return {}
        # print(bookId)
        token = self.shuqi_get_header_token(bookId)
        if token:
            pass
        else:
            print("获取token authorization 失败")
            return False
        headers = {
            'User-Agent': UserAgent().random,
            "Proxy-Tunnel": str(random.randint(1, 10000)),
            'authority': 'ocean.shuqireader.com',
            'accept': 'application/json, text/plain, */*',
            # 'authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI4MDAwMDAwIiwidXRkaWQiOiIiLCJpbWVpIjoiIiwic24iOiIiLCJleHAiOjE2MDA4NDgyNTYsInVzZXJJZCI6IjgwMDAwMDAiLCJpYXQiOjE2MDA4MzAyNTYsIm9haWQiOiIiLCJwbGF0Zm9ybSI6IjAifQ.tjgtZMMoMWCoA7Z-z1M55d7MUEFy4GjruQoeoyAOnSWYy1glqk-YkEbOHfX6oSH_3T-bhF0NKz6-4If4gSKz1A',
            'authorization': "Bearer " + self.shuqi_get_header_token(bookId),
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Mobile Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://t.shuqi.com',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://t.shuqi.com/cover/7027302',
            'accept-language': 'zh-CN,zh;q=0.9',
        }

        data = {
            'user_id': '%s' % (user_id),
            'bookId': '%s' % (bookId),
            'timestamp': '%s' % (time_stamp),
            'sign': '%s' % (self.shuqi_jiami(bookId, time_stamp, user_id=user_id)),
            'platform': '0'
        }
        # print(headers,data)
        # response = requests.post('https://ocean.shuqireader.com/webapi/bcspub/openapi/book/info', headers=headers,
        #                          data=data)
        response = unify_requests(url="https://ocean.shuqireader.com/webapi/bcspub/openapi/book/info", method="POST", headers=headers, data=data, proxies=self.proxy)
        # print(json.loads(response.text))
        return response

    # 获取小说所有详细信息
    def get_novel_info(self, novel_url, **kwargs):
        search_result = self.parse_novel_info(self.get_response(novel_url, **kwargs), novel_url, **kwargs)
        return search_result


    # 获取评论数
    def get_comment(self, novel_url, **kwargs):
        if kwargs.get('qin_quan_id_int'):
            bookId = str(kwargs.get('qin_quan_id_int'))
        elif novel_url:
            bookId = str(novel_url).split('?')[0].split('/')[-1]
        else:
            return {}
        token = self.shuqi_get_header_token(bookId)
        if token:
            pass
        else:
            print("获取token authorization 失败")
            return False
        headers = {
            'User-Agent': UserAgent().random,
            "Proxy-Tunnel": str(random.randint(1, 10000)),
            'authority': 'ocean.shuqireader.com',
            'accept': 'application/json, text/plain, */*',
            'authorization': "Bearer " + self.shuqi_get_header_token(bookId),
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            'origin': 'https://t.shuqi.com',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://t.shuqi.com/',
            'accept-language': 'zh-CN,zh;q=0.9',
            # 'Cookie': 'XSRF-TOKEN=1f1a10da-49bc-44eb-a39a-8fc19e44f8a0'
        }

        info_base_url = "https://ocean.shuqireader.com/webapi/comment/novel/i.php?do=sp_get&bookId={}&fetch=merge&sqUid=8000000&source=store&size=3&page=1&score=yes&authorId=8000000"  # 129676 数字id

        if kwargs.get('qin_quan_id_int'):
            respose_info = unify_requests(url=info_base_url.format('kwargs.get("qin_quan_id_int")'),
                                     headers=headers, proxies=self.proxy)
        elif novel_url:
            # print(info_base_url.format((str(novel_url).split('?')[0].split('/')[-1])))
            respose_info = unify_requests(url=info_base_url.format((str(novel_url).split('?')[0].split('/')[-1])),
                                     headers=headers, proxies=self.proxy)
        else:
            return {}
        return respose_info

    # 搜索视频响应解析
    def parse_novel_info(self, respose_info, novel_url='', **kwargs) -> dict:
        try:
            print(novel_url)
            response_dict = json.loads(respose_info.text).get('data', {})
            comment_dict = json.loads(self.get_comment(novel_url, **kwargs).text)
        except Exception as e:
            print(e)
            return {}
        else:
            # info_book_dict = info_dict.get('book', {})
            novel_dict = dict()
            # ''.join(response_data.xpath(''))
            # response_dict.get('', '')
            novel_dict['all_recommend_str'] = None  # 总推荐数 str
            novel_dict['month_recommend_str'] = None  # 月推荐数 str
            novel_dict['week_recommend_str'] = None  # 周推荐数 str
            novel_dict['all_read_int'] = None  # 总阅读数 int
            novel_dict['month_read_int'] = None  # 月阅读数 int
            novel_dict['week_read_int'] = None  # 周阅读数 int
            novel_dict['all_words_number_int'] = int(float(response_dict.get('wordCount', '')) * 10000) if response_dict.get('wordCount', '') else None # 总字数
            book_status = response_dict.get('state', '')
            if book_status == "1":
                book_status_str = "连载"
            elif book_status == "2":
                book_status_str = "完结"
            else:
                book_status_str = "暂无"
            novel_dict['book_status_str'] = book_status_str # 书籍状态 （连载，完结，暂无）bookCP
            novel_dict['book_property_str'] = None # 书籍属性 （免费，会员，限免）
            novel_dict['author_type_str'] = None # 作者类型 （金牌，签约，独立 默认无）
            novel_dict['book_lable_str'] = "|".join([i.get('tagName') for i in response_dict.get('tag', [])]) # 书籍标签 （用｜分割的字符串 ''科幻｜现实｜励志''）
            novel_dict['book_type_str'] = None # 书籍分类 （玄幻 ,科幻，言情...）按搜索结果来多个按｜分割
            novel_dict['book_update_time'] = datetime.datetime.strftime(datetime.datetime.fromtimestamp(response_dict.get('lastChapter', {}).get('updateTime')), "%Y-%m-%d") # 书籍更新日期 年-月-日
            novel_dict['book_zong_zhang_jie_int'] = None # 书籍总的章节 完结的，未完结就填目前的总章节
            novel_dict['book_zui_xin_zhang_jie_name_str'] = response_dict.get('lastChapter', {}).get('updateTime') # 最新章节名称
            novel_dict['book_introduce_text'] = response_dict.get('desc', '') # 书籍简介 text
            novel_dict['book_cover_image_str'] = response_dict.get('imgUrl', '')  # 书籍封面 URL imgUrl
            novel_dict['book_detail_url_str'] = novel_url  # 书籍详情URL
            novel_dict['book_detail_id_int'] = response_dict.get('bookId', '') # 书籍简介 text  # 书籍详情ID 数字形式 bookId
            novel_dict['book_detail_id_str'] = str(response_dict.get('bookId', ''))  # 书籍详情ID 字符形式
            novel_dict['book_zhan_dian_str'] = None  # 书籍站点 （男生，女生，暂无）
            novel_dict['book_publish_str'] = '书旗小说'  # 出版社 默认侵权平台'
            novel_dict['book_commeds_int'] = comment_dict.get('info', {}).get('total')  # 书籍评论数
            novel_dict['author_grade_float'] = None  # 作者评分
            novel_dict['author_id_str'] = str(response_dict.get('authorId', '')) # 作者ID 字符形式 ## 新增 authorId
            novel_dict['author_page_url_str'] = None  # 作者主页链接 userId
            novel_dict['author_book_number_int'] = None  # 作者书籍总数
            novel_dict['author_likes_int'] = None  # 作者获赞总数
            novel_dict['author_all_words_number_str'] = None  # 作者累计创作字数
            novel_dict['author_produce_days_str'] = None  # 作者累计创作天数
            novel_dict['author_fens_number_int'] = None  # 作者粉丝数
            novel_dict['author_head_image_url_str'] = response_dict.get('authorIcon', '')  # 作者头像URL authorIcon
            return novel_dict


# 统一的调用 search_novels
search_novel_info = SFQingNovel(use_proxy=False).get_novel_info
if __name__ == "__main__":
    result = search_novel_info('https://t.shuqi.com/cover/7329628')
    print(result)