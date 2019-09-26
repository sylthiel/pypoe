# This will analyze item data grabbed by fourth_project.py
import json

actual_sorted_link_groups=[]

def allocate_gems(groups, gems):
	itemgems=[]
	tmp=''
	for group in groups:
		if(len(group) and len(gems)):
			if (len(gems)>=len(group)):
				tmp=''.join(sorted((gems[:len(group)])))
				gems=gems[len(group):]
				itemgems.append(tmp)
			elif(len(gems) < len(group)):
				itemgems.append(''.join(sorted(gems)))
	return itemgems



items = open("C:\\items\\items.json", "r", encoding="utf-8")
linkdata=open("C:\\items\\linkdata.txt", "w+", encoding="utf-8")
socketgroups=['','','','','','']
items_json=json.load(items)
socketgroups_data=[]
#print(items_json[0]["character"]["name"])
gems=""
for rank, character in enumerate(items_json):
	#print(f"Rank {rank}: {character['character']['name']}")
	for item in character['items']:
		if ('sockets' in item):
			for socket in item['sockets']:
				if(socket['sColour'] != 'A'):
					socketgroups[socket['group']]+=socket['sColour']
		if ('socketedItems' in item):
			for gem in item['socketedItems']:
				if(gem['colour']=='S'):	
					gems+='R'
				elif(gem['colour']=='D'):	
					gems+='G'
				elif(gem['colour']=='I'):	
					gems+='B'
				elif(gem['colour']=='W'):	
					gems+='W'
		if((gems) and socketgroups):
			#print (f"Allocating {gems} into {socketgroups}")
			#print(allocate_gems(socketgroups, gems))
			for linkset in allocate_gems(socketgroups, gems):
				if(len(linkset) >= 4):
					actual_sorted_link_groups.append(linkset)
			
		gems=''
		socketgroups=['','','','','','']
#socketgroups_data=sorted(socketgroups_data)

for datapoint in actual_sorted_link_groups:
	linkdata.write(datapoint)
	linkdata.write("\n")



