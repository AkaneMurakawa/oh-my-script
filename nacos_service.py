#! /usr/bin/env python3

""""
Search Nacos Service
api: <https://nacos.io/zh-cn/docs/open-api.html>
"""
import requests

IP = '192.168.180.11'
SEARCH_PORT = '8106'

SERVER = f'http://{IP}:8848'
SERVICE_LIST_API = f'{SERVER}/nacos/v1/ns/service/list'
INSTANCE_LIST_API = f'{SERVER}/nacos/v1/ns/instance/list'


def main():
    print('Search Nacos Service')
    response = requests.get(SERVICE_LIST_API, params={
        'pageNo': 1,
        'pageSize': 100
    })
    data = response.json()
    service_list = data['doms']
    print('service list:', service_list)
    if len(service_list) == 0:
        print('no service')
        return
    for service in service_list:
        response = requests.get(INSTANCE_LIST_API, params={
            'serviceName': service
        })
        data = response.json()
        if SEARCH_PORT in response.text:
            print(f'port: {SEARCH_PORT}, found service: {service}')
            print(f'{service} instance list: {data}')
            return
    print('port not found')


if __name__ == '__main__':
    main()
