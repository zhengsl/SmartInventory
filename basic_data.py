#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import xlrd
import pickle

A_HUGE_INT = 2147483647

# 省份全称和简称字典
province_dict = {'安徽省': ('安徽', 0), '北京': ('北京', 1), '福建省': ('福建', 2), '甘肃省': ('甘肃', 3), '广东省': ('广东', 4),
                 '广西壮族自治区': ('广西', 5), '贵州省': ('贵州', 6), '海南省': ('海南', 7), '河北省': ('河北', 8),
                 '河南省': ('河南', 9), '黑龙江省': ('黑龙江', 10), '湖北省': ('湖北', 11), '湖南省': ('湖南', 12),
                 '吉林省': ('吉林', 13), '江苏省': ('江苏', 14), '江西省': ('江西', 15), '辽宁省': ('辽宁', 16),
                 '内蒙古自治区': ('内蒙古', 17), '宁夏回族自治区': ('宁夏', 18), '青海省': ('青海', 19), '山东省': ('山东', 20),
                 '山西省': ('山西', 21), '陕西省': ('陕西', 22), '上海': ('上海', 23), '四川省': ('四川', 24),
                 '天津': ('天津', 25), '西藏自治区': ('西藏', 26), '新疆维吾尔自治区': ('新疆', 27), '云南省': ('云南', 28),
                 '浙江省': ('浙江', 29), '重庆': ('重庆', 30)}

# 顺丰日常时效矩阵，按省份划分
daily_leadtime_province_matrix = [
    [2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3],
    [2, 1, 3, 3, 3, 3, 3, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 3, 3, 2, 3, 3, 2, 3, 1, 3, 3, 3, 2, 2],
    [3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 2, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 2, 3, 3, 3, 3, 3],
    [3, 2, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3],
    [3, 2, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2],
    [3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2],
    [2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 2, 3, 3, 1, 3, 3, 3, 3, 3, 2, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3],
    [3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 2, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 2],
    [2, 2, 2, 3, 2, 3, 3, 2, 2, 2, 3, 2, 2, 2, 1, 2, 3, 3, 2, 3, 2, 3, 3, 1, 2, 1, 3, 3, 3, 1, 2],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 1],
    [3, 1, 2, 3, 3, 3, 3, 2, 2, 3, 3, 2, 3, 3, 2, 3, 2, 3, 3, 3, 2, 3, 3, 2, 3, 1, 3, 3, 3, 2, 2],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3],
    [3, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 2, 3, 2, 3, 3, 1, 3, 3, 3, 3, 3, 2, 2],
    [3, 2, 3, 3, 2, 3, 2, 2, 3, 2, 3, 2, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 3, 3, 3, 2, 1]
]

# 根据17年包裹数据统计出的不同重量包裹的分布情况，用于估算快递费用
weight_dist = [(2.5, 0.798), (1, 0.128), (3.5, 0.028), (6, 0.035), (3, 0.004), (9, 0.005), (6, 0.001), (1.5, 0.001)]


def read_sf_price(file_path, from_cache=None, persist_path=None):
    if from_cache is None:
        result = {}
        with xlrd.open_workbook(file_path) as excel:
            table = excel.sheet_by_index(0)
            for i in range(2, table.nrows):
                row_v = table.row_values(i)

                from_cities = row_v[1].strip().split('/')
                to_cities = row_v[3].strip().split('/')
                price = (int(row_v[9]), int(row_v[10]))

                for fc in from_cities:
                    for tc in to_cities:
                        if fc in result and (
                                tc not in result[fc] or (tc in result[fc] and result[fc][tc][0] > price[0])):
                            result[fc][tc] = price
                        elif fc not in result:
                            result[fc] = {tc: price}
        if persist_path is not None:
            with open(persist_path, 'wb') as pkl_file:
                pickle.dump(result, pkl_file)
        return result
    else:
        with open(from_cache, 'rb') as pkl_file:
            return pickle.load(pkl_file)


def city_price_matrix(filepath, delimiter, sf_price_dict, total_sales):
    result = []
    cities = []
    sales = []
    with open(filepath, 'rb') as fp:
        lines = fp.readlines()
        for line in lines:
            data = line.decode('utf-8').strip().split(delimiter)
            if "NA" not in data:
                city = data[2][1:-1]
                if city in sf_price_dict and city != "阿勒泰地区":
                    province = data[3][1:-1]
                    cities.append((city, province))
                    sales.append(int(float(data[12]) * total_sales))
    size = len(cities)
    for i in range(size):
        result.append([sf_price_dict[cities[i][0]][cities[j][0]] for j in range(size)])
    return result, cities, sales


sales_data_col_map = {
    2017: 4,
    2014: 6,
    2015: 8,
    2016: 10,
    2018: 12
}


def get_city_sales_count(filepath, sf_price_dict, years, from_cache=None, persist_path=None):
    if from_cache is None:
        result = []
        with open(filepath, 'rb') as fp:
            lines = fp.readlines()
            for line in lines:
                data = line.decode('utf-8').strip().split(' ')
                print(data)
                if "NA" not in data:
                    city = data[2][1:-1]
                    if city in sf_price_dict and city != "阿勒泰地区":
                        province = data[3][1:-1]
                        city_sales = [city, province]
                        sales_count = {}
                        for year in years:
                            sales_count[year] = (
                                int(data[sales_data_col_map[year]]), float(data[sales_data_col_map[year] + 1]))
                        result.append(city_sales)
        if persist_path is not None:
            with open(persist_path, 'wb') as pkl_file:
                pickle.dump(result, pkl_file)
        return result
    else:
        with open(from_cache, 'rb') as pkl_file:
            return pickle.load(pkl_file)


sf_price_dict = read_sf_price('/Users/leon/Documents/Inventory/顺丰全国到全国标快及特惠报价单201709.xlsx',
                              from_cache='/Users/leon/Documents/Inventory/Test/sf_price_real_01.dat')

city_sales_count = get_city_sales_count('/Users/leon/Documents/Inventory/Test/city_yby_update.txt', sf_price_dict,
                                        [2014, 2015, 2016, 2017],
                                        persist_path='/Users/leon/Documents/Inventory/Test/sales_counts.dat')
