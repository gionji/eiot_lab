import serial, time, sys

ser = serial.Serial('/dev/ttyMCC', 9600)

try:
 while 1:
  ser.write('1')
  time.sleep(1) # sleep 
  ser.write('0')
  time.sleep(1) # sleep 
except KeyboardInterrupt:
 print 'Interrupted'
 try:
  ser.close() # Only executes once the loop exits			
  sys.exit(0)
 except SystemExit:
  ser.close() # Only executes once the loop exits
  os._exit(0)
