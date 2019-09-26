# This will analyze item data grabbed by fourth_project.py
import json
import requests

actual_sorted_link_groups=[]

def allocate_gems(groups, gems):
	itemgems=[]
	tmp=''
	for group in groups:
		if(len(group) and len(gems)):
			if (len(gems)>=len(group)):
				tmp=''.join((gems[:len(group)]))
				gems=gems[len(group):]
				itemgems.append(tmp)
			elif(len(gems) < len(group)):
				itemgems.append(''.join(sorted(gems)))
	return itemgems

class poe_gem:
	#colour=''
	#name=''
	#gemtype=''
	#tags=['']
	def __repr__(self):
		return str(self.name) + str(self.colour)
	def __init__(self):
		self.colour=''
		self.name=''
		self.support=False
		self.tags=[]

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


items = open("C:\\items\\items.json", "r", encoding="utf-8")
linkdata=open("C:\\items\\linkdata.txt", "w+", encoding="utf-8")
socketgroups=['','','','','','']
items_json=json.load(items)
socketgroups_data=[]
translation={"S" : "R", "D" : "G", "I" : "B", "W" : "W", "A": "A"}
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
	for item in character['items']:
		if ('sockets' in item):
			for socket in item['sockets']:
				if(socket['sColour'] != 'A'):
					socketgroups[socket['group']]+=socket['sColour']
		if ('socketedItems' in item):
			for gem in item['socketedItems']:
				if('abyssJewel' in gem):
					continue
				tmp=poe_gem()
				tmp.colour=translation.get(gem['colour'])	
				tmp.name=gem['typeLine']
				tmp.support=gem['support']
				tmp.tags=gem['properties'][0]["name"]
			gems.append(tmp)
		tmp_character.socketgroupsdump.append(socketgroups)
		tmp_character.gemdump.append(gems)
		gems=[]
		socketgroups=['','','','','','']
	characters.append(tmp_character)

for i in range (3):
	print (i)
	for x in characters[i].gemdump:
		print(x)