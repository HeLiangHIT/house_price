#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-25 22:42:43
# @Author  : He Liang (heianghit@foxmail.com)
# @Link    : https://github.com/HeLiangHIT

import pinyin
import datetime


# # 全国各省市数据参数
# ref: https://github.com/baixuexiyang/geocoord
_PROVINCE_NAME = [
{'province':'甘肃', 'geoCoord':[103.73, 36.03]},
{'province':'青海', 'geoCoord':[101.74, 36.56]},
{'province':'四川', 'geoCoord':[104.06, 30.67]},
{'province':'河北', 'geoCoord':[114.48, 38.03]},
{'province':'云南', 'geoCoord':[102.73, 25.04]},
{'province':'贵州', 'geoCoord':[106.71, 26.57]},
{'province':'湖北', 'geoCoord':[114.31, 30.52]},
{'province':'河南', 'geoCoord':[113.65, 34.76]},
{'province':'山东', 'geoCoord':[117, 36.65]},
{'province':'江苏', 'geoCoord':[118.78, 32.04]},
{'province':'安徽', 'geoCoord':[117.27, 31.86]},
{'province':'浙江', 'geoCoord':[120.19, 30.26]},
{'province':'江西', 'geoCoord':[115.89, 28.68]},
{'province':'福建', 'geoCoord':[119.3, 26.08]},
{'province':'广东', 'geoCoord':[113.23, 23.16]},
{'province':'湖南', 'geoCoord':[113, 28.21]},
{'province':'海南', 'geoCoord':[110.35, 20.02]},
{'province':'辽宁', 'geoCoord':[123.38, 41.8]},
{'province':'吉林', 'geoCoord':[125.35, 43.88]},
{'province':'黑龙江', 'geoCoord':[126.63, 45.75]},
{'province':'山西', 'geoCoord':[112.53, 37.87]},
{'province':'陕西', 'geoCoord':[108.95, 34.27]},
{'province':'台湾', 'geoCoord':[121.30, 25.03]},
# 4直辖市 - 地址需要特殊处理
# {'province':'北京', 'geoCoord':[116.46, 39.92]},
# {'province':'上海', 'geoCoord':[121.48, 31.22]},
# {'province':'重庆', 'geoCoord':[106.54, 29.59]},
# {'province':'天津', 'geoCoord':[117.2, 39.13]},
# 5自治区
{'province':'内蒙古', 'geoCoord':[111.65, 40.82]},
{'province':'广西', 'geoCoord':[108.33, 22.84]},
{'province':'西藏', 'geoCoord':[91.11, 29.97]},
{'province':'宁夏', 'geoCoord':[106.27, 38.47]},
{'province':'新疆', 'geoCoord':[87.68, 43.77]},
# 2特别行政区
# {'province':'香港', 'geoCoord':[114.17, 22.28]},
# {'province':'澳门', 'geoCoord':[113.54, 22.19]}
]


PROVINCE_NAME = [
    {'province': item['province'], 
        'prpinyin': pinyin.get(item['province'], format="strip", delimiter=""), 
        'coord': item['geoCoord']} for item in _PROVINCE_NAME
]
# for pr in PROVINCE_NAME:
#     print("province={province:<8}, pinyin={pinyin:^20}, coord={coord}".format(**pr))


NOW = datetime.datetime.now()
BASE_URL = 'http://www.creprice.cn'

def gen_province_info():
    # 从最新到最旧生成地址
    all_info = []
    # 1. 当年当月的地址
    for pr in PROVINCE_NAME:
        new_pr = {}
        new_pr['url'] = "%s/proprice/pc%s.html" % (BASE_URL, pr['prpinyin'])
        new_pr['year'] = NOW.year
        new_pr['month'] = NOW.month
        all_info.append(dict(pr, **new_pr))
    # 2. 今年早些时候的地址
    for pr in PROVINCE_NAME:
        for month in range(NOW.month - 1, 0, -1):
            new_pr = {}
            new_pr['url'] = "%s/proprice/pc%s-ti%d%02d.html" % (BASE_URL, pr['prpinyin'], NOW.year, month)
            new_pr['year'] = NOW.year
            new_pr['month'] = month
            all_info.append(dict(pr, **new_pr))
    # 3. 早些年的地址
    for pr in PROVINCE_NAME:
        for year in range(NOW.year - 1, 2007, -1):
            for month in range(12, 0, -1):
                new_pr = {}
                new_pr['url'] = "%s/proprice/pc%s-ti%d%02d.html" % (BASE_URL, pr['prpinyin'], year, month)
                new_pr['year'] = year
                new_pr['month'] = month
                all_info.append(dict(pr, **new_pr))
    return all_info


STRAIT_LIST = [{'province':'北京', 'prpinyin':'bj'},
{'province':'上海', 'prpinyin':'sh'},
{'province':'重庆', 'prpinyin':'cq'},
{'province':'天津', 'prpinyin':'tj'}]

def gen_strait_info():
    all_info = []
    for pr in STRAIT_LIST:
        for year in range(NOW.year, 2007, -1):
            months = range(12, 0, -1) if year < NOW.year else range(NOW.month, 0, -1)
            for month in months:
                new_pr = {}
                new_pr['url'] = 'http://www.creprice.cn/market/distrank/city/%s.html?flag=1&month=%d-%02d&type=11' %\
                     (pr['prpinyin'], year, month)
                new_pr['year'] = year
                new_pr['month'] = month
                all_info.append(dict(pr, **new_pr))
    return all_info


def gen_all_info():
    infos = gen_strait_info()
    infos.extend(gen_province_info())
    return infos


ITEM_KEYS = ['province' ,'city', 'year', 'month', 'price', 'url']


if __name__ == '__main__':
    # 打印省份
    # for info in gen_province_info():
    #     print(info)
    # for info in gen_strait_info():
    #     print(info)
    for info in gen_all_info():
        print(info)
