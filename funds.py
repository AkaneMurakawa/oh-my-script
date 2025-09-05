#! /usr/bin/env python3

""""
api: <http://fundgz.1234567.com.cn/js/%s.js?rt=%d>
任务名称
name: 基金净值
定时规则
cron: 0 45 9 * * 1-5
      0 0 11 * * 1-5
      0 0 14 * * 1-5
      0 40 14 * * 1-5
"""

import json
import time

import requests

funds = ['013566', '016709', '012414', '012734',
         '005909', '012842', '001595', '006381',
         '012349', '005675']
FUND_URL = 'https://fundgz.1234567.com.cn/js'


# 对齐问题：<https://blog.csdn.net/qq_42311391/article/details/126925740>
def align(string, length):
    difference = length - len(string)
    if difference == 0:  # 若差值为0则不需要补
        return string
    elif difference < 0:
        print('错误：限定的对齐长度小于字符串长度!')
        return None
    new_string = ''
    space = '　'
    for i in string:
        codes = ord(i)  # 将字符转为ASCII或UNICODE编码
        if codes <= 126:  # 若是半角字符
            new_string = new_string + chr(codes + 65248)  # 则转为全角
        else:
            new_string = new_string + i  # 若是全角，则不转换
    return new_string + space * difference  # 返回补齐空格后的字符串


def search():
    result_list = []
    header = f"{align('名称', 18)}{align('代码', 6)}{align('单位净值', 6)}{align('净值估值', 6)}{align('涨跌幅', 6)}"
    result_list.append(header)
    for fund in funds:
        timestamp = time.time()
        url = f'{FUND_URL}/{fund}.js?rt={timestamp}'
        response = requests.get(url)
        if response.status_code != 200:
            print(f'请求失败，{response.text}')
            continue
        text = response.text.replace("jsonpgz(", '').replace(');', '')
        data = json.loads(text)
        r = f"{align(data['name'], 18)}{data['fundcode']:<10}{data['dwjz']:<10}{data['gsz']:<10}{data['gszzl']:<10}"
        result_list.append(r)
    return result_list


if __name__ == '__main__':
    results = search()
    for result in results:
        print(result)
    # QLAPI.notify('基金净值', '\n\n'.join(results))
