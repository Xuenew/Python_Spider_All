# -*- coding:utf-8 -*-
# Chance favors the prepared mind.
# author : pyl owo,
# time : 2020/9/21
import json
import random
import re

from fake_useragent import UserAgent
from fontTools.ttLib import TTFont
from lxml import etree
import requests
from my_font_content import XYYTTFont

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
class SFQingNovel:
    def __init__(self, use_proxy=True):
        self.proxy = get_proxy() if use_proxy else None
        self.headers = {
            'User-Agent': UserAgent().random,
            "Proxy-Tunnel": str(random.randint(1, 10000)),
            'authority': 'book.qidian.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://www.qidian.com/',
            'accept-language': 'zh-CN,zh;q=0.9',
            # 'Cookie': 'newstatisticUUID=1600686041_884209914; _csrfToken=nXOEpjuFF7PUkwPJoOkBd7dTo2BV5jSkPu3suGGs'
        }
        # self.novel_url_pre = "https://t.shuqi.com/cover/"

    # 获取小说所有详细信息
    def get_novel_info(self, novel_url, **kwargs):
        respose = unify_requests(url=novel_url, headers=self.headers, proxies=self.proxy)
        search_result = self.parse_novel_info(respose, novel_url, **kwargs)
        return search_result

    def get_id(self, novel_url, **kwargs):
        return novel_url.split('/')[-1]

    def get_info(self, info_response, **kwargs):
        number_dict = {
            '.notdef': "薛忆阳",
            'period': '.',
            'zero': '0',
            'one': '1',
            'two': '2',
            'three': '3',
            'four': '4',
            'five': '5',
            'six': '6',
            'seven': '7',
            'eight': '8',
            'nine': '9',
        }
        response = info_response

        # 拿到下载字体的网址
        # @font-face.*?src: url.*?src: url(.*?) format('woff'),
        content = re.search(re.compile(r"@font-face.*?src: url.*?src: url(.*?)format.*?,", re.S), response.text)
        # ('https://qidian.gtimg.com/qd_anti_spider/yMxThZoL.woff')
        font_url = content.groups()[0].strip("( | )").strip("'")
        # print(font_url)

        font_content = unify_requests(url=font_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'}, proxies=self.proxy).content

        # with open('qidian_lx.woff', 'wb') as f:
        #     f.write(font_content)
        #
        # font1 = TTFont('qidian_lx.woff')
        # font1.saveXML('qidian_lx.xml')

        # 源码中提取十进制数据:

        data = re.findall(re.compile(
            r'<div class="book-info ">.*?<p>.*?<span class=".*?">(.*?)</span>.*?<span class=".*?">(.*?)</span>.*?<span class=".*?">(.*?)</span>.*?<span class=".*?">(.*?)</span>',
            re.S), response.text)[0]

        four_list = []
        # 遍历这四组数据
        for d in data:
            # print(d)  # 拿到元组中的一个  &#100152;&#100153;&#100153;&#100150;&#100157;&#100157;
            one_list = []
            d = d.split(';')  # 去除分号
            # 遍历每组数据
            for x in d:
                res = x.replace('&#', '')
                if res:  # 判断是否有空格有的话不转化
                    # 将res十进制转化成16进制
                    a = int(res)  # 先转化成int类型
                    one_list.append(a)

            four_list.append(one_list)
        map_dict = XYYTTFont(font_content).getBestCmap()
        # print(map_dict)
        result_list = []
        # 遍历含有四组数据的列表
        for one in four_list:
            two_string = ""
            # 遍历每一组数据
            for a in one:
                # print("a",a)
                if a in map_dict:
                    number = map_dict[a]  # 找到对应的键
                    number = number_dict[number]  # 通过键找到对应的值
                    # print(number)
                    two_string += number

            result_list.append(two_string)
        return result_list
    def get_int_num(self, numstr):
        if '.' in numstr:
            return int(numstr.replace('.','')) * 100
        else:
            return int(numstr)
    # 搜索视频响应解析
    def parse_novel_info(self, respose_info, novel_url='', **kwargs) -> dict:
        try:
            # print(novel_url)
            response_data = etree.HTML(respose_info.text)
            info_list = self.get_info(respose_info, **kwargs)
        except Exception as e:
            print(e)
            return {}
        else:
            # info_book_dict = info_dict.get('book', {})
            novel_dict = dict()
            novel_dict['all_recommend_str'] = self.get_int_num(info_list[2])  # 总推荐数 str book_interact
            novel_dict['month_recommend_str'] = None  # 月推荐数 str
            novel_dict['week_recommend_str'] = self.get_int_num(info_list[3])  # 周推荐数 str
            novel_dict['all_read_int'] = None  # 总阅读数 int
            novel_dict['month_read_int'] = None  # 月阅读数 int
            novel_dict['week_read_int'] = None  # 周阅读数 int
            novel_dict['all_words_number_int'] = self.get_int_num(info_list[0]) # 总字数
            novel_dict['book_status_str'] = response_data.xpath('//p[@class="tag"]/span/text()')[0]  # 书籍状态 （连载，完结，暂无）bookCP
            novel_dict['book_property_str'] = response_data.xpath('//p[@class="tag"]/span/text()')[1] # 书籍属性 （免费，会员，限免）
            novel_dict['author_type_str'] = "".join(response_data.xpath('//div[@class="author-photo"]/span/text()')) # 作者类型 （金牌，签约，独立 默认无）
            novel_dict['book_type_str'] = '|'.join(response_data.xpath('//p[@class="tag"]/a/text()'))  # 书籍分类 （玄幻 ,科幻，言情...）按搜索结果来多个按｜分割
            novel_dict['book_update_time'] = ''.join(response_data.xpath('//li[@class="update"]/div/p[@class="cf"]/em/text()'))  # 书籍更新日期 年-月-日
            novel_dict['book_zong_zhang_jie_int'] = ''  # 书籍总的章节 完结的，未完结就填目前的总章节
            novel_dict['book_zui_xin_zhang_jie_name_str'] = ''.join(response_data.xpath('//li[@class="update"]/div/p[@class="cf"]/a/text()')) # 最新章节名称
            novel_dict['book_introduce_text'] =  ''.join(response_data.xpath('//div[@class="book-intro"]/p//text()')).replace(' ', '').replace('\u3000', '').replace('\r', '').replace('\n', '').replace('\t', '') # 书籍简介 text
            novel_dict['book_lable_str'] = '|'.join(response_data.xpath('//p[@class="tag"]/a/text()')) # 书籍标签 （用｜分割的字符串 ''科幻｜现实｜励志''）
            novel_dict['book_cover_image_str'] = "https:" + "".join(response_data.xpath('//div[@class="book-information cf"]/div[@class="book-img"]/a/img/@src')).replace('\n', '') # 书籍封面 URL
            novel_dict['book_detail_url_str'] = novel_url  # 书籍详情URL
            novel_dict['book_detail_id_int'] = None  # 书籍详情ID 数字形式
            novel_dict['book_detail_id_str'] = None  # 书籍详情ID 字符形式
            novel_dict['book_zhan_dian_str'] = None  # 书籍站点 （男生，女生，暂无）
            novel_dict['book_publish_str'] = '起点中文网'  # 出版社 默认侵权平台'
            novel_dict['book_commeds_int'] = None  # 书籍评论数 Pinglunfont
            novel_dict['author_grade_float'] = None  # 作者评分
            novel_dict['author_id_str'] =  None # 作者ID 字符形式 ## 新增
            novel_dict['author_page_url_str'] = "https:" + ''.join(response_data.xpath('//a[@class="writer"]/@href')) # 作者主页链接 userId
            author_info_data = response_data.xpath('//ul[@class="work-state cf"]/li/em/text()')
            novel_dict['author_book_number_int'] = author_info_data[0]  # 作者书籍总数
            novel_dict['author_likes_int'] = None  # 作者获赞总数
            novel_dict['author_all_words_number_str'] = author_info_data[1]  # 作者累计创作字数
            novel_dict['author_produce_days_str'] = author_info_data[2]  # 作者累计创作天数
            novel_dict['author_fens_number_int'] = None  # 作者粉丝数
            novel_dict['author_head_image_url_str'] = "https:" + "".join(response_data.xpath('//div[@class="author-photo"]/a/img/@src'))  # 作者头像URL
            # novel_dict[''] = ''  #
            return novel_dict


# 统一的调用 search_novels
search_novel_info = SFQingNovel(use_proxy=True).get_novel_info
if __name__ == "__main__":
    result = search_novel_info('https://book.qidian.com/info/1010734492')
    print(result)
