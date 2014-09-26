#!/usr/bin/env python

from flask import Flask
from flask import render_template
from flask import request

import xmlrpclib

com = xmlrpclib.ServerProxy('http://localhost:8000')

app = Flask(__name__)



@app.route('/')
def hello(name=None):
      return render_template('index.html', name=name)


@app.route('/leds.cgi', methods=['POST', 'GET'])
def led():
    searchword = request.args.get('led', '')
    

    led = int(searchword) -1
    if(com.led_read(led)):
        com.led_write(led, 0)
    else:
        com.led_write(led, 1)     
    return ""

@app.route('/up.cgi', methods=['POST', 'GET'])
def up():
    com.data_write(0x51, 1)
    com.data_write(0x50, 1)  
    return ""

@app.route('/down.cgi', methods=['POST', 'GET'])
def down():
    com.data_write(0x51, 2)
    com.data_write(0x50, 1)  
    return ""

@app.route('/right.cgi', methods=['POST', 'GET'])
def right():
    com.data_write(0x51, 3)
    com.data_write(0x50, 1)  
    return ""
    
@app.route('/left.cgi', methods=['POST', 'GET'])
def left():
    com.data_write(0x51, 4)
    com.data_write(0x50, 1)  
    return ""
    
@app.route('/stop.cgi', methods=['POST', 'GET'])
def stop():
    com.data_write(0x51, 0)
    com.data_write(0x50, 1)  
    return ""
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)

