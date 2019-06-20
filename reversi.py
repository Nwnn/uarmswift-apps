from pprint import pprint
import random

X = 0
Y = 1

class Board:
    board = [ [None] * 8 for i in range(8) ]
    
    def getBoard(self) -> 'Board':
        return self.board

    def setStone(self, stone: bool, x: int, y: int) -> 'Board':
        self.board[x][y] = stone
        return self

    def putStone(self, stone: bool, x: int, y: int) -> 'Board':
        target = self.board[x][y]
        if(target != None):
            raise ValueError("いやそこ石置かれてるし...")
        
        else:
            revs = self.canPutStone(stone, x, y)
            # print(revs)
            if(len(revs) > 0):
                
                self.setStone(stone, x, y)

                for revTarget in revs:
                    # print(revTarget)
                    self.setStone(not self.board[revTarget[X]][revTarget[Y]], revTarget[X], revTarget[Y])
                    pass

            else:
                raise ValueError("一つも返せないよ！")

        return self

    # def getAvailableList(self, stone: bool) -> 'list[x, y]':
        # 00~77まで対象の石を走査する
        # 黒なら白を探す


    def canPutStone(self, stone: bool, targetX: int, targetY: int):
        # 指定位置の周りに
        #石のある場所に対しての向き（-1 , 1とか）も記録
        # 一か所を対象にして順番に探す

        mainRoutes = []
        
        def search(stone: bool, px: int, py: int, vx: int, vy: int, routes: list):
            tx = px + vx
            ty = py + vy

            # print("search -> " + str(tx) + ":" + str(ty))
            if((tx > 0 and tx < 8) and (ty > 0 and ty < 8)):
                tStone = self.board[tx][ty]

                if(tStone != None):
                    if(tStone == stone):
                        for route in routes:
                            mainRoutes.append(route)

                    elif(tStone != stone):
                        routes.append([tx, ty])
                        search(stone, tx, ty, vx , vy, routes)

        # 指定位置に石がある場合はそもそも置けない
        if(self.board[targetX][targetY] == None):
            # -1 → 0 → 1
            for vx in range(-1, 2):
                for vy in range(-1, 2):
                    if(not(vx == 0 and vy == 0)):
                        search(stone, targetX, targetY, vx, vy, [])

        else:
            pass

        return(mainRoutes)

    def availableList(self, stone):
        list = []

        for x in range(0, 8):
            for y in range(0, 8):
                if(len(self.canPutStone(stone, x , y)) > 0):
                    list.append([x , y])

        return list


    
class ReversiGame:
    board = Board()

    turn = None
    passTurn = None

    def reset(self):
        self.board.setStone(True,  3, 3)
        self.board.setStone(False,  3, 4)
        self.board.setStone(True,  4, 4)
        self.board.setStone(False,  4, 3)

        # 手番
        self.turn = True
        return True

    def showBoard(self):
        print("+---------------------+")
        print("|   0 1 2 3 4 5 6 7   |")

        rowNum = 0
        for row in self.board.getBoard():
            rowStr = "| " + str(rowNum) + ""


            for stone in row:
                if(stone == None):
                    rowStr += "  "
                
                elif(stone == True):
                    rowStr += " o"

                else:
                    rowStr += " x"

            rowStr += " " + str(rowNum) + " |"

            rowNum += 1
            print(rowStr)
        
        print("|   0 1 2 3 4 5 6 7   |")
        print("+---------------------+")

    # cbBlackは引数に予想済み駒が渡るので，そのタイミングでなんかできる
    # cbWhiteに[x, y]でreturnをかけるとなんかうごく
    def start(self, cbBlackOutput, cbWhiteInput):
        while(True):
            self.showBoard()
            availables = self.board.availableList(self.turn)
            print(availables)

            if(len(availables) == 0):
                print(str(self.turn) + " pass!")

                # 二連パスで終了
                if((self.passTurn != None) and (self.passTurn != self.turn)):
                    print("終了")
                    break

                else:
                    self.passTurn = self.turn
                    pass

            else:

                if(self.turn):

                    position = cbWhiteInput()

                    x = position[X]
                    y = position[Y]

                    try:
                        self.board.putStone(self.turn, x , y )
                    except:
                        print("おけません")
                        continue

                else:
                    self.passTurn = None

                    # 敵のAIはここから書く 結果は[x, y]でpredictに渡す
                    predict = availables[random.randint(0, len(availables) - 1 )]


                    self.board.putStone(self.turn, predict[X] , predict[Y])

                    cbBlackOutput(predict)

            self.turn = not self.turn
