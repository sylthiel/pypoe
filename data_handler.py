#data_handler
#this script will combine the functionality of 2-5.py
#first it will obtain the ladder and store it in grabbed.json
#then it will handle the characters and store their items in SQL

#limit can be set with the function call parameter request_limit for debug
import json
import requests
import mysql.connector as sql
import time
import datetime

class poe_gem:
	def __repr__(self):
		return f"{self.name} ({self.colour})"
	def __init__(self):
		self.colour=''
		self.name=''
		self.support=False
		self.tags=[]
		self.socketedIn=''
class poe_item:
	def __init__(self, inventoryId='', socketgroups=[], gems=[]):
		self.inventoryId=inventoryId
		self.socketgroups=socketgroups
		self.gems=gems
		self.links=''
		self.sortedlinks=''
	def create_links(self):
		linkage=''
		for x in self.socketgroups:
			if (x):
				linkage=linkage+x
			else:
				linkage=linkage + '.'
		self.links=linkage.rstrip('.')
		self.sortedlinks=''.join(sorted(self.links))
	def __repr__(self):
		s = f"{self.inventoryId}\n links are {self.links}\n {(self.gems)}"
		return s
class poe_character:
	def __init__ (self, rank, account_name, character_name, subclass):
		self.rank=rank
		self.account_name = account_name
		self.character_name = character_name
		self.subclass=subclass
		self.gemdump=[]
		self.socketgroupsdump=[]
		self.items=[]
	def yeet_to_sql(self):
		dbg.write(f"Yeeting {self.rank} --	 {self.account_name} -- {self.account_name}")
		for item in self.items:
			cursor.execute(INSERT_ITEM_QUERY, (item.inventoryId, item.sortedlinks, self.rank))
			for gem in item.gems:
				cursor.execute(INSERT_GEM_QUERY, (gem.colour, gem.name, gem.support, " ".join(gem.tags), self.rank, gem.socketedIn))
		sql_connection.commit()





## QUERY DEFINITIONS
GET_CHARACTERS_QUERY = """SELECT * FROM characters WHERE (%s <= char_id) AND (char_id <= %s);"""
INSERT_ITEM_QUERY = "INSERT INTO items (inventory_id, sorted_links, char_id) VALUES (%s, %s, %s);"
INSERT_GEM_QUERY = "INSERT INTO gems (colour, name, support, tags, char_id, socketed_in) VALUES (%s, %s, %s, %s, %s, %s);"
##

# CURRENT CONSTANTS: 3.8
current_league_url = "https://www.pathofexile.com/api/ladders/Blight"
MAX_LADDER=15000
# GEM COLOR TRANLSATION -- GGG CODES SOCKETS AS RGB BUT GEMS AS SDI ¯\_(ツ)_/¯¯
translation={"S" : "R", "D" : "G", "I" : "B", "W" : "W", "A": "A"}
#

# SQL connection 
rds_host='pypoe.cgqezikpygym.eu-west-2.rds.amazonaws.com'
with open('creds.txt', 'r') as creds:
	pwd=(creds.read()).strip()
sql_connection=sql.connect(host=rds_host, user='admin', password=pwd, database='pytest')
cursor=sql_connection.cursor(buffered=True)
cursor.execute("SET NAMES 'utf8mb4';")
#very_nice_credntial_handling.jpeg

# File opening
#db=open("grabbed.json", "w+", encoding='utf-8')
dbg=open("dbg.log", "a+", encoding="utf-8")
with open('computerid', 'r') as id:
	computerid=int(id.read())
#


def tagify (tags):
	return sorted((tags.replace(',','').split()))

def parse_api_character_items(api_character_items, rank, account, character):
	socketgroups=[]
	gems=[]
	items=[]
	tmp_character=poe_character(rank, account, character, api_character_items["character"]["class"])
	has_items=0
	print(f"rank {rank} character {character} items parsing")
	for item in api_character_items['items']:
		tmp_item=poe_item()
		if ('sockets' in item):
			has_items=1
			tmp_socketgroup=['','','','','','']
			for socket in item['sockets']:				
				if(socket['sColour'] != 'A'):
					tmp_socketgroup[socket['group']]+=socket['sColour']
			tmp_item=poe_item(item["inventoryId"], tmp_socketgroup)
		if ('socketedItems' in item):
			for gem in item['socketedItems']:
				if('abyssJewel' in gem):
					continue
				tmp=poe_gem()
				tmp.socketedIn=item["inventoryId"]
				tmp.colour=translation.get(gem['colour'])	
				tmp.name=gem['typeLine']
				tmp.support=gem['support']
				tmp.tags=tagify(gem['properties'][0]["name"])
				print(f"tmp.tags={tmp.tags}")
				#print(type(gem['properties'][0]["name"]))
				#print(sorted((gem['properties'][0]["name"])))
				gems.append(tmp)
		if(gems):
			tmp_item.gems = gems
			tmp_item.create_links()
			tmp_character.items.append(tmp_item)
		gems=[]
	if(has_items):
		tmp_character.yeet_to_sql()
	else:
		dbg.write(f"Character {tmp_character.character_name} of rank {tmp_character.rank} has no items -- omitting from yeeting")
		print(f"Character {tmp_character.character_name} of rank {tmp_character.rank} has no items -- omitting from yeeting")
def handle_ladder_request_response(offset, current_league_url):
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
		chunk=handle_ladder_request_response(offset, current_league_url)
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
def grab_items(lboundary=int(computerid)*5000, rboundary=int(computerid*5000 + 5000), request_limit=9001):
	dbg.write("----------------------------------------------------------")
	dbg.write(f"[{datetime.datetime.now()}] started working item data")
	list_items=[]
	cursor.execute(GET_CHARACTERS_QUERY, (lboundary, rboundary,))
	list_of_acctchr=cursor.fetchall()
	request=0
	for acct_chr in (list_of_acctchr):
		rank, acct, chr = acct_chr[0], acct_chr[1], acct_chr[2]
		print (f"Reqest number {acct_chr[0]}")
		print (f"https://www.pathofexile.com/character-window/get-items?accountName={acct}&character={chr}")
		attempts=0
		success=0
		while(True):
			if(attempts > 3): 
				break
			try:
				response = requests.get(f"https://www.pathofexile.com/character-window/get-items?accountName={acct}&character={chr}")
			except ConnectionError as err:
				dbg.write(f"FATALLY FAILING ON {request} with {str(err)}. Sleeping for 180")
				time.sleep(180)
				continue
			except:
				dbg.write(f"{sys.exc_info} FUCKED ME UP")
			print(response.status_code)
			if(response.status_code==200):
				current_character_items=response.json()
				success=1
				break
			elif(response.status_code!=429):
				break
			attempts += 1 
		request += 1
		if(success):
			parse_api_character_items(current_character_items, rank, acct, chr)
		dbg.write(f"[{datetime.datetime.now()}] Request iteration {request} for https://www.pathofexile.com/character-window/get-items?accountName={acct}&character={chr} with response code {response.status_code}\n")
		time.sleep(1)
		if(request >= request_limit):
			break;
#print(datetime.datetime.now())
#ladder_to_sql()
#print(datetime.datetime.now())
#grab_items()
#print(datetime.datetime.now())
#json.dump(obtain_ladder(current_league_url), db, indent=4, ensure_ascii=False)
