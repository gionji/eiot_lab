
import time
import json
from time import gmtime, strftime
import datetime as dt

import sqlite3 as lite
import sys

import udooIotLib as udooiot

USERNAME = "pwc_iot_testbed"
PASSWORD = "123qweASD"

REQUEST_INTERVAL = 10


if __name__ == '__main__':
	[token, companies] = udooiot.login(USERNAME,PASSWORD)

    ## get the company
	company = udooiot.getCompany(companies)

    ## get the network status
	gateways, gw_aliases, nd_aliases = udooiot.getGatewaysByCompany(token, company['company_id'])


	startTime = str(strftime("%Y%m%d%H%M%S", gmtime()))
	
	if len(sys.argv) == 2:
		con = lite.connect('db_' + str(sys.argv[1]) + '.db')
	else:
		con = lite.connect('db_' + startTime + '.db')
	
	# parse the network to a gateways list and related sensors value in a dictionary with following keys:
	# gateway temperature, pressure, light, presence, mq135
	data = udooiot.getSensorsAndGatewaysList(gateways)
	
	with con:
		cur = con.cursor()    
		cur.execute("CREATE TABLE IF NOT EXISTS environmentalData( gateway VARCHAR(50), time timestamp, temperature float, pressure float, light int, presence int, mq135 int )")
		for x in data:
			cur.execute("INSERT INTO environmentalData VALUES(?,?,?,?,?,?,?)", (x['gateway'], dt.datetime.now(), x['temperature'], x['pressure'], x['light'], x['presence'], x['mq135'] ) )
			con.commit()
		try:
			while(1):
				try:
					gateways, gw_aliases, nd_aliases = udooiot.getGatewaysByCompany(token, company['company_id'])
					data = udooiot.getSensorsAndGatewaysList(gateways)
					print(str( dt.datetime.now() ) + '  :::  sensors data acquired (' + str( len(data) ) + ' gateways)' )
					for x in data:
						cur.execute("INSERT INTO environmentalData VALUES(?,?,?,?,?,?,?)", (x['gateway'], dt.datetime.now(), x['temperature'], x['pressure'], x['light'], x['presence'], x['mq135'] ) )
						con.commit()
					time.sleep( REQUEST_INTERVAL )
				except Exception as e:
					con.commit()
					print e			
		except KeyboardInterrupt :
			cur.execute("SELECT * FROM environmentalData")
			rows = cur.fetchall()
			print('\nNumber of raws: ' + str(len(rows)) )
			con.commit()
			con.close()
				
			
