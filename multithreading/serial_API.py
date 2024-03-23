import serial
ser = None
def serial_init():
  global ser
  if not ser:
    ser = serial.Serial(
      port = '/dev/ttyTHS1',
      baudrate = 115200,
      timeout = .1,
    )
  return ser
def serial_close():
  global ser
  ser.close()
