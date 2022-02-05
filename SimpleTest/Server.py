import socket
import time

HEADER_SIZE = 10

s = socket.socket(
    socket.AF_INET,     # IPv4
    socket.SOCK_STREAM  # TCP
)
s.bind((socket.gethostname(), 16548))
s.listen(5)             # Max connections: 5

while True:
    clientSocket, address = s.accept()
    print("Connection from " + address[0] + ":" + str(address[1]) + " has been established!")

    msg = "Welcome to the server!"
    sendingMsg = f"{len(msg):<{HEADER_SIZE}}" + msg

    clientSocket.send(sendingMsg.encode("utf-8"))

    while True:
        time.sleep(0.3)
        clientSocket.send(sendingMsg.encode("utf-8"))
