# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2022/6/9
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64

# 作者主页字符ID转数字ID
def uid2eid(uid):
    """ 用户数字ID 加密为 字符串ID"""
    return encrypt(uid, type_str=1)

# 视频字符ID转数字ID
def uid2vid(uid):
    """ 视频数字ID 加密为 字符串ID """
    return encrypt(uid, type_str=2)

# 字符串转int
def eid2uid(eid,type_str:int):
    """ 字符串ID 解密为 数字ID """
    uid = ""
    if type_str==1:
        uid = int(str_to_int(eid[1:]))/4
    elif type_str==2:
        uid = int(str_to_int(eid[4:]))/4

    return str(int(uid))

# 字符串形式转ID的方法 bs64
def str_to_int(eid:str):
    uid = base64.b64decode(eid).decode()
    return uid

# 数字转换字符串形式的
def encrypt(int_id:int, type_str:int):
    num = str(int(int_id)*4)
    eid = base64.b64encode(num.encode()).decode()
    if type_str==1:
        return "U"+eid
    elif type_str==2:
        return "id_X"+eid

if __name__ == '__main__':
    # 1/作者主页 2/视频
    print(eid2uid("UODExNjMwNTc1Ng==",1))
    # print(uid2eid("1596252942"))
