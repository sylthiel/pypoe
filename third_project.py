##GRABBER

import json
import requests

with open("C:\\grabbed.json", "r") as data_file:
	character_list = json.load(data_file)
list_of_acctchr=open("C:\\list_of_acctchr.txt", "w+", encoding="utf-8")
char_count=0
for i in range(len(character_list)):
	for j in range (len(character_list[i]["entries"])):
		acct_chr=("", "")
		acct_chr=(str(character_list[i]["entries"][j]["character"]["name"]), str(character_list[i]["entries"][j]["account"]["name"]))
		
		list_of_acctchr.write(acct_chr[0] + "," +  acct_chr[1] + "\n")
		char_count += 1
print (char_count, " characters written to list_of_acctchr.txt")
