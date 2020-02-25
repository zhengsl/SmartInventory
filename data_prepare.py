#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import xlrd
import pymongo
import pymysql
from datetime import datetime, timedelta
import traceback

month_dict = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
              'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}

year_dict = {'13': 2013, '14': 2014, '15': 2015, '16': 2016, '17': 2017}


def read_from_excel_to_mongo(file):

    mongo_client = pymongo.MongoClient()

    db_test_01 = mongo_client.db_test_01

    with xlrd.open_workbook(file) as excel:
        table = excel.sheet_by_index(0)
        row_num = table.nrows - 1

        group_size = 10000
        group_num = row_num // group_size
        last_group = row_num - group_num * group_size
        if last_group != 0:
            group_num = group_num + 1

        for i in range(group_num):
            records = []
            iter_size = group_size if i != group_num - 1 else last_group
            for j in range(iter_size):
                index = j + i * group_size + 1
                row_v = table.row_values(index)
                record = {
                    "owner": row_v[0],
                    "code": row_v[1],
                    "slip_code": row_v[2],
                    "create_time": gen_datetime(row_v[3]),
                    "province": row_v[4],
                    "city": row_v[5],
                    "sku_code": row_v[6],
                    "bar_code": row_v[7],
                    "wms_sku_color_original": row_v[8],
                    "wms_sku_size_original": row_v[9],
                    "sku_categories_id": int(row_v[10]) if row_v[10] != '' else -1,
                    "sku_type_id": int(row_v[11]) if row_v[11] != '' else -1,
                    "supplier_code": row_v[12],
                    "quantity": int(row_v[13])
                }
                print("{}: {}".format(index, record.values()))
                records.append(record)

            print("Bulk write to MongoDB...")
            db_test_01.source.insert_many(records)

    mongo_client.close()


def gen_datetime(date_time_str):

    dt_array = date_time_str.split(' ')

    date_array = dt_array[0].split('-')
    day = int(date_array[0])
    month = month_dict[date_array[1]]
    year = year_dict[date_array[2]]

    time_array = dt_array[1].split('.')
    hour = int(time_array[0]) + 12 if dt_array[2] == 'PM' and time_array[0] != '12' else int(time_array[0])
    minute = int(time_array[1])
    second = int(time_array[2])

    return datetime(year, month, day, hour, minute, second)


def read_from_excel_to_mysql(file):

    start = 1

    mysqldb = pymysql.connect(host="localhost", user="root", passwd="zhengsl", db="nike_sales", charset="utf8")

    cursor = mysqldb.cursor()

    sql = '''insert into sales_detail(shop, tb_order_id, platform_id, out_time, province, city, sku_color,
             sku_size, outer_sku_id, jmsku_code, supplier_sku_code, bu, global_category, descriptio, genderage,
             msrp, sihouette, global_category_gender, requested_qty, price, total_amt, discount_amt) 
             values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

    genderage = {'MENS': 0, 'WOMENS': 1, 'ADULT UNISEX': 2, 'KIDS': 3, '': -1}

    try:
        with xlrd.open_workbook(file) as excel:
            table = excel.sheet_by_index(0)
            for rowIndex in range(start, table.nrows):
                row_v = table.row_values(rowIndex)
                print(row_v)
                cursor.execute(sql, (row_v[0], row_v[1], row_v[2], getsqldatestr(row_v[3]), row_v[4], row_v[5], row_v[6],
                                     row_v[7], row_v[8], row_v[9], row_v[10], get_int(row_v[11]), row_v[12], row_v[13],
                                     genderage[row_v[14]], get_float(row_v[15]), row_v[16], row_v[17], int(row_v[18]),
                                     get_float(row_v[19]), get_float(row_v[20]), get_float(row_v[21])))
                print("ROW NO.{} inserted".format(rowIndex))
        mysqldb.commit()
        print("Completed")
    except pymysql.err.DataError:
        traceback.print_exc()
        mysqldb.commit()
        print("ROW NO.{} to be inserted".format(rowIndex+1))
    finally:
        mysqldb.close()


def read_from_excel_to_mysql_11(file, year):

    start = 1

    mysqldb = pymysql.connect(host="localhost", user="root", passwd="zhengsl", db="nike_sales", charset="utf8")

    cursor = mysqldb.cursor()

    sql = '''insert into double_eleven_all(shop, repo, year, province, city, outer_sku_id, name, sku_color, sku_size, 
             genderage, global_category,  bu, sihouette, requested_qty, global_category_gender, msrp, price, total_amt) 
             values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

    genderage = {'MENS': 0, 'WOMENS': 1, 'ADULT UNISEX': 2, 'KIDS': 3, '': -1}

    try:
        with xlrd.open_workbook(file) as excel:
            table = excel.sheet_by_index(0)
            for rowIndex in range(start, table.nrows):
                row_v = table.row_values(rowIndex)
                print(row_v)
                cursor.execute(sql, (row_v[0], row_v[1], year, row_v[2], row_v[3], row_v[4], row_v[5], row_v[6],
                                     row_v[7], genderage[row_v[8]], row_v[9], get_int(row_v[10]), row_v[11],
                                     get_int(row_v[12]), row_v[13], get_float(row_v[14]), get_float(row_v[15]),
                                     get_float(row_v[16])))
                print("ROW NO.{} inserted".format(rowIndex))
        mysqldb.commit()
        print("Completed")
    except pymysql.err.DataError:
        traceback.print_exc()
        #mysqldb.commit()
        print("ROW NO.{} to be inserted".format(rowIndex+1))
    finally:
        mysqldb.close()


def read_from_txt_to_mysql(file, year, start=0):

    mysqldb = pymysql.connect(host="localhost", user="root", passwd="zhengsl", db="nike_sales", charset="utf8")

    cursor = mysqldb.cursor()

    sql = '''insert into not_deleven_all_{}(out_time, shop, order_id, repo, province, city, supplier_sku_code, sku_color,
             sku_size, sku_name, sap_division, gender_age, global_category_name, global_focus_name, qty) 
             values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''.format(year)

    try:
        count = 0
        with open(file, mode='r', encoding='utf-8') as source:
            line = source.readline()
            while line and line.strip() != '':
                line = source.readline()
                if line and line.strip() != '':
                    count += 1
                    ignore = True
                    print("{}: {}".format(count, line))
                    if count >= start:
                        line = line.replace('?', '').replace('？', '')
                        data = line.split('\t')
                        cursor.execute(sql, (getsqldatefromstr(data[0]), data[1], data[2], data[3], data[4], data[5], data[6],
                                             data[7], data[8], data[9], get_int(data[10]), get_int(data[11]), data[12], data[13],
                                             get_int(data[14])))
                        ignore = False
                    if not ignore and count % 1000000 == 0:
                        mysqldb.commit()
                else:
                    break
        mysqldb.commit()
    except Exception:
        traceback.print_exc()
    finally:
        mysqldb.close()


def getsqldatestr(original):
    delta = int(original) - 41758
    return datetime(2014, 4, 29) + timedelta(days=delta)


def getsqldatefromstr(dstr):
    mdy = dstr.split('/')
    return datetime(2000+int(mdy[2]), int(mdy[0]), int(mdy[1]))


def get_int(original):
    try:
        return int(original)
    except:
        return 0


def get_float(original):
    try:
        return float(original)
    except:
        return 0


if __name__ == "__main__":
    #read_from_excel_to_mysql_11("/Users/leon/Desktop/data/new/JORDAN双11发货分析_17.xlsx", 17)
    read_from_txt_to_mysql("/Users/leon/Desktop/NIKE/NIKE17年数据.txt", 2017, 5000001)
