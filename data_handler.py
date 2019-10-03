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


def obtain_ladder(current_league_url):
	list_grabbed = []
	offset=0
	while (offset+200<= MAX_LADDER):
		response=handle_ladder_request_response(offset)
		response = requests.get(f"{current_league_url}?limit=200&offset={str(offset)}")
		offset+=200
		db.write("\n")
		print (response.status_code)
json.dump(list_grabbed, db, indent=4, ensure_ascii=False)




