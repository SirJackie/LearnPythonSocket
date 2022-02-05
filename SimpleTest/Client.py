import socket

HEADER_SIZE = 10

s = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)
s.connect((socket.gethostname(), 16548))

while True:
    fullMsg = ""
    hasNewMsg = True
    while True:
        msg = s.recv(16).decode("utf-8")
        if hasNewMsg:
            print(f"Start receiving new message, length = {msg[:HEADER_SIZE]}")
            msgLen = int(msg[:HEADER_SIZE].strip())
            hasNewMsg = False

        fullMsg += msg

        if len(fullMsg) - HEADER_SIZE == msgLen:
            print("Full new message received")
            print(fullMsg[HEADER_SIZE:])
            hasNewMsg = True
            fullMsg = ""

    print(fullMsg)
