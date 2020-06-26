# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/6/25

from hashlib import md5

# 获取加密字符串_s
def _get_params__s(api,_q) -> str:
    '''
    :param api: URL的地址     /api/search/searchSongs
    :param _q:  需要加密的参数     {"key":"在希望的田野上","pagingVO":{"page":2,"pageSize":30}}
    :param xm_sg_tk cookie xm_sg_tk去掉是时间戳得值     7f2df3233537f81aae848dc4f47bdeb8
    :return: 加密字符串
    '''
    xm_sg_tk = '7f2df3233537f81aae848dc4f47bdeb8' #
    data = xm_sg_tk + "_xmMain_" + api + "_" + _q
    # data = '7f2df3233537f81aae848dc4f47bdeb8_xmMain_/api/search/searchSongs_{"key":"在希望的田野上","pagingVO":{"page":2,"pageSize":30}}'
    # data = 'e2853d0e0c49aab4a44dce64fd26b4ba_xmMain_/api/search/searchSongs_{"key":"在希望的田野上","pagingVO":{"page":1,"pageSize":30}}'
    return md5(bytes(data, encoding="utf-8")).hexdigest()


print(_get_params__s())