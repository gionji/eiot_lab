import requests
import json
from time import gmtime, strftime
import time

## Alternatives URL
#iot_url = "https://cmu.udoo.cloud"
#iot_url = "https://udoo-iot-beta.cleverapps.io/"


BASE_URL    = "https://udoo.cloud"
API_URL     = "/ext"
API_VERSION = "/v1"
IOT_URL = BASE_URL + API_URL + API_VERSION

USERNAME = "pwc_iot_testbed"
PASSWORD = "123qweASD"

def login(username, password):
    url = BASE_URL + '/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': USERNAME, 'password': PASSWORD}
    #print(payload)

    result = requests.post(url, headers=headers, data=payload)
    try:
        data = json.loads(result.text)
        # print(data)
        if data['status']:
            return [data['token'], data['companies']]
        else:
            exit()
    except ValueError as e:
        print(e)
        print(result)

def composeHeader(token):
    header = {'Authorization': 'JWT ' + token}
    return header

def getCompany(companies):
    if len(companies) > 1:
        print('COMPANIES FOUND:')
        for i, company in enumerate(companies):
            if company[2]:
                print(str(i) + ' - ' + company[0] + '(default)')
            else:
                print(str(i) + ' - ' + company[0])

        companyId = input('Select Company:')
        company = companies[companyId]
    else:
        company = companies[0]
        print('Company selected automatically: ' + company['displayName'])

    return company


def getGatewaysByCompany(token, companyId):
    url = IOT_URL + '/network/' + companyId
    # print(url)
    # print(composeHeader(token))
    result = requests.get(url, headers=composeHeader(token))
    network = json.loads(result.text)
    if 'gateways' not in network:
        network['gateways'] = []
    if 'gateway_aliases' not in network:
        network['gateway_aliases'] = []
    if 'node_aliases' not in network:
        network['node_aliases'] = []

    return network['gateways'], network['gateway_aliases'], network['node_aliases']


def getSensorValue(token, gateway, device, sensor_type, sensor_id):
    url = IOT_URL + '/sensors/read/' + gateway + '/' + device + '/' + sensor_type + '/' + sensor_id

    print(url)
    # print(composeHeader(token))
    result = requests.get(url, headers=composeHeader(token))
    try:
        data = json.loads(result.text)
        return data
    except ValueError as e:
        print(e)


def getSensorHistory(token, gateway, device, sensor_type, sensor_id, history_type, limit):
    url = IOT_URL + '/sensors/history/' + history_type + '/' + gateway + '/' + device + '/' + sensor_type + '/' + sensor_id + '/' + str(limit)

    print(url)
    # print(composeHeader(token))
    result = requests.get(url, headers=composeHeader(token))
    try:
        data = json.loads(result.text)
        return data
    except ValueError as e:
        print(e)


def sendActuatorWrite(token, gateway, device, actuator_type, actuator_id, value):
    url = IOT_URL + '/sensors/write/' + gateway + '/' + device + '/' + actuator_type + '/' + actuator_id + '/' + value

    print(url)
    # print(composeHeader(token))
    result = requests.get(url, headers=composeHeader(token))
    try:
        data = json.loads(result.text)
        return data
    except ValueError as e:
        print(e)


### GET METHODS ################3

def getTemperatures(gateways):
    csvLine = str(strftime("%Y%m%d%H%M%S", gmtime()))

    print ("\nTemperature sensors readed at "+ str(csvLine))
    for g in gateways:
        for d in g['nodes']:  # get devices
            for s in d['sensors']:  # get sensors
                if s['sensor_id'] == '1-0060':
                    if g['connected']:
                        csvLine = csvLine + "," + str(s['last_read']['value'][1])
                    else:
                        csvLine = csvLine + "," + str(-100)
    return csvLine


def getPressures(gateways):
    csvLine = str(strftime("%Y%m%d%H%M%S", gmtime()))

    print str("\nPressure sensors  readed at "+ str(csvLine))
    for g in gateways:
        for d in g['nodes']:  # get devices
            for s in d['sensors']:  # get sensors
                if s['sensor_id'] == '1-0060':
                    if g['connected']:
                        csvLine = csvLine + "," + str(s['last_read']['value'][0])
                    else:
                        csvLine = csvLine + "," + str(-100)
    return csvLine

def getLights(gateways):
    csvLine = str(strftime("%Y%m%d%H%M%S", gmtime()))
    print str("\nLight sensors readed at "+ str(csvLine))
    for g in gateways:
        for d in g['nodes']: # get devices
            for s in d['sensors']: # get sensors
                if s['sensor_id'] == '1-0029':
                    if g['connected']:
                        csvLine = csvLine + "," + str(s['last_read']['value'][0])
                    else:
                        csvLine = csvLine + "," + str(-100)
    return csvLine


def getPirPresences(gateways):
    csvLine = str(strftime("%Y%m%d%H%M%S", gmtime()))
    print str("\nPresence sensors readed at "+ str(csvLine))
    for g in gateways:
        for d in g['nodes']:  # get devices
            for s in d['sensors']:  # get sensors
                if d['product_type'] == 'arduino' and s['display_name'] == 'PresencePIR':
                    if g['connected']:
                        csvLine = csvLine + "," + str(s['last_read']['value'][0])
                    else:
                        csvLine = csvLine + "," + str(-100)
    return csvLine


def getAirQualitiesMQ135(gateways):
    csvLine = str(strftime("%Y%m%d%H%M%S", gmtime()))
    print str("\nAir quality readed at "+ str(csvLine))
    for g in gateways:
        for d in g['nodes']:  # get devices
            for s in d['sensors']:  # get sensors
                if d['product_type'] == 'arduino' and s['display_name'] == 'AirQuality_MQ135':
                    if g['connected']:
                        csvLine = csvLine + "," + str(s['last_read']['value'][0])
                    else:
                        csvLine = csvLine + "," + str(-100)
    return csvLine


### GET CSV HEADER METHODS ################3

def getTemperaturesCsvHeader(gateways):
    csvLine = ""
    for g in gateways:
        for d in g['nodes']:  # get devices
            for s in d['sensors']:  # get sensors
                if s['sensor_id'] == '1-0060':
                    csvLine = csvLine + "," + str(g['displayName'])

    return csvLine


def getPressuresCsvHeader(gateways):
    csvLine = ""
    for g in gateways:
        for d in g['nodes']:  # get devices
            for s in d['sensors']:  # get sensors
                if s['sensor_id'] == '1-0060':
                    csvLine = csvLine + "," + str(g['displayName'])
    return csvLine

def getLightsCsvHeader(gateways):
    csvLine = ""
    for g in gateways:
        for d in g['nodes']: # get devices
            for s in d['sensors']: # get sensors
                if s['sensor_id'] == '1-0029':
                    csvLine = csvLine + "," + str(g['displayName'])
    return csvLine


def getPirPresencesCsvHeader(gateways):
    csvLine = ""
    for g in gateways:
        for d in g['nodes']:  # get devices
            for s in d['sensors']:  # get sensors
                if d['product_type'] == 'arduino' and s['display_name'] == 'PresencePIR':
                    csvLine = csvLine + "," + str(g['displayName'])
    return csvLine


def getAirQualitiesMQ135CsvHeader(gateways):
    csvLine = ""
    for g in gateways:
        for d in g['nodes']:  # get devices
            for s in d['sensors']:  # get sensors
                if d['product_type'] == 'arduino' and s['display_name'] == 'AirQuality_MQ135':
                    csvLine = csvLine + "," + str(g['displayName'])
    return csvLine






def getDisconnectedGateways(gateways):
    csvLine = str(strftime("%Y%m%d%H%M%S", gmtime()))
    print str("\nDisconnetted boards checked at "+ str(csvLine))
    for g in gateways:
        if not g['connected']:
            csvLine = csvLine + "," + str(0)
        else:
            csvLine = csvLine + "," + str(1)
    return csvLine


def getGatewaysNamesAndId(gateways):
    csvLine = ""
    for g in gateways:
        csvLine = csvLine + "," + str(str(g['displayName']))
    csvLine = csvLine + "\n"
    for g in gateways:
        csvLine = csvLine + "," + str(str(g['gateway_id']))
    return csvLine



### PRINT METHODS ################3

def printTemperatures(gateways):
    print ("\nTemperature sensors")
    for g in gateways:
        for d in g['nodes']:  # get devices
            for s in d['sensors']:  # get sensors
                if s['sensor_id'] == '1-0060':
                    if g['connected']:
                        print "\t" + str(g['displayName']) + "  " + str(
                            s['last_read']['value'][1]) + " C at " + str(
                            s['last_read']['last_update'])
                    else:
                        print "\t" + str(g['displayName']) + " disconnected"

def printPressures(gateways):
    print ("\nPressure sensors")
    for g in gateways:
        for d in g['nodes']:  # get devices
            for s in d['sensors']:  # get sensors
                if s['sensor_id'] == '1-0060' and s['enabled']:
                    if g['connected'] :
                        print "\t" + str(g['displayName']) + "  " + str(
                            s['last_read']['value'][0]) + " kPa at " + str(
                            s['last_read']['last_update'])
                    else:
                        print "\t" + str(g['displayName']) + " disconnected"

def printLights(gateways):
    print ("\nLight sensors")
    for g in gateways:
        for d in g['nodes']: # get devices
            for s in d['sensors']: # get sensors
                if s['sensor_id'] == '1-0029' and s['enabled']:
                    if g['connected']:
                        print "\t" + str(g['displayName']) + "  " + str(s['last_read']['value'][0]) + " lumen at " + str(s['last_read']['last_update'])
                    else:
                        print "\t" + str(g['displayName']) + " disconnected"


def printPirPresences(gateways):
    print ("\nPresence sensors")
    for g in gateways:
        for d in g['nodes']:  # get devices
            for s in d['sensors']:  # get sensors
                if d['product_type'] == 'arduino' and s['display_name'] == 'PresencePIR':
                    if g['connected']:
                        print "\t" + str(g['displayName']) + "  " + str(
                            s['last_read']['value'][0]) + " at " + str(
                            s['last_read']['last_update'])
                    else:
                        print "\t" + str(g['displayName']) + " disconnected"

def printAirQualitiesMQ135(gateways):
    print ("\nAir quality sensors")
    for g in gateways:
        for d in g['nodes']:  # get devices
            for s in d['sensors']:  # get sensors
                if d['product_type'] == 'arduino' and s['display_name'] == 'AirQuality_MQ135':
                    if g['connected']:
                        print "\t" + str(g['displayName']) + "  " + str(
                            s['last_read']['value'][0]) + " at " + str(
                            s['last_read']['last_update'])
                    else:
                        print "\t" + str(g['displayName']) + " disconnected"

def printDisconnectedGateways(gateways):
    print "\nDisconnetted boards:"
    for g in gateways:
        if not g['connected']:
            print "\t" + str(g['displayName'])


def printLastRfidTag(gateways):
    print ("\nRFID")
    for g in gateways:
        for d in g['nodes']:  # get devices
            for s in d['sensors']:  # get sensors
                if s['sensor_id'] == 'usbRFID':
                    if g['connected']:
                        print "\t" + str(g['displayName']) + "  " + str(
                            s['last_read']['value'][0]) + " at " + str(
                            s['last_read']['last_update'])
                    else:
                        print "\t" + str(g['displayName']) + " disconnected"



def printZwaveNodes(gateways, gatewayName):
    print ("\nConnected Zwave devices to a gateway:")
    for g in gateways:
        if g['displayName'] == str(gatewayName):
            for n in g['nodes']:
                if "ozw" in n['id']:
                    print(n['id'] + " : " + n['display_name'] + ' - ' + n['_id'])



def printZwaveNodeType(gateways, gatewayName, nodeType):
    print ("\nConnected Sensors to a gateway:")
    for g in gateways:
        if g['displayName'] == str(gatewayName):
            for n in g['nodes']:
                if n['product_type'] == nodeType:
                    print(n['id'] + " : " + n['display_name'] + '    - NodeID: ' + n['_id'])

def printZwaveNodeSensorAvailable(gateways, gatewayName, nodeType):
    print ("\nConnected Sensors to a gateway:")
    for g in gateways:
        if g['displayName'] == str(gatewayName):
            for n in g['nodes']:
                if n['product_type'] == nodeType:
                    for s in n['sensors']:
                        print( s['product_name'] + ' (' + str(s['value_type'][0]['unit']) + ')')
                    break



def printZwaveNodeType(gateways, gatewayName, nodeType):
    print ("\nConnected Sensors to a gateway:")
    for g in gateways:
        if g['displayName'] == str(gatewayName):
            for n in g['nodes']:
                if n['product_type'] == nodeType:
                    print('')
                    for s in n['sensors']:
                        print(s['node'] + " --> " + s['product_name'] + ': ' + str(s['last_read']['value'][0]) + ' ' + str(s['value_type'][0]['unit']) )

def printZwaveSensorData(gateways, gatewayName, nodeType, sensorType):
    print ("\n" + sensorType + " sensors data:")
    for g in gateways:
        if g['displayName'] == str(gatewayName):
            for n in g['nodes']:
                if n['product_type'] == nodeType:
                    for s in n['sensors']:
                        if s['product_name'] == sensorType:
                            print(s['node'] + " --> " + s['product_name'] + ': ' + str(s['last_read']['value'][0]) + ' ' + str(s['value_type'][0]['unit']) )

def getZwaveSensorData(gateways, gatewayName, nodeType, sensorType):
    ans = getDateStamp()
    for g in gateways:
        if g['displayName'] == str(gatewayName):
            for n in g['nodes']:
                if n['product_type'] == nodeType:
                    for s in n['sensors']:
                        if s['product_name'] == sensorType:
                            ans = ans + ',' + str(s['last_read']['value'][0])
    return ans


def getGatewayIdByName(gateways, gatewayName):
    for g in gateways:
        if g['displayName'] == str(gatewayName):
            return g['gateway_id']


def getZwaveNodeSensorAvailable(gateways, gatewayName, nodeType):
    ans = ""
    for g in gateways:
        if g['displayName'] == str(gatewayName):
            for n in g['nodes']:
                if n['product_type'] == nodeType:
                    for s in n['sensors']:
                        ans = ans + ',' + str( s['product_name'] )
                    break
    return ans




def getZwaveSensorDataByGateway(gateways, gatewayName, nodeType):
    ans = getDateStamp()
    for g in gateways:
        if g['displayName'] == str(gatewayName):
            for n in g['nodes']:
                if n['product_type'] == nodeType:
                    ans = ans + n['id']
                    for s in n['sensors']:
                        ans = ans + "," +str(s['last_read']['value'][0])
                    ans = ans + '\n'
    return ans




def getSensorsAndGatewaysList(gateways):
    _gateways = list()

    #iterate the gateways
    for g in gateways:
        _sensors = {'gateway': '', 'temperature': -100, 'pressure': -100, 'light': -100, 'presence': -100, 'mq135': -100}
        for n in g['nodes']:
            _sensors['gateway'] = str(g['displayName'])
            for s in n['sensors']:  # get sensors
                # check the temp and baro
                if s['sensor_id'] == '1-0060' and s['enabled']:
                    try:
                        _sensors['temperature'] = s['last_read']['value'][1]
                        _sensors['pressure']    = s['last_read']['value'][0]
                    except:
                        _sensors['temperature'] = -102
                        _sensors['pressure']    = -102
                # check the light# get sensors
                if s['sensor_id'] == '1-0029' and s['enabled']:
                    try:
                        _sensors['light']       = s['last_read']['value'][0]
                    except:
                        _sensors['light']       = -101
                # check the presence
                if n['product_type'] == 'arduino' and s['display_name'] == 'PIR':
                    try :
                        _sensors['presence'] = s['last_read']['value'][0]
                    except:
                        _sensors['presence']    = -101
                # check the mq135
                if n['product_type'] == 'arduino' and s['display_name'] == 'MQ135_AIRQUALITY':
                    try :
                        _sensors['mq135']       = s['last_read']['value'][0]
                    except:
                        _sensors['mq135']       = -101

        _gateways.append(_sensors)

    return _gateways

def printSensorAndActuatorCount(gateways):
    i = 0
    j = 0
    for g in gateways:
         for d in g['nodes']: # get devices
             for s in d['sensors']: # get sensors
                 if s['enabled']:
                     i = i+1
             for a in d['actuators']:
                 j = j+1

    print "Sensors connected   : " + str(i)
    print "Actuators connected : " + str(j)


def getDateStamp():
    return str(strftime("%Y%m%d%H%M%S", gmtime()))


def getDateFromIotTimestamp(timestamp):
    YYYY = timestamp[:4]
    MM   = timestamp[4:6]
    DD   = timestamp[6:8]
    hh   = str((int(timestamp[8:10])+24-5) % 24)
    mm   = timestamp[-2:]

    return str(YYYY + "/" + MM + "/" + DD + " - " + hh + ":" + mm)
