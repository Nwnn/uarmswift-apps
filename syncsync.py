from uarm.wrapper import SwiftAPI
import random;

swift1 = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})
swift2 = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})


swift1.waiting_ready()
device_info = swift1.get_device_info()
print(swift1.port, device_info)
firmware_version = device_info['firmware_version']
if firmware_version and not firmware_version.startswith(('0.', '1.', '2.', '3.')):
    swift1.set_speed_factor(0.00001)

swift2.waiting_ready()
device_info = swift2.get_device_info()
print(swift2.port, device_info)
firmware_version = device_info['firmware_version']
if firmware_version and not firmware_version.startswith(('0.', '1.', '2.', '3.')):
    swift2.set_speed_factor(0.00001)


X = 0
Y = 1
Z = 2
R = 3

swift1.set_servo_detach()

swift1.register_report_position_callback(lambda position: swift2.set_position(x=position[X], y=position[Y], z=position[Z], speed=100000000, timeout=1))
# swift1.register_report_position_callback(lambda position: swift2.set_position(x=position[X] + random.random() * 5, y=position[Y] + random.random() * 5 , z=position[Z], speed=100000000, timeout=1))


swift1.set_report_position(interval = 0.001)
input()

swift1.disconnect()

