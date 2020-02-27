#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

api_host = '0.0.0.0'
api_port = 500

backend_db_type = 'mysql'
backend_db_address = ''

analysis_db_type = 'mongo'
analysis_db_address = ''
analysis_db_username = ''
analysis_db_password = ''


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = backend_db_address
backend_db = SQLAlchemy(app)
