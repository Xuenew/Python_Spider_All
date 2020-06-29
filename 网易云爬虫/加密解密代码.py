# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/6/28
from Crypto.Cipher import AES
import base64

# 加密
def py_aes_first(text):
    BS = AES.block_size
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode('utf-8')
    unpad = lambda s : s[0:-s[-1]]

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
    print("第一次加密结果",encrypted)
    return encrypted
def py_aes_second(text):
    BS = AES.block_size
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode('utf-8')
    unpad = lambda s : s[0:-s[-1]]

    key = b'TXhkKroQJSgrKrnN'
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
    print("第二次加密结果",encrypted)

    key = b'0CoJUm6Qyw8W8jud'
    text = encrypted
    IV = b'0102030405060708'

    cipher = AES.new(key, mode=AES.MODE_CBC, IV=IV)

    return encrypted


# 解密
def py_aes_third(encrypted):
    key = b'TXhkKroQJSgrKrnN'
    IV = b'0102030405060708'
    unpad = lambda s: s[0:-s[-1]]
    cipher2 = AES.new(key, mode=AES.MODE_CBC, IV=IV)

    decrypted = base64.b64decode(encrypted)
    # print(decrypted)
    decrypted = cipher2.decrypt(decrypted)
    # print(decrypted)  # will be 'to be encrypted'
    decrypted = unpad(decrypted)
    print("第一次解密结果",str(decrypted,encoding='utf-8'))
    key = b'0CoJUm6Qyw8W8jud'
    IV = b'0102030405060708'

    cipher = AES.new(key, mode=AES.MODE_CBC, IV=IV)

    decrypted = base64.b64decode(decrypted)
    # print(decrypted)
    decrypted = cipher.decrypt(decrypted)
    # print(decrypted)  # will be 'to be encrypted'
    decrypted = unpad(decrypted)
    print("第二次解密结果",str(decrypted,encoding='utf-8'))


def jiami_(text):
    info = py_aes_second(py_aes_first(text))
    print(info)
    return info

def jiemi_(text):
    jiemi_info = py_aes_third(text)
    print(jiemi_info)
    return jiemi_info



if __name__ == '__main__':
    jiami_('sdfadfaf')
    jiemi_('zi8Y6TYtv3TQ3vPiamaUE+arzvFjlbFzNGdkSTxKRrw=zi8Y6TYtv3TQ3vPiamaUE+arzvFjlbFzNGdkSTxKRrw=')
# py_aes_first('{"s":"在田野","csrf_token":""}')
# py_aes_second(py_aes_first('{"s":"在田野","csrf_token":""}'))
# xx = py_aes_second(py_aes_first('{"hlpretag":"<span class=\"s-fc7\">","hlposttag":"</span>","s":"在意义","type":"1","offset":"90","total":"false","limit":"30","csrf_token":”"}'))
# py_aes_second(py_aes_first('{"hlpretag":"<span class=\"s-fc7\">","hlposttag":"</span>","s":"在田野","type":"1","offset":"90","total":"false","limit":"30","csrf_token":”"}'))





# 解密测试
# xx = 'RidsQl08PTom8lbreQjS0wrkPfv02Ib1P+7WYmAYUmHz3V3KhauA0kodLg+VIPLXEn393pGiP6j7E9soFzuH09jq/XFIcjEMKCIZb3npxxc='
# py_aes_third(xx)

# 加密测试
# py_aes_second(py_aes_first('{"hlpretag":"<span class=\\"s-fc7\\">","hlposttag":"</span>","#/discover":"","s":"在一起","type":"1","offset":"30","total":"false","limit":"30","csrf_token":"”}'))

