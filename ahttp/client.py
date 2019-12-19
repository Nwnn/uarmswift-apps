from swift import swift
import socket
import json.decoder
import sys
import time

decoder = json.decoder.JSONDecoder()

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('192.168.2.4', 80))
        # s.connect(('localhost', 80))
        s.send(b'hello')

        data = s.recv(1024)
        
        posStr = data.decode('utf-8').split('\n')[4]
        req = decoder.decode(posStr)

        swift.set_position(x=req['pos'][0], y=req['pos'][1], z=req['pos'][2], speed=1000)
        swift.set_wrist(angle=req['pos'][3])
        swift.set_pump(on=req['pump'])
        swift.flush_cmd()

        s.close()