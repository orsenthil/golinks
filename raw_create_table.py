#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.sql import text

eng = create_engine("mysql://root@localhost/testdb")

with eng.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS Cars"))
    conn.execute(text("""CREATE TABLE Cars(Id INTEGER PRIMARY KEY, Name Text, Price INTEGER)"""))
    data = (
        {"Id": 1, "Name": "Audi", "Price": 52642},
        {"Id": 2, "Name": "Mercedes", "Price": 57127},
        {"Id": 3, "Name": "Skoda", "Price": 9000},
        {"Id": 4, "Name": "Volvo", "Price": 29000},
        {"Id": 5, "Name": "Bentley", "Price": 350000},
        {"Id": 6, "Name": "Citroen", "Price": 21000},
        {"Id": 7, "Name": "Hummer", "Price": 41400},
        {"Id": 8, "Name": "Volkswagen", "Price": 21600})
    for line in data:
        conn.execute(text("""INSERT INTO Cars(Id, Name, Price) VALUES(:Id, :Name, :Price)"""), **line)
