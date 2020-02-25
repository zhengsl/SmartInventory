#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import pymongo
from collections import defaultdict
from dateutil.parser import parse


def extract_whole_sale_volumn():

    mongo_client = pymongo.MongoClient()

    db_test_01 = mongo_client.db_test_01

    sale_volumns_dict = defaultdict(int)

    for doc in db_test_01.source.find():
        create_date = str(doc['create_time'].date())
        quantity = doc['quantity']
        sale_volumns_dict[create_date] += quantity

    sorted_data = sorted(sale_volumns_dict.items())

    sale_volumns = [{"create_date": parse(day_sale[0]), "quantity": day_sale[1]} for day_sale in sorted_data]

    db_test_01.whole_sale_volumn_day.insert_many(sale_volumns)

    mongo_client.close()


def extract_province_sale_volumn():

    mongo_client = pymongo.MongoClient()

    db_test_01 = mongo_client.db_test_01

    sale_volumns_dicts = {'重庆': defaultdict(int), '云南省': defaultdict(int), '陕西省': defaultdict(int),
                          '四川省': defaultdict(int), '贵州省': defaultdict(int), '甘肃省': defaultdict(int),
                          '青海省': defaultdict(int)}

    sale_volumns_cols = {'重庆': 'chongqing_sale_volumn_day', '云南省': 'yunnan_sale_volumn_day',
                         '陕西省': 'shanxi_sale_volumn_day', '四川省': 'sichuan_sale_volumn_day',
                         '贵州省': 'guizhou_sale_volumn_day', '甘肃省': 'gansu_sale_volumn_day',
                         '青海省': 'qinghai_sale_volumn_day'}

    for doc in db_test_01.source.find():
        create_date = str(doc['create_time'].date())
        quantity = doc['quantity']
        province = doc['province']
        if province in sale_volumns_dicts:
            sale_volumns_dicts[province][create_date] += quantity
        else:
            print("{}: {}, {}, {}".format(doc['_id'], create_date, quantity, province))

    for k, v in sale_volumns_dicts.items():
        sorted_data = sorted(v.items())
        sale_volumns = [{"create_date": parse(day_sale[0]), "quantity": day_sale[1]} for day_sale in sorted_data]
        print("{}: {}".format(k, len(sale_volumns)))
        db_test_01[sale_volumns_cols[k]].insert_many(sale_volumns)


def extract_whole_sku_sale_volumn():
    mongo_client = pymongo.MongoClient()

    db_test_01 = mongo_client.db_test_01

    sale_volumns_dict = defaultdict(int)

    for doc in db_test_01.source.find():
        create_date = str(doc['create_time'].date())
        sku_code = doc['sku_code']
        sku_cate_id = doc['sku_categories_id']
        sku_type_id = doc['sku_type_id']
        quantity = doc['quantity']
        key = "{}:{}:{}:{}".format(create_date, sku_code, sku_cate_id, sku_type_id)
        sale_volumns_dict[key] += quantity

    sorted_data = sorted(sale_volumns_dict.items(), key=lambda x: x[0].split(":")[0])

    sale_volumns = []
    for day_sale in sorted_data:
        key_info = day_sale[0].split(":")
        sale_volumns.append({"create_date": parse(key_info[0]), "sku_code": key_info[1],
                             "sku_categories_id": int(key_info[2]), "sku_type_id": int(key_info[3]),
                             "quantity": day_sale[1]})

    db_test_01.sku_sale_volumn_day.insert_many(sale_volumns)

    mongo_client.close()


if __name__ == "__main__":
    extract_whole_sku_sale_volumn()
