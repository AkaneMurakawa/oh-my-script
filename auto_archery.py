# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
auto archery

:copyright: (c) 2020 by AkaneMurakwa.
:date: 2020-11-27
"""

import requests
import datetime
import time
import json
import re

# demo
# url: https://demo.archerydms.com
# username/password: archer / archer
SERVER_URL = 'https://demo.archerydms.com'
USERNAME = 'archer'
PASSWORD = 'archer'
DING_TALK_URL = 'https://oapi.dingtalk.com/robot/send?access_token=xxxxxx'
MOBILE = {
    'xxxxx': '12345678991'
}


# constant variable
LOGIN_URL = SERVER_URL + '/login/'
Referer = SERVER_URL + "/sqlworkflow/"
AUTHENTICATE_URL = SERVER_URL + '/authenticate/'
SQL_WORK_FLOW_URL = SERVER_URL + '/sqlworkflow_list/'
SQL_DETAIL_URL = SERVER_URL + '/detail/'
SQL_AUDIT_URL = SERVER_URL + '/passed/'
SQL_EXECUTE_URL = SERVER_URL + '/execute/'
LIMIT = 20


def run():
    login()


def login():
    """
    login to archery
    :return:
    """
    print('============================================Auto Archery===========================================')
    print('start login ', SERVER_URL)
    login_response = requests.get(LOGIN_URL)
    print('login response : ', login_response)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Referer': Referer
    }
    data = {'username': USERNAME, 'password': PASSWORD}
    set_cookie(headers, login_response)
    response = requests.post(AUTHENTICATE_URL, headers=headers, data=data)
    response.raise_for_status()
    print(response.text)
    if response.text.split(',')[0].split(':')[1].strip() == '1':
        print('login fail, msg: ', response.content.get('msg'))
        return

    set_cookie_token(headers, response)
    query(headers, 0)


def set_cookie(headers, response):
    """
    get cookie and resolve CSRFToken for request headers
    :param headers:
    :param response:
    :return:
    """
    cookie = response.headers.get('Set-Cookie').split(";")[0]
    csrftoken = cookie.split('=')[1]
    headers['X-CSRFToken'] = csrftoken
    headers['Cookie'] = cookie


def set_cookie_token(headers, response):
    """
    get cookie (contains session id) and resolve CSRFToken for request headers
    :param headers:
    :param response:
    :return:
    """
    cookie = response.headers.get('Set-Cookie').split(";")[0]
    sessionid = ''
    if len(response.headers.get('Set-Cookie').split(';')) > 3:
        sessionid = '; ' + response.headers.get('Set-Cookie').split(';')[3].split(',')[1].strip()
    csrftoken = cookie.split('=')[1]
    headers['X-CSRFToken'] = csrftoken
    headers['Cookie'] = cookie + sessionid


def query(headers, offset):
    """
    only query today sql workflow
    something you know:
        param 'search' is keyword
        param 'navStatus' is status about sql workflow, 'workflow_manreviewing' means 'wait to audit'
    :param headers:
    :param offset: it means pageNum
    :return:
    """
    date_time = datetime.date.today()
    data = {
        'limit': LIMIT,
        'offset': offset,
        'navStatus': 'workflow_manreviewing',
        'instance_id': '',
        'group_id': '',
        # 'start_date': date_time,
        'start_date': date_time + datetime.timedelta(days=-7),
        'end_date': date_time,
        'search': '',
    }
    headers['Sec-Fetch-Site'] = 'same-origin'
    response = requests.post(SQL_WORK_FLOW_URL, headers=headers, data=data)
    try: 
        total = response.json().get('total')
    except:
        print('err: ', response.text)
        return
    print('query workflow list, total:', total)
    if total == 0:
        print('query result, total 0')
        return

    rows = response.json().get('rows')
    for row in rows:
        set_cookie_token(headers, response)
        detail(headers, row)

    # next page
    if (offset+1) * LIMIT <= total:
        time.sleep(2)
        set_cookie_token(headers, response)
        query(headers, offset+1)


def detail(headers, row):
    """
    the detail of workflow id
    :param headers:
    :param row:
    :return:
    """
    # check something, syntax_type == 2 means DML, syntax_type == 1 means DDL, syntax_type == 0 means other
    if row['syntax_type'] != 2:
        print('unsupported audit type')
        return
    if row['engineer_display'] not in MOBILE:
        print('user not in the auto audit list', row['engineer_display'] )
        return

    # query detail for setting csrfmiddlewaretoken
    workflow_id = row['id']
    response = requests.get(SQL_DETAIL_URL + str(workflow_id), headers=headers)
    try:
        csrfmiddlewaretoken = re.search("csrfmiddlewaretoken' value='.*/>", response.text, 0).group().split("value='")[1].split("'")[0]
    except:
        csrfmiddlewaretoken = response.text.split('form')[2].replace(' ', '').split('csrfmiddlewaretoken')[1].split('\'/>')[0].split('value=\'')[1]

    set_cookie_token(headers, response)
    audit(headers, csrfmiddlewaretoken, row)


def audit(headers, csrfmiddlewaretoken, row):
    """
    audit sql
    :param headers:
    :param csrfmiddlewaretoken:
    :param row:
    :return:
    """
    workflow_id = row['id']
    data = {
        'csrfmiddlewaretoken': csrfmiddlewaretoken,
        'workflow_id': workflow_id,
        'audit_remark': 'auto audit by python3',
        'btnPass': ''
    }
    try:
        response = requests.post(SQL_AUDIT_URL, headers=headers, data=data)
        csrfmiddlewaretoken = re.search("csrfmiddlewaretoken' value='.*/>", response.text, 0).group().split("value='")[1].split("'")[0]
    except:
        try:
            csrfmiddlewaretoken = response.text.split('form')[2].replace(' ', '').split('csrfmiddlewaretoken')[1].split('\'/>')[0].split('value=\'')[1]
        except:
            print('SQL audit fail')
            return
    set_cookie_token(headers, response)
    execute(headers, csrfmiddlewaretoken, row)


def execute(headers, csrfmiddlewaretoken, row):
    """
    execute sql
    :param headers:
    :param csrfmiddlewaretoken:
    :param row:
    :return:
    """
    workflow_id = row['id']
    data = {
        'csrfmiddlewaretoken': csrfmiddlewaretoken,
        'mode': 'auto',
        'workflow_id': workflow_id
    }
    try:
        response = requests.post(SQL_EXECUTE_URL, headers=headers, data=data)
        response.raise_for_status()
        print('execute', response)
    except:
        print('SQL execute fail')
    finally:
        send_dingtalk(row)


def send_dingtalk(row):
    """
    send the result to ding talk, if you need @some, you should set atMobiles and the text content should include @mobile
    :param row:
    :return:
    """
    headers = {
        'Accept-Encoding': '',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
    }

    name = row['engineer_display']
    mobile = MOBILE[name]
    text = '### 工单执行中：' + row['workflow_name'] + '\n<br/><br/>' + \
           '用户：' + name + ' ' + row['instance__instance_name'] + ' ' + row['db_name'] + '\n\n<br/>' + \
           '时间：' + row['create_time'] + \
           ' @' + mobile
    title = 'Archery Auto Audit'
    data = {
        'msgtype': 'markdown',
        'markdown': {
            'title': title,
            'text': text
        },
        'at': {
            'atMobiles': [
                mobile
            ],
            "isAtAll": False
        }
    }
    try:
        response = requests.post(DING_TALK_URL, headers=headers, data=json.dumps(data))
        response.raise_for_status()
    except:
        print('send ding talk fail')
    # wait a time
    time.sleep(2)


if __name__ == '__main__':
    run()
