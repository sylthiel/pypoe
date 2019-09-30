##GRABBER
import json
import requests
import mysql.connector as sql

rds_host='pypoe.cgqezikpygym.eu-west-2.rds.amazonaws.com'
creds=open('creds.txt', 'r')
pwd=(creds.read()).strip()

con=sql.connect(host=rds_host, user='admin', password=pwd, database='pytest')
cursor=con.cursor(buffered=True)

insert_query="INSERT INTO Acc_Chr VALUES (%s, %s);"


with open("grabbed.json", "r") as data_file:
	character_list = json.load(data_file)

for i in range(len(character_list)):
	for j in range (len(character_list[i]["entries"])):
		acct_chr=("", "")
		acct_chr=(str(character_list[i]["entries"][j]["account"]["name"]), str(character_list[i]["entries"][j]["character"]["name"]))
		
		cursor.execute(insert_query, acct_chr)
		char_count += 1

con.commit()