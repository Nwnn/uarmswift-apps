import socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

    s.bind(('127.0.0.1', 50000))

    while True:
        msg, address = s.recvfrom(1024)
        print(msg)
        pass


