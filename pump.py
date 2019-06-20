from uarm.wrapper import SwiftAPI

print("アームと接続を開始...")

swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})
swift.waiting_ready()
print(swift.get_device_info())

print("アームと接続完了")

swift.set_pump(on=True)

