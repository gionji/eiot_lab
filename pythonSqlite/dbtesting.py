#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

con = lite.connect('dbtest01.db')

with con:
    cur = con.cursor()    
    cur.execute("CREATE TABLE table01( sensors VARCHAR(20), value INT)")
    cur.execute("INSERT INTO table01 VALUES('Audi',52642)")
    cur.execute("INSERT INTO table01 VALUES('Mercedes',57127)")
    cur.execute("INSERT INTO table01 VALUES('Skoda',9000)")
    cur.execute("INSERT INTO table01 VALUES('Volvo',29000)")
    cur.execute("INSERT INTO table01 VALUES('Bentley',350000)")
