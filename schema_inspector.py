#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, inspect

eng = create_engine("mysql://root@localhost/testdb")

insp = inspect(eng)

print(insp.get_table_names())
print(insp.get_columns("Cars"))
print(insp.get_primary_keys("Cars"))
print(insp.get_schema_names())
