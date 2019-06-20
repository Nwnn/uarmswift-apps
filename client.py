from uarm.wrapper import SwiftAPI
from bottle import route, run, get, post, request
import json

swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})
swift.waiting_ready()
print(swift.get_device_info())

swift.reset(wait=True, speed=10000)
swift.set_servo_detach()
swift.set_servo_attach()
# swift.flush_cmd(wait_stop=True)

@post('/')
def do_request():
    print(request.json)
    posX = request.json['x']
    posY = request.json['y']
    posZ = request.json['z']

    swift.set_position(x=posX, y=posY, z=posZ, speed=10000)
    # swift.flush_cmd(wait_stop=True)
    return "do"

run(host='0.0.0.0', port=80)

# swift.set_servo_detach()

# swift.register_report_position_callback(lambda position: print(position))
# swift.set_report_position(interval = 0.01)
# input()
# swift.disconnect()

