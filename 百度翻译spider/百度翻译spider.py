# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/5/29
import json

import requests
import execjs

def js_dd(r:str):
    js_compile = execjs.compile(
        r"""
            function a(r) {
                if (Array.isArray(r)) {
                    for (var o = 0, t = Array(r.length); o < r.length; o++)
                        t[o] = r[o];
                    return t
                }
                return Array.from(r)
            }
            function n(r, o) {
                for (var t = 0; t < o.length - 2; t += 3) {
                    var a = o.charAt(t + 2);
                    a = a >= "a" ? a.charCodeAt(0) - 87 : Number(a),
                    a = "+" === o.charAt(t + 1) ? r >>> a : r << a,
                    r = "+" === o.charAt(t) ? r + a & 4294967295 : r ^ a
                }
                return r
            }
            var xx = function e(r) {
                var o = r.match(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g);
                if (null === o) {
                    var t = r.length;
                    t > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(t / 2) - 5, 10) + r.substr(-10, 10))
                } else {
                    for (var e = r.split(/[\uD800-\uDBFF][\uDC00-\uDFFF]/), C = 0, h = e.length, f = []; h > C; C++)
                        "" !== e[C] && f.push.apply(f, a(e[C].split(""))),
                        C !== h - 1 && f.push(o[C]);
                    var g = f.length;
                    g > 30 && (r = f.slice(0, 10).join("") + f.slice(Math.floor(g / 2) - 5, Math.floor(g / 2) + 5).join("") + f.slice(-10).join(""))
                }
                var u = void 0
                  , l = "" + String.fromCharCode(103) + String.fromCharCode(116) + String.fromCharCode(107);
                u = null !== i ? i : (i = "320305.131321201" || "") || "";
                for (var d = u.split("."), m = Number(d[0]) || 0, s = Number(d[1]) || 0, S = [], c = 0, v = 0; v < r.length; v++) {
                    var A = r.charCodeAt(v);
                    128 > A ? S[c++] = A : (2048 > A ? S[c++] = A >> 6 | 192 : (55296 === (64512 & A) && v + 1 < r.length && 56320 === (64512 & r.charCodeAt(v + 1)) ? (A = 65536 + ((1023 & A) << 10) + (1023 & r.charCodeAt(++v)),
                    S[c++] = A >> 18 | 240,
                    S[c++] = A >> 12 & 63 | 128) : S[c++] = A >> 12 | 224,
                    S[c++] = A >> 6 & 63 | 128),
                    S[c++] = 63 & A | 128)
                }
                for (var p = m, F = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(97) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(54)), D = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(51) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(98)) + ("" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(102)), b = 0; b < S.length; b++)
                    p += S[b],
                    p = n(p, F);
                return p = n(p, D),
                p ^= s,
                0 > p && (p = (2147483647 & p) + 2147483648),
                p %= 1e6,
                p.toString() + "." + (p ^ m)
            }
            var i = null;
        """
    )
    info = js_compile.call('xx', r)
    return info

def run(key):
    sign = js_dd(key)
    url = "https://fanyi.baidu.com/v2transapi?from=en&to=zh"

    payload = "from=en&to=zh&query={}&transtype=realtime&simple_means_flag=3&sign={}&token=886aa9b1d94bd35f736c15b865355987&domain=common".format(key,sign)
    headers = {
      'authority': 'fanyi.baidu.com',
      'accept': '*/*',
      'x-requested-with': 'XMLHttpRequest',
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
      'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'origin': 'https://fanyi.baidu.com',
      'sec-fetch-site': 'same-origin',
      'sec-fetch-mode': 'cors',
      'sec-fetch-dest': 'empty',
      'referer': 'https://fanyi.baidu.com/translate?aldtype=16047&query=&keyfrom=baidu&smartresult=dict&lang=auto2zh',
      'accept-language': 'zh-CN,zh;q=0.9',
      'cookie': 'BIDUPSID=4440053665E634D40225BDB0D03E06FB; PSTM=1587886677; BAIDUID=4440053665E634D478DDC8C16E9C7B12:FG=1; BDUSS=y1qektIM1ZwM2JGS1ZOcWR2TDd5cXNOUUw5UzBXZUpBemZxaFJzcnU0N2l6TXhlRVFBQUFBJCQAAAAAAAAAAAEAAABJ60F6x63RptLk0fQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOI~pV7iP6VeY; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BDSFRCVID=tjPOJeCAa7berx3uzpK9uyZdfmKK0gOTH6qcdz7sDYu7og_VfHNgEG0Pox8g0KubKALAogKK0mOTHUuF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tJutoIPMtKv0jbTg-tP_-4_tbh_X5-RLfb5PLp7F5lONHt3uXj5NMRQL5UrQBbbv-2o-ahkM5h7xOKQSM-5pMJFUXp7ULpOAQeQghf5N3KJmDPP9bT3v5Dun3J3r2-biWbRL2MbdbDnP_IoG2Mn8M4bb3qOpBtQmJeTxoUJ25DnJhhCGe6KMD5cbDNKfqbT32CnKW5rtKRTffjrnhPF35-IrXP6-3MoKJKr-QtPbb4c2OITG2q6fb4uUyN3MWh37Jj620PF5-hbZfD3vbpn4bxkNbPoxJpOyMnbMopvaKqvN8hjvbURvD-ug3-7P-x5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIE3-oJqCLabKPw3f; H_PS_PSSID=; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; delPer=0; PSINO=2; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1590665640,1590739020,1590740573; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1590740573; __yjsv5_shitong=1.0_7_311eefede6fd974d4f71d2b54434efb086cc_300_1590740573647_221.223.193.45_cdfd764c; yjs_js_security_passport=c5fb1118c64b458b25325a4dbb9225810a243137_1590740578_js; BAIDUID=1EFD4CDE99B11CB1B31310352198C496:FG=1'
    }

    response = requests.request("POST", url, headers=headers, data = payload)

    print(response.text)

if __name__ == '__main__':
    run(key="hi")
