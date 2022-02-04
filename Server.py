import socket

s = socket.socket(
    socket.AF_INET,     # IPv4
    socket.SOCK_STREAM  # TCP
)
s.bind((socket.gethostname(), 1234))
s.listen(5)             # Max connections: 5

while True:
    clientSocket, address = s.accept()
    print("Connection from " + address + "has been established!")
    clientSocket.send(bytes("Welcome to the server!", "utf-8"))

