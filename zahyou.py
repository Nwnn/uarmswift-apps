from uarm.wrapper import SwiftAPI
# from bottle import route, run, get, post, request
import json

swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})
swift.waiting_ready()
print(swift.get_device_info())

swift.set_servo_detach()

swift.register_report_position_callback(lambda position: print(position))
swift.set_report_position(interval = 0.01)
input()
swift.disconnect()

