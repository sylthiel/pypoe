#data_handler
#this script will combine the functionality of 2-5.py
#first it will obtain the ladder and store it in grabbed.json
#then it will handle the characters and store their items in SQL
import json
import requests
import mysql.connector as sql
import time
import datetime


## QUERY DEFINITIONS
GET_CHARACTERS_QUERY = """SELECT * FROM characters WHERE char_id <= %s;"""
##

# CURRENT CONSTANTS: 3.8
current_league_url = "https://www.pathofexile.com/api/ladders/Blight"
MAX_LADDER=15000
#

# SQL connection 
rds_host='pypoe.cgqezikpygym.eu-west-2.rds.amazonaws.com'
with open('creds.txt', 'r') as creds:
	pwd=(creds.read()).strip()
sql_connection=sql.connect(host=rds_host, user='admin', password=pwd, database='pytest')
cursor=sql_connection.cursor(buffered=True)
#very_nice_credntial_handling.jpeg

# File opening
#db=open("grabbed.json", "w+", encoding='utf-8')
dbg=open("dbg.log", "a+", encoding="utf-8")
with open('computerid', 'r') as id:
    computerid=int(id.read())
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
	return json.dumps(list_grabbed, indent=4, ensure_ascii=False)

def ladder_to_sql():
    insert_query="INSERT INTO characters (account_name, character_name, char_id) VALUES (%s, %s, %s);"
    character_list=json.loads(obtain_ladder(current_league_url))
    
    for i in range(len(character_list)):
        for j in range (len(character_list[i]["entries"])):
            acct_chr=(str(character_list[i]["entries"][j]["account"]["name"]), str(character_list[i]["entries"][j]["character"]["name"]), str(character_list[i]["entries"][j]["rank"]))
            cursor.execute(insert_query, acct_chr)
    sql_connection.commit()
def grab_items():
    dbg.write("----------------------------------------------------------")
    dbg.write(f"[{datetime.datetime.now()}] started working item data")
    
    cursor.execute(GET_CHARACTERS_QUERY, (int(computerid*5000 + 5000),))
    list_of_acctchr=cursor.fetchall()
    for acct_chr in enumerate(list_of_acctchr):
        acct, chr=acct_chr[1][0], acct_chr[1][1]
        print (f"Reqest number {acct_chr[0]}")
        print (f"https://www.pathofexile.com/character-window/get-items?accountName={acct}&character={chr}")
        attempts=0
        request=0
        while(True):
            if(attempts > 3): 
                break
            try:
                response = requests.get(f"https://www.pathofexile.com/character-window/get-items?accountName={acct}&character={chr}")
            except ConnectionError as err:
                dbg.write(f"FATALLY FAILING ON {request} with {str(err)}. Sleeping for 180")
                time.sleep(180)
                continue
            print(response.status_code)
            if(response.status_code==200):
                list_items.append(response.json())
                break
            elif(response.status_code!=429):
                break
            attempts+=1
        
        request+=1
        dbg.write(f"[{datetime.datetime.now()}] Request iteration {request} for https://www.pathofexile.com/character-window/get-items?accountName={acct}&character={chr} with response code {response.status_code}\n")
        time.sleep(2)
        
        if(request >= 500):
            break;
    
    
print(datetime.datetime.now())
#ladder_to_sql()
grab_items()
print(datetime.datetime.now())
#json.dump(obtain_ladder(current_league_url), db, indent=4, ensure_ascii=False)




