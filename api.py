#!/usr/bin/env python
#  -*- coding: utf-8 -*-
from dao_base import *
from flask import jsonify


@app.route('/smartinventory/decision/base/province?name=<names>', methods=['GET'])
def get_base_province(names):
    if names == 'all':
        return jsonify(query_province_all())
    else:
        result = []
        for name in names.split(','):
            p = query_province_by_name(name)
            if not p:
                p = query_province_by_fullname(name)
            if p:
                result.append(p)
        return jsonify(result)


@app.route('/smartinventory/decision/base/province_city?name=<name>&id=<pid>', methods=['GET'])
def get_base_province_city(name, pid):
    return 'Hello API 1.2'


@app.route('/smartinventory/decision/base/city?name=<name>', methods=['GET'])
def get_base_city(name):
    return 'Hello API 1.3'


@app.route('/smartinventory/decision/base/express/sf?from=<from_city>&to=<to_city>', methods=['GET'])
def get_base_express_sf(from_city, to_city):
    return 'Hello API 1.4'


@app.route('/smartinventory/decision/base/metadata?id=<data_id>', methods=['GET'])
def get_base_metadata(data_id):
    return 'Hello API 1.5'


@app.route('/smartinventory/decision/stats/sales/province', methods=['POST'])
def stat_sales_province():
    return 'Hello API 2.1'


@app.route('/smartinventory/decision/stats/sales/city', methods=['POST'])
def stat_sales_province():
    return 'Hello API 2.2'


@app.route('/smartinventory/decision/stats/packages/province', methods=['POST'])
def stat_packages_province():
    return 'Hello API 2.3'


@app.route('/smartinventory/decision/stats/packages/city', methods=['POST'])
def stat_packages_province():
    return 'Hello API 2.4'


@app.route('/smartinventory/decision/stats/express/province', methods=['POST'])
def stat_express_cost_province():
    return 'Hello API 2.5'


@app.route('/smartinventory/decision/stats/express/city', methods=['POST'])
def stat_express_cost_province():
    return 'Hello API 2.6'


@app.route('/smartinventory/decision/plan/warehouse/static', methods=['POST'])
def plan_warehouse_static():
    return 'Hello API 3.1'


@app.route('/smartinventory/decision/plan/warehouse/dynamic', methods=['POST'])
def plan_warehouse_dynamic():
    return 'Hello API 3.2'


@app.route('/smartinventory/decision/forecast/sales/province', methods=['POST'])
def forecast_sales_province():
    return 'Hello API 4.1'


@app.route('/smartinventory/decision/forecast/sales/city', methods=['POST'])
def forecast_sales_city():
    return 'Hello API 4.2'


if __name__ == '__main__':
    app.run(api_host, api_port)
