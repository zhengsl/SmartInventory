#!/usr/bin/env python
#  -*- coding: utf-8 -*-
from config import *


class Province(backend_db.Model):
    __tablename__ = 'base_province'

    id = backend_db.Column(backend_db.Integer, primary_key=True)
    name = backend_db.Column(backend_db.String(10), nullable=False)
    full_name = backend_db.Column(backend_db.String(20), nullable=False)

    def __init__(self, name, full_name):
        self.name = name
        self.full_name = full_name
