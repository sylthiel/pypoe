#data_handler
#this script will combine the functionality of 2-5.py
#first it will obtain the ladder and store it in grabbed.json
#then it will handle the characters and store their items in SQL
import json
import requests
import mysql.connector as sql
import time




# CURRENT CONSTANTS: 3.8
current_league_url = "https://www.pathofexile.com/api/ladders/Blight"
MAX_LADDER=15000
#

# SQL connection 
rds_host='pypoe.cgqezikpygym.eu-west-2.rds.amazonaws.com'
with open('creds.txt', 'r') as creds
	pwd=(creds.read()).strip()
sql_connection=sql.connect(host=rds_host, user='admin', password=pwd, database='pytest')
cursor=sql_connection.cursor(buffered=True)
#very_nice_credntial_handling.jpeg

# File opening
db=open("grabbed.json", "w+", encoding='utf-8')
dbg=open("dbg.log", "a+", encoding="utf-8")
#

def handle_ladder_request_response(offset):
	response = requests.get(f"{current_league_url}?limit=200&offset={str(offset)}")
	if(response.status_code == 200):
		return response.json()
	elif(response.status_code == 429):
		time.sleep(2)
		response = requests.get(f"{current_league_url}?limit=200&offset={str(offset)}")
		if (response.status_code == 429):
			dbg.write(f"DENIED(429): {datetime.datetime.now()} for {current_league_url}?limit=200&offset={str(offset)}")
			return ''
		elif(response.status_code == 200):
			return response.json()
		else:
			dbg.write(f"ERROR {response.status_code}: {datetime.datetime.now()} for {current_league_url}?limit=200&offset={str(offset)}")
			return ''
def obtain_ladder(current_league_url):
	list_grabbed = []
	offset=0
	while (offset+200<= MAX_LADDER):
		chunk=handle_ladder_request_response(offset)
		if(chunk):
			list_grabbed.append(chunk)
		offset+=200
		db.write("\n")
	return json.dump(list_grabbed, indent=4, ensure_ascii=False)

def ladder_to_sql():
    insert_query="INSERT INTO Characters (account_name, character_name, char_id) VALUES (%s, %s, %s);"
    character_list=obtain_ladder(current_league_url)
    
    for i in range(len(character_list)):
        for j in range (len(character_list[i]["entries"])):
            acct_chr=(str(character_list[i]["entries"][j]["account"]["name"]), str(character_list[i]["entries"][j]["character"]["name"]), str(character_list[i]["entries"][j]["rank"]))
            cursor.execute(insert_query, acct_chr)
    sql_connection.commit()

ladder_to_sql()
#json.dump(obtain_ladder(current_league_url), db, indent=4, ensure_ascii=False)




