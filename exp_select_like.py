#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import select, and_

eng = create_engine("mysql://root@localhost/testdb")

with eng.connect() as conn:
    meta = MetaData(eng)
    cars = Table("Cars", meta, autoload=True)
    stm = select([cars]).where(cars.c.Name.like('%en'))
    rs = conn.execute(stm)
    print(rs.fetchall())
