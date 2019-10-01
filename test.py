import json
import requests
import time
import datetime
import mysql.connector as sql

current_league_url = "https://www.pathofexile.com/api/ladders/Blight"


rds_host='pypoe.cgqezikpygym.eu-west-2.rds.amazonaws.com'
creds=open('creds.txt', 'r')
pwd=(creds.read()).strip()
idfile=open('computerid', 'r')
computerid=int(idfile.read())
con=sql.connect(host=rds_host, user='admin', password=pwd, database='pytest')
cursor=con.cursor(buffered=True)

#list_of_acctchr=open("C:\\list_of_acctchr.txt", "r", encoding="utf-8")

cursor.execute("SELECT * FROM Acc_Chr")
list_of_acctchr=cursor.fetchall()

dbg=open("dbg.log", "w+", encoding="utf-8")
dbg.write("----------------------------------------------------------")
dbg.write(f"[{datetime.datetime.now()}] script start\n")
items = open("items.json", "w+", encoding="utf-8")
list_items=[]
request=0
for acct_chr in enumerate(list_of_acctchr):
	#if()
	print (acct_chr)
	print ("----")
