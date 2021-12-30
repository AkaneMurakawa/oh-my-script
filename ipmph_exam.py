# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""

人卫教学助手V5.9 - 题库获取脚本
修改USER_ID, SIGN, KEYWORD

"""

import requests
import re

URL_SUFFIX = 'http://tk.ipmph.com/exam/a/5.9'
USER_ID = 'xxxxxxxx'
SIGN = 'XKzlN2pnNxIWnAP2BIF4l10HkSqi4uS1R2CkiTzqV6cJ7w+4kbfECH9j6r3+jH1CL8ulm10pyktWyiLBnYCrU4DSooRuZqni' \
                'm73zCOxWFscHgbHUSyWQgpTKWiFd6MYb5IoMKftTFXcSsPFfyjJEgcNmNK1TOClsNRnSaqR+G6A='
KEYWORD = '2017级临床'

CHOICE_DICT = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D',
    4: 'E',
}
f = open(KEYWORD + ".md", "w", encoding='utf-8')
pattern = re.compile(r'<[^>]+>', re.S)


def run():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
    }
    data = {
        'sign': SIGN,
        'userId': USER_ID,
        'pageNo': 1,
        'status': 2,
        'examName': KEYWORD,
        'pageSize': 10
    }
    # 获取题库列表
    response = requests.post(URL_SUFFIX + '/api/examTask/list', headers=headers, data=data)
    print('人卫教学助手 - 获取题库列表')
    f.write('人卫教学助手 - 获取题库列表')
    # print(response.text)
    # print(response.json())

    rows = response.json().get('data')
    for row in rows:
        detail(headers, row)


def detail(headers, row):
    exam_student_id = row['examStudentId']
    many_exam_id = row['id']
    data = {
        'examStudentId': exam_student_id,
        'frequencyNum': 1,
        'sign': SIGN,
        'manyExamId': many_exam_id,
        'userId': USER_ID,
    }
    response = requests.post(URL_SUFFIX + '/api/examTask/detail', headers=headers, data=data)
    # print(response.text)
    # print(response.json())

    print('=================================================START==================================================')
    f.write('=================================================START=================================================\n')
    result = response.json().get('data')
    print('标题:', result['examName'])
    print('Total:', result['questionTotal'])
    f.write('标题:' + result['examName'] + '\n')
    f.write('Total:' + str(result['questionTotal']) + '\n')

    model_question_list = result['modelQuestionList']
    for i, row in enumerate(model_question_list):
        print(i+1, row['name'])
        f.write(str(i+1) + pattern.sub('', row['name']) + '\n')
        choice_ist = row['choiceList']
        if choice_ist:
            for j, choice in enumerate(choice_ist):
                print(CHOICE_DICT[j], ' ', choice)
                f.write(CHOICE_DICT[j] + ' ' + choice + '\n')
            print('正确答案 ', row['answer'], '\n')
            f.write('正确答案 ' + ",".join(row['answer']) + '\n\n')
        else:
            children = row['children']
            children_choice_list = children[0].get('choiceList')

            for j, choice in enumerate(children_choice_list):
                print(CHOICE_DICT[j], ' ', choice)
                f.write(CHOICE_DICT[j] + ' ' + choice + '\n')
            print('正确答案 ', row['answer'], '\n')
            f.write('正确答案 ' + ",".join(children[0]['answer']) + '\n\n')
        # time.sleep(2)


if __name__ == '__main__':
    run()
    print('=================================================END================================================')
    f.write('=================================================END================================================')
    f.close()
