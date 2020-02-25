#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from optimize_cost import *

from collections import defaultdict

sales_data_col_map = {
    2017: 4,
    2014: 6,
    2015: 8,
    2016: 10,
    2018: 12
}


def city_price_matrix_test(filepath, delimiter, sf_price_dict, year):

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
                    sales.append(int(data[sales_data_col_map[year]]))
    size = len(cities)
    for i in range(size):
        result.append([sf_price_dict[cities[i][0]][cities[j][0]] for j in range(size)])
    return result, cities, sales


def get_city_sales_count(filepath, delimiter, sf_price_dict, years):

    result = []

    with open(filepath, 'rb') as fp:
        lines = fp.readlines()
        for line in lines:
            data = line.decode('utf-8').strip().split(delimiter)
            print(data)
            if "NA" not in data:
                city = data[2][1:-1]
                if city in sf_price_dict and city != "阿勒泰地区":
                    province = data[3][1:-1]
                    city_sales = [city, province]
                    city_sales.extend([data[sales_data_col_map[year]] for year in years])
                    result.append(city_sales)

    return result


def start_clustering_test(year, store_num):
    sf_price_dict = read_sf_price('/Users/leon/Documents/Inventory/顺丰全国到全国标快及特惠报价单201709.xlsx',
                                  from_cache='/Users/leon/Desktop/sf_price.dat')
    sf_matrix, cities, sales = city_price_matrix_test('/Users/leon/Desktop/city_yby_update.txt', ' ', sf_price_dict,
                                                 year)
    print(sum(sales))
    tlc = compute_total_logistics_cost(sf_matrix, sales)
    ttc = compute_total_time_cost(cities)
    print("Data Preparing Stage clear.")
    print("Start to clustering for {} stores.".format(store_num))
    clusters = find_out_solution(tlc, ttc, cities, sales, store_num)

    with open('/Users/leon/Desktop/city_index_{}.txt'.format(store_num), 'w', encoding='utf-8') as city_fp:
        for i, city in enumerate(cities):
            city_fp.write("{}: {} {}\n".format(i, city[0], city[1]))

    with open('/Users/leon/Desktop/cluster_index_{}.txt'.format(store_num), 'w', encoding='utf-8') as cluster_i_fp:
        for cluster in clusters:
            cluster_i_fp.write("{}:{}:{}:{}:{}:{}\n".format(cluster.center, cluster.time_distance,
                                                            cluster.total_quantities, cluster.cost,
                                                            len(cluster.nodes), cluster.nodes))

    with open('/Users/leon/Desktop/cluster_city_{}.txt'.format(store_num), 'w', encoding='utf-8') as cluster_c_fp:
        for cluster in clusters:
            cluster_c_fp.write("{}:{}:{}:{}:{}:{}\n".format(cities[cluster.center][0], cluster.time_distance,
                                                            cluster.total_quantities, cluster.cost, len(cluster.nodes),
                                                            [cities[node][0] for node in cluster.nodes]))


def get_time_distance(ttc_matrix, quantities, nodes, center):
    total_time_cost = 0
    total_quantities = 0
    for index in nodes:
        total_time_cost += ttc_matrix[center][index] * quantities[index]
        total_quantities += quantities[index]
    return total_time_cost / total_quantities


def start_clustering_fix_center(total_sales, centers):
    sf_price_dict = read_sf_price('/Users/leon/Documents/Inventory/顺丰全国到全国标快及特惠报价单201709.xlsx',
                                  from_cache='/Users/leon/Documents/Inventory/Test/sf_price_real_01.dat')

    sf_matrix, cities, sales = city_price_matrix('/Users/leon/Documents/Inventory/Test/city_yby_update.txt', ' ',
                                                 sf_price_dict, total_sales)

    tlc = compute_total_logistics_cost(sf_matrix, sales)
    ttc = compute_total_time_cost(cities)

    cities_dict = {}

    for i, city in enumerate(cities):
        cities_dict[city[0]] = i

    row_num = len(tlc[0])

    result = defaultdict(list)
    result_cost = defaultdict(int)
    for j in range(row_num):
        min_center, min_cost = -1, 2147483647000000000
        for center in centers:
            center_index = cities_dict[center]
            if tlc[center_index][j] < min_cost:
                min_cost = tlc[center_index][j]
                min_center = center_index
        result[min_center].append(j)
        result_cost[min_center] += min_cost

    with open('/Users/leon/Desktop/cluster_fix_center.txt', 'w', encoding='utf-8') as cluster_fp:
        total_cost = 0
        for center, cluster in result.items():
            avg_lead_time = get_time_distance(ttc, sales, cluster, center)
            cluster_fp.write("{}:{}:{}:{}:{}\n".format(cities[center][0], avg_lead_time, result_cost[center],
                                                       len(cluster), [cities[i][0] for i in cluster]))
            total_cost += result_cost[center]
        cluster_fp.write("total cost: {}\n".format(total_cost))


if __name__ == "__main__":
    sf_price_dict = read_sf_price('/Users/leon/Documents/Inventory/顺丰全国到全国标快及特惠报价单201709.xlsx',
                                  from_cache='/Users/leon/Documents/Inventory/Test/sf_price_real_01.dat')
    sales_counts = get_city_sales_count('/Users/leon/Documents/Inventory/Test/city_yby_update.txt', ' ', sf_price_dict, [2014, 2015])
    with open('/Users/leon/Desktop/sales_cout_2014_2015.txt', 'w', encoding='utf-8') as fp:
        for sc in sales_counts:
            fp.write("{},{},{},{}\r\n".format(sc[0], sc[1], sc[2], sc[3]))
