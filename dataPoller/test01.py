import json
import time
from time import gmtime, strftime

import udooIotLib as udooiot

USERNAME = "pwc_iot_testbed"
PASSWORD = "123qweASD"


if __name__ == '__main__':
    [token, companies] = udooiot.login(USERNAME,PASSWORD)

    ## get the company
    company = udooiot.getCompany(companies)

    ## get the gateway list
    gateways, gw_aliases, nd_aliases = udooiot.getGatewaysByCompany(token, company['company_id'])

    ## print the network structure
    #print(json.dumps(gateways, indent=4, sort_keys=True))

    startTime = str(strftime("%Y%m%d%H%M%S", gmtime()))

    tempFile = open("./csv_out/"+startTime+"temperature.csv","a+")
    humiFile = open("./csv_out/" + startTime + "humidity.csv", "a+")
    lighFile = open("./csv_out/"+startTime+"light.csv","a+")
    pirFile =  open("./csv_out/"+startTime+"pirPresence.csv","a+")

    for i in range(0, 1440):
        #la prima riga con gli id dei gateway
        gateways, gatewayAliases, nodeAliases = udooiot.getGatewaysByCompany(token, company['company_id'])

        tempFile.write( udooiot.getZwaveSensorData(gateways, 'udooneo-Zwave', 'multisensor6', 'Temperature')       + '\n' )
        humiFile.write( udooiot.getZwaveSensorData(gateways, 'udooneo-Zwave', 'multisensor6', 'Relative Humidity') + '\n' )
        lighFile.write( udooiot.getZwaveSensorData(gateways, 'udooneo-Zwave', 'multisensor6', 'Luminance')         + '\n' )
        pirFile.write(  udooiot.getZwaveSensorData(gateways, 'udooneo-Zwave', 'multisensor6', 'Sensor')            + '\n' )

        tempFile.flush()
        humiFile.flush()
        lighFile.flush()
        pirFile.flush()

        print "Iteration " + str(i) + " -------------------------------------------"
        time.sleep(0.1)