#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from optimize_cost import *

city_in_use = ["'成都市'", "'廊坊市'", "'苏州市'", "'广州市'"]


def compute_cost_per_cluster(clusters, center, tlc, ttc, cities_dict, sales_dict):
    total_cost, total_time, total_sales = 0, 0, 0

    for city in clusters:
        city_name = city[1:-1]
        total_cost += tlc[cities_dict[center]][cities_dict[city_name]]
        total_time += sales_dict[city_name] * ttc[cities_dict[center]][cities_dict[city_name]]
        total_sales += sales_dict[city_name]
    avg_lead_time = round(total_time / total_sales, 2)

    return avg_lead_time, total_sales, total_cost, total_time


def compute_whole_index(costs):
    whole_cost = 0
    whole_sales = 0
    tavg_sum = 0
    for (center, avg_lt, sales, cost, tt) in costs:
        whole_cost += cost
        whole_sales += sales
        tavg_sum += tt
    return whole_cost, round(tavg_sum / whole_sales, 2)


def compute_cost(cluster_file, total_sales, cost_dir, cost_update_dir, cost_file_name):

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
    costs_update = []
    with open(cluster_file, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
        for line in lines:
            data = line.split(':')
            center = data[0]
            clusters = data[5][1:-2].split(', ')

            avg_lead_time, total_sales, total_cost, total_time = compute_cost_per_cluster(clusters, center, tlc, ttc, cities_dict,
                                                                              sales_dict)

            center_u, avg_lead_time_u, total_sales_u, total_cost_u, total_time_u = center, avg_lead_time, total_sales, \
                                                                                   total_cost, total_time

            for ciu in city_in_use:
                if ciu in clusters and ciu[1:-1] != center:
                    center_u = ciu[1:-1]
                    avg_lead_time_u, total_sales_u, total_cost_u, total_time_u = compute_cost_per_cluster(clusters,
                                                                                                          center_u, tlc,
                                                                                            ttc, cities_dict,
                                                                                            sales_dict)
                    break

            costs.append((center, avg_lead_time, total_sales, total_cost, total_time))
            costs_update.append((center_u, avg_lead_time_u, total_sales_u, total_cost_u, total_time_u))

    whole_cost, tavg_time = compute_whole_index(costs)
    whole_cost_u, tavg_time_u = compute_whole_index(costs_update)

    with open(cost_dir + cost_file_name, 'w', encoding='utf-8') as out:
        for (center, avg_lt, sales, cost, tt) in costs:
            out.write("{}:{}:{}:{}\r\n".format(center, avg_lt, sales, cost))
        out.write("Total Cost: {}\r\n".format(whole_cost))
        out.write("Total Avg Time: {}\r\n".format(tavg_time))

    with open(cost_update_dir + cost_file_name, 'w', encoding='utf-8') as out:
        for (center, avg_lt, sales, cost, tt) in costs_update:
            out.write("{}:{}:{}:{}\r\n".format(center, avg_lt, sales, cost))
        out.write("Total Cost: {}\r\n".format(whole_cost_u))
        out.write("Total Avg Time: {}\r\n".format(tavg_time_u))


if __name__ == "__main__":
    for index in range(4, 21):
        file_name = 'cluster_city_{}.txt'.format(index)
        print("processing {}".format(file_name))
        compute_cost('/Users/leon/Documents/Inventory/Test/20180125/cluster_cities/' + file_name, 4400000,
                     '/Users/leon/Documents/Inventory/Test/20180125/costs/',
                     '/Users/leon/Documents/Inventory/Test/20180125/costs_update/',  file_name)
