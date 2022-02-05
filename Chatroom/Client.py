import socket
import select
import errno
import sys

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

myUsername = input("Username: ")
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((IP, PORT))
clientSocket.setblocking(False)  # Set recv function not blocking

username = myUsername.encode("utf-8")
usernameHeader = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
clientSocket.send(usernameHeader + username)

while True:
    message = input(f"{myUsername} > ")

    if message:
        message = message.encode("utf-8")
        messageHeader = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
        clientSocket.send(messageHeader + message)

    try:
        while True:
            # Receive Things
            usernameHeader = clientSocket.recv(HEADER_LENGTH)
            if not len(usernameHeader):
                print("Connection Closed by the Server")
                sys.exit()
            usernameLength = int(usernameHeader.decode("utf-8").strip())
            username = clientSocket.recv(usernameLength).decode("utf-8")

            messageHeader = clientSocket.recv(HEADER_LENGTH)
            messageLength = int(messageHeader.decode("utf-8").strip())
            message = clientSocket.recv(messageLength).decode("utf-8")

            print(f"{username} > {message}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print(f"Reading error: {str(e)}")
            sys.exit()
        continue

    except Exception as e:
        print(f"General error: {str(e)}")
        sys.exit()
