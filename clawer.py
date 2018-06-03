#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-27 20:41:18
# @Author  : He Liang (heianghit@foxmail.com)
# @Link    : https://github.com/HeLiangHIT

import os, sys, time
import requests
from bs4 import BeautifulSoup
from constant import *
from tools import *
from requests.adapters import HTTPAdapter



HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
           'Referer': 'http://www.creprice.cn/naprice/funation.html',
           'Referrer Policy': 'no-referrer-when-downgrade',
           'Connection': 'keep-alive'}


class Clawer(object):
    def __init__(self, username=None, passwd=None, url='http://www.creprice.cn/naprice/funation.html'):
        super(Clawer, self).__init__()
        self.username = username
        self.passwd = passwd
        self.session = requests.Session()
        self.session.mount('http://', HTTPAdapter(max_retries=3)) # 重试3次
        self.filter = set()

    def parse_city_price(self, html):
        # #order_f > tr:nth-child(1)
        city_prices = []
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.select('table.table-style5.tablesorter')
        if(len(table) == 0):
            return city_prices
        for record in table[0].select('tr')[1:]: # 第0个是标题栏
            city = record.select('td')[1].text.strip() # 城市名称
            price = record.select('td')[2].text.strip() # 房价
            if '--' != price:
                city_prices.append({'city':city, 'price':float(''.join(price.split(',')))})
            # else:
            #     city_prices.append({'city':city, 'price':-1})
        return city_prices

    # @time_it
    def fill_city_price(self, record):
        # example 
        records = []
        if record.get('url', None) is None:
            warn(f'{record} has no url addr!')
            return records
        if record['url'] in self.filter:
            warn(f"{record['url']} is already fetched!")
            return records
        self.filter.add(record['url'])
        log(f"get {record['url']} for {record['province']} in {record['year']}-{record['month']} ......")
        res = self.session.get(record['url'], headers=HEADERS, timeout=60) # 超时60s
        city_prices = self.parse_city_price(res.text)
        for rec in city_prices:
            records.append(dict(record.items(), **rec))
        log(f'...done with {len(records)} records!')
        return records
# records = [item for item in UrlGen().gen_all_info()]
# cl = Clawer()
# for index in range(0, 20):
#     print(cl.fill_city_price(records[index]))


import random, time
def main():
    '''爬取数据保存到数据库'''
    house_db = HouseDatabase('residential')
    clawer = Clawer()
    house_db.delete_records() # 先删除数据库
    for record in gen_all_info():
        time.sleep(0.1 + random.random() * 1.9) # 别把别人网站搞塌了
        records = clawer.fill_city_price(record)
        for rec in records:
            house_db.save_record(rec)


# import gevent
# from gevent import monkey
# monkey.patch_all()
# def _main_sync():
#     '''爬取数据保存到数据库--猴子补丁异步'''
#     house_db = HouseDatabase('residential')
#     clawer = Clawer()
#     def do_with_record(record):
#         records = clawer.fill_city_price(record)
#         for rec in records:
#             house_db.save_record(rec) # 猴子补丁不支持会导致出错
#     house_db.delete_records() # 先删除数据库
#     gevent.joinall([gevent.spawn(do_with_record, record) for record in gen_all_info()])

# def __main_sync():
#     '''爬取数据保存到数据库--猴子补丁异步+串行'''
#     house_db = HouseDatabase('residential')
#     clawer = Clawer()
#     house_db.delete_records() # 先删除数据库
#     let_prcs = [gevent.spawn(clawer.fill_city_price, record) for record in gen_all_info()] # 获取返回值必须这样
#     recordslist = gevent.joinall(let_prcs)
#     for records in let_prcs:
#         for rec in records.get():
#             # 因为猴子补丁还不支持mysql，所以放在后面串行处理
#             house_db.save_record(rec)


if __name__ == '__main__':
    main() #还是串行可控性好
    # _main_sync() # mysql不支持该操作
    # __main_sync() # 还是会出粗



