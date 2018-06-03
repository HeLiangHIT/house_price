#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-27 20:43:53
# @Author  : He Liang (heianghit@foxmail.com)
# @Link    : https://github.com/HeLiangHIT

import pymysql
from constant import *


def log_warp(level='info', log_name='test', file=True, console=True):
    import logging
    formatter = logging.Formatter('[%(asctime)s][%(filename)s-%(lineno)d][%(levelname)s]: %(message)s')  # [%(thread)d]
    # 创建一个logger
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)
    # 写入日志文件
    if log_name is not None:
        fh = logging.FileHandler("./log/%s.log" % log_name, encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    # 输出到控制台
    if console:
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    ret_func = {
        'debug': logger.debug,
        'info': logger.info,
        'warning': logger.warning,
        'error': logger.error,
        'critical': logger.critical
        }
    return ret_func.get(level,logger.info)


debug = log_warp('debug','house_debug', True, False)
log = log_warp('info','house_info')
warn = log_warp('warning','house_warn')
error = log_warp('error', 'house_error')


def time_it(func):
    '''测试函数的计算时间并打印输出'''
    import time, functools
    @functools.wraps(func)
    def clocked_func(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
            arg_lst.append(', '.join(pairs))
        arg_str = ', '.join(arg_lst)
        debug('[%0.8fs] %s(%s) -> %r ' % (elapsed, name, arg_str, result))
        return result
    return clocked_func


class HouseDatabase(object):
    """房子数据库"""
    def __init__(self, tables = 'test'):
        self.conn = pymysql.Connect(host='localhost', port=3306, user='root', passwd='xyz123', db='house', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()
        self.conn.autocommit(True)
        # self.cursor.close()
        # self.conn.close()
        
        self.INSERT_TMP = '''INSERT IGNORE INTO %s(province ,city, year, month, price, url) 
                            VALUES('{province}','{city}', {year}, {month}, {price}, '{url}')''' % tables  # 忽略重复url
        self.QUERY_TMP = '''SELECT province, city, year, month, price, url FROM %s''' % tables
        self.DELETE_TMP = '''DELETE FROM %s''' % tables

    # @time_it
    def save_record(self, item):
        '''保存单个数据'''
        sqltext = self.INSERT_TMP.format(
            province=pymysql.escape_string(item['province']),
            city=pymysql.escape_string(item.get('city','NULL')),
            year=item.get('year', NOW.year),
            month=item.get('month',NOW.month),
            price=item.get('price', 0),
            url=pymysql.escape_string(item.get('url', 'NULL'))
            )
        log("Insert " + sqltext.split('VALUES')[1])
        line = self.cursor.execute(sqltext)

    def delete_records(self, condition=None):
        sqltext = self.DELETE_TMP if condition is None else "%s where %s" % (self.DELETE_TMP, condition)
        log(sqltext)
        self.cursor.execute(sqltext)

    # @time_it
    def query_records(self, condition=None):
        '''查询所有数据'''
        sqltext = self.QUERY_TMP if condition is None else "%s where %s" % (self.QUERY_TMP, condition)
        log(sqltext)
        self.cursor.execute(sqltext)
        records = []
        for each in self.cursor.fetchall():
            records.append({
                'province':each[0],
                'city':each[1],
                'year':int(each[2]),
                'month':int(each[3]),
                'price':float(each[4]),
                'url':each[5]
                })
        log('Query database return %d records.' % len(records))
        return records

    def dump_to_csv(self, filename):
        # 保存到csv文件
        pass


if __name__ == '__main__':
    # log
    log('test')
    # database
    records = [item for item in gen_all_info()]
    house_db = HouseDatabase('test')
    house_db.delete_records()
    for index in range(0, 10):
        house_db.save_record(records[index])
    records = house_db.query_records() # "year=2018"
    print(records)



