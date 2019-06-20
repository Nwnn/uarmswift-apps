from uarm.wrapper import SwiftAPI
import time

import reversi
import random


# armPositionのエイリアス
X = 0
Y = 1
Z = 2

def measureBoardSector(swift):
    print("キャリブレーションを開始します")
    # 左上位置測定
    swift.set_servo_detach()
    input("* アームを手で直接動かし，対面から盤上の左上にアームを配置してから，Enterキーを押す \n ヒント: 全てのポジションにアームが届くことを確認してください（特に本体直下にはアームが届かない場合があります！）")

    swift.set_servo_attach()
    posA = swift.get_position()

    swift.set_servo_detach()
    input("* 次に，対面から盤上の右下にアームを配置してから，Enterキーを押す")
    swift.set_servo_attach()
    posB = swift.get_position()

    sector = [ posA, posB ]
    print("区画距離(mm)")
    print(sector)

    length = getSectorLength(sector) 
    print("セル区間距離(mm)")
    print(length)

    return(getPositions(sector, length))

            #     targetX = sector[0][X] + ((length[X] / 7) * selectX)
            # targetY = sector[0][Y] + ((length[Y] / 7) * selectY)


def getSectorLength(sector: list):
    return [abs(sector[0][X] - sector[1][X]), abs(sector[0][Y] - sector[1][Y])]

def getPositions(sector: list, length: list):
    return [[[sector[0][X] + ((length[X] / 7) * selectX) , sector[0][Y] + ((length[Y] / 7) * selectY)] for selectY in range(8)] for selectX in range(8)]
    # target[X][Y]


input("* セットアップ * \n 1: リバーシ盤を任意の位置に配置（なるべく水平が望ましい）\n 2: ロボ本体を対面に配置（高さを揃え，なるべく中央が望ましい） \n 4: ロボ本体とコンピュータをUSB経由で接続 \n 5: 準備が完了したらEnterキーを押す \n")

print("アームロボットと接続を開始...")

swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})
swift.waiting_ready(timeout=3)

device_info = swift.get_device_info()
print(device_info)
firmware_version = device_info['firmware_version']
if firmware_version and not firmware_version.startswith(('0.', '1.', '2.', '3.')):
    swift.set_speed_factor(0.0005)

swift.set_mode(0)

print("アームロボットと接続完了 \n")



# ユーザが完了と宣言するまで無限ループ
setupDisable = True
while(setupDisable):
    target = measureBoardSector(swift)


    input("\n* アーム，ロボットから手を放してください，安全が確認できたらEnterキーを押してください")

    swift.reset(speed=100000, wait=True)

    print("\n * セル移動チェック * \n 入力したポジションに移動することができます \n 数値以外を入力すると終了します \n 特に X 0, Y 3 や X 0, Y 4 に移動することが出来るか必ず確認してください")
    while(True):
        try:
            selectX = int(input("X (0 ~ 7) >> "))
            selectY = int(input("Y (0 ~ 7) >> "))

            
            targetX = target[selectX][selectY][X] # sector[0][X] + ((len[X] / 7) * selectX)
            targetY = target[selectX][selectY][Y] #sector[0][Y] + ((len[Y] / 7) * selectY)
            swift.set_position(targetX, targetY, 30.0, wait=True)
        except:
            break

    if(input("セットアップをやりなおす場合は n を入力しEnterを押してください \n n 以外が入力された場合セットアップを完了します") != 'n'):
        setupDisable = False



def moveArmByReversiPredicted(predict):
    predictPosition = predict

    swift.reset(speed=100000, wait=True)
    swift.set_pump(on=True, wait=True)
    time.sleep(3)
    swift.flush_cmd()
    
    targetX = target[predictPosition[X]][predictPosition[Y]][X]
    targetY = target[predictPosition[X]][predictPosition[Y]][Y]

    swift.set_position(targetX, targetY, 30.0, wait=True)
    swift.flush_cmd()
    time.sleep(1)

    swift.set_pump(on=False)

    swift.reset(wait=True)

def setWhitePosition():
    x = int(input("X >"))
    y = int(input("Y >"))

    return [x, y]

game = reversi.ReversiGame()
game.reset()
game.start(lambda predict: moveArmByReversiPredicted(predict), lambda :setWhitePosition())
