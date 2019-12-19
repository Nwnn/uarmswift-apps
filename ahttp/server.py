from swift import swift
import socket

# 管理者として実行！！

swift.set_servo_detach()
position = [0,0,0,0]

def onReportPosition(pos):
    global position
    position = pos
    pass

# アームの座標を取得して表示
swift.register_report_position_callback(lambda position: onReportPosition(position))
swift.set_report_position(interval = 0.01)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 8080))

    while True:
        s.listen(10)

        client_socket, addr = s.accept()

        with client_socket:
            try:
                print(position)
                msg = client_socket.recv(1024)
                client_socket.send(('HTTP/1.1 200 OK \nAccess-Control-Allow-Origin: * \ncontent-type: application/json; \n\n{ "pos" : [' + str(position[0]) + ',' + str(position[1]) + ',' + str(position[2]) + ',' + str(position[3]) + '], "pump" : '+ str(swift.get_limit_switch()).lower() +' }').encode('utf-8'))

            except socket.error as err:
                print(err)
                client_socket.close()
                break
                


