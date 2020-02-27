#!/usr/bin/env python
#  -*- coding: utf-8 -*-
from entity_core import *


def query_province_all():
    return Province.query.all()


def query_province_by_id(pid):
    return Province.query.filter(Province.id == pid).first()


def query_province_by_name(name):
    return Province.query.filter(Province.name == name)


def query_province_by_fullname(full_name):
    return Province.query.filter(Province.full_name == full_name)


def insert_province(name, full_name):
    backend_db.session.add(Province(name=name, full_name=full_name))
    backend_db.session.commit()


def delete_province(pid):
    province = query_province_by_id(pid)
    if province:
        backend_db.session.delete(province)
        backend_db.session.commit()


def update_province(pid, name, full_name):
    province = query_province_by_id(pid)
    if province:
        province.update({'name': name, 'full_name': full_name})
        backend_db.session.commit()
