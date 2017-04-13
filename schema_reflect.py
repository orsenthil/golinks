#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import (create_engine, Table, Column, Integer, String, MetaData)

eng = create_engine("mysql://root@localhost/testdb")

meta = MetaData()
meta.reflect(bind=eng)

for table in meta.tables:
    print(table)
