
import time
import json
from time import gmtime, strftime
import datetime as dt

import sqlite3 as lite
import sys

import udooIotLib as udooiot

USERNAME = "pwc_iot_testbed"
PASSWORD = "123qweASD"


if __name__ == '__main__':
	[token, companies] = udooiot.login(USERNAME,PASSWORD)

    ## get the company
	company = udooiot.getCompany(companies)

    ## get the gateway list
	gateways, gw_aliases, nd_aliases = udooiot.getGatewaysByCompany(token, company['company_id'])

	data = udooiot.getSensorsAndGatewaysList(gateways)

#	for x in res:
#		print (x['gateway'] + '   ' + str(x['temperature']) + '   ' + str(x['pressure']) + '   ' + str(x['light']) + '   ' + str(x['presence']) + '  ' + str(x['mq135']))

	startTime = str(strftime("%Y%m%d%H%M%S", gmtime()))
	
	if len(sys.argv) == 2:
		con = lite.connect('db_' + str(sys.argv[1]) + '.db')
	else:
		con = lite.connect('db_' + startTime + '.db')
	
	with con:
		cur = con.cursor()    
		cur.execute("CREATE TABLE IF NOT EXISTS environmentalData( gateway VARCHAR(50), time timestamp, temperature float, pressure float, light int, presence int, mq135 int )")
		for x in data:
			cur.execute("INSERT INTO environmentalData VALUES(?,?,?,?,?,?,?)", (x['gateway'], dt.datetime.now(), x['temperature'], x['pressure'], x['light'], x['presence'], x['mq135'] ) )
		cur.execute("SELECT * FROM environmentalData")

		rows = cur.fetchall()
 
		for row in rows:
			print(row)
