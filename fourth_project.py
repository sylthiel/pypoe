import json
import requests
import time
import datetime
list_of_acctchr=open("C:\\list_of_acctchr.txt", "r", encoding="utf-8")
current_league_url = "https://www.pathofexile.com/api/ladders/Blight"
dbg=open("C:\\dbg.log", "w+", encoding="utf-8")
dbg.write("----------------------------------------------------------")
dbg.write(f"[{datetime.datetime.now()}] script start\n")
items = open("C:\\items\\items.json", "w+", encoding="utf-8")
list_items=[]
request=0
for rank, acct_chr in enumerate(list_of_acctchr):
	acct, chr = acct_chr.split(",")
	acct, chr = acct.strip(), chr.strip()
	#print (acct.strip(), chr.strip())
	print (f"https://www.pathofexile.com/character-window/get-items?accountName={chr}&character={acct}")
	attempts=0
	while(True):
		if(attempts >= 3): 
			break
		response = requests.get(f"https://www.pathofexile.com/character-window/get-items?accountName={chr}&character={acct}")

		print(response.status_code)
		if(response.status_code==200):
			list_items.append(response.json())
			#json.dump(response.json(), items, indent=4)
			#items.write(",\n")
			break
		if(response.status_code==403):
			break
		time.sleep(30)
		attempts+=1
	request+=1
	dbg.write(f"[{datetime.datetime.now()}] Request iteration {request} for https://www.pathofexile.com/character-window/get-items?accountName={chr}&character={acct} with response code {response.status_code}\n")
	if (request >= 105):
		break
json.dump(list_items, items, indent=4)