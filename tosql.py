#takes data created by other scripts and pushes it to SQL

import mysql.connector as sql
rds_host='pypoe.cgqezikpygym.eu-west-2.rds.amazonaws.com'
creds=open('creds.txt', 'r')
pwd=creds.read()

con=sql.connect(host=rds_host, user='admin', password=pwd)

