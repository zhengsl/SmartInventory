#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from optimize_cost import *
from collections import defaultdict


four_dc_old_dict = {'成都市': ['甘肃省', '宁夏回族自治区', '新疆维吾尔自治区', '青海省', '四川省', '重庆', '云南省', '贵州省',
                          '陕西省', '西藏自治区'],
                '廊坊市': ['北京', '河北省', '天津', '辽宁省',  '黑龙江省', '吉林省', '山西省', '内蒙古自治区', '河南省'],
                '广州市': ['佛山市', '广州市', '深圳市', '东莞市'],
                '苏州市': ['安徽省', '湖北省', '江苏省', '江西省', '上海', '浙江省', '福建省', '广西壮族自治区',
                          '海南省', '湖南省', '山东省', '广东省-other']}


four_dc_dict = {'成都市': ['甘肃省', '宁夏回族自治区', '新疆维吾尔自治区', '青海省', '四川省', '重庆', '云南省', '贵州省',
                          '陕西省', '西藏自治区'],
                '廊坊市': ['北京', '河北省', '天津', '辽宁省', '山东省', '黑龙江省', '吉林省', '山西省', '内蒙古自治区'],
                '广州市': ['广东省', '福建省', '广西壮族自治区', '湖南省', '海南省'],
                '苏州市': ['安徽省', '河南省', '湖北省', '江苏省', '江西省', '上海', '浙江省']}


three_dc_dict = {'廊坊市': ['北京', '河北省', '天津', '辽宁省', '山东省', '黑龙江省', '吉林省', '山西省', '内蒙古自治区',
                           '甘肃省', '宁夏回族自治区', '新疆维吾尔自治区', '青海省', '四川省', '重庆', '云南省', '贵州省',
                           '西藏自治区'],
                '广州市': ['广东省', '福建省', '广西壮族自治区', '湖南省', '海南省'],
                '苏州市': ['安徽省', '河南省', '湖北省', '江苏省', '江西省', '上海', '浙江省', '陕西省']}


def compute_cost_per_cluster(clusters, center, tlc, ttc, cities_dict, sales_dict):
    total_cost, total_time, total_sales = 0, 0, 0

    for city in clusters:
        city_name = city
        total_cost += tlc[cities_dict[center]][cities_dict[city_name]]
        total_time += sales_dict[city_name] * ttc[cities_dict[center]][cities_dict[city_name]]
        total_sales += sales_dict[city_name]
    avg_lead_time = round(total_time / total_sales, 2)

    return avg_lead_time, total_cost


def get_city_clusters(cities, provinces):
    province_city_dict = defaultdict(list)
    for city_province in cities:
        province_city_dict[city_province[1]].append(city_province[0])
    cities = []
    for province in provinces:
        cities.extend(province_city_dict[province])
    return cities


def compute_cost(total_sales):

    sf_price_dict = read_sf_price('/Users/leon/Documents/Inventory/顺丰全国到全国标快及特惠报价单201709.xlsx',
                                  from_cache='/Users/leon/Documents/Inventory/Test/sf_price_real_01.dat')

    sf_matrix, cities, sales = city_price_matrix('/Users/leon/Documents/Inventory/Test/city_yby_update.txt', ' ',
                                                 sf_price_dict, total_sales)

    tlc = compute_total_logistics_cost(sf_matrix, sales)

    sales_dict = {}
    cities_dict = {}

    for i, city in enumerate(cities):
        sales_dict[city[0]] = sales[i]
        cities_dict[city[0]] = i

    ttc = compute_total_time_cost(cities)

    costs = []

    final_cost = 0
    for center, provinces in four_dc_dict.items():
        clusters = get_city_clusters(cities, provinces)
        print("{}:{}:{}".format(center, len(clusters), clusters))
        avg_lead_time, total_cost = compute_cost_per_cluster(clusters, center, tlc, ttc, cities_dict, sales_dict)
        costs.append((center, avg_lead_time, total_cost))
        final_cost += total_cost

    with open('/Users/Leon/Desktop/4DC_cost.txt', 'w', encoding='utf-8') as out:
        for (center, avg_lt, cost) in costs:
            out.write("{}:{}:{}\n".format(center, avg_lt, cost))
        out.write("total cost: {}\n".format(final_cost))

    costs = []
    final_cost = 0
    for center, provinces in three_dc_dict.items():
        clusters = get_city_clusters(cities, provinces)
        print("{}:{}:{}".format(center, len(clusters), clusters))
        avg_lead_time, total_cost = compute_cost_per_cluster(clusters, center, tlc, ttc, cities_dict, sales_dict)
        costs.append((center, avg_lead_time, total_cost))
        final_cost += total_cost

    with open('/Users/Leon/Desktop/3DC_cost.txt', 'w', encoding='utf-8') as out:
        for (center, avg_lt, cost) in costs:
            out.write("{}:{}:{}\n".format(center, avg_lt, cost))
        out.write("total cost: {}\n".format(final_cost))


def get_city_clusters_old(cities, provinces):
    province_city_dict = defaultdict(list)
    for city_province in cities:
        province_city_dict[city_province[1]].append(city_province[0])
    for city in province_city_dict['广东省']:
        if city not in ['佛山市', '广州市', '深圳市', '东莞市']:
            province_city_dict['广东省-other'].append(city)

    cities = []
    for province in provinces:
        if province in province_city_dict:
            cities.extend(province_city_dict[province])
        else:
            cities.append(province)
    return cities


def compute_cost_old(total_sales):

    sf_price_dict = read_sf_price('/Users/leon/Documents/Inventory/顺丰全国到全国标快及特惠报价单201709.xlsx',
                                  from_cache='/Users/leon/Documents/Inventory/Test/sf_price_real_01.dat')

    sf_matrix, cities, sales = city_price_matrix('/Users/leon/Documents/Inventory/Test/city_yby_update.txt', ' ',
                                                 sf_price_dict, total_sales)

    tlc = compute_total_logistics_cost(sf_matrix, sales)

    sales_dict = {}
    cities_dict = {}

    for i, city in enumerate(cities):
        sales_dict[city[0]] = sales[i]
        cities_dict[city[0]] = i

    ttc = compute_total_time_cost(cities)

    costs = []

    final_cost = 0
    for center, provinces in four_dc_old_dict.items():
        clusters = get_city_clusters_old(cities, provinces)
        print("{}:{}:{}".format(center, len(clusters), clusters))
        avg_lead_time, total_cost = compute_cost_per_cluster(clusters, center, tlc, ttc, cities_dict, sales_dict)
        costs.append((center, avg_lead_time, total_cost))
        final_cost += total_cost

    with open('/Users/Leon/Desktop/4DC_old_cost.txt', 'w', encoding='utf-8') as out:
        for (center, avg_lt, cost) in costs:
            out.write("{}:{}:{}\n".format(center, avg_lt, cost))
        out.write("total cost: {}\n".format(final_cost))


if __name__ == "__main__":
    compute_cost_old(4400000)
