from swift import swift
import time
import math

####################################
#  アームをプログラム上から動かす  #
####################################

# 初期位置の取得と表示
swift.reset(speed=100000)
position = swift.get_position()
print(position)

# 動かす
X = 0
Y = 1
Z = 2

t = 0

while True:
    t += 0.2

    swift.set_position(
        x=math.sin(t) * 50 + position[X],
        y=math.cos(t) * 50 + position[Y],
        z=position[Z]
    )

    time.sleep(0.1)
    pass

