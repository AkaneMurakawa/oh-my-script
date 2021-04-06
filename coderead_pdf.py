# /usr/bin/python3
# -*- coding:utf-8 -*-

"""
源码阅读网题库下载 仅供娱乐，非商业用途
程序说明：下载的思路很简单，发现在源码阅读网首页直接就展示了所有pdf的名称，于是直接下载了首页的html文件，
然后利用正则 "/r//.*pdf"直接匹配到所有pdf的url路径，然后拼接前缀 "http://r.coderead.cn"，
在这里我利用的是vscode的批量复制功能，Ctrl+Shift+L。最后就是简单的使用python的requests库进行下载，
这里会进行拦截认证，因此需要将必要的请求头或者cookie进行设置，发现这里并没有进行cookie存储，然后请求header
里用的key是不变的，因此本程序就这样完成了。

:copyright: (c) 2021 by AkaneMurakwa.
:date: 2021-04-06
"""
import requests
import re 
import os
import time

url_list = ["http://r.coderead.cn/r//2021年BATJ%20JAVA经典必考面试题库/考试题库.pdf",
"http://r.coderead.cn/r//2021年BATJ%20JAVA经典必考面试题库/2020最新BAT%20java经典必考面试题.pdf",
"http://r.coderead.cn/r//2021年JAVA核心面试题库/JAVA核心面试知识整理.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/数据库/数据库.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/MySQL/MySQL性能优化的21个最佳实践.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/MySQL/MySQL55题答案.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/MySQL/mysql面试专题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/MySQL/MySQL面试题（含答案）_.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/MySQL/mysql面试题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/MySQL/MySQL篇.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Linux/Linux面试题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Linux/Linux面试专题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Kafka/Kafka面试题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/SpringBoot/SpringBoot面试题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/SpringBoot/SpringBoot面试专题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/多线程/多线程面试59题（含答案）_.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/多线程/多线程，高并发.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/多线程/java面试题_多线程(68题).pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Zookeeper/zookeeper面试专题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Zookeeper/zookeeper面试题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Zookeeper/Zookeeper+分布式过程.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Redis/Redis面试题（二）.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Redis/Redis面试专题（二）.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Redis/Redis篇.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Redis/Redis面试专题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Redis/Redis面试题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Redis/Redis高频面试题%20-%201.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Redis/Redis面试题（含答案）_.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/SpringCloud/SpringCloud面试题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/SpringCloud/SpringCloud面试专题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/MongoDB/MongoDB面试题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/MongoDB/MongDB篇.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/MongoDB/MongoDB面试专题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/ActiveMQ消息中间件/ActiveMQ消息中间件面试题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Dubbo/java面试题_微服务--dubbo(41题).pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Dubbo/Dubbo面试题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Dubbo/Dubbo面试专题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Dubbo/Dubbo服务框架面试题及答案.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Nginx/Nginx面试题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Nginx/Nginx篇.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Nginx/Nginx面试专题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Nginx/Nginx实战书籍.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Nginx/Nginx面试专题(1).pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/集合框架/集合框架.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/设计模式/设计模式面试专题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/设计模式/设计模式面试题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/设计模式/java面试题_设计模式(26题).pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/MyBatis/Mybatis面试题（含答案）_.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/MyBatis/MyBatis面试专题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/MyBatis/MyBatis面试题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/RabbitMQ消息中间件/RabbitMQ消息中间件面试题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/RabbitMQ消息中间件/java面试题_消息中间件--RabbitMQ(20题).pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/RabbitMQ消息中间件/java面试题_消息中间件--RocketMq(14题).pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/并发编程/并发编程面试题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/并发编程/并发面试题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/JVM/JVM常见面试题指南.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/JVM/JVM面试题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/JVM/JVM面试专题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/JVM/JVM性能优化相关问题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/JVM/JVM.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/JVM/JVM执行子系统.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Tomcat/Tomcat优化相关问题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Tomcat/Tomcat面试题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Tomcat/Tomcat面试专题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Spring/Spring面试专题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Spring/Spring面试专题及答案.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Spring/Spring面试题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Spring/Spring面试题（含答案）_.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/SpringMVC/SpringMVC面试题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/SpringMVC/SpringMVC面试专题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/性能优化/深入了解性能优化.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/乐观锁与悲观锁/面试必备之乐观锁与悲观锁.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Netty/Netty面试专题.pdf",
"http://r.coderead.cn/r//2021年Java各知识点综合面试题/Netty/Netty面试题.pdf",
"http://r.coderead.cn/r//2021年JAVA常见面试题库/整理的多家公司常见面试题库350道.pdf"]

if __name__ == "__main__":
    for url in url_list:
        print(url)
        file_name = url.split('/')[-1]

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
            'Upgrade-Insecure-Requests': '1',
            'Authorization': 'Basic ZGFveW91OmRhb3lvdQ==',
            'Referer': 'http://r.coderead.cn/',
            'User-Agent': 'SMozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
        }
        data = {}
        print('========================================================================')
        print('开始下载')
        print(file_name)
        r = requests.get(url, headers=headers, data=data)
        if r.status_code == 401:
            print('something error')
            continue
        with open(file_name, 'wb') as f:
            f.write(r.content)
        time.sleep(1)
        print('下载成功')
