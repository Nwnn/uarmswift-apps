import socket
import time

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    # サーバを指定
    s.connect(('127.0.0.1', 50000))
    # サーバにメッセージを送る
    while True:
        s.sendall(b'hello')