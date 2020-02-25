#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import pymongo
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict


def whole_sale_volumn_day_plot(colName, title):
    mongo_client = pymongo.MongoClient()

    db_test_01 = mongo_client.db_test_01

    create_dates = []
    quantities = []

    for doc in db_test_01[colName].find():
        create_dates.append(doc['create_date'])
        quantities.append(doc['quantity'])

    ts = pd.Series(quantities, index=create_dates)

    ts.plot(figsize=(12, 8), title=title)

    plt.show()


def whole_sale_volumn_month_plot(colName, title):
    mongo_client = pymongo.MongoClient()

    db_test_01 = mongo_client.db_test_01

    month_quantities = defaultdict(int)

    for doc in db_test_01[colName].find():
        create_date = doc['create_date']
        month_quantities[str(create_date)[:7]] += doc['quantity']

    sorted_data = sorted(month_quantities.items())

    ts = pd.Series([sd[1] for sd in sorted_data], index=[sd[0] for sd in sorted_data])

    ts.plot(kind='bar', figsize=(12, 8), title=title, color='DarkBlue', alpha=0.7)

    print(ts)

    plt.show()


if __name__ == '__main__':
    whole_sale_volumn_month_plot(colName='whole_sale_volumn_day',
                               title="2015-2017 Nike Online Monthly Sales Trend (7 Province)")
