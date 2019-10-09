#query processor function that will handle web-form request and spit out a simplified table of builds that use the defined criteria
#this needs to be fairly minimalistic in order to not flood the screen with irrelevant info


#I CAN'T REMEMBER THE ALPHABET
#B < G < R < W

import mysql.connector as sql

# SQL connection 
rds_host='pypoe.cgqezikpygym.eu-west-2.rds.amazonaws.com'
with open('creds.txt', 'r') as creds:
	pwd=(creds.read()).strip()
sql_connection=sql.connect(host=rds_host, user='admin', password=pwd, database='pytest')
cursor=sql_connection.cursor(buffered=True)
cursor.execute("SET NAMES 'utf8mb4';")
#very_nice_credntial_handling.jpeg

#
COLOR_QUERY = """SELECT char_id, inventory_id FROM items WHERE sorted_links LIKE %s;;"""
#


def process_webform_request(colors = '', tags = ''):
	white_gems_present = ('W' in colors)
	if(colors != ''):
		cursor.execute(COLOR_QUERY, (colors.replace('W', '%'),))
	tmp_list=cursor.fetchall()
	print(tmp_list)

		

