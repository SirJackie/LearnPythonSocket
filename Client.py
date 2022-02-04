import socket

s = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)
s.connect((socket.gethostname(), 16548))

while True:
    msg = s.recv(8).decode("utf-8")
    print(msg)
