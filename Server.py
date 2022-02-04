import socket

s = socket.socket(
    socket.AF_INET,     # IPv4
    socket.SOCK_STREAM  # TCP
)
s.bind((socket.gethostname(), 16548))
s.listen(5)             # Max connections: 5

while True:
    clientSocket, address = s.accept()
    print("Connection from " + address[0] + ":" + str(address[1]) + " has been established!")
    clientSocket.send("Welcome to the server!".encode("utf-8"))
