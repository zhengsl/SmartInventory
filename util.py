#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from numpy import mat


def file2matrix(path, delimiter):
    fp = open(path, "rb")
    content = fp.read()
    fp.close()
    row_list = content.splitlines()
    record_list = [map(eval, row.split(delimiter)) for row in row_list if row.strip()]
    return mat(record_list)
