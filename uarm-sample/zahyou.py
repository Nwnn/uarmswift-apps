from swift import swift

####################################################
#  アームの座標（先端の位置）を取得するプログラム  #
####################################################

# アームのロックを解除（手で動かせるようにする）
swift.set_servo_detach()

position = []
switch = False

def onReportPosition(pos):
    global position
    position = pos
    pass

# アームの座標を取得して表示
swift.register_report_position_callback(lambda position: onReportPosition(position))
swift.set_report_position(interval = 0.01)


while True:
    print(swift.get_limit_switch())
    print(position)
    pass

