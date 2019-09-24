#FETCHER

import requests
import json
list_grabbed = []
current_league_url = "https://www.pathofexile.com/api/ladders/Blight"
offset=0
db = open("C:\\grabbed.json", "a+")
while (offset <= 14800):
	response = requests.get(current_league_url+"?limit=200&offset="+str((offset)))
	offset+=200
	list_grabbed.append(response.json())
	db.write("\n")
	#print(response.json)
	print (response.status_code)
json.dump(list_grabbed, db, indent=4)
