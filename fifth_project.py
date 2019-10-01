# This will analyze item data grabbed by fourth_project.py
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
cursor.execute("SET NAMES 'utf8mb4';")
#list of grabbed characters with their items
items = open("items.json", "r", encoding="utf-8")
items_json=json.load(items)

# GEM COLOR TRANLSATION -- GGG CODES SOCKETS AS RGB BUT GEMS AS SDI ¯\_(ツ)_/¯¯
translation={"S" : "R", "D" : "G", "I" : "B", "W" : "W", "A": "A"}

class poe_gem:
	def __repr__(self):
		return f"{self.name} ({self.colour})"
	def __init__(self):
		self.colour=''
		self.name=''
		self.support=False
		self.tags=[]
		self.socketedIn=''

class link_set:
	def __init__(self):
		self.gems=[]
		self.inventoryId=''
		self.length=-1
	def __init__(self, gemlist: list):
		self.gems=gemlist
		self.inventoryId=gemlist[0].socketedIn
		self.length=len(gemlist)

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
	def __init__(self):
		self.rank=15001
		self.account_name = ''
		self.character_name = ''
		self.character_view_url = ''
		self.gems_used=[]
		self.subclass=''
		self.gemdump=[]
		self.socketgroupsdump=[]
		self.items=[]
		self.linksets=[]

def get_account_name(charname):
	response=requests.get(f"https://www.pathofexile.com/character-window/get-account-name-by-character?character={charname}")
	if (response.status_code == 200):
		rjson=response.json()
		return rjson["accountName"]
	if (response.status_code == 429):
		time.sleep(3)
		response=requests.get(f"https://www.pathofexile.com/character-window/get-account-name-by-character?character={tmp_character.character_name}")
		if (response.status_code == 429):
			return "429"
		elif(response.status_code == 200):
			rjson=response.json()
			return rjson["accountName"]

socketgroups=[]
gems=[]
characters=[]
for rank, character in enumerate(items_json):
	print(f"Rank {rank}: {character['character']['name']}")
	tmp_character = poe_character()
	tmp_character.rank = rank
	tmp_character.character_name = character["character"]["name"]
	tmp_character.subclass = character["character"]["class"]
	response=requests.get(f"https://www.pathofexile.com/character-window/get-account-name-by-character?character={tmp_character.character_name}")
	rjson=response.json()
	if (response.status_code == 200):
		tmp_character.account_name = rjson["accountName"]
	if (response.status_code == 429):
		time.sleep(3)
		response=requests.get(f"https://www.pathofexile.com/character-window/get-account-name-by-character?character={tmp_character.character_name}")
		if (response.status_code == 429):
			tmp_character.account_name = "429"
		elif(response.status_code == 200):
			rjson=response.json()
			tmp_character.account_name = rjson["accountName"]
	real_items=0
	for item in character['items']:
		tmp_item=poe_item()
		if ('sockets' in item):
			real_items=1
			tmp_socketgroup=['','','','','','']
			for socket in item['sockets']:				
				#print( f"{socket['group']} <- {socket['sColour']} \n")
				if(socket['sColour'] != 'A'):
					tmp_socketgroup[socket['group']]+=socket['sColour']
			#print(f"tmp_socketgroup = {tmp_socketgroup}\n")
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
				tmp.tags=gem['properties'][0]["name"]
				gems.append(tmp)
				#print(f"current len = {len(gems)}")

		if(gems):
			tmp_item.gems = gems
			tmp_item.create_links()
			tmp_character.items.append(tmp_item)
		gems=[]
	if(real_items):
		characters.append(tmp_character)
print(f"AN {characters[0].account_name} CN {characters[0].character_name}")

INSERT_CHAR_QUERY = "INSERT INTO characters (char_id, account_name, character_name) VALUES (%s, %s, %s);"
INSERT_ITEM_QUERY = "INSERT INTO items (item_id, inventory_id, sorted_links, char_id) VALUES (%s, %s, %s, %s);"
INSERT_GEM_QUERY = "INSERT INTO gems (colour, name, support, tags, item_id, char_id) VALUES (%s, %s, %s, %s, %s, %s);"
item_id=0
for char_id, char in enumerate(characters):
	print ("running the following query:")
	print (INSERT_CHAR_QUERY)
	print (f"{char_id} --  {char.account_name} -- {char.account_name}")
	cursor.execute(INSERT_CHAR_QUERY, (char_id, char.account_name, char.character_name))
	for item in char.items:
		cursor.execute(INSERT_ITEM_QUERY, (item_id, item.inventoryId, item.sortedlinks, char_id))
		for gem in item.gems:
			cursor.execute(INSERT_GEM_QUERY, (gem.colour, gem.name, gem.support, gem.tags, item_id, char_id))
		item_id+=1

con.commit()
