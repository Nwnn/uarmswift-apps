from uarm.wrapper import SwiftAPI

print("アームロボットと接続を開始...")

swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})
swift.waiting_ready(timeout=3)

swift.set_speed_factor(100)

swift.set_mode(0)

print("アームロボットと接続完了 \n")