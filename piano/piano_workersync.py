from uarm.wrapper import SwiftAPI
import time
import threading

def scheduler(interval, f, wait = True):
    base_time = time.time()
    next_time = 0
    while True:
        t = threading.Thread(target = f)
        t.start()
        if wait:
            t.join()
        next_time = ((base_time - time.time()) % interval) or interval
        time.sleep(next_time)


X = 0
Y = 1
Z = 2

d = {
    "A"  : 0,
    "A#" : 1, 
    "B"  : 2,
    "C"  : 3,
    "C#" : 4,
    "D"  : 5,
    "D#" : 6,
    "E"  : 7,
    "F"  : 8,
    "F#" : 9,
    "G"  : 10,
    "G#" : 11

}

d = {
    "A"  : 0, 
    "B"  : 1,
    "C"  : 2,
    "D"  : 3,
    "E"  : 4,
    "F"  : 5,
    "G"  : 6,

}

swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})
# swift2 = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})
# swift3 = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})

swift.waiting_ready()
device_info = swift.get_device_info()
print(swift.port, device_info)
firmware_version = device_info['firmware_version']
if firmware_version and not firmware_version.startswith(('0.', '1.', '2.', '3.')):
    swift.set_speed_factor(0.00001)

swift.set_servo_detach()
input('A4')
swift.set_servo_attach()
pos = swift.get_position()

print(pos);

bias = 23;

swift.reset(speed=10000000);

seqs = ["F", "G", "E", "A", "D", "G", "C", "C"]
# seqs = ["C", "C", "D", "D", "E", "E", "D", "D"]

count = 0;
def worker():
    global count
    count = count + 1
    seq = seqs[count % len(seqs)]
    print(seq);
    print(time.time())

    # move
    swift.set_position(x=pos[X], y=pos[Y] + (-d[seq] * bias), z=pos[Z] + 5, speed=10000000)

    # push
    swift.set_position(x=pos[X], y=pos[Y] + (-d[seq] * bias), z=pos[Z] - 15, speed=10000000)

    # return
    swift.set_position(x=pos[X], y=pos[Y] + (-d[seq] * bias), z=pos[Z] + 5, speed=10000000)
    swift.flush_cmd()

scheduler(1, worker, False)




# while True:
#     for seq in seqs:
#         # move
#         swift.set_position(x=pos[X], y=pos[Y] + (-d[seq] * bias), z=pos[Z] + 5, speed=10000000)
#         swift.flush_cmd()

#         # push
#         swift.set_position(x=pos[X], y=pos[Y] + (-d[seq] * bias), z=pos[Z] - 15, speed=10000000)
#         swift.flush_cmd()

#         # return
#         swift.set_position(x=pos[X], y=pos[Y] + (-d[seq] * bias), z=pos[Z] + 5, speed=10000000)
#         swift.flush_cmd()


#         pass

#     pass

