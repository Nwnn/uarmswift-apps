import os
import sys
import time
import pretty_midi
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from uarm.wrapper import SwiftAPI

swift1 = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})
swift2 = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})
# swift3 = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})

swift1.waiting_ready()
device_info = swift1.get_device_info()
print(swift1.port, device_info)
firmware_version = device_info['firmware_version']
if firmware_version and not firmware_version.startswith(('0.', '1.', '2.', '3.')):
    swift1.set_speed_factor(0.00001)

time.sleep(1)


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

def freq(sc, pitch):
    return 440 * pow(2, ( d[sc] + pitch * 12 )  / 12)


# midiData = pretty_midi.PrettyMIDI('')

swift1.set_buzzer(frequency=freq("C", -1), duration=0.5)