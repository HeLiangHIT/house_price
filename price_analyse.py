#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-29 23:06:15
# @Author  : He Liang (heianghit@foxmail.com)
# @Link    : https://github.com/HeLiangHIT

from constant import *
from tools import *
from pyecharts import Geo, Line, Overlap
import numpy

STOP_CITY = ['甘南', '海北', '海东', '海南州', '黄南', '海西', '阿坝', '达州', '德宏', '迪庆', '黔东南', '池州', '白沙',
    '保亭', '昌江', '澄迈', '定安', '大兴安岭', '阿拉善', '崇左', '固原', '中卫', '阿拉尔', '巴州', '北屯', '崇明区', '梁平区',
    '璧山区', '石柱县', '静海区', '宁河区', '延庆区', '密云区', '蓟州区', '博州', '酉阳县', '彭水县', '合川区', '秀山县', '两江新区',
    '潼南区', '开州区', '南川区', '铜梁区', '武隆区', '永川区', '荣昌区', '江津区', '庆阳', '果洛', '广安', '黔南', '万宁', '文昌',
    '五指山', '贺州', '五家渠', '眉山', '丽江']


def debug():
    # 数据获取-绘图-排错-测试
    house_db = HouseDatabase('residential')
    latest_price = house_db.query_records('year=%d and month=%d' %(NOW.year, NOW.month - 4))
    cities_prices = [(item['city'], item['price']) for item in latest_price if item['city'] not in STOP_CITY]
    # print(cities_prices)

    # 地图绘制
    geo = Geo("全国房价图", '%d - %d' %(NOW.year, NOW.month),
        title_color="#fff", title_pos="center", width=1000, height=600, background_color='#404a59')  
    cities, prices = geo.cast(cities_prices)

    ''' # 获取不支持的城市的信息
    for c, p in zip(cities, prices):
        try:
            geo.add('%d - %d' %(NOW.year, NOW.month), [c,], [p,], maptype='china', type="heatmap",
                is_visualmap=True, visual_range=[numpy.min(prices), numpy.max(prices)], visual_text_color="#fff")
        except Exception as e:
            print(e)
    '''
    # 增加数据
    geo.add('%d - %d' %(NOW.year, NOW.month), cities, prices, maptype='china', type="heatmap",
        is_visualmap=True, visual_range=[numpy.min(prices), numpy.max(prices)], visual_text_color="#fff")
    geo.render("./out/全国房价图.html")


def gen_price_map(year=None, month=None, province='china'):
    # 绘制地区温度图
    house_db = HouseDatabase('residential')
    year_cond = 'year=%d' % year if year is not None else ''
    month_cond = ' and month=%d' % month if month is not None else ''
    province_cond = " and province='%s'" % province if province not in ['china', '中国'] else ''
    condition =  year_cond + month_cond + province_cond
    latest_price = house_db.query_records(condition)
    cities_prices = [(item['city'], item['price']) for item in latest_price if item['city'] not in STOP_CITY]
    geo = Geo("", '', title_color="#fff", title_pos="left", background_color='#404a59') # width=1000, height=600,   
    cities, prices = geo.cast(cities_prices)
    geo.add('%d-%d' %(NOW.year, NOW.month), cities, prices, maptype=province, type="heatmap",
        is_visualmap=True, visual_range=[numpy.min(prices), numpy.max(prices)], visual_text_color="#fff")
    geo.render("./out/房价温度图-%s.html" % condition.replace(' and ', '-').replace('=', '_'))
# gen_price_map(2018, 5, '浙江')
# gen_price_map(2018, None, 'china')


def city_price_trend(city='海淀区'):
    # 绘制多个城市的房价走势图
    house_db = HouseDatabase('residential')
    def gen_line(city, times_prices):
        line = Line()
        times, prices = line.cast(times_prices)
        line.add(city, times, prices)
        return line
    if isinstance(city, list):
        overlap = Overlap()
        for c in city:
            condition = "city='%s' order by year, month" % c
            times_prices = [(f"{item['year']}-{item['month']}", item['price']) for item in house_db.query_records(condition)]
            overlap.add(gen_line(c, times_prices))
        overlap.render('./out/%s房价走势图.html' % ','.join(city))
    else:
        condition = "city='%s' order by year, month" % city
        times_prices = [(f"{item['year']}-{item['month']}", item['price']) for item in house_db.query_records(condition)]
        gen_line(city, times_prices).render('./out/%s房价走势图.html' % city)

# city_price_trend(['贵阳', '杭州', '成都', '毕节', '哈尔滨', '重庆', '西安', '遵义'])
# city_price_trend()







