import json
import requests
import time
import datetime
import mysql.connector as sql

current_league_url = "https://www.pathofexile.com/api/ladders/Blight"


rds_host='pypoe.cgqezikpygym.eu-west-2.rds.amazonaws.com'
creds=open('creds.txt', 'r')
pwd=(creds.read()).strip()

con=sql.connect(host=rds_host, user='admin', password=pwd, database='pytest')
cursor=con.cursor(buffered=True)

#list_of_acctchr=open("C:\\list_of_acctchr.txt", "r", encoding="utf-8")

cursor.execute("SELECT * FROM Acc_Chr")
list_of_acctchr=cursor.fetchall()
dbg=open("dbg.log", "w+", encoding="utf-8")
dbg.write("----------------------------------------------------------")
dbg.write(f"[{datetime.datetime.now()}] script start\n")

idfile=open('computerid', 'r')
paramfile=open('params_fourth', 'r')
requestlimit=int(paramfile.read())
computerid=int(idfile.read())

items = open("items.json", "w+", encoding="utf-8")
list_items=[]
request=0

for acct_chr in enumerate(list_of_acctchr):
	if(computerid * 5000 <= acct_chr[0] <= computerid*5000 + 5000):
		acct=acct_chr[1][0]
		chr=acct_chr[1][1]
		print (f"Reqest number {acct_chr[0]}")
		print (f"https://www.pathofexile.com/character-window/get-items?accountName={acct}&character={chr}")
		attempts=0
		while(True):
			if(attempts >= 4): 
				break
			response = requests.get(f"https://www.pathofexile.com/character-window/get-items?accountName={acct}&character={chr}")

			print(response.status_code)
			if(response.status_code==200):
				list_items.append(response.json())
				break
			elif(response.status_code!=429):
				break
			time.sleep(30)
			attempts+=1
		request+=1
		dbg.write(f"[{datetime.datetime.now()}] Request iteration {request} for https://www.pathofexile.com/character-window/get-items?accountName={acct}&character={chr} with response code {response.status_code}\n")
		time.sleep(2.5)
		if (request >= requestlimit):
			time.sleep(15)
			request=0
json.dump(list_items, items, indent=4, ensure_ascii=False)