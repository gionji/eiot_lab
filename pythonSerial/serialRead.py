import serial, time, sys

ser = serial.Serial('/dev/ttyMCC', 9600)

try:
 while 1:
  serial_line = ser.readline()

  print(serial_line) # If using Python 2.x use: print serial_line
  
  if str(serial_line) == '0':
   print('Led 13 OFF')
  elif str(serial_line) == '1':
   print('Led 13 OFF')

  time.sleep(0.01) # sleep 
except KeyboardInterrupt:
 print 'Interrupted'
 try:
  ser.close() # Only executes once the loop exits			
  sys.exit(0)
 except SystemExit:
  ser.close() # Only executes once the loop exits
  os._exit(0)
