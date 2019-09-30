from swift import swift
import socket
import json.decoder
import sys
import time

jsondecoder = json.decoder.JSONDecoder()

swift.reset()

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

    s.bind(('', 9000))

    while True:
        try:
            msg, address = s.recvfrom(1024)
            # print(str(msg))
            req = jsondecoder.decode(msg.decode("utf-8"))
            swift.set_position(x=req['pos'][0], y=req['pos'][1], z=req['pos'][2], speed=1000)
            swift.set_wrist(angle=req['pos'][3])
            swift.set_pump(on=req['pump'])
            swift.flush_cmd()

        except Exception as e:
            print(e)
            pass



