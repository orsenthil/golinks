#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.sql import text

eng = create_engine("mysql://root@localhost/testdb")

with eng.connect() as conn:
	rs = conn.execute(text('SELECT * FROM Cars'))
	print(rs.keys())
