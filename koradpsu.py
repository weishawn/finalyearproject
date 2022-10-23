import serial
import time

ser = serial.Serial()
#ser.port = "/dev/ttyUSB0"
# ser.port = "/dev/ttyS0"
ser.port = 'COM3'
ser.baudrate = 9600
ser.bytesize = serial.EIGHTBITS #number of bits per bytes
ser.parity = serial.PARITY_NONE #set parity check: no parity
ser.stopbits = serial.STOPBITS_ONE #number of stop bits
ser.timeout = 1            #non-block read

ser.open()

def Write(x):
    ser.write(bytes(x, 'utf-8'))
#ser.write("LOCK1OUT0VSET1:31.00ISET1:3.480VSET2:31.00ISET2:5.100")

while True:
    # write("VSET1:23.00ISET1:2.700VSET2:5.00ISET2:1.900")
    # print("mode 1")
    # write("VSET1:22.00")
    # write("ISET1:2.600")
    # time.sleep(0.1)
    # write("OUT1")
    # time.sleep(2)
    # write("*DIN?")
    # time.sleep(0.1)
	# print(ser.read(17))
    # print('mode 2')
    # write("VSET2:10.00")
    # write("ISET2:1.930")
    # time.sleep(0.1)
    # write("OUT2")
    # time.sleep(5)
    # write("*DIN?")
	Write("VSET1:25.00")
	time.sleep(2)
	Write("ISET1:2.050")
	time.sleep(0.1)
	Write("OUT1")
	time.sleep(2)
	Write("*DIN?")
	time.sleep(0.1)



