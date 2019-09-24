import json

with open("C:\\grabbed.json", "r") as data_file:
	character_items = json.load(data_file)

print (character_items["items"][0])