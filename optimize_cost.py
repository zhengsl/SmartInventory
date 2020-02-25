#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import xlrd
import pickle


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
                        if fc in result and (tc not in result[fc] or (tc in result[fc] and result[fc][tc][0] > price[0])):
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


def read_leadtime_matrix(file_path):
    result = []
    with xlrd.open_workbook(file_path) as excel:
        table = excel.sheet_by_index(0)
        for i in range(2, table.nrows):
            row_v = table.row_values(i)
            result.append([int(x) for x in row_v[1:]])
    return result


province_map = {'安徽省': ('安徽', 0), '北京': ('北京', 1), '福建省': ('福建', 2), '甘肃省': ('甘肃', 3), '广东省': ('广东', 4),
                '广西壮族自治区': ('广西', 5), '贵州省': ('贵州', 6), '海南省': ('海南', 7), '河北省': ('河北', 8),
                '河南省': ('河南', 9), '黑龙江省': ('黑龙江', 10), '湖北省': ('湖北', 11), '湖南省': ('湖南', 12),
                '吉林省': ('吉林', 13), '江苏省': ('江苏', 14), '江西省': ('江西', 15), '辽宁省': ('辽宁', 16),
                '内蒙古自治区': ('内蒙古', 17), '宁夏回族自治区': ('宁夏', 18), '青海省': ('青海', 19), '山东省': ('山东', 20),
                '山西省': ('山西', 21), '陕西省': ('陕西', 22), '上海': ('上海', 23), '四川省': ('四川', 24),
                '天津': ('天津', 25), '西藏自治区': ('西藏', 26), '新疆维吾尔自治区': ('新疆', 27), '云南省': ('云南', 28),
                '浙江省': ('浙江', 29), '重庆': ('重庆', 30)}


leadtime_matrix = [
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


def city_price_matrix_not_d11(filepath, delimiter, sf_price_dict):
    result = []
    cities = []
    sales = []
    with open(filepath, 'rb') as fp:
        lines = fp.readlines()
        for line in lines:
            data = line.decode('utf-8').strip().split(delimiter)
            if "NA" not in data:
                city = data[0]
                if city in sf_price_dict and city != "阿勒泰地区":
                    province = data[1]
                    cities.append((city, province))
                    sales.append(int(data[2]))
    size = len(cities)
    for i in range(size):
        result.append([sf_price_dict[cities[i][0]][cities[j][0]] for j in range(size)])
    return result, cities, sales



def file2matrix(filepath, delimiter):
    result = []
    with open(filepath, 'rb') as fp:
        lines = fp.readlines()
        for line in lines:
            costs = line.decode('utf-8').strip().split(delimiter)
            #print(costs)
            result.append([int(c) for c in costs])
    return result


weight_dist = [(2.5, 0.798), (1, 0.128), (3.5, 0.028), (6, 0.036), (3, 0.004), (9, 0.005), (1.5, 0.001)]


def compute_total_logistics_cost(logistics_cost, quantities):
    total_logistics_cost = []

    for lc_row in logistics_cost:
        tlc_row = []
        for index, lc in enumerate(lc_row):
            weight_cost = 0
            for wd in weight_dist:
                weight_cost += quantities[index] * wd[1] * (lc[0] + lc[1] * (wd[0] - 1))
            tlc_row.append(int(weight_cost))
        total_logistics_cost.append(tlc_row)

    return total_logistics_cost


def compute_total_time_cost(cities):
    total_time_cost = []

    size = len(cities)
    for i in range(size):
        time_array = []
        for j in range(size):
            from_index = province_map[cities[i][1]][1]
            to_index = province_map[cities[j][1]][1]
            time_array.append(leadtime_matrix[from_index][to_index])
        total_time_cost.append(time_array)

    return total_time_cost


def find_out_solution(tlc_matrix, ttc_matrix, cities, quantities, max_cluster_num=3):
    row_num = len(tlc_matrix[0])
    max_distance = 2147483647000000000

    cluster_list = [Cluster(index, tlc_matrix, ttc_matrix, quantities) for index in range(row_num)]
    rested_index = [index for index in range(row_num)]

    while len(rested_index) > max_cluster_num:
        min_distance, leadtime, min_i, min_j = max_distance, max_distance, 0, 0
        for i in rested_index:
            for j in rested_index:
                if i != j:
                    cost_distance, time_distance = cluster_list[i].distance_to(cluster_list[j])
                    if cost_distance < min_distance or (cost_distance == min_distance and time_distance < leadtime):
                        min_distance, leadtime, min_i, min_j = cost_distance, time_distance, i, j
        cluster_list[min_i].merge(cluster_list[min_j])
        print("{}: {}@{}<--{}@{} {}".format(len(rested_index), cities[min_i][0], cities[min_i][1], cities[min_j][0],
                                         cities[min_j][1], cluster_list[min_i].time_distance))
        rested_index.remove(min_j)

    return [cluster_list[ri] for ri in rested_index]


class Cluster(object):
    def __init__(self, index, tlc_matrix, ttc_matrix, quantities):
        self.nodes = [index]
        self.center = index
        self.tlc_matrix = tlc_matrix
        self.ttc_matrix = ttc_matrix
        self.quantities = quantities
        self.cost = self.tlc_matrix[self.center][self.center]
        self.time_distance = self.ttc_matrix[self.center][self.center]
        self.total_quantities = 0

    def distance_to(self, other):
        before = self.cost + other.cost
        temp_nodes = self.nodes + other.nodes
        (after, center, td) = self._choose_center(temp_nodes)
        cost_distance = after - before
        return cost_distance, td

    def merge(self, other):
        self.nodes = self.nodes + other.nodes
        (cost, index, td) = self._choose_center(self.nodes)
        self.center = index
        self.cost = cost
        self.time_distance = td
        self.total_quantities = sum([self.quantities[i] for i in self.nodes])

    def _choose_center(self, node_list):
        cost_list = []
        for i in node_list:
            total = 0
            for j in node_list:
                total += self.tlc_matrix[i][j]
            cost_list.append((total, i))
        center_tuple = min(cost_list, key=lambda x: x[0])
        time_distance = self._get_time_distance(node_list, center_tuple[1])
        return center_tuple[0], center_tuple[1], time_distance

    def _get_time_distance(self, nodes, center):
        total_time_cost = 0
        total_quantities = 0
        for index in nodes:
            total_time_cost += self.ttc_matrix[center][index] * self.quantities[index]
            total_quantities += self.quantities[index]
        return total_time_cost / total_quantities


def start_clustering(total_sales, store_num, sf_price_dict):
    sf_matrix, cities, sales = city_price_matrix('/Users/leon/Documents/Inventory/Test/city_yby_update.txt', ' ',
                                                 sf_price_dict, total_sales)

    print(sum(sales))

    tlc = compute_total_logistics_cost(sf_matrix, sales)
    ttc = compute_total_time_cost(cities)
    print("Data Preparing Stage clear.")
    print("Start to clustering for {} totally sales and {} stores.".format(total_sales, store_num))
    clusters = find_out_solution(tlc, ttc, cities, sales, store_num)

    with open('/Users/leon/Documents/Inventory/Test/20180125/city_index_{}.txt'.format(store_num), 'w', encoding='utf-8') as city_fp:
        for i, city in enumerate(cities):
            city_fp.write("{}: {} {}\n".format(i, city[0], city[1]))

    with open('/Users/leon/Documents/Inventory/Test/20180125/cluster_index_{}.txt'.format(store_num), 'w', encoding='utf-8') as cluster_i_fp:
        for cluster in clusters:
            cluster_i_fp.write("{}:{}:{}:{}:{}:{}\n".format(cluster.center, cluster.time_distance,
                                                            cluster.total_quantities, cluster.cost,
                                                            len(cluster.nodes), cluster.nodes))

    with open('/Users/leon/Documents/Inventory/Test/20180125/cluster_city_{}.txt'.format(store_num), 'w', encoding='utf-8') as cluster_c_fp:
        for cluster in clusters:
            cluster_c_fp.write("{}:{}:{}:{}:{}:{}\n".format(cities[cluster.center][0], cluster.time_distance,
                                                            cluster.total_quantities, cluster.cost, len(cluster.nodes),
                                                            [cities[node][0] for node in cluster.nodes]))


def start_clustering_nd11(store_num, sf_price_dict):
    sf_matrix, cities, sales = city_price_matrix_not_d11('/Users/leon/Documents/Inventory/2017_not_d11_city_sales.txt',
                                                         ';', sf_price_dict)

    tlc = compute_total_logistics_cost(sf_matrix, sales)
    ttc = compute_total_time_cost(cities)
    print("Data Preparing Stage clear.")
    print("Start to clustering for {} totally sales and {} stores.".format(sum(sales), store_num))
    clusters = find_out_solution(tlc, ttc, cities, sales, store_num)

    with open('/Users/leon/Documents/Inventory/Test/20180321/city_index_{}.txt'.format(store_num), 'w', encoding='utf-8') as city_fp:
        for i, city in enumerate(cities):
            city_fp.write("{}: {} {}\n".format(i, city[0], city[1]))

    with open('/Users/leon/Documents/Inventory/Test/20180321/cluster_index_{}.txt'.format(store_num), 'w', encoding='utf-8') as cluster_i_fp:
        for cluster in clusters:
            cluster_i_fp.write("{}:{}:{}:{}:{}:{}\n".format(cluster.center, cluster.time_distance,
                                                            cluster.total_quantities, cluster.cost,
                                                            len(cluster.nodes), cluster.nodes))

    with open('/Users/leon/Documents/Inventory/Test/20180321/cluster_city_{}.txt'.format(store_num), 'w', encoding='utf-8') as cluster_c_fp:
        for cluster in clusters:
            cluster_c_fp.write("{}:{}:{}:{}:{}:{}\n".format(cities[cluster.center][0], cluster.time_distance,
                                                            cluster.total_quantities, cluster.cost, len(cluster.nodes),
                                                            [cities[node][0] for node in cluster.nodes]))


if __name__ == "__main__":
    sf_price_dict = read_sf_price('/Users/leon/Documents/Inventory/顺丰全国到全国标快及特惠报价单201709.xlsx',
                                  from_cache='/Users/leon/Documents/Inventory/Test/sf_price_real_01.dat')
    for store_count in range(4, 6):
        start_clustering_nd11(store_count, sf_price_dict)


