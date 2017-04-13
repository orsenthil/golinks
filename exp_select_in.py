#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Table, MetaData, tuple_
from sqlalchemy.sql import select, asc

eng = create_engine("mysql://root@localhost/testdb")

with eng.connect() as conn:
    meta = MetaData(eng)
    cars = Table("Cars", meta, autoload=True)

    k = [(2,), (4,), (6,), (8,)]

    stm = select([cars]).where(tuple_(cars.c.Id).in_(k))
    rs = conn.execute(stm)
    print(rs.fetchall())
