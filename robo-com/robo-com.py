#!/usr/bin/env python2

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from wiringpi2 import *
import serial
import array

#-------------------------------------------------------------------------------
# SERIEL SETUP
#-------------------------------------------------------------------------------

com = serial.Serial("/dev/ttyAMA0")

#-------------------------------------------------------------------------------
# WIRING PI SETUP
#-------------------------------------------------------------------------------
wiringPiSetupGpio()

OUTPUT = 1
INPUT = 0
HIGH = 1
LOW = 0

#-------------------------------------------------------------------------------
# XML RPC SETUP
#-------------------------------------------------------------------------------
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
server = SimpleXMLRPCServer(("localhost", 8000),
                            requestHandler=RequestHandler)

                          
#-------------------------------------------------------------------------------
# HARDWARW SETUP
#-------------------------------------------------------------------------------                            

LED = [0, 1, 2, 3]

for led in LED:
    digitalWrite(led, HIGH)
    pinMode(led, HIGH)


#-------------------------------------------------------------------------------
# HARDWARE FUNCTION
#-------------------------------------------------------------------------------

def led_write(led, value):
    digitalWrite(LED[led], value);
    return 0

def led_read(led):
    return digitalRead(LED[led]);

server.register_function(led_write, 'led_write')
server.register_function(led_read, 'led_read')

#-------------------------------------------------------------------------------
# PIC32 COMMUNICATION
#-------------------------------------------------------------------------------

def data_read(addr):
    com.write("!R")
    com.write(str(unichr(addr)))
    com.write(str(unichr(0)))
    com.flush()
    read = com.read(4)
    return ord(read[3])

def data_write(addr, value):
    com.write("!W")
    com.write(str(unichr(addr)))
    com.write(str(unichr(value)))
    com.flush()
    return 0
        
server.register_function(data_read, 'data_read')   
server.register_function(data_write, 'data_write')    

#-------------------------------------------------------------------------------
# EXAMPLE
#-------------------------------------------------------------------------------

# Register pow() function; this will use the value of
# pow.__name__ as the name, which is just 'pow'.
server.register_function(pow)

# Register a function under a different name
def adder_function(x,y):
    return x + y
server.register_function(adder_function, 'add')

# Register an instance; all the methods of the instance are
# published as XML-RPC methods (in this case, just 'div').
class MyFuncs:
    def div(self, x, y):
        return x // y

server.register_instance(MyFuncs())


#-------------------------------------------------------------------------------
# LED BLINK
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
# Run the server's main loop
#-------------------------------------------------------------------------------
server.serve_forever()

