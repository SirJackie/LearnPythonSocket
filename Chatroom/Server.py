import socket
import select

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Enable Reconnect

serverSocket.bind((IP, PORT))
serverSocket.listen(32)

socketList = [serverSocket]

clients = {}


def ReceiveMessage(clientSocket):
    try:
        messageHeader = clientSocket.recv(HEADER_LENGTH)

        if not len(messageHeader):
            return False

        messageLength = int(messageHeader.decode("utf-8").strip())
        return {"header": messageHeader, "data": clientSocket.recv(messageLength)}

    except:
        return False


while True:
    readSockets, _, exceptionSockets = select.select(socketList, [], socketList)

    for notifiedSocket in readSockets:
        if notifiedSocket == serverSocket:
            clientSocket, clientAddress = serverSocket.accept()

            user = ReceiveMessage(clientSocket)
            if user is False:
                continue

            socketList.append(clientSocket)

            clients[clientSocket] = user

            print(f"Accepted new connection from {clientAddress[0]}:{clientAddress[1]} username:{user['data'].decode('utf-8')}")
        else:
            message = ReceiveMessage(notifiedSocket)

            if message is False:
                print(f"Closed connection from{clients[notifiedSocket]['data'].decode('utf-8')}")
                socketList.remove(notifiedSocket)
                del clients[notifiedSocket]
                continue

            user = clients[notifiedSocket]
            print(f"Received message from{user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            for clientSocket in clients:
                if clientSocket != notifiedSocket:
                    clientSocket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notifiedSocket in exceptionSockets:
        socketList.remove(notifiedSocket)
        del clients[notifiedSocket]
