import json 
import pymysql
import os 
import re
#I CAN'T REMEMBER THE ALPHABET
#B < G < R < W


rds_host=os.environ['rds_host'] 
pwd=os.environ['rds_creds'] 
sql_connection=pymysql.connect(host=rds_host, user='admin', password=pwd, database='pytest') 
cursor=sql_connection.cursor()
cursor.execute("SET NAMES 'utf8mb4';") 


COLOR_AND_TAGS_QUERY="""SELECT DISTINCT account_name, character_name, items.char_id, items.inventory_id from items join gems on (items.char_id=gems.char_id AND items.sorted_links LIKE %s and items.inventory_id=gems.socketed_in and gems.support=0 and gems.tags LIKE %s) JOIN characters ON (characters.char_id=items.char_id)"""
GET_CHAR_QUERY="""SELECT char"""

def process_webform_request(colors = '%', tags = '%'):
	poeninjaurl="https://poe.ninja/challenge/builds/char/"
	colors=colors.replace('W', '_')
	if(tags!='%'):
		tags="%"+("%".join(sorted((tags.replace(",", " ").split()))))+"%"
		print(tags)
	
	tmp_list=[]
	cursor.execute(COLOR_AND_TAGS_QUERY, (colors, tags,))
	tmp_list=[list(item) for item in (cursor.fetchall())]
	for i in range(len(tmp_list)):
		tmp_list[i].append(f"<a href=\"{poeninjaurl}{tmp_list[i][0]}/{tmp_list[i][1]}\">{poeninjaurl}{tmp_list[i][0]}/{tmp_list[i][1]}</a>")
	return tmp_list

def lambda_handler(event, context):
# TODO implements
	try:
		r=int(event['queryStringParameters']['rcolours'])
		g=int(event['queryStringParameters']['gcolours'])
		b=int(event['queryStringParameters']['bcolours'])
		w=int(event['queryStringParameters']['wcolours'])
	except ValueError:
		return {
			'statusCode': 400,
			"headers": {
				"Access-Control-Allow-Origin": "*",
			},
			'body': json.dumps("Incorrect Input (R,G,B,W should be integer numbers)")
		}
	if(r+g+b+w>6):
		return {
			'statusCode': 400,
			"headers": {
				"Access-Control-Allow-Origin": "*",
			},
			'body': json.dumps("Incorrect Input (R+G+B+W needs to be below 6)")
		}
	tags=event['queryStringParameters']['tags']
	
	if((re.search("[^a-zA-Z,]", tags))):
		return {
			'statusCode': 400,
			"headers": {
				"Access-Control-Allow-Origin": "*",
			},
			'body': json.dumps("Incorrect tags format: Should follow Tag1,Tag2,Tag3,Tag4. Maximum number of tags is 4. Here is a list of supported tags: Warcry,Spell,Cast,Attack,Aura,Herald,Curse,Minion,Golem,Totem,Trap,Mine,Fire,Cold,Lightning,Chaos,AoE,Projectile,Melee,Bow,Chaining,Channelling,Duration,Movement,Trigger,Vaal")
		}
	colours="B"*b + "G"*g + "R"*r + "W"*w
	if(tags):
		result=process_webform_request(colours, tags)
	else:
		result=process_webform_request(colours)
	return {
		'statusCode': 200,
		"headers": {
            "Access-Control-Allow-Origin": "*",
        },
		'body': json.dumps(result, ensure_ascii=False)		
	}
	