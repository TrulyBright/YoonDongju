# test.py

import oracledb
import os

with oracledb.connect(externalauth=True, dns="wallet") as connection:
    with connection.cursor() as cursor:
        sql = """select sysdate from dual"""
        for r in cursor.execute(sql):
            print(r)
