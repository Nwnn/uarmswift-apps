import socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

    s.connect(('192.168.1.13', 9000))    

    while True:
        s.sendall(b'{"pos" : [100, 100, 10], "pump" : true }')
        pass
